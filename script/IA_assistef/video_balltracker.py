import cv2
import numpy as np

# Set up the video capture
cap = cv2.VideoCapture('/Users/hugo/Documents/Cours/Prepa/TIPE/TIPE_Baskettball/script/IA_assistef/match.mp4')

# Define the lower and upper HSV color range of the basketball
lower_color = np.array([20, 100, 100])
upper_color = np.array([30, 255, 255])

# Initialize variables for tracking
prev_count = 0
count = 0

while True:
    # Capture frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to isolate the basketball
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply morphological transformations to the mask
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # Find contours of the basketball
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the basketball and count them
    count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            count += 1

    # Display the tracking result on the screen
    cv2.putText(frame, "Basketballs: " + str(count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Basketball Tracker", frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update the previous count
    prev_count = count

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
