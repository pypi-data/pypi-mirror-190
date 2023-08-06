from plugins.conf import connDB
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import gc
import urllib.request
from image_track.tracker import CentroidTracker
from image_track.trackableobject import TrackableObject
import sys
sys.path.append('/home/user1/Settings')
import settings

conn = connDB()

queryip = "SELECT ipdevice,zone_one,zone_two FROM config_cam WHERE id = 1"
dt_query = conn.queryOneResult(queryip)

ct = CentroidTracker(maxDisappeared=2, maxDistance=50)
ct2 = CentroidTracker(maxDisappeared=2, maxDistance=50)

get_urldev = str(dt_query[0])
if get_urldev != None :
    get_urldev = get_urldev
else :
    get_urldev = settings.root_url
root_url = "http://"+get_urldev

control_outOPEN1=root_url+"/OPEN_OUT1"
control_outCLOSE1=root_url+"/CLOSE_OUT1"
control_outOPEN2=root_url+"/OPEN_OUT2"
control_outCLOSE2=root_url+"/CLOSE_OUT2"
control_outOPEN3=root_url+"/OPEN_OUT3"
control_outOPEN4=root_url+"/OPEN_OUT4"

x1 = 0
x2 = 800
x3 = 0
x4 = 800
y1 = int(dt_query[1])
if y1 != None :
    y1 = y1
else :
    y1 = settings.nilai_y1
y2 = y1
y3 = int(dt_query[2])
if y3 != None :
    y3 = y3
else :
    y3 = settings.nilai_y2
y4 = y3

prev_time = 0
new_time = 0

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default="modelssd/MobileNetSSD_deploy.prototxt",
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model",default="modelssd/MobileNetSSD_deploy.caffemodel",
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
    help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
    help="# of skip frames between detections")
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
print("[INFO] starting video stream...")

class device:
    def sendRequest(url):
        try :
            n = urllib.request.urlopen(url)
        except Exception as e : 
            print("Connection to device is disconnected :", e)
        finally :
            print("Please checking your device")
            n = urllib.request.urlopen(url)
           
class maincam:
    
    def __init__(self):
        self.frame = None

    def cam1(self,frame,socketio):
        global prev_time, new_time
        startX = 0
        startY = 0 
        endX = 0 
        endY = 0
        idx = 0 
        W = None
        H = None
        trackers = []
        y5 = y3+1
        frame = frame[1] if args.get("input", False) else frame
        frame = imutils.resize(frame, width=800)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.line(frame, (x1, y1), (x2,y2), (0, 255, 255), 1)
        cv2.line(frame, (x3, y3), (x4,y4), (0, 0, 255), 1)
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        rects = []
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        net.setInput(blob)
        detections = net.forward()
        
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > args["confidence"]:
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] != "person":
                    continue
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                # label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(startX, startY, endX, endY)
                tracker.start_track(rgb, rect)
                trackers.append(tracker)
            
                # if CLASSES[idx] == 'person':
                cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                # cv2.putText(frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # for tracker in trackers:
                tracker.update(rgb)
                pos = tracker.get_position()
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())
                rects.append((startX, startY, endX, endY))
                objects = ct.update(rects)
                for (objectID, centroid) in objects.items():
                    cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                    if centroid[1] > y1 and centroid[1] < y3:
                        device.sendRequest(control_outOPEN1)
                        socketio.emit("zone", "warning")
                    if centroid[1] > y5:
                        device.sendRequest(control_outOPEN2)
                        socketio.emit("zone", "danger")
                    if centroid[1] > y5 and centroid[1] < y1:
                        device.sendRequest(control_outOPEN4)
                        socketio.emit("zone", "danger")
                    if centroid[1] > y1 and centroid[1] < y1:
                        device.sendRequest(control_outOPEN3)
                        socketio.emit("zone", "warning")
                    if centroid[1] < y1:
                        device.sendRequest(control_outCLOSE1)
                        device.sendRequest(control_outCLOSE2)
                        socketio.emit("zone", "safe")

        # cv2.imshow("CAM1", frame)
        self.frame = frame.copy()
        new_time = time.time()

        fps = 1/(new_time-prev_time)
        prev_time = new_time
        fps = round(fps, 2)
        socketio.emit("fps", fps)
        gc.collect()
        
    def frames(self):
        frame = self.frame
        return frame
