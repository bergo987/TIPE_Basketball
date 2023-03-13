import cv2

print(cv2.getBuildInformation())

webcam = cv2.VideoCapture(1)
if webcam.isOpened():
    while True:
        bImgReady, imageframe = webcam.read() # get frame per frame from the webcam
        if bImgReady:
            cv2.imshow('My webcam', imageframe) # show the frame
        else:
            print('No image available')
        keystroke = cv2.waitKey(20) # Wait for Key press
        if (keystroke == 27):
            break # if key pressed is ESC then escape the loop
 
    webcam.release()
    cv2.destroyAllWindows()  