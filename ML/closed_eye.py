import cv2 as cv
import time

video = cv.VideoCapture(0)

face_cascade_path = "haarcascade_frontalface_alt.xml"
eye_cascade_path = "haarcascade_eye_tree_eyeglasses.xml"

face_cascade = cv.CascadeClassifier(face_cascade_path)
eye_cascade = cv.CascadeClassifier(eye_cascade_path)

# Initialize variables for fps
past_time = 0
current_time = 0

while True:
    s, img = video.read()

    # Convert img to grayscale as that is what the haarcascade expects the img to be
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1,  minNeighbors=5, minSize=(30,30))

    if len(faces)>0:
        for (x,y,w,h) in faces:
            cv.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        
        img_temp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
        img_eye = img_gray[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
        eyes = eye_cascade.detectMultiScale(img_eye, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        if len(eyes) == 0:
            msg = "What Ma! Why sleeping ma!"
            cv.putText(img, msg, (150,70), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255))

        else:
            msg = "Noice! Why not sleeping Ma!"
            cv.putText(img, msg, (150,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0))
        img_temp = cv.resize(img_temp, (400, 400), interpolation=cv.INTER_LINEAR)

    # Fps
    current_time = time.time()
    fps = int(1/(current_time-past_time))
    past_time = current_time

    cv.putText(img, f"Fps:{fps}", (50,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv.imshow("sleep", img)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break
