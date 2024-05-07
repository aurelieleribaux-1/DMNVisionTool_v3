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
import nltk
from collections import Counter
import Levenshtein

# Load English words dictionary from nltk
nltk.download('words')
english_words = set(nltk.corpus.words.words())

def get_valid_word(word, all_words):
    english_word_matches = []
    for w in all_words:
        if w.lower() in english_words:
            english_word_matches.append(w)
    if english_word_matches:
        best_match = min(english_word_matches, key=lambda x: Levenshtein.distance(word.lower(), x.lower()))
        return best_match
    else:
        # If no valid replacement word is found, correct the existing word 
        return TextBlob(word).correct().string

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

    if len(predictions) > 14:
        resize_factor = 27
    elif len(predictions) > 7:
        resize_factor = 20
    else: 
        resize_factor = 10
    # Initialize list to store extracted text with bounding boxes
    text_list = []

    # Iterate over the predictions and extract text from each predicted box
    for prediction in predictions:
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        # Extract the ROI from the grayscale image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        # Resize the ROI based on the resizing factor
        roi_resized = cv2.resize(roi, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_CUBIC)
        # Perform OCR on the ROI
        text = pytesseract.image_to_string(roi_resized, config="--psm 12 --oem 1 -c tessedit_char_blacklist={+-,./?;:@[]()*&^%$£!¬`}|><_}")
        # Tokenize the text
        words = text.split()
        # Initialize a set to keep track of unique words in the corrected text
        unique_words = set()
        # Replace nonsensical words with the most frequent English word
        corrected_text = []
        for word in words:
            if word.lower() not in english_words:
                # If the word is not in the English words dictionary, replace it with a valid word
                valid_word = get_valid_word(word, words)
                if valid_word not in unique_words:
                    # Add the valid word to the corrected text and the set of unique words
                    corrected_text.append(valid_word)
                    unique_words.add(valid_word)
            else:
                # If the word is in the English words dictionary, keep it in the corrected text
                corrected_text.append(word)
        # Join the corrected text into a single string
        corrected_text = " ".join(corrected_text)
        # Create a GraphText object with the corrected text and bounding box
        graph_text = GraphText(corrected_text, x1, y1, x2 - x1, y2 - y1)
        # Append the GraphText object to the list
        text_list.append(graph_text) 

    return text_list

def get_text_from_img2(img, elements: List[Element]):
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

def get_text_from_table_img_sketch(img,predictions: List[TablePrediction]):
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

    if len(predictions) > 19:
        resize_factor = 2
    else: 
        resize_factor = 1
    # Initialize list to store extracted text with bounding boxes
    text_list = []

    # Iterate over the predictions and extract text from each predicted box
    for prediction in predictions:
        x1, y1, x2, y2 = prediction.get_box_coordinates()
        # Extract the ROI from the grayscale image
        roi = img[int(y1):int(y2), int(x1):int(x2)]
        # Resize the ROI based on the resizing factor
        roi_resized = cv2.resize(roi, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_CUBIC)
        # Perform OCR on the ROI
        if len(predictions) > 19:
          # Perform OCR on the ROI
          text = pytesseract.image_to_string(roi_resized, config="--psm 6 --oem 1 -c tessedit_char_blacklist={+-}")
        else: 
          text = pytesseract.image_to_string(roi_resized, config="--psm 12 --oem 1 -c tessedit_char_blacklist={+-}")
        # Tokenize the text
        words = text.split()
        # Initialize a set to keep track of unique words in the corrected text
        unique_words = set()
        # Replace nonsensical words with the most frequent English word
        corrected_text = []
        for word in words:
            if word.lower() not in english_words:
                # If the word is not in the English words dictionary, replace it with a valid word
                valid_word = get_valid_word(word, words)
                if valid_word not in unique_words:
                    # Add the valid word to the corrected text and the set of unique words
                    corrected_text.append(valid_word)
                    unique_words.add(valid_word)
            else:
                # If the word is in the English words dictionary, keep it in the corrected text
                corrected_text.append(word)
        # Join the corrected text into a single string
        corrected_text = " ".join(corrected_text)
        # Create a GraphText object with the corrected text and bounding box
        table_text = GraphText(corrected_text, x1, y1, x2 - x1, y2 - y1)
        # Append the GraphText object to the list
        text_list.append(table_text) 

    return text_list


def get_text_from_table_img_sketch2(img, table_elements: List[TableElement]) -> List[TableElement]:
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