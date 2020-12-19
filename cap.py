import cv2
import os
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
while ret:
    cv2.imshow("capture", frame)
    inputs = cv2.waitKey(1)
    print(inputs)
    if(inputs==ord('q')):   
        break
    ret, frame = cap.read()
cap.release()
cv2.destroyAllWindows()