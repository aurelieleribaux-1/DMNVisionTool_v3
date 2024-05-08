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
          <div style="font-size: 18px">{{ $t('home.examplesInstruction') }}</div>
          <div style="font-size: 18px; text-align: left">
            <ol>
              <li>{{ $t('home.specifyImageType') }}</li>
              <li>{{ $t('home.specifyHandwritten') }}</li>
              <li>{{ $t('home.specifyContent') }}</li>
              <li>{{ $t('home.convertImages') }}</li>
            </ol>
          </div>
        </div>
      </div>
    </header>

    <!-- Left Content Section -->
    <main class="main-content">
      <div class="upload-container">
        <!-- Left Section -->
        <section class="upload-section" @dragover="allowDrop($event)" @drop="drop($event, 'left')">
          <h2 style="font-size: 32px;">Upload Your DRD's Image Here</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePickerLeft?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePickerLeft"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp, .tiff, .tif"
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
                  @click="downloadModel()"
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
              :disable="isTableLeft"
              class="q-pr-md"
              v-model="isGraphLeft"
              label="DRD"
            ></q-checkbox>
            <q-checkbox
              :disable="SketchLeft"
              class="q-pr-md"
              v-model="DigitalLeft"
              label="Digitally drawn DRD file"
            ></q-checkbox>
            <q-checkbox
              :disable="DigitalLeft"
              class="q-pr-md"
              v-model="SketchLeft"
              label="Hand-written DMN file"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <div class="image-container">
              <q-img
                :style="'border: 2px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 400px) 400px, (max-height: 300px) 300px"
                fit="contain"
                position="50% 50%"
                width="400px"
                height="300px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrcLeft as string)"
                @load="loadingOK"
                @error="loadingError('left')"
                @dragover="allowDrop($event)"
                @drop="drop($event, 'left')"
              ></q-img>
            </div>
          </div>
        </section>

        <!-- Convert Images Button -->
        <div class="q-pa-md" style="text-align: center">
          <q-btn
            color="accent"
            :label="$t('home.convert_images')"
            @click="convertImages"
            class="convert-button"
          ></q-btn>
        </div>

        <!-- Right Section -->
        <section class="upload-section" @dragover="allowDrop($event)" @drop="drop($event, 'right')">
          <h2 style="font-size: 32px;">Upload Your Decision Table Image Here</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePickerRight?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePickerRight"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp, .tiff, .tif"
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
              v-model="isTableRight"
              label="Decision Table"
            ></q-checkbox>
            <q-checkbox
              :disable="SketchRight"
              class="q-pr-md"
              v-model="DigitalRight"
              label="Digitally drawn file"
            ></q-checkbox>
            <q-checkbox
              :disable="DigitalRight"
              class="q-pr-md"
              v-model="SketchRight"
              label="Hand-written file"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <div class="image-container">
              <q-img
                :style="'border: 2px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 400px) 400px, (max-height: 300px) 300px"
                fit="contain"
                position="50% 50%"
                width="400px"
                height="300px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrcRight as string)"
                @load="loadingOK"
                @error="loadingError('right')"
                @dragover="allowDrop($event)"
                @drop="drop($event, 'right')"
              ></q-img>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Example Images Section -->
    <div class="q-pa-md" style="text-align: center">
      <div style="font-size: 32px">{{ $t('home.examples') }}</div>
      <!-- New Instructions for Image Specifications -->
      <div style="font-size: 18px; text-align: left">
        {{ $t('home.ImageExample') }}
      </div>
      <!-- End of New Instructions -->
      <div class="row justify-evenly wrap">
        <div class="q-pa-sm" v-for="i in 4" :key="i">
          <q-img
            :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
            sizes="(max-width: 300px) 300px, (max-height: 300px) 300px"
            fit="contain"
            position="50% 50%"
            width="300px"
            height="300px"
            :src="require(`../assets/example${i}.png`)"
            @click="loadExampleImage(i)"
          ></q-img>
          <q-btn
            flat
            icon="cloud_download"
            label="Download Example"
            color="primary"
            :src="require(`../assets/example${i}.png`)"
            @click="downloadExample(i)"
          />
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
    const isGraphLeft = ref(false);
    const isTableRight = ref(false);
    const DigitalLeft = ref(false);
    const DigitalRight = ref(false);
    const SketchLeft = ref(false);
    const SketchRight = ref(false);

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

    const downloadModel = () => {
      const fileName = (imageFileLeft.value?.name as string).replace(/\..+$/, '.dmn');
      exportFile(
         fileName,
         conversionResultLeft.value as string,
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
      formData.append('graphLeft', String(isGraphLeft.value));
      formData.append('sketchLeft', String(SketchLeft.value));
      formData.append('DigitalLeft', String(DigitalLeft.value));

      return formData;
    };

    const prepareFormDataRight =  () => {
      const formData = new FormData();
      formData.append('imageRight', imageFileRight.value as File);
      formData.append('decisionLogicRight', String(isTableRight.value));
      formData.append('sketchRight', String(SketchRight.value));
      formData.append('DigitalRight', String(DigitalRight.value));

      return formData;
    };

    const downloadExample = async (exampleNumber: number) => {
      console.log('Button clicked');
      const fileName = `example${exampleNumber}.png`;
      const imagePathModule = await import(`../assets/${fileName}`) as { default: string };
      const imagePath: string = imagePathModule.default;
      const link = document.createElement('a');
      link.href = imagePath;
      link.download = fileName;
      link.click();
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
      downloadModel,
      downloadExample,
      loadImageLeft,
      loadImageRight,
      convertImages,
      conversionDialogLeft,
      conversionDialogRight,
      isTableRight,
      isGraphLeft,
      SketchLeft,
      SketchRight,
      DigitalLeft,
      DigitalRight,
    };
  },
});
</script>
