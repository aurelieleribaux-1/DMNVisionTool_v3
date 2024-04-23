import pytesseract
from typing import List
from numpy import ndarray
from DMNVisionTool_backend.graphs.graph_elements import Element
from DMNVisionTool_backend.graphs.graph_predictions import Text as GraphText
from DMNVisionTool_backend.graphs.graph_predictions import ObjectPrediction
from DMNVisionTool_backend.tables.table_elements import TableElement
from DMNVisionTool_backend.tables.table_predictions import Text as TableText
from DMNVisionTool_backend.commons.utils import get_nearest_element
from DMNVisionTool_backend.api.services.ROI_selection_service import detect_lines
from textblob import TextBlob
import numpy as np


from textblob import TextBlob

import cv2
import pytesseract
from textblob import TextBlob
from DMNVisionTool_backend.graphs.graph_predictions import Text as GraphText

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
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initialize list to store extracted text with bounding boxes
    text_list = []

    # Iterate over the predictions and extract text from each predicted box
    for prediction in predictions:
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        # Extract the ROI from the grayscale image
        roi = gray_img[int(y1):int(y2), int(x1):int(x2)]
        # Resize the ROI if needed
        roi_resized = cv2.resize(roi, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
        # Perform OCR on the ROI
        text = pytesseract.image_to_string(roi_resized, config="--psm 12")
        # Spell-check the extracted text using TextBlob
        corrected_text = TextBlob(text).correct().string
        # Create a GraphText object with the corrected text and bounding box
        graph_text = GraphText(corrected_text, x1, y1, x2 - x1, y2 - y1)
        # Append the GraphText object to the list
        text_list.append(graph_text)
            
    

    return text_list


def get_text_from_table_img_pdf(img: np.ndarray) -> List[TableText]:
    """Extract all the text from an image using OCR with pytesseract

    Parameters
    ----------
    img: ndarray
        The image to use for the text extraction (as Numpy ndarray)

    Returns
    -------
    List[TableText]
        The list of detected Text with their bounding boxes
    """
    text_list = []

    custom_config = r'--psm 12 load_system_dawg=false load_freq_dawg=false'  # Custom configuration string
    
    # Detect horizontal and vertical lines in the image
    horizontal_lines, vertical_lines = detect_lines(img)
    
    # Loop over each ROI defined by the intersection of horizontal and vertical lines
    for i, h_line in enumerate(horizontal_lines[:-1]):
        for j, v_line in enumerate(vertical_lines[:-1]):
            x1, y1, _, h1 = h_line
            _, x2, w2, _ = v_line
            
            # Check if ROI coordinates are valid
            if x1 >= x2 or y1 >= h1:
                continue
            
            # Extract ROI image
            roi = img[y1:h1, x2:x2+w2]
            
            # Skip empty ROIs
            if roi.size == 0:
                continue

            # Apply OCR to the ROI
            d = pytesseract.image_to_data(roi, output_type=pytesseract.Output.DICT, config=custom_config)

            # Process OCR results and extract text along with bounding boxes
            for k in range(len(d["level"])):
                text = d["text"][k]
                if (
                    len(text) == 0
                    or any(not c.isalnum() for c in text[:-1])
                    or len(text) > 1
                    and not (text[-1].isalnum() or text[-1] in "-?")
                    or text.lower().count(text[0].lower()) == len(text)
                ):
                    continue
                (x, y, w, h) = (d["left"][k] + x2, d["top"][k] + y1, d["width"][k], d["height"][k])
                text_list.append(TableText(text, x, y, w, h))

    return text_list

def get_text_from_table_img_sketch(img: ndarray) -> List[TableText]:
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

    text_list = []

    d = pytesseract.image_to_data(
        img, output_type=pytesseract.Output.DICT, config="--psm 12"
    )
    n_boxes = len(d["level"])
    for i in range(n_boxes):
        text = d["text"][i]
        if (
            len(text) == 0
            or any(not c.isalnum() for c in text[:-1])
            or len(text) > 1
            and not (text[-1].isalnum() or text[-1] in "-?")
            or text.lower().count(text[0].lower()) == len(text)
            
        ):
            continue
        (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text_list.append(([x, y, w, h], text))

    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    return [TableText(txt, *box) for box, txt in text_list]


    
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