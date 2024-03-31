<template>
  <div class="absolute-full" @dragover="allowDrop($event)" @drop="drop($event)">
    <div class="content" id="js-drop-zone">
      <div class="message intro">
        <div class="note">
          <q-btn
            class="drop-button"
            disable
            outline
            :label="$t('editor.drop')"
          />
          /
          <q-file
            ref="filePicker"
            style="display: none"
            accept=".dmn"
            v-model="pickedFile"
            @update:model-value="uploadDiagram(pickedFile as File)"
          ></q-file>
          <q-btn
            class="open-button"
            outline
            :label="$t('editor.open')"
            @click="filePicker?.pickFiles()"
          />
          /
          <q-btn
            class="create-button"
            outline
            :label="$t('editor.create')"
            @click="createNewDiagram"
          />
          {{ $t('editor.intro') }}
        </div>
      </div>

      <div class="message error">
        <div class="note">
          <p>Ooops, we could not display the DMN 1.3 diagram.</p>

          <div class="details">
            <span>cause of the problem</span>
            <pre></pre>
          </div>
        </div>
      </div>

      <div class="canvas" id="js-canvas"></div>
    </div>

    <ul class="download-buttons" v-if="successfulLoadDMN">
      <q-file
        ref="dmnFilePicker"
        style="display: none"
        accept=".dmn"
        v-model="dmnFile"
        @update:model-value="uploadDiagram(dmnFile as File)"
      ></q-file>
      <li>
        <q-btn
          icon="upload"
          label="DMN"
          outline
          @click="dmnFilePicker?.pickFiles()"
        />
      </li>
      <li>
        <q-btn icon="download" label="DMN" outline @click="downloadAsDMN" />
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, Ref, onUnmounted } from 'vue';
import { useQuasar, QFile, exportFile } from 'quasar';
import 'dmn-js/dist/assets/diagram-js.css';
import 'dmn-js/dist/assets/dmn-font/css/dmn-embedded.css';
import 'dmn-js/dist/assets/diagram-js.css';
import 'dmn-js/dist/assets/dmn-js-shared.css';
import 'dmn-js/dist/assets/dmn-js-drd.css';
import 'dmn-js/dist/assets/dmn-js-decision-table.css';
import 'dmn-js/dist/assets/dmn-js-decision-table-controls.css';
import 'dmn-js/dist/assets/dmn-font/css/dmn.css';
import Modeler from 'dmn-js/lib/Modeler';
import { onBeforeRouteLeave } from 'vue-router';
import { i18n } from 'src/boot/i18n';
import { useDmnStore } from 'src/store/dmnStore';

export default defineComponent({
  name: 'EditorComponent',

  setup() {
    const $q = useQuasar();
    const dmnStore = useDmnStore();
    const filePicker: Ref<QFile | null> = ref(null);
    const pickedFile: Ref<File | null> = ref(null);
    const dmnFilePicker: Ref<QFile | null> = ref(null);
    const dmnFile: Ref<File | null> = ref(null);
    const successfulLoadDMN = ref(false);

    let container: HTMLElement | null;
    let modeler: Modeler;

    async function openDiagram(xml: string) {
      try {
        await modeler.importXML(xml);
        container?.classList.remove('with-error');
        container?.classList.add('with-diagram');
        successfulLoadDMN.value = true;
      } catch (err) {
        container?.classList.remove('with-diagram');
        container?.classList.add('with-error');
        const errorNode = container?.querySelectorAll('.error pre')[0];
        (errorNode as Element).textContent = (err as Error).message;
        successfulLoadDMN.value = false;
      }
    }

    function registerFileDrop(callback: (xml: string) => Promise<void>) {
      function handleFileSelect(e: Event) {
        e.stopPropagation();
        e.preventDefault();

        const file = (e as DragEvent).dataTransfer?.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
          const xml = e.target?.result;
          void callback(xml as string);
        };
        try {
          reader.readAsText(file as File);
        } catch (err) {
          console.error(err);
        }
      }

      function handleDragOver(e: Event) {
        e.stopPropagation();
        e.preventDefault();

        ((e as DragEvent).dataTransfer as DataTransfer).dropEffect = 'copy';
      }

      container
        ?.getElementsByClassName('message intro')[0]
        .addEventListener('dragover', handleDragOver, false);
      container
        ?.getElementsByClassName('message intro')[0]
        .addEventListener('drop', handleFileSelect, false);
    }

    // Ask for confirmation before leaving the editor
    onBeforeRouteLeave((_to, _from, next) => {
      if (!successfulLoadDMN.value) {
        next();
        return;
      }
      $q.dialog({
        message: i18n.global.t('editor.exit'),
        cancel: true,
      })
        .onOk(() => {
          next();
        })
        .onCancel(() => next(false));
    });

    onMounted(() => {
      container = document.getElementById('js-drop-zone');
      modeler = new Modeler({
        container: '#js-canvas',
        // Enable dmn-js keyboard shortcuts
        keyboard: { bindTo: document },
      });
      if (!window.FileList || !window.FileReader) {
        $q.notify({
          message:
            'Looks like you use an older browser that does not support drag and drop. Try using Chrome, Firefox or the Internet Explorer > 10.',
          type: 'negative',
        });
      } else {
        registerFileDrop(openDiagram);
      }

      if (dmnStore.model) {
        void openDiagram(dmnStore.model);
      }
    });

    // Detach the dmn-js modeler from parent when changing page
    onUnmounted(() => {
      modeler.detach();
    });

    const allowDrop = (e: DragEvent) => {
      e.preventDefault();
    };

    const drop = async (e: DragEvent) => {
      e.preventDefault();
      const files = e.dataTransfer?.files;
      if (files?.length == 1) {
        if (files[0].name.endsWith('.dmn')) {
          await openDiagram(await files[0].text());
        }
      }
    };

    return {
      allowDrop,
      drop,
      filePicker,
      pickedFile,
      dmnFilePicker,
      dmnFile,
      successfulLoadDMN,

      async downloadAsDMN() {
            try {
                // Get the diagram XML from the modeler
                const xmlPromise = new Promise<string>((resolve, reject) => {
                   modeler.saveXML({ format: true }, (err: any, xmlOrWarn: string | any) => {
                     if (err) {
                        reject(err);
                     } else {
                          resolve(xmlOrWarn as string);
                     }
                   }).catch((error) => {
                     console.error('Error saving XML:', error);
                     reject(error); // Reject the promise if an error occurs during saving XML
                   });
                });
                 const xml = await xmlPromise; 

                 if (xml) {
                        const blob = new Blob([xml], { type: 'application/xml' });
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'diagram.dmn';
                        a.click();
                        window.URL.revokeObjectURL(url);
                   } else {
                        $q.notify({
                          message: i18n.global.t('editor.errorSaveDMN'),
                          type: 'negative',
                        });
                   }
                } catch(error) {
                    $q.notify({
                      message: i18n.global.t('editor.errorSaveDMN'),
                      type: 'negative',
                    });
                }
      },



      // When creating a new diagram, just open the default one
      createNewDiagram() {
        const sampleDiagram =
          '<?xml version="1.0" encoding="UTF-8"?><dmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dmn2="http://www.omg.org/spec/DMN/20180521/MODEL/" xmlns:dmndi="http://www.omg.org/spec/DMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xsi:schemaLocation="http://www.omg.org/spec/DMN/20100524/MODEL DMN20.xsd" id="sample-diagram" targetNamespace="http://dmn.io/schema/dmn"><dmn2:process id="Process_1" isExecutable="false"><dmn2:startEvent id="StartEvent_1" /></dmn2:process><dmndi:DMNDiagram id="DMNDiagram_1"><dmndi:DMNPlane id="DMNPlane_1" dmnElement="Process_1"><dmndi:DMNShape id="_DMNShape_StartEvent_2" dmnElement="StartEvent_1"><dc:Bounds height="36.0" width="36.0" x="412.0" y="240.0" /></dmndi:dmnShape></dmndi:DMNPlane></dmndi:DMNDiagram></dmn2:definitions>';
        void openDiagram(sampleDiagram);
      },

      uploadDiagram(file: File) {
        const reader = new FileReader();
        reader.onload = (res) => {
          void openDiagram(res.target?.result as string);
        };
        reader.onerror = () => {
          $q.notify({
            message: i18n.global.t('editor.errorUpload'),
            type: 'negative',
          });
        };
        reader.readAsText(file, 'utf8');
      },
    };
  },
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}
body,
html {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 100px;
  height: 100%;
  padding: 0;
  margin: 0;
}
a:link {
  text-decoration: none;
}
.content,
.content > div {
  width: 100%;
  height: 100%;
}
.content > .message {
  text-align: center;
  display: table;
  font-size: 16px;
}
.content > .message .note {
  vertical-align: middle;
  text-align: center;
  display: table-cell;
}
.content .error .details {
  max-width: 500px;
  font-size: 12px;
  margin: 20px auto;
  text-align: left;
}
.content .error pre {
  border: solid 1px #ccc;
  background: #eee;
  padding: 10px;
}
.content:not(.with-error) .error,
.content.with-error .intro,
.content.with-diagram .intro {
  display: none;
}
.content
.canvas {
    width: 100%;
    height: 100%;
    position: relative;
}
.content.with-error .canvas {
  visibility: visible;
}
.content.with-diagram .canvas {
  visibility: visible;
  height: 100%;
  padding: 50px 100px; /* Adjust top and bottom padding */
}
.download-buttons {
  position: absolute;
  bottom: 10px;
  left: 75px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.download-buttons > li {
  display: inline-block;
  margin-right: 10px;
}
.download-buttons > li > a {
  background: #ddd;
  border: solid 1px #666;
  display: inline-block;
  padding: 5px;
}
.download-buttons a {
  opacity: 0.3;
}
.download-buttons a.active {
  opacity: 1;
}
</style>
