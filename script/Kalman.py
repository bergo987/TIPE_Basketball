import numpy as np 
import cv2
from math import * 

class KalmanFilter(object): 
    """dt : temps d'actualisation
    point : coordonné initiaux du point
    erreur : plus l'entier est grand, plus le filtre pense que c'est brouillé """
    def __init__ (self, dt, point, erreur : float ):
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

class Annexe(object):
    """w: Largeur de l'image
        h : hauteur de l'image
        mw : 1/3 de la largeur
        mh : 1/8 de l'image """
    def __init__(self,w,h ,mw : int,mh : int):
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
    
    def center(self,x,y,w,h):
        return round(x+(w/2)),round(y+(h/2))

    def scored(self,c_ba, c_bu): 
        return self.delta(c_bu,c_ba) < 10
    
    def detect_bu(self, frame,min_surface,lo,hi, prev,iter : int): 
        """Renvoie un tableau trié par surface décroissante"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image=cv2.blur(hsv, (10, 10))
        bu_mask=cv2.inRange(image, lo, hi)
        bu_mask=cv2.erode(bu_mask, None, iterations=iter)
        bu_mask=cv2.dilate(bu_mask, None, iterations=iter)
        contours_bu=cv2.findContours(bu_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours_bu=sorted(contours_bu, key=lambda x:cv2.contourArea(x), reverse=True)
        bu_count = 0 
        center_bu = (-2,-2)
        for i in range(0,len(contours_bu)) : 
            area_bu = cv2.contourArea(contours_bu[i])
            xb,yb,wb,hb = cv2.boundingRect(contours_bu[i])
            center_bu = self.center(xb,yb,wb,hb)
            if area_bu > min_surface and  yb < self.mid_h and 5*self.mid_w<xb < self.width :
                print(i)
                if self.delta(center_bu,prev) < 30: 
                    cv2.rectangle(frame, (xb,yb),(xb+wb,yb+hb), (255,255,255),2)
                    print("on a mis à jours center")
                    bu_count += 1
                    break
        return bu_count, bu_mask, center_bu

    def detect_ball(self, image, min_surface,max_surface,lo,hi,pos_bu):
        """Renvoie un tableau trié par surface décroissante"""
        img = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image=cv2.blur(image, (10, 10))
        mask=cv2.inRange(image, lo, hi)
        mask=cv2.erode(mask, None, iterations=6)
        mask=cv2.dilate(mask, None, iterations=6)
        elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        elements=sorted(elements, key=lambda x:cv2.contourArea(x), reverse=True)
        i = 0 
        c = (-1,-1)
        for i in range(0, len(elements)):
            if cv2.contourArea(elements[i])>min_surface and cv2.contourArea(elements[i])<max_surface:
                ((x, y), r)=cv2.minEnclosingCircle(elements[i])
                x,y,r = round(x,None),round(y,None),round(r,None)
                c = x,y
                if self.delta(c,pos_bu)>40 : 
                    x,y,r = round(x,None),round(y,None),round(r,None)
                    img = cv2.circle(img,(x,y),r,(0, 0, 255),2)
                    i+=1
                    print("i vaut", i )
                    print ("le rayon vaut : ",r)
                    break
            else:
                break
        return mask,img,c