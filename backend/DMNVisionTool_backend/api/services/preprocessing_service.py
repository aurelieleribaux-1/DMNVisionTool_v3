import os
import numpy as np
import cv2


def get_ocr_image(image_path: str):
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


import cv2
import numpy as np

def get_predict_image(image_path: str):
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

    # Upscale the resolution to 600 DPI
    upscale_ratio = 600.0 / min(img.shape[0], img.shape[1]) # Calculate scaling ratio
    new_width = int(img.shape[1] * upscale_ratio) # New width after scaling
    new_height = int(img.shape[0] * upscale_ratio) # New height after scaling
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Apply sharpening filter
    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel_sharpening)

    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold_img


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

    ocr_img = get_ocr_image(path)
    predict_img = get_predict_image(path)
    #if ocr_img is not None and predict_img is not None:
    #    os.remove(path)
    return ocr_img, predict_img