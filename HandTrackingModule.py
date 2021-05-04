# Добавяме си нужните библиотеки
# Библиотека за използване на opencv
import cv2
# Библиотеза за използванена mediaPipe
import mediapipe as mp
# Библиотека с която ще следим честотата на кадъра
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # Проберяваме дали показваме на камерата една или две ръце
        if self.results.multi_hand_landmarks:
            # За всяка ръка визуализираме нейните маркерни точки и връзките между тях (HAND_CONNECTIONS)
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        landmark_list = []
        # Проберяваме дали показваме на камерата една или две ръце
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            # Ще открием всички маркерна точки на ръката и тяхния номер
            for id, landmark in enumerate(myHand.landmark):
                # Отпечатваме уникалния номер за всяка една маркерна точка. Ще използваме кординатите (x,y) на всяка
                # точка, за да открием точната им локация върху ръката
                # print(id, landmark)
                # Височина, ширина и канали на изображението
                height, width, channels = img.shape
                center_x, center_y = int(landmark.x * width), int(landmark.y * height)
                # Отпечатваме координатите на всяка една маркерна точка
                # print(id, center_x, center_y)
                landmark_list.append([id, center_x, center_y])
                if draw:
                    # Одебеляваме маркерната точка, която има уникален номер равен на предоставения по-горе в
                    # if условието
                    cv2.circle(img, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED)
        return landmark_list


def main():
    previousTime = 0
    currentTime = 0

    # Достъпваме камерата на  комютъра
    web_camera = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = web_camera.read()
        img = detector.findHands(img)
        landmark_list = detector.findPosition(img)
        if len(landmark_list) != 0:
            print(landmark_list[4])

        currentTime = time.time()
        framePerSecond = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(framePerSecond)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
