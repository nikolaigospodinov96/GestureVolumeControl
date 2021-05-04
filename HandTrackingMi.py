# Добавяме си нужните библиотеки
# Библиотека за използване на opencv
import cv2
# Библиотеза за използванена mediaPipe
import mediapipe as mp
# Библиотека с която ще следим честотата на кадъра
import time

# Достъпваме камерата на  комютъра
web_camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

previousTime = 0
currentTime = 0

while True:
    success, img = web_camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    # Проберяваме дали показваме на камерата една или две ръце
    if results.multi_hand_landmarks:
        # За всяка ръка визуализираме нейните маркерни точки и връзките между тях (HAND_CONNECTIONS)
        for hand_landmark in results.multi_hand_landmarks:
            # Ще открием всички маркерна точки на ръката и тяхния номер
            for id, landmark in enumerate(hand_landmark.landmark):
                # Отпечатваме уникалния номер за всяка една маркерна точка. Ще използваме кординатите (x,y) на всяка
                # точка, за да открием точната им локация върху ръката
                # print(id, landmark)
                # Височина, ширина и канали на изображението
                height, width, channels = img.shape
                center_x, center_y = int(landmark.x*width), int(landmark.y*height)
                # Отпечатваме координатите на всяка една маркерна точка
                print(id, center_x, center_y)
                if id == 4:
                    # Одебеляваме маркерната точка, която има уникален номер равен на предоставения по-горе в
                    # if условието
                    cv2.circle(img, (center_x, center_y), 14, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

        currentTime = time.time()
        framePerSecond = 1/(currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(framePerSecond)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
