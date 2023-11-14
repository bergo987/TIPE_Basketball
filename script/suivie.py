import cv2
from Detector import detect_inrange
from Kalman import KalmanFilter
import numpy as np

VideoCap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/vid_.mp4')

lower_ball = np.array([8, 96, 115])
upper_ball = np.array([14, 255, 255])

KF=KalmanFilter(0.1, [0, 0],1)

while(True):
    ret, frame=VideoCap.read()

    points, mask=detect_inrange(frame, 1500,lower_ball,upper_ball)


    etat=KF.predict()

    cv2.circle(frame, (int(etat[0]), int(etat[1])), 2, (0, 255, 0), 5)
    x = int(etat[0]+etat[2]),int(etat[1]+etat[3])
    y = int(etat[0]), int(etat[1])
    cv2.arrowedLine(frame,
                    y, x,
                    color=(0, 255, 0),
                    thickness=3,
                    tipLength=0.2)
    if (len(points)>0):
        cv2.circle(frame, (points[0][0], points[0][1]), 20, (0, 0, 255), 2)
        KF.update(np.expand_dims(points[0], axis=-1))
    if mask is not None:
        cv2.imshow('mask', mask) 
    cv2.imshow('image', frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        VideoCap.release()
        cv2.destroyAllWindows()
        break