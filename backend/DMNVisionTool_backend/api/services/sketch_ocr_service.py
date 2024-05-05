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
#from textblob import TextBlob
import numpy as np
import cv2

def get_text_from_img(img, elements: List[Element]):
    """Extract text from an image using OCR with Tesseract after ROI selection.

    Parameters
    ----------
    img: ndarray
        The image to use for text extraction (as Numpy ndarray)
    elements: 
        List[Element]

    Returns
    -------
    List[Element]
        The list of updated Element
    """
    # Iterate over the elements to extract text from each predicted box
    for element in elements:
        prediction = element.prediction
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        
        # Extract the ROI from the image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        
        # Perform OCR on the ROI
        extracted_text = ''

        d = pytesseract.image_to_data(
            roi, output_type=pytesseract.Output.DICT, config="--psm 12"
            )
        
        n_boxes = len(d["level"])
        extracted_words = []
        for i in range(n_boxes):
            text = d["text"][i]
            if (
                len(text) == 0
                or any(not c.isalnum() for c in text[:-1])
                or (len(text) > 1 and not (text[-1].isalnum() or text[-1] in "-?"))
                or text.lower().count(text[0].lower()) == len(text)
                ):
                continue
            
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            
        extracted_words.append((text))

        for word in extracted_words:
            extracted_text += word
            extracted_text +=' '
            print("Extracted text:", extracted_text)
            
        # Add extracted text to a graph element
        table_text = GraphText(extracted_text, x1, y1, x2, y2)
            
        element.name.append(table_text)
            
    return elements

def get_text_from_table_img_sketch(img, table_elements: List[TableElement]) -> List[TableElement]:
    """Extract all the text from an image using OCR with pytesseract

    Parameters
    ----------
    img: ndarray
        The image to use for the text extraction (as Numpy ndarray)
    table_elements: List[TableElement]
        The table recognized elements

    Returns
    -------
    table_elements: List[TableElement]
        The table updated elements with recognized text
    """
    # Iterate over the elements to extract text from each predicted box
    for table_element in table_elements:
        prediction = table_element.prediction
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        
        # Extract the ROI from the image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        
        # Perform OCR on the ROI
        extracted_text = ''

        d = pytesseract.image_to_data(
            roi, output_type=pytesseract.Output.DICT, config="--psm 12"
            )
        
        n_boxes = len(d["level"])
        extracted_words = []
        for i in range(n_boxes):
            text = d["text"][i]
            if (
                len(text) == 0
                or any(not c.isalnum() for c in text[:-1])
                or (len(text) > 1 and not (text[-1].isalnum() or text[-1] in "-?"))
                or text.lower().count(text[0].lower()) == len(text)
                ):
                continue
            
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            
        extracted_words.append((text))

        for word in extracted_words:
            extracted_text += word
            extracted_text +=' '
            print("Extracted text:", extracted_text)
            
        # Add extracted text to a graph element
        table_text = TableText(extracted_text, x1, y1, x2, y2)
            
        table_element.label.append(table_text)
            
    return table_elements