import cv2
import numpy as np

cap = cv2.VideoCapture(0)
whT = 416
conf_threshold = 0.2
nms_threshold = 0.3

classesFile = "coco.names"
classNames = []
with open(classesFile, 'r') as f:
    classNames = f.read().rstrip("\n").split("\n")

# print(classNames)
# print(len(classNames))


modelConfig = "yolov3-320.cfg"
modelWeights = "yolov3.weights"

net  = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findObjects(outputs, img):
    ht, wt, ct = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > conf_threshold:
                w, h = int(detection[2]*wt), int(detection[3]*ht)
                x, y = int((detection[0]*wt) - (w/2)), int((detection[1]*ht) - (h/2))
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    # print(len(bbox))
    indices = cv2.dnn.NMSBoxes(bbox, confs, conf_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 255), 2)
        cv2.putText(img, f"{classNames[classIds[i]].upper()} {int(confs[i]*100)}%", (x,y-10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)


while True:
    success, img = cap.read()
    # img = cap
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0] ,1, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    # print(layerNames)
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(outputNames)
    # print(outputs[0].shape)
    # print(outputs[1].shape)
    # print(outputs[2].shape)
    # print(outputs[0][0])
    findObjects(outputs, img)



    cv2.imshow("Webcam", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break