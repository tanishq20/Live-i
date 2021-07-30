import cv2
from tensorflow.keras.models import load_model
import numpy as np
from random import choice
import imutils

REV_CLASS_MAP = {
    0: "none",
    1: "paper",
    2: "rock",
    3: "scissors"
}

def mapper(val):
    return REV_CLASS_MAP[val]

def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"






class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.prev_move = None
        self.model = load_model("./rock-paper-scissors-model.h5")
        self.computer_move_name="none"
        self.winner ="waiting..."

    def __del__(self):
        self.video.release()
    
    def get_frame(self):

        ret, frame = self.video.read()
        frame = imutils.resize(frame, height = 1440, width=1920)
        #print(frame.shape)
        #prev_move = None
        
        # rectangle for user to play
        #cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
        # rectangle for computer to play
        #cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)

        # extract the region of image within the user rectangle
        roi = frame
        img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))

        # predict the move made
            
        pred = self.model.predict(np.array([img]))
        move_code = np.argmax(pred[0])
        user_move_name = mapper(move_code)

        # predict the winner (human vs computer)
        if self.prev_move != user_move_name:
            if user_move_name != "none":
                self.computer_move_name = choice(['rock', 'paper', 'scissors'])
                self.winner = calculate_winner(user_move_name, self.computer_move_name)
            else:
                self.computer_move_name = "none"
                self.winner = "Waiting..."
        self.prev_move = user_move_name

        # display the information
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Your Move: " + user_move_name,
                    (50, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Computer's Move: " + self.computer_move_name,
                    (750, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Winner: " + self.winner,
                    (400, 600), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

    #     if computer_move_name != "none":
    #         icon = cv2.imread(
    #             "./images/{}.jpg".format(computer_move_name))
    #         icon = cv2.resize(icon, (400,400))
            
    # #      icon = cv2.Canny(icon,100,100, L2gradient= True)
    #         icon = icon.reshape(400,400,3)
    #         frame[100:500,800:1200,:] = icon
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()




  
            
