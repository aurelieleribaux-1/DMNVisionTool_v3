<template>
  <div class="container">
    <!-- Header Section -->
    <header class="header">
      <h1>DMN Computer Vision Tool</h1>
      <div class="header-controls">
        <dark-mode-changer></dark-mode-changer>
        <locale-changer></locale-changer>
      </div>
    </header>

    <!-- Main Content Section -->
    <main class="main-content">
      <!-- Image Upload Section -->
      <section class="upload-section">
        <h2>Upload Image</h2>
        <q-file
          ref="filePicker"
          style="display: none"
          accept=".png, .jpeg, .jpg, .bmp"
          v-model="file"
          @update:model-value="loadImage(file as File)"
        ></q-file>
        <q-btn
          color="positive"
          icon="upload_file"
          :label="$t('home.load')"
          @click="filePicker?.pickFiles()"
        ></q-btn>
      </section>

      <!-- Image Display Section -->
      <section class="image-display">
        <h2>Uploaded Image</h2>
        <div class="image-container">
          <q-img
            :style="'border: 1px ' + ($q.dark.mode ? 'gray' : 'black') + ' solid'"
            sizes="(max-width: 400px) 400px, (max-height: 400px) 400px"
            fit="contain"
            position="50% 50%"
            width="400px"
            height="400px"
            placeholder-src="../assets/default-placeholder.png"
            no-spinner
            :src="(imgSrc as string)"
            @load="loadingOK"
            @error="loadingError"
            @dragover="allowDrop($event)"
            @drop="drop($event)"
          >
          </q-img>
        </div>
      </section>

      <!-- Options Section -->
      <section class="options-section">
        <h2>Options</h2>
        <div class="options">
          <q-checkbox
            class="q-pr-md"
            v-model="elementsEnabled"
            :label="$t('home.elements')"
          ></q-checkbox>
          <q-checkbox
            :disable="!elementsEnabled"
            class="q-pr-md"
            v-model="flowsEnabled"
            :label="$t('home.flows')"
          ></q-checkbox>
          <q-checkbox
            :disable="!elementsEnabled"
            class="q-pr-md"
            v-model="ocrEnabled"
            label="OCR"
          ></q-checkbox>
          <q-btn
            :disable="!imageLoaded"
            color="primary"
            icon-right="arrow_forward"
            :label="$t('home.convert')"
            @click="convertImage()"
          ></q-btn>
        </div>
      </section>
    </main>

    <!-- Footer Section -->
    <footer class="footer">
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

    return {
      tab,
    };
  },
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Full height of the viewport */
}

.header {
  background-color: #4caf50; /* Green background */
  color: white; /* White text */
  padding: 15px;
}

.header-controls {
  margin-left: auto; /* Align to the right */
}

.main-content {
  flex: 1; /* Fill remaining vertical space */
  padding: 20px;
  overflow-y: auto; /* Enable vertical scrolling if needed */
}

.footer {
  background-color: #4caf50; /* Green background */
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
