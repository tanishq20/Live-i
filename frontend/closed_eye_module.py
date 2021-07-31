import cv2 as cv

# video = cv.VideoCapture(0)

class EyeDetector:
    def __init__(self):
        self.face_cascade_path = "haarcascade_frontalface_alt.xml"
        self.eye_cascade_path = "haarcascade_eye_tree_eyeglasses.xml"

        self.face_cascade = cv.CascadeClassifier(self.face_cascade_path)
        self.eye_cascade = cv.CascadeClassifier(self.eye_cascade_path)

    def detect_eyes(self, img):
        # Convert img to grayscale as that is what the haarcascade expects the img to be
        type(img)
        img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        # Detect faces in the image
        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.1,  minNeighbors=5, minSize=(30,30))

        if len(faces)>0:
            for (x,y,w,h) in faces:
                cv.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            
            img_temp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
            img_eye = img_gray[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
            eyes = self.eye_cascade.detectMultiScale(img_eye, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

            if len(eyes) == 0:
                msg = "WAKE UP!"
                cv.putText(img, msg, (150,70), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255))

            else:
                msg = "Eyes are open."
                cv.putText(img, msg, (150,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0))
            img_temp = cv.resize(img_temp, (400, 400), interpolation=cv.INTER_LINEAR)

        return img


def main():
    video = cv.VideoCapture(0)
    eye_detector = EyeDetector()

    while True:
        success, img = video.read()
        if success ==True:
            img = eye_detector.detect_eyes(img)
            cv.imshow("sleep", img)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    main()
