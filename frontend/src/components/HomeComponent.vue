<template>
  <div class="container">
    <!-- Header Section -->
    <header class="header">
      <div class="header-controls">
        <dark-mode-changer></dark-mode-changer>
        <locale-changer></locale-changer>
      </div>
      <h1>Welcome to DMN Computer Vision Tool</h1>
    </header>

    <!-- Main Content Section -->
    <main class="main-content">
      <!-- Image Upload Section -->
      <section class="upload-section">
        <h2>Get Started</h2>
        <div style="display: flex; align-items: center;">
          <!-- First upload button -->
          <q-btn
            color="positive"
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

          <!-- Second upload button -->
          <q-btn
            color="positive"
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
        </div>
      </section>

      <!-- Options Section -->
      <section class="options-section">
        <h2>Customize Your Experience</h2>
        <div class="options">
          <!-- Checkboxes for first image -->
          <div>
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
            <!-- Additional checkboxes for specifying image type -->
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

          <!-- Checkboxes for second image -->
          <div>
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
            <!-- Additional checkboxes for specifying image type -->
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
        </div>
        <q-btn
          :disable="!imageLoaded"
          color="primary"
          icon-right="arrow_forward"
          :label="$t('home.convert_image')"
          @click="convertImage()"
        ></q-btn>
      </section>

      <!-- Image Display Section -->
      <section class="image-display">
        <h2>Your Uploaded Images</h2>
        <div class="image-container" style="display: flex;">
          <!-- First image display -->
          <div style="margin-right: 20px;">
            <q-img
              v-if="imgSrc"
              :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
              sizes="(max-width: 200px) 200px, (max-height: 200px) 200px"
              fit="contain"
              position="50% 50%"
              width="200px"
              height="200px"
              placeholder-src="../assets/default-placeholder.png"
              no-spinner
              :src="imgSrc"
              @load="loadingOK"
              @error="loadingError"
              @dragover="allowDrop($event)"
              @drop="drop($event)"
            ></q-img>
          </div>

          <!-- Second image display -->
          <div>
            <q-img
              v-if="imgSrc2"
              :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
              sizes="(max-width: 200px) 200px, (max-height: 200px) 200px"
              fit="contain"
              position="50% 50%"
              width="200px"
              height="200px"
              placeholder-src="../assets/default-placeholder.png"
              no-spinner
              :src="imgSrc2"
              @load="loadingOK"
              @error="loadingError"
              @dragover="allowDrop($event)"
              @drop="drop($event)"
            ></q-img>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer Section -->
    <footer class="footer">
      <h2>Navigation</h2>
      <q-tabs
        align="justify"
        v-model="tab"
        inline-label
        indicator-color="secondary"
        active-bg-color="positive"
      >
        <q-route-tab
          name="home"
          default="true"
          icon="home"
          label="Home"
          :to="{ name: 'home' }"
        />
        <q-route-tab
          name="edit"
          icon="edit"
          label="Editor"
          :to="{ name: 'editor' }"
        />
      </q-tabs>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import LocaleChanger from 'src/components/LocaleChanger.vue';
import DarkModeChanger from 'src/components/DarkModeChanger.vue';

export default defineComponent({
  name: 'MainLayout',

  components: {
    LocaleChanger,
    DarkModeChanger,
  },

  setup() {
    const tab = ref('home');
    const file = ref(null);
    const imgSrc = ref('');
    const elementsEnabled = ref(false);
    const flowsEnabled = ref(false);
    const ocrEnabled = ref(false);
    const imageLoaded = ref(false);

    const loadImage = (file: File) => {
      // Logic to load the image
    };

    const convertImage = () => {
      // Logic to convert image
    };

    const loadingOK = () => {
      // Logic when image loading is successful
    };

    const loadingError = () => {
      // Logic when image loading fails
    };

    const allowDrop = (event: Event) => {
      // Logic to allow dropping
    };

    const drop = (event: Event) => {
      // Logic when dropping
    };

    return {
      tab,
      file,
      imgSrc,
      elementsEnabled,
      flowsEnabled,
      ocrEnabled,
      imageLoaded,
      loadImage,
      convertImage,
      loadingOK,
      loadingError,
      allowDrop,
      drop,
    };
  },
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Fills the whole screen */
}

.header {
  background-color: #4caf50; /* Green header background */
  color: white; /* White text */
  padding: 15px;
}

.header-controls {
  margin-left: auto; /* Right-align header controls */
}

.main-content {
  flex: 1; /* Fill remaining vertical space */
  padding: 20px;
  overflow-y: auto; /* Enable vertical scrolling if needed */
}

.footer {
  background-color: #4caf50; /* Green footer background */
  color: white; /* White text */
  padding: 15px;
}

/* Style for individual sections */
section {
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 10px;
}
</style>
