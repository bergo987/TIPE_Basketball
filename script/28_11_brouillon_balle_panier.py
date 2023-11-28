 #importation des librairies
import cv2
import numpy as np
from Kalman import KalmanFilter

#Définition des valeurs maximale et minimale prise par le filtre HSV pour la balle 
lower = np.array([0, 123, 115]) 
upper = np.array([179, 218, 197])

bu_lower = np.array([0, 129, 104]) 
bu_upper = np.array([179, 193, 255])

width = 0 
height = 0 

mid_w = 0
mid_h = 0 


def scored(x,y,x2,y2,x3,y3): 
    if x <x3 and x3 <x2 and y< y2 and y2< y3 :
        return True
    else :
        return False 

KF = KalmanFilter(0.1,[0,0],1)

def detect_inrange(image, surface,lo,hi):
    points=[]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image=cv2.blur(image, (10, 10))
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    elements=sorted(elements, key=lambda x:cv2.contourArea(x), reverse=True)
    for element in elements:
        if cv2.contourArea(element)>surface:
            ((x, y), rayon)=cv2.minEnclosingCircle(element)
            points.append(np.array([int(x), int(y)]))
        else:
            break
    return points,mask 

def detect_bu(image,min_surface,lo,hi,h,w, ): 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image=cv2.blur(hsv, (10, 10))
    bu_mask=cv2.inRange(image, lo, hi)
    bu_mask=cv2.erode(bu_mask, None, iterations=4)
    bu_mask=cv2.dilate(bu_mask, None, iterations=4)
    contours_bu=cv2.findContours(bu_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours_bu=sorted(contours_bu, key=lambda x:cv2.contourArea(x), reverse=True)
    mid_h = round(h/3)
    mid_w = round(w/3)
    bu_count = 0 
    for countour in contours_bu : 
        area_bu = cv2.contourArea(countour)
        xb,yb,wb,hb = cv2.boundingRect(countour)
        if area_bu > min_surface and  yb < mid_h and xb < mid_w :
            cv2.rectangle(frame, (xb,yb),(xb+wb,yb+hb), (255,0,0),2)
            y_area = yb + 50
            x_area = xb 
            y_area_2 = y_area +2
            x_area_2 = xb + wb
            cv2.rectangle(frame, (x_area,y_area),(x_area_2,y_area_2),(0,0,255), 2 )
            bu_count += 1
        if area_bu > 1500 and  yb < mid_h and 2*mid_w<xb < width :
            cv2.rectangle(frame, (xb,yb),(xb+wb,yb+hb), (255,0,0),2)
            bu_count += 1
    return bu_count

cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/video_perso/IMG_3542.MOV')
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

mid_w = round((width/3))
mid_h = round((height/3))

print("hauteur : ", height, "largeur : ",width)
print("1/2 hauteur : ", mid_h, "1/2 largeur : ",mid_w)
surface = 200
while True:
    # Capture frame from the video
    isclosed = 0
    point_count = 0 
    bu_count = 0
    # Initialisation du flux vidéo, pour pouvoir le réutiliser facilement 
    #Récuperation de la hauteur, de la largeur et de leurs moitiés 

    ret, frame = cap.read()
    if not ret :
        isclosed
        break
    points, mask = detect_inrange(frame,surface,lower,upper)
    etat= KF.predict().astype(np.int32)

    cv2.circle(frame,(int(etat[0]),int(etat[1])),2,(255,0,0),5)
    cv2.arrowedLine(frame,
                (int(etat[0]), int(etat[1])), (int(etat[0]+etat[2]), int(etat[1]+etat[3])),
                color=(0, 255, 0),
                thickness=3,
                tipLength=0.2)
    
    if (len(points)>0):
        cv2.circle(frame, (points[0][0], points[0][1]), 10, (0, 0, 255), 2)
        KF.update(np.expand_dims(points[0], axis=-1))
    
    if mask is not None:
        cv2.imshow('ball',mask)
    
    bu_count += detect_bu(mask,1500,bu_lower,bu_upper,height,width)
    
    # Display the tracking result on the screen
    c_line = (255,0,0)
    tick_line = 2
    cv2.line(img=frame,pt1=(0,mid_h), pt2=(1919,mid_h), color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(mid_w,0), pt2=(mid_w,mid_h),color=c_line, thickness= tick_line)
    cv2.line(img=frame, pt1=(2*mid_w,0), pt2=(2*mid_w,mid_h),color=c_line, thickness= tick_line)    
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