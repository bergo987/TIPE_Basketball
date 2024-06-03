#importation des librairies
import cv2 
import numpy as np 
from Kalman import KalmanFilter,Annexe

#déclaration des variables 
lower = np.array([0, 90, 0]) 
upper = np.array([8, 222, 140])


bu_lower = np.array([0, 110, 50]) 
bu_upper = np.array([10, 255, 200])
prev_pos_bu = (-1,-1)

width  = 0 
height = 0 

mid_w = 0
mid_h = 0 
links = '/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Basketball/script/video_perso/match_interieur.MOV'

#initialisation du flux vidéo
cap = cv2.VideoCapture(links)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

mid_w = round((width/8))
mid_h = 5*round((height/12))

KF = KalmanFilter(0.1,[0,0],4)
A = Annexe(width,height,mid_w,mid_h)

score = 0
nb_frame = 0 #sert a compter le nombre de frame entre deux paniers marqués 

nb_iter = 7
blur = 4
print("hauteur : ", height, "largeur : ",width)
print("1/2 hauteur : ", mid_h, "1/2 largeur : ",mid_w)



while True : 
    isclosed = 0  
    bu_count = 0 
    nb_frame +=1

    ret, frame = cap.read()
    if not ret :
        isclosed = 1 
        break
    #on commence par détecter les paniers
    bu_count, bu_mask, pos_bu= A.detect_bu(frame, 200,bu_lower,bu_upper,prev_pos_bu, nb_iter,blur)
    
    if pos_bu == (-2,-2) or bu_count == 0:
        print("Pas de panier détecter pour le moment")
    prev_pos_bu = pos_bu
    b_mask, img , pos_ba= A.detect_ball(frame,0,1700,lower,upper, prev_pos_bu)
    
    etat=KF.predict().astype(np.int32)
    x,y = round(etat.item(0)),round(etat.item(1))

    cv2.circle(frame,(x,y),10,(255, 255, 255),2)

    cv2.circle(frame, pos_ba, 10, (0, 0, 255), 2)
    KF.update(np.expand_dims(pos_ba, axis=-1))


    if A.scored(pos_ba,pos_bu):
        if nb_frame > 10: 
            score +=2 
            nb_frame = 0 

    c_line = (255,0,0)
    tick_line = 2
    cv2.line(img=frame,pt1=(0,mid_h), pt2=(int(width-1),mid_h), color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(3*mid_w,0), pt2=(3*mid_w,mid_h),color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(5*mid_w,0), pt2=(5*mid_w,mid_h),color=c_line, thickness= tick_line)    
    cv2.putText(frame, "nb panier: "+str(bu_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame, "taille: "+str(width)+" x "+str(height), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(frame, "score: "+str(score), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("Basketball Tracker", frame)

    if b_mask is not None:
        cv2.imshow('ball',b_mask)

    #if bu_mask is not None :
    #   cv2.imshow('bu',bu_mask)

    # On quitte le programme si l'on presse Q lorsque l'on est sur la bonne fenêtre
    if cv2.waitKey(1) & 0xFF == ord('q'):
        isclosed= 1
        print("on quitte manuellement")
        break

#On ferme le flux correctement
cap.release()
cv2.destroyAllWindows()

print("\t c'est finis")