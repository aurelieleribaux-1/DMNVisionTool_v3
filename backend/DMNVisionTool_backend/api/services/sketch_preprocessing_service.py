import os
import numpy as np
import cv2

def get_ocr_image_sketch(image_path: str):
    """Service that reads and enhances an image for OCR tasks, given its path

    Parameters
    ----------
    image_path: str
        The path where to read the image

    Returns
    -------
    ndarray
        The enhanced image for OCR
    """
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Prepare RGBA image for display by handling transparency - Image has an alpha channel
    if img is not None and len(img.shape) == 3 and img.shape[2] == 4:
        print("Image is not none and has an alpha channel")
        trans_mask = img[:, :, 3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        img = (
            img.astype(np.uint16)
            + 255
            - np.repeat(np.expand_dims(img[:, :, 3], 2), 4, axis=2)
            )
        img = np.ndarray.clip(img, 0, 255)
        img = img[:, :, [0, 1, 2]]
        img = np.ascontiguousarray(img, dtype=np.uint8)
        
        return img
    
    # Image does not have an alpha channel
    elif img is not None:
        print("Image is not none but does not have an alpha channel")
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to create a binary image
        _, binary_image = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        # Invert the binary image to make darker pixels black and lighter pixels white
        img = cv2.bitwise_not(binary_image)
        
        return img
        
    else: 
        print('Failed to load image')

def get_predict_image_sketch(image_path: str):
    """Service that reads and returns an image suitable for an Object/KeyPoints detection task, given its path

    Parameters
    ----------
    image_path: str
        The path where to read the image

    Returns
    -------
    ndarray
        The image for the Object/KeyPoints detection
    """
    # Read the image
    img = cv2.imread(image_path)
    
    return img

def get_ocr_and_predict_images(path: str):
    """Service that returns the images for the OCR and Object/KeyPoints detection tasks. 
    It retrieve the original image from Firebase storage given its name

    Parameters
    ----------
    path: str
        The local path where the image is downloaded

    Returns
    -------
    tuple
        The two images for OCR and predictions

    """
    ocr_img_sketch = get_ocr_image_sketch(path)
    predict_img_sketch = get_predict_image_sketch(path)

    return ocr_img_sketch , predict_img_sketch