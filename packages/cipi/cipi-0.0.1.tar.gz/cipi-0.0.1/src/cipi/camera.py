import cv2
from imutils.video import VideoStream
import imutils

def cam(frame):
    # frame = vid.read()
    frame = imutils.resize(frame, width=800)
    cv2.line(frame, (0, 180), (800,180), (0, 255, 255), 1)
    cv2.line(frame, (0, 320), (800,320), (0, 0, 255), 1)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)