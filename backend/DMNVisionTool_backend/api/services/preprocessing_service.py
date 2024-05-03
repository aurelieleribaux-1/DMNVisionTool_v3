import os
import numpy as np
import cv2

def get_ocr_image_pdf(image_path: str):
    """Service that reads, sharpens, and enhances an image for OCR tasks, given its path

    Parameters
    ----------
    image_path: str
        The path where to read the image

    Returns
    -------
    ndarray
        The enhanced image for OCR
    """

    # Read the sharpened image using OpenCV
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is not None and img.shape[2] == 4:
        print('image will be enhanced')
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

def get_predict_image_pdf(image_path: str):
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
    -> Change os.remove ?? TO DO

    Parameters
    ----------
    path: str
        The local path where the image is downloaded

    Returns
    -------
    tuple
        The two images for OCR and predictions

    """
    ocr_img_pdf = get_ocr_image_pdf(path)
    predict_img_pdf = get_predict_image_pdf(path)
    return ocr_img_pdf , predict_img_pdf