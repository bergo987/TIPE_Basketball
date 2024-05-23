 #importation des librairies
import cv2
import numpy as np
from Kalman import KalmanFilter,Annexe

#Définition des valeurs maximale et minimale prise par le filtre HSV pour la balle 
lower = np.array([3, 125, 43]) 
upper = np.array([14, 255, 156])

bu_lower =np.array([3, 125, 43]) 
bu_upper = np.array([14, 255, 156])

width = 0 
height = 0 

mid_w = 0
mid_h = 0 

cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/video_perso/lancer_franc1_(1).MOV')
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

mid_w = round((width/8))
mid_h = round((height/3))

KF = KalmanFilter(0.1,[0,0],0.5)
A = Annexe(width,height,mid_w,mid_h)

print("hauteur : ", height, "largeur : ",width)
print("1/2 hauteur : ", mid_h, "1/2 largeur : ",mid_w)
while True:
    # Capture frame from the video
    isclosed = 0
    point_count = 0 
    bu_count = 0
    # Initialisation du flux vidéo, pour pouvoir le réutiliser facilement 
    #Récuperation de la hauteur, de la largeur et de leurs moitiés 

    ret, frame = cap.read()
    if not ret :
        isclosed = 1
        break
    points, mask = A.detect_ball(frame,0,1700,lower,upper)
    etat= KF.predict().astype(np.int32)
    
    # le tableau etat contient les previsions, le tableau point contient la position que le filtre estime 
#    cv2.circle(frame,(int(etat[0]),int(etat[1])),5,(255,0,0),5)

 #   cv2.arrowedLine(frame,
  #              (int(etat[0]), int(etat[1])), (int(etat[0]+etat[2]), int(etat[1]+etat[3])),
   #             color=(0, 255, 0),
    #            thickness=3,
     #           tipLength=0.2)
    print(points[1])
    """
    for i in range(len(points)):
        u = points[i]
        cv2.circle(frame, (int(u[0]), int(u[1])), 15, (0, 0, 255), 2)
        x= points[i][0]
        y = points[i][1]
        print("les coordonnées sont : (", x,";",y,")")
        KF.update(np.expand_dims(points[0], axis=-1))
        """
    
    if mask is not None:
        cv2.imshow('ball',mask)
    
    bu_count, bu_mask = A.detect_bu(mask,500,bu_lower,bu_upper)
    
    if bu_mask is not None : 
        cv2.imshow('bu',bu_mask)


    # Display the tracking result on the screen
    c_line = (255,0,0)
    tick_line = 2
    cv2.line(img=frame,pt1=(0,mid_h), pt2=(int(width-1),mid_h), color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(3*mid_w,0), pt2=(3*mid_w,mid_h),color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(5*mid_w,0), pt2=(5*mid_w,mid_h),color=c_line, thickness= tick_line)    
    cv2.putText(frame, "nb panier: "+str(bu_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame, "taille: "+str(width)+" x "+str(height), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(frame, "kalman detecte : "+str(len(points))+" balles", (10, 90), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Basketball Tracker", frame)
    
    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        isclosed= 1
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()