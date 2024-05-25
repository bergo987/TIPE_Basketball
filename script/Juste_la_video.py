#importation des librairies
import cv2 
import numpy as np 
from Kalman import KalmanFilter,Annexe

#declaration des variables 
lower = np.array([3, 125, 43]) 
upper = np.array([14, 255, 156])

bu_lower =np.array([3, 125, 43]) 
bu_upper = np.array([14, 255, 156])

width = 0 
height = 0 

mid_w = 0
mid_h = 0 
links = '/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/video_perso/lancer_franc1_(1).MOV'

#initialisation du flux vidéo
cap = cv2.VideoCapture(links)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

mid_w = round((width/8))
mid_h = round((height/3))

KF = KalmanFilter(0.1,[0,0],0.5)
A = Annexe(width,height,mid_w,mid_h)

print("hauteur : ", height, "largeur : ",width)
print("1/2 hauteur : ", mid_h, "1/2 largeur : ",mid_w)

while True : 
    isclosed = 0 
    point_count = 0 
    bu_count = 0 

    ret, frame = cap.read()
    if not ret :
        isclosed = 1 
        break
    points, b_mask, img = A.detect_ball(frame,0,1700,lower,upper)
    print("premier élément du tableau point : ",points[0])
    print("nombre de points détecté : ", points.shape[0])
    if b_mask is not None:
        cv2.imshow('ball',b_mask)

    bu_count, bu_mask = A.detect_bu(frame, 500,bu_lower,bu_upper)

    if bu_mask is not None : 
        cv2.imshow('bu',bu_mask)

    c_line = (255,0,0)
    tick_line = 2
    cv2.line(img=frame,pt1=(0,mid_h), pt2=(int(width-1),mid_h), color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(3*mid_w,0), pt2=(3*mid_w,mid_h),color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(5*mid_w,0), pt2=(5*mid_w,mid_h),color=c_line, thickness= tick_line)    
    cv2.putText(frame, "nb panier: "+str(bu_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame, "taille: "+str(width)+" x "+str(height), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(frame, "kalman detecte : "+str(len(points))+" balles", (10, 90), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Basketball Tracker", frame)
    # On quitte le programme si l'on presse Q lorsque l'on est sur la bonne fenêtre
    if cv2.waitKey(1) & 0xFF == ord('q'):
        isclosed= 1
        break

#On ferme le fluw correctement
cap.release()
cv2.destroyAllWindows()

print("c'est finis")