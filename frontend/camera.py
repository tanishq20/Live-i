import cv2
import imutils

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    
    def get_frame(self):

        ret, frame = self.video.read()
        frame = imutils.resize(frame, height = 1440, width=1920)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()