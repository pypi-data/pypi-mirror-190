import numpy as np 
import cv2 

from cerberuspackage import scrdf_cbr

detector = scrdf_cbr.SCRFD('/home/hoangleminh/work_ceberus/face_reg/weights/scrfd_2.5g_kps.onnx')

img = cv2.imread("./images/s_l.jpg")
boxes, kpss = detector.detect(img, 0.5, input_size = (640, 640))
# kp = kpss[2][1].astype(int)
for i, box in enumerate(boxes):
    x1,y1,x2,y2,score = box.astype(int)
    left_eye = kpss[i][0]
    right_eye = kpss[i][1]
    crop_face = img[y1:y2, x1:x2]
    align_face = detector.alignment(crop_face, left_eye, right_eye)
    cv2.imshow("a", align_face)
    cv2.waitKey()
# cv2.circle(img, tuple(kp) , 1, (0,0,255) , 2)
print(kpss)

# print(kp)