import cv2

# define the video capture object
cap = cv2.VideoCapture(0)

# set the initial value of the counter
counter = 0

# define the coordinates of the line
line_y = 300

# define the color of the line
line_color = (0, 255, 0)  # green color in BGR format

# define the font to display the counter value
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # read a frame from the video capture object
    ret, frame = cap.read()

    # draw the line on the frame
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), line_color, 2)

    # convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply a threshold to the frame to binarize it
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # find the contours in the thresholded frame
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for contour in contours:
        # get the coordinates of the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # check if the center of the bounding box is below the line
        if y + h > line_y:
            # increment the counter
            counter += 1

            # draw the bounding box of the contour on the frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # display the counter value on the frame
    cv2.putText(frame, "Counter: {}".format(counter), (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # display the frame
    cv2.imshow("Frame", frame)

    # check if the 'q' key is pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
