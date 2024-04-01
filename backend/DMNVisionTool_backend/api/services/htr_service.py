# File for the handwritten text recognition
# Instead of recognizing text on the whole image and then linking to the elements, we look for text on the predicted elements
from PIL import Image
from typing import List
from transformers import TrOCRProcessor
from transformers import VisionEncoderDecoderModel

from DMNVisionTool_backend.graphs.graph_elements import Element

model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def get_text_from_element(image_path: str, elements: List[Element]):
    """ Function that recognise text within one element
    Parameters
    ----------
    image_path: Path where the image is located
    elements: List[Element]
        List of Element recognised on the graph

    Returns
    -------
    List[Element]
        The list of updated Element with their text
    """
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    
    image = Image.open(image_path).convert("RGB")
    
    for element in elements:
        bbox = element.prediction.get_box_coordinates()
        cropped_image = image.crop(bbox)
    
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        #model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to(device)
        pixel_values = processor(cropped_image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]        
        
        element.name.append(generated_text)
    return elements