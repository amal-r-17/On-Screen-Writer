# Lower and upper bounds to detect the pink color in the HSV color space
# lower bound [142 102 184] 
# upper bound [255 255 255]
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
img = np.zeros((480,640,3),np.uint8)
points = []

while True:
    # Reading frame
    _, frame = cap.read()
    # Converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Lower and upper bound to detect the pink color in the hsv color space
    l_b = np.array([142,102,184])
    u_b = np.array([255,255,255])
    
    # Creating the mark to separate out the color
    mask = cv2.inRange(hsv,l_b,u_b)
    mask = cv2.flip(mask, 1)# Flipping the mask

    # Detecting where the pink color is the mask
    x = np.where(mask==255)
    # Checking if there is actually any pink color in the frame
    if len(x[0]) == 0:
        pass
    else:
        img = cv2.circle(img,(x[1][0],x[0][0]),3,(0,0,255),-1)# drawing circles at the postion where color is detected
        points.append((x[1][0],x[0][0],time.time()))# setting up the time of detection of each point to remove unwanted lines
        if len(points) > 2:
            if points[-1][2] - points[-2][2] <1:
                img = cv2.line(img,points[-1][:2],points[-2][:2], (0,0,255),3)# Drawing lines between 2 identified points

    img1 = cv2.bitwise_or(cv2.flip(frame, 1),img)# Combining the static drawing to the live stream
    cv2.imshow("Testing",img1)# Showing the net result

    k = cv2.waitKey(1)
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()