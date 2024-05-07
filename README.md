# DMN Computer Vision Tool

DMN Computer Vision Tool is a web application that allows to upload images representing DMN models to convert them in actual DMN models stored in *.dmn* format.

## Table of contents
<!--ts-->
   * [Functionalities](#functionalities)
   * [Quickstart](#quickstart)
   * [How to run](#how-to-run)
   * [Backend](#backend)
   * [Frontend](#frontend)
<!--te-->

## Functionalities

Users can easily load images from local storage in various formats (PNG, JPEG, BMP, TIFF) using the simple and intuitive graphical user interface (GUI). Once loaded, the image is displayed and ready for conversion. The backend processes the loaded image, extracting its elements and linking them together to generate the final .dmn file. Upon completion, the result is sent back to the frontend where users can interact with it through the GUI. They have the option to download the file directly or view and edit it using the bpmn-js library seamlessly integrated into the interface.

Overall, the application is able to provide the following functionalities:
- Convert an image into the corresponding *.dmn* model;
- Download the converted model;
- Visualize the converted model;
- Edit the converted model;
- Open, edit and download an existing *.dmn* model;
- Create a DMN model from scratch and download it as *.dmn* file ;


## Quickstart

#Our web application is available and ready to use at the following link:
**[BPMN Redrawer](https://pros.unicam.it/bpmn-redrawer-tool/)**.

#A tutorial on its usage is available by clicking the image below:
[![Watch the video](https://img.youtube.com/vi/0e2qnbSp9XY/maxresdefault.jpg)](https://youtu.be/0e2qnbSp9XY)

The user can perform very simple steps to obtain a *.dmn* file starting from an image:
- In the *HOME* page, the user can load an image from local storage with the corresponding button or one of the sample images by clicking on them;
<p align="center">
<img src="extra/images/home.png" width="90%" />
</p>

- If correctly loaded, the image will be displayed;
- Different options can be enabled to be performed by the backend, such as:
    - object detection for the DMN elements;
    - keypoint detection for the DMN flows;
    - OCR for the DMN labels;
- Then the *CONVERT* button can be clicked to start the conversion (it takes a few seconds to complete the process);
- Once the conversion is done, the user can either download or view and edit the resulting model;
- By selecting the *VIEW IN EDITOR* button, the *EDITOR* page will allow the user to see the converted model and, if needed, to edit and correct it. The starting image is displayed next to the model and simplifies the revising process (a vertical splitter can be moved to resize the BPMN editor and the image viewer);
<p align="center">
<img src="extra/images/editor.png" width="90%" />
</p>

- If the user is happy with the result, the final model can be downloaded either as *.bpmn* file or as *.svg* image.

The user can also use the *EDITOR* page to open, edit and download an existing *.bpmn* model or to create a BPMN model from scratch, as well as loading an image in the image viewer.

## How to run

BPMN Redrawer is available as a Docker image by creating it from this folder or pulling it from [DockerHub](https://hub.docker.com/r/proslab/bpmn-redrawer).

First of all, download the trained detectron2 models from [Hugging Face](https://huggingface.co/PROSLab/BPMN-Redrawer-Models/tree/main) and move them in the [detectron_model](backend/bpmn_redrawer_backend/detectron_model) folder.

In particular these two models are:
- <b>final_model.pth</b>: the Object Detection model;
- <b>kp_final_model.pth</b>: the KeyPoint Prediction model.

This is needed when working with the application without using containers. When using the containers, the models will be downloaded automatically.

To build the image, from the root folder it is sufficient to launch the command:
```bash
docker build -t dmn-computer-vision-tool .
```

Once the image has been built, it is possible to run it with the command:
```bash
docker run -d -p 5000:5000 -e BACKEND_PORT=5000 -e BACKEND_MODE=production --name dmn-visiontool-container dmn-computer-vision-tool
```


Two variables are available when running the container:
- BACKEND_MODE: <b>development</b> or <b>production</b> (default=<b>production</b>)
- BACKEND_PORT: which port the container will use internally to run the app (default=<b>5000</b>). This is the containerPort in the command:
    ```bash
    -p hostPort:containerPort
    ```

Once launched, the application will be available at [http://localhost:5000](http://localhost:5000).

## Backend

The [Backend README](backend/README.md) contains more instructions on how to launch/develop the backend.

## Frontend

The [Frontend README](frontend/README.md) contains more instructions on how to launch/develop the frontend.
