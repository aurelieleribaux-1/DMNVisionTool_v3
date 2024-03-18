FROM node:14.18 AS frontend
RUN mkdir /app
WORKDIR /app
COPY frontend ./
RUN yarn
RUN yarn build

# Use Python 3.8 base image
FROM python:3.8 AS backend

# Print Python version
RUN python --version

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
RUN [ -f DMNVisionTool_backend/detectron_model/TableStructure_model_final.pth ] && echo "Object Detection model found" || { echo "KeyPoint Prediction model not found!"; wget -O DMNVisionTool_backend/detectron_model/TableStructure_model_final.pth https://huggingface.co/aurelieleribaux/DMNComputerVisionTool_Models/blob/main/TableStructure_model_final.pth; }

# Install/update Pillow
RUN pip install -U pip

# Install PyTorch
RUN pip install torch torchvision torchaudio

RUN pip install uvicorn


# Update package lists and install tesseract-ocr
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install -y apt-transport-https
RUN echo 'deb https://notesalexp.org/tesseract-ocr-dev/bullseye/ bullseye main' >> /etc/apt/sources.list
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -
RUN apt-get update

# Install Python dependencies
COPY backend/DMNVisionTool_backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/facebookresearch/detectron2.git@ff53992b1985b63bd3262b5a36167098e3dada02


# Copy frontend static files
COPY --from=frontend /app/dist/spa /app/DMNVisionTool_backend/static

# Set the command to run the application
CMD uvicorn --host 0.0.0.0 --port ${BACKEND_PORT} --factory DMNVisionTool_backend.app:create_app

# Expose the port the application runs on
EXPOSE ${BACKEND_PORT}
