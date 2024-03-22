import { defineStore } from 'pinia';

// Pinia store for state management
export const useDmnStore = defineStore('dmn', {
  state: () => ({
    model: null as string | null,
    image: null as string | null,
  }),
});
