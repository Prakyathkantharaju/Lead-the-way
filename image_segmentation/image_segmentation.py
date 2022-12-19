import detectron2
import time

# import some common libraries
import numpy as np
import os, json, cv2, random
import matplotlib.pyplot as plt







cam = cv2.VideoCapture(0)


i = 0
while True:
    ret, frame = cam.read()
    i += 1
    if i == 100:
      # import some common detectron2 utilities
      from detectron2 import model_zoo
      from detectron2.engine import DefaultPredictor
      from detectron2.config import get_cfg
      from detectron2.utils.visualizer import Visualizer, ColorMode
      from detectron2.data import MetadataCatalog, DatasetCatalog
      from predictor import VisualizationDemo
      cfg = get_cfg()
      # # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
      cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
      cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
      # # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
      cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
      # predictor = DefaultPredictor(cfg)
      predictor = VisualizationDemo(cfg)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    
    # Display the resulting frame
    
    if i > 100 and i % 10:
      predictor_information, image = predictor.run_on_image(frame)
      print(f"Weight of the predictor{np.sum(np.sum(predictor_information['instances'].get_fields()['pred_masks'].cpu().numpy(), axis = 1),axis= 1)}")
      print(f"prediction accuracy: {predictor_information['instances'].get_fields()['scores'].cpu().numpy()}")
      frame = image.get_image()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break