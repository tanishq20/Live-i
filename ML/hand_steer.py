import mediapipe as mp
import cv2 as cv

video = cv.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
Hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.9)

tips = [4,8,12,16,20]
while True:
    s, img = video.read()
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = Hands.process(img_rgb)
    lmList = []
    if results.multi_hand_landmarks:
        # print(results.multi_hand_landmarks)
        for landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(landmarks.landmark):
                h,w,_ = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
            mp_drawing.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)
            
        if len(lmList)!=0:
            fingers = []

            if lmList[tips[0]][1] > lmList[tips[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tips[id]][2] < lmList[tips[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            total_fingers = fingers.count(1)

            if total_fingers > 2:
                msg = "Hold the Steering Wheel Properly MA!"
                cv.putText(img, msg, (50, 70), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            else:
                msg = "Good Job!"
                cv.putText(img, msg, (50, 70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    cv.imshow("Steer", img)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break