import numpy as np 
import cv2
from math import * 

class KalmanFilter(object): 
    """dt : temps d'actualisation 
    point : coordonné initiaux du point
    erreur : plus l'entier est grand, plus le filtre pense que c'est brouillé """
    def __init__ (self, dt, point, erreur):
        self.dt = dt
        self.erreur = int(erreur)

        #vecteur 
        self.E=np.matrix([[point[0]],[point[1]], [0],[0]])

        #Matrice de transition 
        self.A=np.matrix([[1, 0, self.dt, 0],
                          [0, 1, 0, self.dt],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
        
           # Matrice d'observation, on observe que x et y
        self.H=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0]])

        self.Q=np.matrix([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        self.R=np.matrix([[erreur, 0],
                          [0, erreur]])

        self.P=np.eye(self.A.shape[1])

    def predict(self):
        self.E=np.dot(self.A, self.E)
        # Calcul de la covariance de l'erreur
        self.P=np.dot(np.dot(self.A, self.P), self.A.T)+self.Q
        return self.E

    def update(self, z):
        # Calcul du gain de Kalman
        S=np.dot(self.H, np.dot(self.P, self.H.T))+self.R
        K=np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Correction / innovation
        self.E=np.round(self.E+np.dot(K, (z-np.dot(self.H, self.E))))
        I=np.eye(self.H.shape[1])
        self.P=(I-(K*self.H))*self.P

        return self.E

class Forme():
    def __init__(self):
        pass
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = -1
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        print("on a :",len(approx),"contours")
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = 0
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = 0 if ar >= 0.95 and ar <= 1.05 else 0
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = 0
        elif len(approx) == 6:
            shape = 0
        elif len(approx) == 10 or len(approx) == 12:
            shape = 0
        # otherwise, we assume the shape is a circle
        else:
            shape = 1
        # return the name of the shape
        return shape   

class Annexe(object):
    def __init__(self,w,h,mw,mh):
        self.width = w
        self.height = h
        self.mid_w = mw
        self.mid_h = mh       

    def delta(self, x, y ):
        u,v = x
        w, z = y
        if u ==-1 and v ==-1 :
            return (0)
        else : 
            return (sqrt((u-w)**2 + (v-z)**2))
    
    def scored(self, x,y,x2,y2,x3,y3): 
        if x <x3 and x3 <x2 and y< y2 and y2< y3 :
            return True
        else :
            return False 
        

    def detect_ball(self, image, min_surface,max_surface,lo,hi):
        """Renvoie un tableau trié par surface décroissante"""
        points=np.empty(2,int)
        img = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image=cv2.blur(image, (10, 10))
        mask=cv2.inRange(image, lo, hi)
        mask=cv2.erode(mask, None, iterations=6)
        mask=cv2.dilate(mask, None, iterations=6)
        elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        elements=sorted(elements, key=lambda x:cv2.contourArea(x), reverse=True)
        i = 0 
        for element in elements:
            if cv2.contourArea(element)>min_surface and cv2.contourArea(element)<max_surface:
                ((x, y), r)=cv2.minEnclosingCircle(element)
                x,y,r = round(x,None),round(y,None),round(r,None)
                img = cv2.circle(img,(x,y),r,(0, 0, 255),2)
                points =np.append(points,np.array([(x,y)]))
                i+=1
                print("i vaut", i )
                print ("le rayon vaut : ",r)
            else:
                break
        return points,mask,img

    def detect_bu(self, frame,min_surface,lo,hi, prev): 
        """Renvoie un tableau trié par surface décroissante"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image=cv2.blur(hsv, (10, 10))
        bu_mask=cv2.inRange(image, lo, hi)
        bu_mask=cv2.erode(bu_mask, None, iterations=5)
        bu_mask=cv2.dilate(bu_mask, None, iterations=5)
        contours_bu=cv2.findContours(bu_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours_bu=sorted(contours_bu, key=lambda x:cv2.contourArea(x), reverse=True)
        bu_count = 0 
        for i in range(0,len(contours_bu)) : 
            area_bu = cv2.contourArea(contours_bu[i])
            xb,yb,wb,hb = cv2.boundingRect(contours_bu[i])
            center = (round(xb+(wb/2)),round((yb+hb)/2))
            if area_bu > min_surface and  yb < self.mid_h and 5*self.mid_w<xb < self.width :
                print(i)
                if self.delta(center,prev) < 50: 
                    cv2.rectangle(frame, (xb,yb),(xb+wb,yb+hb), (255,255,255),2)
                    print("on a mis à jours center")
                    bu_count += 1
                    break
        return bu_count, bu_mask, center