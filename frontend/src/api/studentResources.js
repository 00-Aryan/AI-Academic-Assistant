// Student Resources API
import api from './axios'

/**
 * Get all personal resources for the current student
 */
export const getMyResources = async () => {
  const response = await api.get('/student-resources/my-resources')
  return response.data
}

/**
 * Upload a document file
 * @param {File} file - Document file to upload
 * @param {string} title - Optional title for the resource
 */
export const uploadDocument = async (file, title = null) => {
  const formData = new FormData()
  formData.append('file', file)
  if (title) {
    formData.append('title', title)
  }
  
  const response = await api.post('/student-resources/upload-document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

/**
 * Upload an image file
 * @param {File} file - Image file to upload
 * @param {string} title - Optional title for the resource
 */
export const uploadImage = async (file, title = null) => {
  const formData = new FormData()
  formData.append('file', file)
  if (title) {
    formData.append('title', title)
  }
  
  const response = await api.post('/student-resources/upload-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

/**
 * Add a link resource
 * @param {string} url - URL to add
 * @param {string} title - Optional title for the resource
 */
export const addLink = async (url, title = null) => {
  const formData = new FormData()
  formData.append('url', url)
  if (title) {
    formData.append('title', title)
  }
  
  const response = await api.post('/student-resources/add-link', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

/**
 * Delete a resource
 * @param {number} resourceId - ID of resource to delete
 */
export const deleteResource = async (resourceId) => {
  await api.delete(`/student-resources/${resourceId}`)
}

/**
 * Toggle pin status of a resource
 * @param {number} resourceId - ID of resource to pin/unpin
 */
export const togglePinResource = async (resourceId) => {
  const response = await api.patch(`/student-resources/${resourceId}/pin`)
  return response.data
}

/**
 * Get download URL for a resource
 * @param {number} resourceId - ID of resource to download
 */
export const getDownloadUrl = (resourceId) => {
  return `${api.defaults.baseURL}/student-resources/download/${resourceId}`
}
