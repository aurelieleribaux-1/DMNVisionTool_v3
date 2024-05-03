import pytesseract
from typing import List
from numpy import ndarray
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_elements import Element
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import Text as GraphText
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import ObjectPrediction
from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction
from DMNVisionTool_backend.DecisionTables.table_elements import TableElement
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import Text as GraphText
from DMNVisionTool_backend.DecisionTables.table_predictions import Text as TableText
from DMNVisionTool_backend.commons.utils import get_nearest_element
from textblob import TextBlob
import numpy as np
import cv2

def get_text_from_img(img,predictions: List[ObjectPrediction]):
    """Extract text from an image using OCR with Tesseract after ROI selection.

    Parameters
    ----------
    img: ndarray
        The image to use for text extraction (as Numpy ndarray)

    Returns
    -------
    List[GraphText]
        The list of detected text with bounding boxes
    """
    # Convert the image to grayscale
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize list to store extracted text with bounding boxes
    text_list = []

    # Iterate over the predictions and extract text from each predicted box
    for prediction in predictions:
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        # Extract the ROI from the grayscale image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        # Resize the ROI based on the resizing factor
        roi_resized = cv2.resize(roi, None, fx=20 if len(predictions) > 7 else 10, fy=20 if len(predictions) > 7 else 10, interpolation=cv2.INTER_CUBIC)
        # Perform OCR on the ROI
        text = pytesseract.image_to_string(roi_resized, config="--psm 12")
        # Spell-check the extracted text using TextBlob
        corrected_text = TextBlob(text).correct().string
        # Create a GraphText object with the corrected text and bounding box
        graph_text = GraphText(corrected_text, x1, y1, x2 - x1, y2 - y1)
        # Append the GraphText object to the list
        text_list.append(graph_text)
            
    

    return text_list

def get_text_from_table_img_sketch(img: ndarray,predictions: List[TablePrediction]) -> List[TableText]:
    """Extract all the text from an image using OCR with pytesseract

    Parameters
    ----------
    img: ndarray
        The image to use for the text extraction (as Numpy ndarray)

    Returns
    -------
    List[Text]
        The list of detected Text
    """

    # Convert the image to grayscale
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize list to store extracted text with bounding boxes
    text_list = []

    # Iterate over the predictions and extract text from each predicted box
    for prediction in predictions:
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        # Extract the ROI from the grayscale image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        # Resize the ROI if needed
        roi_resized = cv2.resize(roi, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
        # Perform OCR on the ROI
        text = pytesseract.image_to_string(roi_resized, config="--psm 12")
        # Spell-check the extracted text using TextBlob
        corrected_text = TextBlob(text).correct().string
        # Create a GraphText object with the corrected text and bounding box
        table_text = TableText(corrected_text, x1, y1, x2 - x1, y2 - y1)
        # Append the GraphText object to the list
        text_list.append(table_text)

    return  text_list

def link_text(texts: List[GraphText], elements: List[Element]):
    """Method that links the Text to the corresponding Elements

    Parameters
    ----------
    texts: List[GraphText]
        List of detected Text
    elements: List[Element]
        List of Element to be linked

    Returns
    -------
    List[Element]
        The list of updated Element
    """
    for text in texts:
        nearest = get_nearest_element(text.center, elements)
        nearest.name.append(text)
    return elements

# for tables: !!! 2 classes called Text !!!
def link_text_table(texts: List[TableText], elements: List[TableElement]):
    """Method that links the Text to the corresponding Elements

    Parameters
    ----------
    texts: List[TableText]
        List of detected Text
    elements: List[TableElement]
        List of Element to be linked

    Returns
    -------
    List[TableElement]
        The list of updated Element
    """
    for text in texts:
        nearest = get_nearest_element(text.center, elements)
        nearest.label.append(text)
    return elements