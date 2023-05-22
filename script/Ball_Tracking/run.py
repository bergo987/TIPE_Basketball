"""
To run the algorithm on a video

"""
import time
import cv2
from detector import Detectors

from kalmanfilter import KalmanFilter

def main():

    start_time = time.time()

    vid = cv2.VideoCapture("script/Ball_Tracking/vid(1).mp4")

    fps = vid.get(cv2.CAP_PROP_FPS)
    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    detector = Detectors()

    skipframes = 1 #No of frames skipped + 1 (Time between successive frames given for detection)
    flag = 1 #To find the first detection

    track = [] #Keeps Track of most likely state vectors
    frames = [] #Stores frames of the video

    while(vid.isOpened()):
        ret, frame = vid.read();
        if ret == True:
            frames.append(frame)
            bcenter = detector.detectBall(frame)
            try:
                if(len(bcenter) > 0 and flag == 1):
                    KF = KalmanFilter(bcenter[0], bcenter[1], fps, skipframes)
                    track.append(KF.xk)
                    flag = 0

                xp = KF.predict()
                xmp = KF.update(bcenter[0], bcenter[1])
                track.append(xmp)
            except TypeError:
                pass
        else:
            break

    vid.release()

    print("Time to execute : %s seconds" % (time.time()-start_time))

    #Writing to video
    out = cv2.VideoWriter('script/Ball_Tracking/vid2Kalman.avi',cv2.VideoWriter_fourcc('M','P','E','G'), 10, (frame_width,frame_height))
    for i in range(len(frames)):
      print(i)
      cv2.circle(frames[i], (int(track[i][0]), int(track[i][1])), 10, (255,255,255), 4)
      out.write(frames[i])

    out.release()

if __name__ == "__main__":
    main()
