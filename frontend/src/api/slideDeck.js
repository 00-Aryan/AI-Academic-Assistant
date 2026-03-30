/**
 * Slide Deck API endpoints
 * Handles generation, preview, management, and export of slide decks
 */

import api from './axios'

export const slideDeckAPI = {
  /**
   * Generate a preview outline of the slide deck before actual generation
   * @param {Object} data - Slide deck configuration
   * @param {number} data.course_id - Course ID
   * @param {string} data.title - Slide deck title
   * @param {string[]} data.topics - Topics to cover
   * @param {number} data.num_slides - Number of slides (3-20)
   * @param {string} data.description - Course description
   * @param {string} data.format - Format: 'presentation' or 'document'
   * @returns {Promise} Outline with slide descriptions
   */
  async generatePreview(data) {
    const response = await api.post('/slide-decks/preview', {
      course_id: data.course_id,
      title: data.title,
      topics: data.topics,
      num_slides: data.num_slides,
      description: data.description,
      format: data.format || 'presentation'
    })
    return response.data
  },

  /**
   * Generate full slide deck with content and optional charts
   * @param {Object} data - Slide deck configuration
   * @param {number} data.course_id - Course ID
   * @param {string} data.title - Slide deck title
   * @param {string[]} data.topics - Topics to cover
   * @param {number} data.num_slides - Number of slides (3-20)
   * @param {string} data.description - Course description
   * @param {string} data.format - Format: 'presentation' or 'document'
   * @param {boolean} data.include_graphs - Include chart visualizations
   * @param {string[]} data.graph_types - Chart types: bar, line, pie, scatter
   * @returns {Promise} Generated slide deck with content and metadata
   */
  async generateSlideDeck(data) {
    const response = await api.post('/slide-decks/', {
      course_id: data.course_id,
      title: data.title,
      topics: data.topics,
      num_slides: data.num_slides,
      description: data.description,
      format: data.format || 'presentation',
      include_graphs: data.include_graphs || false,
      graph_types: data.graph_types || ['bar', 'line']
    })
    return response.data
  },

  /**
   * Save slide deck draft with edits and customizations
   * @param {Object} data - Updated slide deck data
   * @param {number} data.deck_id - Slide deck ID
   * @param {string} data.title - Updated title
   * @param {string} data.description - Updated description
   * @param {Array} data.slides - Updated slide content
   * @returns {Promise} Updated slide deck
   */
  async saveSlideDeck(data) {
    const response = await api.put(`/slide-decks/${data.deck_id}`, {
      title: data.title,
      description: data.description,
      slides: data.slides
    })
    return response.data
  },

  /**
   * Get all slide decks with optional filtering
   * @param {Object} params - Query parameters
   * @param {string} params.search - Search by title
   * @param {number} params.course_id - Filter by course
   * @returns {Promise} List of slide decks
   */
  async getAllSlideDecks(params = {}) {
    const response = await api.get('/slide-decks/', { params })
    return response.data
  },

  /**
   * Get a specific slide deck by ID
   * @param {number} deckId - Slide deck ID
   * @returns {Promise} Slide deck data
   */
  async getSlideDeck(deckId) {
    const response = await api.get(`/slide-decks/${deckId}`)
    return response.data
  },

  /**
   * Export slide deck to PPTX format
   * @param {number} deckId - Slide deck ID
   * @param {string} theme - Theme name (professional, modern, colorful, dark, minimalist)
   * @returns {Promise} PPTX file blob
   */
  async exportToPPTX(deckId, theme = 'professional') {
    const response = await api.get(`/slide-decks/${deckId}/export`, {
      params: { format: 'pptx', theme },
      responseType: 'blob'
    })
    
    // Automatically download the file
    const filename = `slide_deck_${deckId}.pptx`
    this.downloadFile(response.data, filename)
    
    return response.data
  },

  /**
   * Export slide deck to PDF format
   * @param {number} deckId - Slide deck ID
   * @param {string} theme - Theme name (professional, modern, colorful, dark, minimalist)
   * @returns {Promise} PDF file blob
   */
  async exportToPDF(deckId, theme = 'professional') {
    const response = await api.get(`/slide-decks/${deckId}/export`, {
      params: { format: 'pdf', theme },
      responseType: 'blob'
    })
    
    // Automatically download the file
    const filename = `slide_deck_${deckId}.pdf`
    this.downloadFile(response.data, filename)
    
    return response.data
  },

  /**
   * Delete a slide deck
   * @param {number} deckId - Slide deck ID
   * @returns {Promise} Deletion confirmation
   */
  async deleteSlideDeck(deckId) {
    const response = await api.delete(`/slide-decks/${deckId}`)
    return response.data
  },

  /**
   * Download file helper function
   * @param {Blob} blob - File blob
   * @param {string} filename - Filename for download
   */
  downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }
}

// Export individual functions for convenience
export const generateSlideDeck = (data) => slideDeckAPI.generateSlideDeck(data)
export const saveSlideDeck = (data) => slideDeckAPI.saveSlideDeck(data)
export const generatePreview = (data) => slideDeckAPI.generatePreview(data)
export const getAllSlideDecks = (params) => slideDeckAPI.getAllSlideDecks(params)
export const getSlideDeck = (deckId) => slideDeckAPI.getSlideDeck(deckId)
export const exportToPPTX = (deckId, theme) => slideDeckAPI.exportToPPTX(deckId, theme)
export const exportToPDF = (deckId, theme) => slideDeckAPI.exportToPDF(deckId, theme)
export const deleteSlideDeck = (deckId) => slideDeckAPI.deleteSlideDeck(deckId)
