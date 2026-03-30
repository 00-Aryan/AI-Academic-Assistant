import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSlideDeckStore = defineStore('slideDeck', () => {
  // State
  const currentConfig = ref(null)

  // Actions
  const setConfig = (config) => {
    currentConfig.value = JSON.parse(JSON.stringify(config)) // Deep copy
  }

  const getConfig = () => {
    return currentConfig.value
  }

  const clearConfig = () => {
    currentConfig.value = null
  }

  return {
    currentConfig,
    setConfig,
    getConfig,
    clearConfig
  }
})
