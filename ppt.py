import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Parameters
width, height = 1280, 720
FolderPath = r'C:\gesture controlled ppt\presentation'                  # location of slides
hs, ws = 120, 180

# Cam_Setup
cam = cv2.VideoCapture(0)
cam.set(4, ws)
cam.set(5, hs)

# load slides
pathSlides = sorted(os.listdir(FolderPath), key=len)
# print(pathSlides)

# Variables
SlideNum = 0
gestureThreshold = 300
button_pressed = False
button_counter = 0
button_delay = 30
annotations = [[]]
annotation_number = -1
annotation_start = False

# HandDetector
detector = HandDetector(detectionCon=0.9, maxHands=1)

while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)                    # To flip the img 1= horizontal , 0= vertical
    img = cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (100, 255, 205), 10)

    pathFullSlides = os.path.join(FolderPath, pathSlides[SlideNum])
    SlideCurrent = cv2.imread(pathFullSlides)

# to flip the image
    hands, img = detector.findHands(img, flipType=False)  

    if hands and button_pressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lm_list = hand['lmList']

# pointer 
        x_val = int(np.interp(lm_list[8][0], [0, width//4], [0, width]))
        y_val = int(np.interp(lm_list[8][1], [0, height-500], [0, height]))
        index_finger = x_val, y_val

        if cy <= gestureThreshold:  #If hand is above the gestureThreshold
            if fingers == [1, 0, 0, 0, 0]:            # thumb up -> previous slide 
                print('Previous Slide')

                if SlideNum > 0:
                    button_pressed = True
                    annotations = [[]]
                    annotation_number = -1
                    annotation_start = False
                    SlideNum -= 1

           
            if fingers == [0, 0, 0, 0, 1]:         # little finger up -> next slide
                print('Next Slide')
                if SlideNum < len(pathSlides)-1:
                    button_pressed = True
                    annotations = [[]]
                    annotation_number = -1
                    annotation_start = False

                    SlideNum += 1

        # Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(SlideCurrent, index_finger, 12, (0, 0, 255), cv2.FILLED)

        # To draw
        if fingers == [0, 1, 0, 0, 0]:
            if annotation_start is False:
                annotation_start = True
                annotation_number += 1
                annotations.append([])
            cv2.circle(SlideCurrent, index_finger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotation_number].append(index_finger)
        else:
            annotation_start = False

        
        if fingers == [0, 1, 1, 1, 1]:
            if annotations:
                annotations.pop(-1)
                annotation_number -= 1
                button_pressed = True

# Button_Pressed itreation
    if button_pressed:
        button_counter += 1
        if button_counter > button_delay:
            button_counter = 0
            button_pressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(SlideCurrent, annotations[i][j-1], annotations[i][j], (0, 255, 0), 12)

# Adding camera to the Slide
    

    cv2.imshow('Slides', SlideCurrent)
    cv2.imshow('Image', img)

    Key = cv2.waitKey(1)
    if Key == ord('q'):
        break