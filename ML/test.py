from yolo_module import PhoneDetector
from hand_steer_module import HandSteer
from closed_eye_module import EyeDetector
import cv2 as cv

video = cv.VideoCapture(0)
ph_detector = PhoneDetector()
steer = HandSteer(max_hands=2, min_detect_conf=0.9)
eye_detector = EyeDetector()
while True:
    success, img = video.read()
    img = ph_detector.detect(img, draw=True)
    #img = steer.track_hands(img=img, draw=True)
    #img = eye_detector.detect_eyes(img)
    cv.imshow("Webcam", img)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break