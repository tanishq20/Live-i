import cv2
import imutils
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np


dict = {
    0: 'safe driving',
    1: 'texting - right',
    2: 'talking on the phone - right',
    3: 'texting - left',
    4: 'talking on the phone - left',
    5: 'operating the radio',
    6: 'drinking',
    7: 'reaching behind',
    8: 'hair and makeup',
    9: 'talking to passenger'
}

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('./1.mp4')
        self.model = load_model('./attention_model.h5')  
    def __del__(self):
        self.video.release()
    
    def get_frame(self):

        ret, img = self.video.read()
        if ret:
            frame = img
            print(ret)
            frame = cv2.resize(frame, (224,224))
            frame = frame/225
            frame = frame.reshape((-1,224,224,3))
            pred =   dict[np.argmax(self.model.predict(frame))]
            # frame = imutils.resize(frame, height = 1440, width=1920)
            cv2.putText(img,str(pred),(50,70),cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(255,0,0),thickness=2)
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()
        else:
            r , jpeg = cv2.imencode('.jpg', np.zeros((224,224,3)))
            return jpeg.tobytes()