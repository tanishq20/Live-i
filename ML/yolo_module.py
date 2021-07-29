import cv2 as cv
import numpy as np

class PhoneDetector:
    def __init__(self, whT=416, conf_thereshold=0.2, nms_threshold=0.3):
        self.whT = whT
        self.conf_threshold = conf_thereshold
        self.nms_threshold = nms_threshold

        self.classesFile = "coco.names"

        self.modelConfig = "yolov3-320.cfg"
        self.modelWeights = "yolov3.weights"

        self.net  = cv.dnn.readNetFromDarknet(self.modelConfig, self.modelWeights)

    def findObjects(self, outputs, img, draw=True):

        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        classNames = []
        with open(self.classesFile, 'r') as f:
            classNames = f.read().rstrip("\n").split("\n")
        ht, wt, _ = img.shape
        bbox = []
        classIds = []
        confs = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.conf_threshold:
                    w, h = int(detection[2]*wt), int(detection[3]*ht)
                    x, y = int((detection[0]*wt) - (w/2)), int((detection[1]*ht) - (h/2))
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        # print(len(bbox))
        indices = cv.dnn.NMSBoxes(bbox, confs, self.conf_threshold, self.nms_threshold)
        for i in indices:
            i = i[0]
            box = bbox[i]
            x,y,w,h = box[0], box[1], box[2], box[3]
            if draw == True:
                cv.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 2)
            cv.putText(img, f"{classNames[classIds[i]].upper()} {int(confs[i]*100)}%", (x,y-10), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
        return img

    def detect(self, img, draw=True):
        # print(type(img))
        blob = cv.dnn.blobFromImage(img, 1/255, (self.whT, self.whT), [0,0,0] ,1, crop=False)
        self.net.setInput(blob)

        layerNames = self.net.getLayerNames()
        outputNames = [layerNames[i[0]-1] for i in self.net.getUnconnectedOutLayers()]

        outputs = self.net.forward(outputNames)
        img = self.findObjects(outputs, img, draw=draw)
        return img



def main():
    video = cv.VideoCapture(0)
    ph_detector = PhoneDetector()

    while True:
        success, img = video.read()
        if success == 1:
            img = ph_detector.detect(img, draw=True)
            cv.imshow("Webcam", img)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    main()