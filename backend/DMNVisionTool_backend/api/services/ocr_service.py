import pytesseract
from typing import List
from numpy import ndarray
from DMNVisionTool_backend.graphs.graph_elements import Element
from DMNVisionTool_backend.graphs.graph_predictions import Text as GraphText
from DMNVisionTool_backend.tables.table_elements import TableElement
from DMNVisionTool_backend.tables.table_predictions import Text as TableText
from DMNVisionTool_backend.commons.utils import get_nearest_element
from textblob import TextBlob



def get_text_from_img(img: ndarray) -> List[GraphText]:
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

    return [GraphText(txt, *box) for box, txt in text_list]
# for graph
def get_text_from_table_img(img: ndarray) -> List[TableText]:
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