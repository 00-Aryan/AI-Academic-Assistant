/**
 * Course API endpoints
 * Handles course-related operations
 */

import api from './axios'

export const courseAPI = {
  /**
   * Get all available courses (public endpoint - no auth required)
   * @returns {Promise} List of courses
   */
  async getAllCourses() {
    const response = await api.get('/courses/public')
    return response.data
  },

  /**
   * Get current user's assigned courses (requires auth)
   * @returns {Promise} List of user's courses
   */
  async getMyCoures() {
    const response = await api.get('/courses/my-courses')
    return response.data
  },

  /**
   * Get course by ID
   * @param {number} courseId - Course ID
   * @returns {Promise} Course data
   */
  async getCourse(courseId) {
    const response = await api.get(`/courses/${courseId}`)
    return response.data
  },

  /**
   * Create a new course
   * @param {Object} data - Course data
   * @returns {Promise} Created course
   */
  async createCourse(data) {
    const response = await api.post('/courses/', data)
    return response.data
  }
}

// Export individual functions for convenience
export const getAllCourses = () => courseAPI.getAllCourses()
export const getMyCoures = () => courseAPI.getMyCoures()
export const getCourse = (courseId) => courseAPI.getCourse(courseId)
export const createCourse = (data) => courseAPI.createCourse(data)
