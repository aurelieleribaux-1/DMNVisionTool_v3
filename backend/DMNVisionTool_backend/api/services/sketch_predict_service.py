from typing import List
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2 import model_zoo # Need to import detectron on Github
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from numpy import ndarray
import os
import cv2

from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten.elements_factories import CATEGORIES
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import (
    ObjectPrediction,
    KeyPointPrediction,
)

from DMNVisionTool_backend.commons.Sketch_utils import here
import numpy as np

############## DRDs ####################   
class SketchObjectPredictor:
    """Class used to represent a Detectron2 predictor trained with a faster_rcnn (Handwritten versions)"""

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        )
        cfg.OUTPUT_DIR = here("../../detectron_model") # Make sure to use right directory
        cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "SketchDRD_model_final.pth")  # path to the trained model
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5
        cfg.MODEL.DEVICE = "cpu"
        self._predictor = DefaultPredictor(cfg)

    def predict(self, img: ndarray):
        """Method used to predict and extract the dmn elements from an image

        Parameters
        ----------
        img: ndarray
            The image used for the detection of the elements (as a ndaary)

        Returns
        -------
        dict
            The predictions of the elements
        """
        # Handle grayscale images
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Ensure image is in HWC format and float32 data type
        img = img.astype(np.float32)

        outs = self._predictor(img)

        v = Visualizer(img[:, :, ::-1],
                       scale=1.5,
                       instance_mode=ColorMode.IMAGE_BW
                       )
        out = v.draw_instance_predictions(outs["instances"].to("cpu"))
        #cv2_imshow(out.get_image()[:, :, ::-1])
        #cv2.waitKey(0)

        return outs


class SketchKeyPointPredictor:
    """Class used to represent a Detectron2 predictor trained with a keypoint_faster_rcnn"""

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_1x.yaml")
        )
        cfg.OUTPUT_DIR = here("../../detectron_model")
        cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "Sketchkp_DRD_model_final.pth")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
        cfg.MODEL.RETINANET.NUM_CLASSES = 4
        cfg.MODEL.ROI_KEYPOINT_HEAD.NUM_KEYPOINTS = 6
        cfg.MODEL.DEVICE = "cpu"
        self._predictor = DefaultPredictor(cfg)
        

    def predict(self, img):
        """Method used to predict and extract the arrows from an image

        Parameters
        ----------
        img: ndarry
            The image used for the detection of the arrow (as a ndaary)

        Returns
        -------
        dict
            The predictions of the arrows
        """
        # Handle grayscale images
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Ensure image is in HWC format and float32 data type
        img = img.astype(np.float32)

        outs = self._predictor(img)

        for kp in outs.get("instances").pred_keypoints.numpy():
             cv2.circle(img, (int(kp[0][0]), int(kp[0][1])), 4, (0, 255, 0), -1)
             cv2.circle(img, (int(kp[3][0]), int(kp[3][1])), 4, (0, 0, 255), -1)
        #cv2_imshow(img)
        #cv2.waitKey(0)

        return outs


#object_predictor = ObjectPredictor()
#keypoint_predictor = KeyPointPredictor()


def SketchPredictObject(image: ndarray) -> List[ObjectPrediction]:
    """Pass an image to a trained object detection neural network model that returns the detected instances with the
    associated labels

    Parameters
    ----------
    image: ndarray
        The image used for the detection of the element (as a ndarray)

    Return
    ------
    List[ObjectPrediction]
        The list of SketchObjectPrediction
    """
    object_predictor = SketchObjectPredictor()

    predictions = object_predictor.predict(image)

    pred_boxes = predictions.get("instances").get("pred_boxes").tensor.numpy()
    pred_classes = predictions.get("instances").get("pred_classes").numpy()

    predictions = list(zip(pred_boxes, pred_classes))
    print('okpredictelemets')

    return [ObjectPrediction(label, *box) for box, label in predictions]



def SketchPredictKeypoint(image: ndarray) -> List[KeyPointPrediction]:
    """Pass an image to a trained keypoint detection neural network model that returns the associated predictions

    Parameters
    ----------
    image: ndarray
        The image used for the detection of the element (as a ndaary)

    Return
    ------
    List[KeyPointPrediction]
        The list of KeyPointPrediction
    """
    keypoint_predictor = SketchKeyPointPredictor()
    
    predictions = keypoint_predictor.predict(image)

    boxes = predictions.get("instances").get("pred_boxes").tensor.numpy()
    classes = predictions.get("instances").get("pred_classes").numpy()
    keypoint = predictions.get("instances").pred_keypoints.numpy()

    predictions = list(zip(classes, boxes, keypoint))
    print('okpredictkeypoints')

    return [
        KeyPointPrediction(clazz, *box, key[0], key[5]) for clazz, box, key in predictions
    ]
    
############## Tables #################### 
from DMNVisionTool_backend.DecisionTables.Handwritten.table_factories import CATEGORIES 
from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction
from DMNVisionTool_backend.commons.Sketch_utils import here 

class SketchTablePredictor:
    """Class used to represent a Detectron2 predictor trained with a faster_rcnn"""

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        )
        cfg.OUTPUT_DIR = here("../../detectron_model") # Make sure to use right directory
        cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "SketchTable_model_final.pth")  # path to the trained model
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 8
        cfg.MODEL.DEVICE = "cpu"
        self._predictor = DefaultPredictor(cfg)

    def predict(self, img: ndarray):
        """Method used to predict and extract tables from an image

        Parameters
        ----------
        img: ndarray
            The image used for the detection of the tables (as a ndaary)

        Returns
        -------
        dict
            The predictions of the tables
        """
        # Handle grayscale images
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Ensure image is in HWC format and float32 data type
        img = img.astype(np.float32)

        outs = self._predictor(img)
        print(outs.get("instances").get_fields())

        v = Visualizer(img[:, :, ::-1],
                       scale=1.5,
                       instance_mode=ColorMode.IMAGE_BW
                       )
        out = v.draw_instance_predictions(outs["instances"].to("cpu"))
        #cv2_imshow(out.get_image()[:, :, ::-1])
        #cv2.waitKey(0)

        return outs


def SketchPredictTable(image: ndarray) -> List[TablePrediction]:
    """Pass an image to a trained object detection neural network model that returns the detected instances with the
    associated labels

    Parameters
    ----------
    image: ndarray
        The image used for the detection of the element (as a ndarray)

    Return
    ------
    List[TablePrediction]
        The list of ObjectPrediction
    """
    table_predictor = SketchTablePredictor()

    predictions = table_predictor.predict(image)

    pred_boxes = predictions.get("instances").get("pred_boxes").tensor.numpy()
    pred_classes = predictions.get("instances").get("pred_classes").numpy()

    predictions = list(zip(pred_boxes, pred_classes))

    return [TablePrediction(label, *box) for box, label in predictions]
