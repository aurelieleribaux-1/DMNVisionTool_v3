<template>
  <q-page>
    <editor-component />
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import EditorComponent from 'src/components/EditorComponent.vue';

export default defineComponent({
  name: 'PageEditor',

  components: { EditorComponent },

  setup() {
    return {};
  },
});
</script>
