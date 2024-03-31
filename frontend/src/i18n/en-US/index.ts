// This is just an example,
// so you can safely delete all default props below

export default {
  home: {
    welcome: 'Welcome to the DMN Computer Vision Tool',
    description:
      'This is a web application able to convert your images of DMN models into a .dmn format. The tool is able to handle 2 images. The best way to use our application is to start by uploading your DRD image in one of the provided upload spaces. Please do not upload more than 1 DRD at a time. Then, if there is a corresponding decision table, upload it in the other provided space. ',
    university: 'University of KULeuven',
    load: 'Load image',
    convert: 'Convert',
    open: 'Open in Editor',
    converted: 'Great! Your image has been converted and is ready to use.',
    errorReading: 'OOPS! An error occured when reading the image.',
    loaded: 'Your image is loaded',
    errorLoading: 'OOPS! An error occured when reading the image.',
    uploading: 'Uploading...',
    uploadingProgress: 'Uploading... {progress}%',
    waitingForConversion:
      'Please give us some seconds. We are busy transforming your model!',
    errorUploading: 'Error while uploading',
    show_elements: 'Elements',
    show_flows: 'Flows',
    examples: 'Examples',
    examplesInstruction: 'How to use our tool? Here you can find some example images. Please follow these instructions:',
    specifyImageType: ' Specify if the image is a table or a graph by ticking the corresponding boxes.',
    specifyHandwritten: 'Specify if the image is a handwritten file or not by ticking the corresponding boxes.',
    specifyContent: ' Describe the content of the image (e.g., elements, flows, OCR) in the designated field. Example; You have uploaded a DRD and you want everything included in the coversion thus you need to tick "elements", "flows" and "enable ocr".',
    convertImages: ' Click on "Home_Convert Images" to proceed with the conversion.',
  },
  editor: {
    drop: 'Drop',
    open: 'Open',
    create: 'Create',
    intro: 'A DMN diagram to get started.',
    load: 'Load image',
    exit: 'Are you sure you want to quit? All unsaved progress will be lost.',
    errorSaveDMN: 'Error while saving the model as DMN',
    errorUpload: 'Error while uploading a DMN model',
  },
};
