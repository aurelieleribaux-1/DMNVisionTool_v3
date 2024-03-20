<template>
  <div class="q-pa-md">
    <div style="text-align: center">
      <!-- Welcome message -->
      <div style="font-size: 32px">{{ $t('home.welcome') }}</div>
      <div style="font-size: 18px">
        {{ $t('home.description') }}
      </div>
    </div>

    <!-- Upload Images button -->
    <div class="q-pt-xl" style="text-align: center">
      <q-btn
        color="positive"
        icon="upload_file"
        :label="$t('home.load')"
        @click="filePicker?.pickFiles()"
      ></q-btn>
    </div>

    <!-- Image display section -->
    <div class="row justify-center q-pa-md" style="text-align: center">
      <div>
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
    </div>

    <!-- Options and Convert button section -->
    <div style="text-align: center">
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

    <!-- Dialog for conversion result -->
    <q-dialog v-model="conversionDialog" persistent>
      <!-- Dialog content -->
    </q-dialog>

    <!-- Examples section -->
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
          >
          </q-img>
        </div>
      </div>
    </div>

    <!-- Footer section -->
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
