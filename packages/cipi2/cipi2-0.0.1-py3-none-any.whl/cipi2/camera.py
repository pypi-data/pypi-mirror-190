import cv2
from imutils.video import VideoStream
import imutils
import argparse

class camm:
    def cam(self,frame):
        # frame = vid.read()
        # frame = frame[1] if args.get("input", False) else frame
        frame = imutils.resize(frame, width=800)
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.line(frame, (0, 180), (800,180), (0, 255, 255), 1)
        cv2.line(frame, (0, 320), (800,320), (0, 0, 255), 1)
        cv2.imshow('frame', frame)
        # cv2.waitKey(1)