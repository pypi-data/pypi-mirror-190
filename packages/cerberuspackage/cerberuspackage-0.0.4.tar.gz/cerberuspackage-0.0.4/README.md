# this repo for cerberus company

borrow many code from: https://github.com/deepinsight/insightface/tree/master/detection/scrfd


# How to use: 

- pip install cerberuspackage

# code python:
from cerberuspackage import SCRFD
detector = SCRFD("your onnx model")
bboxes, kpss = detector(img) # bboxes: [top_left_x, top_left_y, bottom_right_x, bottom_right_y], kpss: corrdinate 5 point on the face
#your postprocess with data predict by dcrfd 

