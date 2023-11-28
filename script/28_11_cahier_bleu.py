 #importation des librairies
import cv2
import numpy as np
from Kalman import KalmanFilter

#Définition des valeurs maximale et minimale prise par le filtre HSV pour la balle 
lower = np.array([33, 89, 69]) 
upper = np.array([179, 191, 209])

def scored(x,y,x2,y2,x3,y3): 
    if x <x3 and x3 <x2 and y< y2 and y2< y3 :
        return True
    else :
        return False 

KF = KalmanFilter(0.1,[0,0],10000)

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

    return points, mask
cap = cv2.VideoCapture(1)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

print("hauteur : ", height, "largeur : ",width)
surface = 200
while True:
    # Capture frame from the video
    isclosed = 0
    point_count = 0 

    # Initialisation du flux vidéo, pour pouvoir le réutiliser facilement 
    #Récuperation de la hauteur, de la largeur et de leurs moitiés 

    ret, frame_normal = cap.read()
    if not ret :
        isclosed
        break
    frame = cv2.flip(frame_normal,1)
    points , mask = detect_inrange(frame,surface,lower,upper)
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
        cv2.imshow('mask',mask)


    # Display the tracking result on the screen
    cv2.putText(frame, "taille: "+str(width)+" x "+str(height), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    
    cv2.putText(frame, "kalman detecte : "+str(len(points))+" balles", (10, 150), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Basketball Tracker", frame)
    
    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        isclosed= 1
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()