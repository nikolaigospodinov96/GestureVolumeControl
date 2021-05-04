# Библиотека за използване на opencv
import cv2
# Библиотеза за използванена mediaPipe
import mediapipe as mp
# Библиотека с която ще следим честотата на кадъра
import time

import HandTrackingModule as htm

previousTime = 0
currentTime = 0

# Достъпваме камерата на  комютъра
web_camera = cv2.VideoCapture(0)

detector = htm.handDetector()

while True:
    success, img = web_camera.read()
    # draw = False - няма да се показват маркери на ръката
    img = detector.findHands(img)
    # draw = False - няма да се показват одебелените маркери на ръката
    landmark_list = detector.findPosition(img)
    if len(landmark_list) != 0:
        print(landmark_list[4])

    currentTime = time.time()
    framePerSecond = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, str(int(framePerSecond)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
