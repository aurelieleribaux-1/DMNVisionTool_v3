<template>
  <q-layout view="lHh LpR fFf">
    <q-header elevated class="bg-purple-6 text-black">
      <q-toolbar>
        <q-toolbar-title> DMN Computer Vision Tool </q-toolbar-title>
        <q-space></q-space>
        <dark-mode-changer></dark-mode-changer>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-tabs
        align="justify"
        v-model="tab"
        inline-label
        indicator-color="secondary"
        active-bg-color="accent"
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
    </q-footer>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import DarkModeChanger from 'src/components/DarkModeChanger.vue';

export default defineComponent({
  name: 'MainLayout',

  components: {
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