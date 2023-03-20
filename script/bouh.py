import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

#initialize the video

cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/Basket/TIPE_Baskettball/script/cvzone/vid (1).mp4')

#create the color finder objet 
mycolorfinder = ColorFinder(True)
hsvVals ='red'
while True :
    #grab the image 
    #success, img = cap.read()
    img = cv2.imread('/Users/hugo/Documents/Cours/Prepa/TIPE/Basket/TIPE_Baskettball/script/cvzone/Ball.png')
    img = img[0:900, : ]


    #Find the color Ball
    imgColor, mask =  mycolorfinder.update(img,hsvVals)
    #display
    img = cv2.resize(img,(0,0), None, 0.7,0.7)
    cv2.imshow("Image", img)
    cv2.imshow("ImageColor", imgColor)    
    cv2.waitKey(50)