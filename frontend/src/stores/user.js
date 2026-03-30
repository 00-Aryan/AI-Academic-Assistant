// src/stores/user.js
import { defineStore } from 'pinia'
import { authAPI } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    role: localStorage.getItem('role') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
    isInstructor: (state) => state.role === 'instructor',
    isTA: (state) => state.role === 'ta',
    isStudent: (state) => state.role === 'student',
    userEmail: (state) => state.user?.email || '',
    userName: (state) => state.user?.full_name || state.user?.email?.split('@')[0] || 'User',
    userId: (state) => state.user?.id || null,
  },

  actions: {
    /**
     * Register a new user
     */
    async register(email, password, role = 'student', fullName = '', courseIds = []) {
      try {
        const data = await authAPI.register({
          email,
          password,
          role,
          full_name: fullName,
          course_ids: courseIds
        })

        this.setAuthData(data)
        return { success: true, data }
      } catch (error) {
        console.error('Registration error:', error)
        return {
          success: false,
          error: error.response?.data?.detail || 'Registration failed'
        }
      }
    },

    /**
     * Login user
     */
    async login(email, password) {
      try {
        const data = await authAPI.login({ email, password })

        this.setAuthData(data)
        return { success: true, data }
      } catch (error) {
        console.error('Login error:', error)
        return {
          success: false,
          error: error.response?.data?.detail || 'Login failed'
        }
      }
    },

    /**
     * Logout user
     */
    async logout() {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearUser()
      }
    },

    /**
     * Get current user profile from API
     */
    async fetchCurrentUser() {
      try {
        const userData = await authAPI.getCurrentUser()
        this.user = userData
        this.role = userData.role
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('role', userData.role)
        return { success: true, data: userData }
      } catch (error) {
        console.error('Fetch user error:', error)
        // If fetch fails (e.g., token expired), clear auth
        this.clearUser()
        return { success: false, error: 'Failed to fetch user data' }
      }
    },

    /**
     * Update user profile
     */
    async updateProfile(updates) {
      try {
        const userData = await authAPI.updateProfile(updates)
        this.user = userData
        localStorage.setItem('user', JSON.stringify(userData))
        return { success: true, data: userData }
      } catch (error) {
        console.error('Update profile error:', error)
        return {
          success: false,
          error: error.response?.data?.detail || 'Update failed'
        }
      }
    },

    /**
     * Set authentication data (tokens and user)
     */
    setAuthData(data) {
      this.token = data.access_token
      this.refreshToken = data.refresh_token
      this.user = data.user
      this.role = data.user.role

      // Persist to localStorage
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      localStorage.setItem('role', data.user.role)
    },

    /**
     * Set tokens (used by axios interceptor for token refresh)
     */
    setTokens(accessToken, refreshToken) {
      this.token = accessToken
      this.refreshToken = refreshToken
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
    },

    /**
     * Set user data and role (legacy support)
     */
    setUser(token, role) {
      this.token = token
      this.role = role
      localStorage.setItem('access_token', token)
      localStorage.setItem('role', role)
    },

    /**
     * Clear all user data (logout)
     */
    clearUser() {
      this.token = null
      this.refreshToken = null
      this.user = null
      this.role = null

      // Clear localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      localStorage.removeItem('role')
    },

    /**
     * Initialize store from localStorage (called on app load)
     */
    initializeAuth() {
      const token = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      const user = localStorage.getItem('user')
      const role = localStorage.getItem('role')

      if (token && user) {
        this.token = token
        this.refreshToken = refreshToken
        this.user = JSON.parse(user)
        this.role = role

        // Optionally fetch fresh user data
        // this.fetchCurrentUser()
      }
    },
  },
})
