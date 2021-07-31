import mediapipe as mp
import cv2 as cv


class HandSteer:
    def __init__(self, max_hands=2, min_detect_conf=0.8):
        self.max_hands = max_hands
        self.min_detect_conf = min_detect_conf

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.Hands = self.mp_hands.Hands(max_num_hands=self.max_hands, min_detection_confidence=self.min_detect_conf)
        self.tips = [4,8,12,16,20]

    def track_hands(self, img, draw=True):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.Hands.process(img_rgb)
        lmList = []
        if results.multi_hand_landmarks:
            # print(results.multi_hand_landmarks)
            for landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(landmarks.landmark):
                    h,w,_ = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id, cx, cy])
                if draw == True:
                    self.mp_drawing.draw_landmarks(img, landmarks, self.mp_hands.HAND_CONNECTIONS)
                
            if len(lmList)!=0:
                fingers = []

                if lmList[self.tips[0]][1] > lmList[self.tips[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lmList[self.tips[id]][2] < lmList[self.tips[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                
                total_fingers = fingers.count(1)

                if total_fingers > 2:
                    msg = "Hold the Steering Wheel Properly!"
                    cv.putText(img, msg, (50, 70), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
                else:
                    msg = "Good Job!"
                    cv.putText(img, msg, (50, 70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
        return img

def main():
    video = cv.VideoCapture(0)
    steer = HandSteer(max_hands=2, min_detect_conf=0.9)
    while True:
        success, img = video.read()
        img = steer.track_hands(img=img, draw=True)
        cv.imshow("Steer", img)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == '__main__':
    main()
