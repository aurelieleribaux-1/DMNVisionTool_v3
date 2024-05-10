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
****.

#A tutorial on its usage is available by clicking the image below:
[![Watch the video]()]()

## How to run

DMNComputerVisionTool is available as a Docker image by creating it from this folder or pulling it from [DockerHub](https://hub.docker.com/r/proslab/bpmn-redrawer).

First of all, download the trained detectron2 models from [Hugging Face]() and move them in the [detectron_model](backend/DMNVisionTool_backend/detectron_model) folder.

In particular these two models are:
- <b>DRD_model_final.pth</b>
- <b>kp_DRD_model_final.pth</b>
- <b>Table_model_final.pth</b>
- <b>SketchDRD_model_final.pth</b>
- <b>Sketchkp_DRD_model_final.pth</b>
- <b>SketchTable_model_final.pth</b>


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
