import cv2
import numpy as np
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(frame.shape)
print(np.array(eval((str(frame.tolist())).encode().decode())).shape)
cap.release()