// This is just an example,
// so you can safely delete all default props below

export default {
  home: {
    welcome: 'Welcome to the DMN Computer Vision Tool',
    description:'This is a web application able to convert your images of DMN models into a .dmn format. The tool is already able to handle one DRD and link one corresponding Decision Table to this DRD. Moreover, it can handle both digitally drawn and handwritten DMN images.',
    university:'KULeuven',
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
    examplesInstruction: 'How to use the tool? Please follow these instructions:',
    specifyImageType: ' First upload your DRD image in the provided area. Then, please confirm that is a DRD by ticking the corresponding checkbox above the uploaded image.',
    specifyContent: 'Similarly, upload your Decision Table images in the provided area below and tick the checkbox. ',
    specifyHandwritten: 'Specify if the image is a handwritten file or Digital file by ticking the corresponding boxes.',
    convertImages: 'Click on "Home_Convert Images" to proceed with the conversion.',
    ImageExample: 'Here you can find some example images. Please feel free to download the first two examples if you want to test a digitally drawn DMN, or the last two examples to test a handwritten DMN model. In case you want to use your own images , beware that these images should be of good quality and resemble the example images.'
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
