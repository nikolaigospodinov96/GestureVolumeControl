# Програме - Контролиране силата на звука с ръце

# Добавяме си библиотека за математически изчисления
import math
import time
# Упревление на звука на компютъра с пръсти
from ctypes import cast, POINTER

#################### Добавяме си нужните библиотеки ####################
import cv2
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Добавяме модула за проследяване на ръцете, който създадох ме първоначално
import HandTrackingModule as htm

import numpy as np

#################### Кода на пробрамата ####################

# Задаваме размерите на екрана на нашата камера (КОНСТАНТИ)
web_camera_w, web_camera_h = 640, 480

# Достъпваме камерата на  комютъра
web_camera = cv2.VideoCapture(0)
web_camera.set(3, web_camera_w)
web_camera.set(4, web_camera_h)
previous_time = 0

# Създаваме обект на класа HandTrackingModule
detector = htm.handDetector(detectionCon=0.7)

# Упревление на звука на компютъра с пръсти
devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

# Обхват за звука (-65.25, 0.0, 0.75)
volumeRange = volume.GetVolumeRange()

# Задаваме минимална и максимална стойност на звука
minVolume = volumeRange[0]
maxVolume = volumeRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = web_camera.read()
    # Извикване метода на класа HandTrackingModule с който ще открием ръцете си
    img = detector.findHands(img)
    # Извикваме метода на класа HandTrackingModule с който ще изведем списък с маркерните точки на ръцете
    landmarks_list = detector.findPosition(img, draw=False)
    if len(landmarks_list) != 0:
        # print(landmarks_list[4], landmarks_list[8])

        # [4, 397, 276] - landmarks_list[4][1] - 397, landmarks_list[4][2] - 276
        x1, y1 = landmarks_list[4][1], landmarks_list[4][2]

        # [8, 347, 173] - landmarks_list[8][1] - 347, landmarks_list[8][2] - 173
        x2, y2 = landmarks_list[8][1], landmarks_list[8][2]

        # Взимаме центъра между двете маркерни точки
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Изчертаваме розови кръгове около двете маркерни точки които ни тряват
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        # Изчертаваме линия между двете маркерни точки
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Изчертаваме розов кръг около централната точка между двете маркерни точки
        cv2.circle(img, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED)

        # Намираме разстоянието между двете маркерни точки
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Конвертираме обхвата на ръката в обхвата на звука
        # Обхвата на ръката 50 - 300
        # Обхвата на звука -65 - 0
        vol = np.interp(length, [50, 300], [minVolume, maxVolume])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)

        # Манипулираме нивото на звука на копмютъра 0 - 100 % сила на звука
        volume.SetMasterVolumeLevel(vol, None)

        # Ако растоянието между двете маркерни точки, стане по-малко от 50
        if length < 50:
            # Оцветяваме централната точка в зелено
            cv2.circle(img, (center_x, center_y), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 8, 8), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 8, 8), cv2.FILLED)
    cv2.putText(img, f': {int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 8, 8), 3)

    # Добавяме визуализация на кадрите в секунда
    current_time = time.time()
    frame_per_seconds = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f'FPS: {int(frame_per_seconds)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
