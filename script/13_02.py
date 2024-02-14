import cv2 
import numpy as np 
from Kalman import KalamnFilter

lower = np.array([3, 125, 43]) 
upper = np.array([14, 255, 156])

bu_lower =np.array([3, 125, 43]) 
bu_upper = np.array([14, 255, 156])

width = 0 
height = 0 

mid_w = 0
mid_h = 0 