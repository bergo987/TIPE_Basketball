import cv2 
import numpy as np
import dlib 

video = cv2.VideoCapture('path')

#on verifie que on peut ouvrir la vidéo ou le flux vidéo 
if video.isOpened() == False :
    print("La vidéo ne peut pas être ouverte")

# on verifie si la première frame de la video est vonne 

ret, frame = video.read()

# check sir la la première est lu ou non 
if ret == False :
    print("on n'arrive pas à lire la première image de la video")

# on la montre

cv2.imshow('première frame', frame)
cv2.waitKey(0)
