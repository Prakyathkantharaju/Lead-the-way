import numpy as np
import cv2 as cv
import cv2
import torch
from predictor import VisualizationDemo
from tqdm import tqdm




cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
Test = 0



cam = cv2.VideoCapture(0)
for vis in tqdm.tqdm(demo.run_on_video(cam)):
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.imshow(WINDOW_NAME, vis)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
cam.release()
cv2.destroyAllWindows()

# # model = build_model(model_zoo.get_config("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# while True:
#     Test += 1 
        
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # Display the resulting frame
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()
