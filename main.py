import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyautogui

# variables
width, height = 190, 90
folderPath = "presentation"

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation Images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

#Variables
imgList = []
delay = 30
imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1) #width and height of small image
gestureThreshold = 300
buttonPressed = False
Counter = 0
buttonDelay = 30
drawMode = False
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False

#Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)



while True:
    #import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    center_x = int(width / 2)
    center_y = int(height / 2)

    # find the hand and its landmark
    hands, img = detectorHand.findHands(img) # with draw

    # define the length of the line (half of the image)
    line_length = int(width / 2)

    # draw a green line in the center of the image
    cv2.line(img, (center_x - line_length, center_y), (center_x + line_length, center_y), (0, 255, 0), 2)

    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detectorHand.fingersUp(hand) # list of which fingers are up
        cx, cy = hand['center']
        lmList = hand['lmList'] # list of 21 landmark points
        indexFinger = lmList[8][0], lmList[8][1]

        #constrain values for earsier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal



        if cy <= gestureThreshold: # if hand is at the height of the face

            # gesture 1 - Right
            if fingers == [1, 0, 0, 0, 0]:
                print("Right")

                if imgNumber > 0:
                    buttonPressed = True
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

            # gesture 2 - Left
            if fingers == [0, 0, 0, 0, 1]:
                print("Left")

                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        # gesture 3 - pointer
        if fingers == [0, 1, 1, 0, 0]:
            screen_width, screen_height = pyautogui.size()
            target_x = int(np.interp(xVal, [0, width], [0, screen_width]))
            target_y = int(np.interp(yVal, [0, height], [0, screen_height]))
            screen_x = 500
            screen_y = 500
            target_x = xVal
            target_y = yVal
            indexFinger = (target_x, target_y) # define indexFinger variable here
            pyautogui.moveTo(target_x, target_y, duration=0.1)
            cv2.circle(imgCurrent, (indexFinger[0], indexFinger[1]), 20, (0, 0, 255), thickness=cv2.FILLED)

        # gesture 4 - annotations
        if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                    print(annotationNumber)
                    annotations[annotationNumber].append(indexFinger)
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), thickness=cv2.FILLED)
        else:
            annotationStart = False

        # gesture 5 - delete annotations
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop()
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        Counter += 1
        if Counter > delay:
            Counter = 0
            buttonPressed = False

            # to define a x,y cooridinates
            #x1 = 100
            #y1 = 200
            #x2 = 300
            #y2 = 400
            #pt1 = (x1, y1)
            #pt2 = (x2, y2)
            #cv2.line(imgCurrent, pt1, pt2, (0, 0, 255), 12)

    for i, annotations in enumerate(annotations):
        for j in range(len(annotations)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)


    #Adding webcam image on the slides

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break