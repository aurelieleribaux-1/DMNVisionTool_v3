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
  </div>
    <!-- Main Content Section -->
    <main class="main-content">
      <div class="upload-container">
        <!-- Left Section -->
        <section class="upload-section">
          <h2>Upload Image 1</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePicker?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePicker"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp"
            v-model="file"
            @update:model-value="loadImage(file as File)"
          ></q-file>
          <div class="options">
            <q-checkbox
              class="q-pr-md"
              v-model="elementsEnabled"
              :label="$t('home.show_elements')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled"
              class="q-pr-md"
              v-model="flowsEnabled"
              :label="$t('home.show_flows')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled"
              class="q-pr-md"
              v-model="ocrEnabled"
              label="Enable OCR"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled"
              class="q-pr-md"
              v-model="isGraph"
              label="Graph"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled"
              class="q-pr-md"
              v-model="isTable"
              label="Table"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <h2>Your Uploaded Image 1</h2>
            <div class="image-container">
              <q-img
                :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 200px) 200px, (max-height: 200px) 200px"
                fit="contain"
                position="25% 25%"
                width="200px"
                height="200px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrc as string)"
                @load="loadingOK"
                @error="loadingError"
                @dragover="allowDrop($event)"
                @drop="drop($event)"
              ></q-img>
            </div>
          </div>
        </section>

        <!-- Right Section -->
        <section class="upload-section">
          <h2>Upload Image 2</h2>
          <q-btn
            color="accent"
            icon="upload_file"
            :label="$t('home.upload_image')"
            @click="filePicker2?.pickFiles()"
          ></q-btn>
          <q-file
            ref="filePicker2"
            style="display: none"
            accept=".png, .jpeg, .jpg, .bmp"
            v-model="file2"
            @update:model-value="loadImage2(file2 as File)"
          ></q-file>
          <div class="options">
            <q-checkbox
              class="q-pr-md"
              v-model="elementsEnabled2"
              :label="$t('home.show_elements')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled2"
              class="q-pr-md"
              v-model="flowsEnabled2"
              :label="$t('home.show_flows')"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled2"
              class="q-pr-md"
              v-model="ocrEnabled2"
              label="Enable OCR"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled2"
              class="q-pr-md"
              v-model="isGraph2"
              label="Graph"
            ></q-checkbox>
            <q-checkbox
              :disable="!elementsEnabled2"
              class="q-pr-md"
              v-model="isTable2"
              label="Table"
            ></q-checkbox>
          </div>
          <div class="image-display">
            <h2>Your Uploaded Image 2</h2>
            <div class="image-container">
              <q-img
                :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
                sizes="(max-width: 200px) 200px, (max-height: 200px) 200px"
                fit="contain"
                position="25% 25%"
                width="200px"
                height="200px"
                placeholder-src="../assets/default-placeholder.png"
                no-spinner
                :src="(imgSrc as string)"
                @load="loadingOK"
                @error="loadingError"
                @dragover="allowDrop($event)"
                @drop="drop($event)"
              ></q-img>
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
import { useBpmnStore } from 'src/store/bpmnStore';

export default defineComponent({
  name: 'HomeComponent',

  setup() {
    const $q = useQuasar();
    const router = useRouter();
    const filePicker: Ref<QFile | null> = ref(null);
    const file: Ref<File | null> = ref(null);
    const imageFile: Ref<File | null> = ref(null);
    const imgSrc: Ref<string | null> = ref(null);
    const conversionDialog: Ref<boolean> = ref(false);
    const conversionResult: Ref<string | null> = ref(null);
    const imageLoaded = ref(false);
    const elementsEnabled = ref(true);
    const flowsEnabled = ref(true);
    const ocrEnabled = ref(true);

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent) => {
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
        await loadImage(file);
      }
    };

    const loadExampleImage = async (i: number) => {
      const blob = await (
        await fetch(
          // eslint-disable-next-line @typescript-eslint/no-var-requires
          require(`../assets/example${i}.png`) as string
        )
      ).blob();
      await loadImage(new File([blob], `example${i}.png`));
    };

    const loadImage = async (fileToLoad: File) => {
      await blobToDataURL(fileToLoad)
        .then((result) => {
          imgSrc.value = result;
          imageLoaded.value = true;
          imageFile.value = fileToLoad;
        })
        .catch(() => {
          imgSrc.value = null;
          imageLoaded.value = false;
          $q.notify({
            message: i18n.global.t('home.errorReading'),
            type: 'negative',
          });
          imageFile.value = null;
        });
      file.value = null;
    };

    const loadingOK = () => {
      $q.notify({
        message: i18n.global.t('home.loaded'),
        type: 'positive',
      });
    };

    const loadingError = () => {
      imgSrc.value = null;
      imageLoaded.value = false;
      $q.notify({
        message: i18n.global.t('home.errorLoading'),
        type: 'negative',
      });
      file.value = null;
      imageFile.value = null;
    };

    const editModel = async () => {
      const bpmnStore = useBpmnStore();
      const image = await blobToDataURL(new Blob([imageFile.value as File]));
      const model = conversionResult.value;
      bpmnStore.image = image;
      bpmnStore.model = model;
      await router.push({
        name: 'editor',
      });
    };

    const downloadModel = () => {
      exportFile(
        (imageFile.value?.name as string) + '.bpmn',
        conversionResult.value as string,
        {
          mimeType: 'text/xml',
          encoding: 'utf-8',
        }
      );
    };

    const convertImage = async () => {
      const formData = new FormData();
      formData.append('image', imageFile.value as File);
      formData.append('elements', String(elementsEnabled.value));
      formData.append('flows', String(flowsEnabled.value));
      formData.append('ocr', String(ocrEnabled.value));
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
          conversionResult.value = res.data;
          conversionDialog.value = true;
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
      imgSrc,
      filePicker,
      file,
      imageFile,
      imageLoaded,
      loadingOK,
      loadingError,
      editModel,
      downloadModel,
      loadImage,
      loadExampleImage,
      convertImage,
      conversionDialog,
      elementsEnabled,
      flowsEnabled,
      ocrEnabled,
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
}

.header-controls {
  margin-left: auto; /* Right-align header controls */
}

.main-content {
  flex: 1; /* Fill remaining vertical space */
  padding: 0 20px 20px; /* Adjust left and right padding */
  overflow-y: auto; /* Enable vertical scrolling if needed */
}


/* Style for individual sections */
.upload-container {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

/* Ensure checkboxes are clickable */
.q-checkbox input[type="checkbox"] {
  pointer-events: auto;
}

.upload-section {
  flex: 1;
  margin: 0px 10px; /* Adjust this margin for spacing between sections */
}

.image-display {
  margin-top: 20px;
}

h2 {
  margin-bottom: 10px;
}
</style>