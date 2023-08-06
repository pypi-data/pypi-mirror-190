# borrow many code from: https://github.com/deepinsight/insightface/tree/master/detection/scrfd


## How to install: 

- pip install cerberuspackage

## code python:

``
from cerberuspackage import SCRFD
detector = SCRFD("your onnx model")

#bboxes: [top_left_x, top_left_y, bottom_right_x, bottom_right_y], 
#kpss: corrdinate 5 point on the face (left_eye, right_eye, nose, left_lip, right_lip)

bboxes, kpss = detector(img) 
#your postprocess with data predict by dcrfd 
``