<template>
  <div class="container">
    <!-- Header Section -->
    <header class="header">
      <div class="q-pa-md">
        <div style="margin: auto; text-align: center">
          <div style="font-size: 32px">{{ $t('home.welcome') }}</div>
          <div style="font-size: 18px">
            {{ $t('home.description') }}
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content Section -->
    <main class="main-content">
      <div class="upload-container">
        <!-- Left Section -->
        <section class="upload-section" @dragover="allowDrop($event)" @drop="drop($event, 'left')">
          <h2>Upload Image 1</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePickerLeft?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePickerLeft"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp"
            v-model="fileLeft"
            @update:model-value="loadImageLeft(fileLeft as File)"
          ></q-file>
          <q-dialog v-model="conversionDialogLeft" persistent>
                <q-card>
                  <q-card-section class="row items-center">
                    <span class="q-ml-sm">{{ $t('home.converted') }}</span>
                    <q-space />
                    <q-btn icon="close" flat round dense v-close-popup />
                  </q-card-section>
                  <q-card-actions align="right">
                    <q-btn
                      flat
                      icon="download"
                      label="Download"
                      color="primary"
                      @click="downloadModelLeft()"
                    />
                    <q-btn
                      flat
                      icon="arrow_forward"
                      :label="$t('home.open')"
                      color="primary"
                      @click="editModelLeft()"
                    />
                  </q-card-actions>
                </q-card>
              </q-dialog>
          <div class="options">
            <q-checkbox
              class="q-pr-md"
              v-model="elementsEnabledLeft"
              :label="$t('home.show_elements')"
            ></q-checkbox>
            <q-checkbox
              :disable="isTableLeft" 
              class="q-pr-md"
              v-model="flowsEnabledLeft"
              :label="$t('home.show_flows')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabledLeft"
              class="q-pr-md"
              v-model="ocrEnabledLeft"
              label="Enable OCR"
            ></q-checkbox>
            <q-checkbox
              :disable="isTableLeft" 
              class="q-pr-md"
              v-model="isGraphLeft"
              label="Graph"
            ></q-checkbox>
            <q-checkbox
              :disable="isGraphLeft" 
              class="q-pr-md"
              v-model="isTableLeft"
              label="Table"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <h2>Your Uploaded Image 1</h2>
            <div class="image-container">
              <q-img
                :style="'border: 2px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 800px) 800px, (max-height: 600px) 600px"
                fit="contain"
                position="50% 50%"
                width="800px"
                height="600px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrcLeft as string)"
                @load="loadingOK"
                @error="loadingError('left')"
                @dragover="allowDrop($event)"
                @drop="drop($event, 'left')"
              ></q-img>
              <q-btn
                 :disable="!imageLoadedLeft"
                 color="accent"
                 icon-right="arrow_forward"
                 :label="$t('home.convert')"
                 @click="convertImageLeft()"
              ></q-btn>
            </div>
          </div>
        </section>

        <!-- Convert Images Button -->
        <div class="q-pa-md" style="text-align: center">
          <q-btn
            color="accent"
            :label="$t('home.convert_images')"
            @click="convertImages"
            :disable="!imageLoadedLeft || !imageLoadedRight" 
            class="convert-button"
          ></q-btn>
        </div>

        <!-- Right Section -->
        <section class="upload-section" @dragover="allowDrop($event)" @drop="drop($event, 'right')">
          <h2>Upload Image 2</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePickerRight?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePickerRight"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp"
            v-model="fileRight"
            @update:model-value="loadImageRight(fileRight as File)"
          ></q-file>
          <q-dialog v-model="conversionDialogRight" persistent>
                <q-card>
                  <q-card-section class="row items-center">
                    <span class="q-ml-sm">{{ $t('home.converted') }}</span>
                    <q-space />
                    <q-btn icon="close" flat round dense v-close-popup />
                  </q-card-section>
                  <q-card-actions align="right">
                    <q-btn
                      flat
                      icon="download"
                      label="Download"
                      color="primary"
                      @click="downloadModelRight()"
                    />
                    <q-btn
                      flat
                      icon="arrow_forward"
                      :label="$t('home.open')"
                      color="primary"
                      @click="editModelRight()"
                    />
                  </q-card-actions>
                </q-card>
              </q-dialog>
          <div class="options">
            <q-checkbox
              class="q-pr-md"
              v-model="elementsEnabledRight"
              :label="$t('home.show_elements')"
            ></q-checkbox>
            <q-checkbox
              :disable="isTableRight" 
              class="q-pr-md"
              v-model="flowsEnabledRight"
              :label="$t('home.show_flows')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabledRight"
              class="q-pr-md"
              v-model="ocrEnabledRight"
              label="Enable OCR"
            ></q-checkbox>
            <q-checkbox
              :disable="isTableRight" 
              class="q-pr-md"
              v-model="isGraphRight"
              label="Graph"
            ></q-checkbox>
            <q-checkbox
              :disable="isGraphRight" 
              class="q-pr-md"
              v-model="isTableRight"
              label="Table"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <h2>Your Uploaded Image 2</h2>
            <div class="image-container">
              <q-img
                :style="'border: 2px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 800px) 800px, (max-height: 600px) 600px"
                fit="contain"
                position="50% 50%"
                width="800px"
                height="600px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrcRight as string)"
                @load="loadingOK"
                @error="loadingError('right')"
                @dragover="allowDrop($event)"
                @drop="drop($event, 'right')"
              ></q-img>
              <q-btn
                :disable="!imageLoadedRight"
                color="accent"
                icon-right="arrow_forward"
                :label="$t('home.convert')"
                @click="convertImageRight()"
              ></q-btn>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Example Images Section -->
    <div class="q-pa-md" style="text-align: center">
      <div style="font-size: 18px">{{ $t('home.examples') }}</div>
      <div style="font-size: 14px">{{ $t('home.examplesInstruction') }}</div>
      <div class="row justify-evenly wrap">
        <div class="q-pa-sm" v-for="i in 3" :key="i">
          <q-img
            :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
            sizes="(max-width: 400px) 400px, (max-height: 400px) 400px"
            fit="contain"
            position="50% 50%"
            width="400px"
            height="400px"
            :src="require(`../assets/example${i}.png`)"
            @click="loadExampleImage(i)"
          ></q-img>
        </div>
      </div>
    </div>

    <!-- Footer Section -->
    <div class="q-py-md" style="margin: auto; text-align: center; width: 100%">
      <div style="font-size: 18px">
        DMN Computer Vision Tool
          <br />
          {{ $t('home.university') }}
          <br />
      </div>
    </div>
  </div>
</template>



<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';
import { exportFile, QFile, useQuasar } from 'quasar';
import { api } from 'src/boot/axios';
import { useRouter } from 'vue-router';
import { i18n } from 'src/boot/i18n';
import { blobToDataURL } from './utils/image-utils';
import axios from 'axios';
import { useDmnStore } from 'src/store/dmnStore';

export default defineComponent({
  name: 'HomeComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const filePickerLeft: Ref<QFile | null> = ref(null);
    const filePickerRight: Ref<QFile | null> = ref(null);
    const fileLeft: Ref<File | null> = ref(null);
    const fileRight: Ref<File | null> = ref(null);
    const imageFileLeft: Ref<File | null> = ref(null);
    const imageFileRight: Ref<File | null> = ref(null);
    const imgSrcLeft: Ref<string | null> = ref(null);
    const imgSrcRight: Ref<string | null> = ref(null);
    const conversionDialogLeft: Ref<boolean> = ref(false);
    const conversionDialogRight: Ref<boolean> = ref(false);
    const conversionResultLeft: Ref<string | null> = ref(null);
    const conversionResultRight: Ref<string | null> = ref(null);
    const imageLoadedLeft = ref(false);
    const imageLoadedRight = ref(false);
    const elementsEnabledLeft = ref(false);
    const elementsEnabledRight = ref(false);
    const flowsEnabledRight = ref(false);
    const flowsEnabledLeft = ref(false);
    const ocrEnabledLeft = ref(false);
    const ocrEnabledRight = ref(false);
    const isGraphLeft = ref(false);
    const isGraphRight = ref(false);
    const isTableLeft = ref(false);
    const isTableRight = ref(false);

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent, section: string) => {
      e.preventDefault();
      const files = (e.dataTransfer as DataTransfer).files;
      if (files.length != 1) {
        return;
      }
      const file = files[0];
      if (
         file.name.endsWith('.png') ||
         file.name.endsWith('.jpeg') ||
         file.name.endsWith('.jpg') ||
         file.name.endsWith('.bmp')
      ) {
        if (section === 'left') {
          if (fileLeft.value !== null) { 
            await loadImageLeft(fileLeft.value);
          }
        } else if (section === 'right') {
          if (fileRight.value !== null) {
           await loadImageRight(fileRight.value);
          }
        }
      }
    };

    
    const loadImageLeft = async (fileToLoad: File) => {
      await blobToDataURL(fileToLoad)
       .then((result) => {
          imgSrcLeft.value = result;
          imageLoadedLeft.value = true;
          imageFileLeft.value = fileToLoad;
       })
       .catch(() => {
          imgSrcLeft.value = null;
          imageLoadedLeft.value = false;
          $q.notify({
              message: i18n.global.t('home.errorReading'),
              type: 'negative',
          });
          imageFileLeft.value = null;
       });
      fileLeft.value = null;
    };

    const loadImageRight = async (fileToLoad: File) => {
      await blobToDataURL(fileToLoad)
       .then((result) => {
          imgSrcRight.value = result;
          imageLoadedRight.value = true;
          imageFileRight.value = fileToLoad;
       })
       .catch(() => {
          imgSrcRight.value = null;
          imageLoadedRight.value = false;
          $q.notify({
              message: i18n.global.t('home.errorReading'),
              type: 'negative',
          });
          imageFileRight.value = null;
       });
      fileRight.value = null;
    };

    const loadingOK = () => {
      $q.notify({
        message: i18n.global.t('home.loaded'),
        type: 'positive',
      });
    };

    const loadingError = (section: 'left' | 'right') => {
        if (section === 'left') {
          imgSrcLeft.value = null;
          imageLoadedLeft.value = false;
        } else if (section === 'right') {
          imgSrcRight.value = null;
          imageLoadedRight.value = false;
        }
        // Other error handling logic
    };

    const editModelLeft = async () => {
      const dmnStore = useDmnStore();
      const image = await blobToDataURL(new Blob([imageFileLeft.value as File]));
      const model = conversionResultLeft.value;
      dmnStore.image = image;
      dmnStore.model = model;
      await router.push({
        name: 'editor',
      });
    };

    const editModelRight = async () => {
      const dmnStore = useDmnStore();
      const image = await blobToDataURL(new Blob([imageFileRight.value as File]));
      const model = conversionResultRight.value;
      dmnStore.image = image;
      dmnStore.model = model;
      await router.push({
        name: 'editor',
      });
    };

    const downloadModelLeft = () => {
      exportFile(
        (imageFileLeft.value?.name as string) + '.dmn',
        conversionResultLeft.value as string,
        {
          mimeType: 'text/xml',
          encoding: 'utf-8',
        }
      );
    };

    const downloadModelRight = () => {
      exportFile(
        (imageFileRight.value?.name as string) + '.dmn',
        conversionResultRight.value as string,
        {
          mimeType: 'text/xml',
          encoding: 'utf-8',
        }
      );
    };

    const convertImages = async () => {
       const formDataLeft = prepareFormDataLeft();
       const formDataRight = prepareFormDataRight();
    
       const formData = new FormData();
       const [leftData, rightData] = await Promise.all([formDataLeft, formDataRight]);
    
       for (const [key, value] of leftData.entries()) {
           formData.append(key, value);  // Appending data for left image
       }
       for (const [key, value] of rightData.entries()) {
           formData.append(key, value);  // Appending data for right image
       }
    
       const result = await uploadAndConvert(formData);

       console.log("Result:", result);
    };


    const prepareFormDataLeft =  () => {
      const formData = new FormData();
      formData.append('imageLeft', imageFileLeft.value as File);
      formData.append('elementsLeft', String(elementsEnabledLeft.value));
      formData.append('flowsLeft', String(flowsEnabledLeft.value));
      formData.append('ocrLeft', String(ocrEnabledLeft.value));
      formData.append('graphLeft', String(isGraphLeft.value));
      formData.append('decisionLogicLeft', String(isTableLeft.value));
      return formData;
    };

    const prepareFormDataRight =  () => {
      const formData = new FormData();
      formData.append('imageRight', imageFileRight.value as File);
      formData.append('elementsRight', String(elementsEnabledRight.value));
      formData.append('flowsRight', String(flowsEnabledRight.value));
      formData.append('ocrRight', String(ocrEnabledRight.value));
      formData.append('graphRight', String(isGraphRight.value));
      formData.append('decisionLogicRight', String(isTableRight.value));
      return formData;
    };

    const uploadAndConvert = async (formData: FormData)  => {
      const source = axios.CancelToken.source();
      const uploadDialog = $q
        .dialog({
          message: i18n.global.t('home.uploading'),
          progress: true,
          persistent: true,
          ok: false,
          cancel: true,
        })
        .onCancel(() => {
          source.cancel();
        });

        await api
        .post<string>('/convert', formData, {
          cancelToken: source.token,
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent: ProgressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            );
            uploadDialog.update({
              message:
                progress == 100
                  ? i18n.global.t('home.waitingForConversion')
                  : i18n.global.t('home.uploadingProgress', {
                      progress: progress,
                    }),
            });
          },
        })
        .then((res) => {
          uploadDialog.hide();
          conversionResultLeft.value = res.data;
          conversionDialogLeft.value = true;
        })
        .catch(() => {
          uploadDialog.hide();
          $q.notify({
            message: i18n.global.t('home.errorUploading'),
            type: 'negative',
          });
        });
    };


    const convertImageLeft = async () => {
      const formData = new FormData();
      formData.append('image', imageFileLeft.value as File);
      formData.append('elements', String(elementsEnabledLeft.value));
      formData.append('flows', String(flowsEnabledLeft.value));
      formData.append('ocr', String(ocrEnabledLeft.value));
      formData.append('graph', String(isGraphLeft.value));
      formData.append('decisionLogic', String(isTableLeft.value));

      const source = axios.CancelToken.source();
      const uploadDialog = $q
        .dialog({
          message: i18n.global.t('home.uploading'),
          progress: true,
          persistent: true,
          ok: false,
          cancel: true,
        })
        .onCancel(() => {
          source.cancel();
        });

        await api
        .post<string>('/convert', formData, {
          cancelToken: source.token,
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent: ProgressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            );
            uploadDialog.update({
              message:
                progress == 100
                  ? i18n.global.t('home.waitingForConversion')
                  : i18n.global.t('home.uploadingProgress', {
                      progress: progress,
                    }),
            });
          },
        })
        .then((res) => {
          uploadDialog.hide();
          conversionResultLeft.value = res.data;
          conversionDialogLeft.value = true;
        })
        .catch(() => {
          uploadDialog.hide();
          $q.notify({
            message: i18n.global.t('home.errorUploading'),
            type: 'negative',
          });
        });
    };
      
    const convertImageRight = async () => {
        const formData = new FormData();
        formData.append('image', imageFileRight.value as File);
        formData.append('elements', String(elementsEnabledRight.value));
        formData.append('flows', String(flowsEnabledRight.value));
        formData.append('ocr', String(ocrEnabledRight.value));
        formData.append('graph', String(isGraphRight.value));
        formData.append('decisionLogic', String(isTableRight.value));
        const source = axios.CancelToken.source();
        const uploadDialog = $q
          .dialog({
            message: i18n.global.t('home.uploading'),
            progress: true,
            persistent: true,
            ok: false,
            cancel: true,
          })
          .onCancel(() => {
            source.cancel();
          });

        await api
          .post<string>('/convert', formData, {
            cancelToken: source.token,
            headers: { 'Content-Type': 'multipart/form-data' },
            onUploadProgress: (progressEvent: ProgressEvent) => {
              const progress = Math.round(
                (progressEvent.loaded / progressEvent.total) * 100
              );
              uploadDialog.update({
                message:
                  progress == 100
                    ? i18n.global.t('home.waitingForConversion')
                    : i18n.global.t('home.uploadingProgress', {
                        progress: progress,
                       }),
              });
            },
          })
          .then((res) => {
            uploadDialog.hide();
            conversionResultRight.value = res.data;
            conversionDialogRight.value = true;
          })
          .catch(() => {
            uploadDialog.hide();
            $q.notify({
              message: i18n.global.t('home.errorUploading'),
              type: 'negative',
            });
        });
    };

    return {
      api,
      allowDrop,
      drop,
      imgSrcLeft,
      imgSrcRight,
      filePickerLeft,
      filePickerRight,
      fileLeft,
      fileRight,
      imageFileLeft,
      imageFileRight,
      imageLoadedLeft,
      imageLoadedRight,
      loadingOK,
      loadingError,
      editModelLeft,
      downloadModelLeft,
      loadImageLeft,
      loadImageRight,
      convertImageLeft,
      convertImageRight,
      convertImages,
      conversionDialogLeft,
      conversionDialogRight,
      elementsEnabledLeft,
      elementsEnabledRight,
      flowsEnabledLeft,
      flowsEnabledRight,
      ocrEnabledLeft,
      ocrEnabledRight,
      isTableLeft,
      isTableRight,
      isGraphLeft,
      isGraphRight,
    };
  },
});
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
}

.header {
  background-color: white; /* White header background */
  color: black; /* Black text */
  padding: 0px 20px; /* Adjust top and bottom padding */
  font-size: 100px; /* Increase font size */
}

.header-controls {
  margin-left: auto; /* Right-align header controls */
}

.main-content {
  flex: 1; /* Fill remaining vertical space */
  padding: 0 40px 40px; /* Adjust left and right padding */
  overflow-y: auto; /* Enable vertical scrolling if needed */
}


/* Style for individual sections */
.upload-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

/*style of the end button*/
.convert-button {
  font-size: 18px; /* Increase font size */
  padding: 16px 32px; /* Increase padding */
}

/* Ensure checkboxes are clickable */
.q-checkbox input[type="checkbox"] {
  pointer-events: auto;
}

.upload-section {
  flex: 1;
  margin: 0px 40px; /* Adjust this margin for spacing between sections */
}

.image-display {
  margin-top: 20px;
}

h2 {
  margin-bottom: 10px;
}
</style>