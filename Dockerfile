FROM node:14.18 AS frontend
RUN mkdir /app
WORKDIR /app
COPY frontend ./
RUN yarn
RUN yarn build

# Use Python 3.8 base image
FROM python:3.8 AS backend

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Git LFS
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install -y git-lfs

RUN mkdir /app
WORKDIR /app

ARG BACKEND_MODE=production
ARG BACKEND_PORT=5000

ENV BACKEND_MODE=${BACKEND_MODE}
ENV BACKEND_PORT=${BACKEND_PORT}

COPY backend/DMNVisionTool_backend DMNVisionTool_backend/
RUN [ -f DMNVisionTool_backend/detectron_model/DRD_model_final.pth ] && echo "Object Detection model found" || { echo "Object Detection model not found!"; wget -O DMNVisionTool_backend/detectron_model/DRD_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/DRD_model_final.pth; }
RUN [ -f DMNVisionTool_backend/detectron_model/kp_DRD_model_final.pth ] && echo "KeyPoint Prediction model found" || { echo "KeyPoint Prediction model not found!"; wget -O DMNVisionTool_backend/detectron_model/kp_DRD_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/kp_DRD_model_final.pth; }
RUN [ -f DMNVisionTool_backend/detectron_model/Table_model_final.pth ] && echo "Object Detection model found" || { echo "Object Detection model not found!"; wget -O DMNVisionTool_backend/detectron_model/Table_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/Table_model_final.pth; }
RUN [ -f DMNVisionTool_backend/detectron_model/SketchDRD_model_final.pth ] && echo "Object Detection model found" || { echo "KeyPoint Prediction model not found!"; wget -O DMNVisionTool_backend/detectron_model/SketchDRD_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/SketchDRD_model_final.pth; }
RUN [ -f DMNVisionTool_backend/detectron_model/Sketchkp_DRD_model_final.pth ] && echo "KeyPoint Detection model found" || { echo "Object Prediction model not found!"; wget -O DMNVisionTool_backend/detectron_model/Sketchkp_DRD_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/Sketchkp_DRD_model_final.pth; }
RUN [ -f DMNVisionTool_backend/detectron_model/SketchTable_model_final.pth ] && echo "Sketch Table Detection model found" || { echo "Sketch Table Detection model not found!"; wget -O DMNVisionTool_backend/detectron_model/SketchTable_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/SketchTable_model_final.pth; }
 

# Install/update Pillow
RUN pip install -U pip


# Update package lists # Install Tesseract OCR and necessary language data for LSTM mode
RUN apt-get update && apt-get install -y \
tesseract-ocr \
tesseract-ocr-eng  # Example: English language data for LSTM mode
RUN apt-get install -y apt-transport-https
RUN echo 'deb https://notesalexp.org/tesseract-ocr-dev/bullseye/ bullseye main' >> /etc/apt/sources.list
#RUN apt-get update

# Install additional trained data for handwritten text recognition
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata/
RUN curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata
RUN curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/eng_lstm.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/eng_lstm.traineddata

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/facebookresearch/detectron2.git@ff53992b1985b63bd3262b5a36167098e3dada02

RUN pip show numpy

# Copy frontend static files
COPY --from=frontend /app/dist/spa /app/DMNVisionTool_backend/static

# Set the command to run the application
CMD uvicorn --host 0.0.0.0 --port ${BACKEND_PORT} --factory DMNVisionTool_backend.app:create_app

# Expose the port the application runs on
EXPOSE ${BACKEND_PORT}
