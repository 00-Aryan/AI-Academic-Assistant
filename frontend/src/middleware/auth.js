/**
 * Authentication and Role-Based Access Control (RBAC) Middleware
 * 
 * This module provides navigation guards to protect routes and enforce
 * role-based access control throughout the application.
 */

import { useUserStore } from '@/stores/user'

/**
 * User roles hierarchy
 * Higher privilege roles can access lower privilege resources
 */
export const UserRoles = {
  STUDENT: 'student',
  TA: 'ta',
  INSTRUCTOR: 'instructor',
  ADMIN: 'admin'
}

/**
 * Role hierarchy map - defines which roles can access other role's resources
 * For example: admin can access all resources, instructor can access ta and student resources
 */
const roleHierarchy = {
  [UserRoles.ADMIN]: [UserRoles.ADMIN, UserRoles.INSTRUCTOR, UserRoles.TA, UserRoles.STUDENT],
  [UserRoles.INSTRUCTOR]: [UserRoles.INSTRUCTOR, UserRoles.TA, UserRoles.STUDENT],
  [UserRoles.TA]: [UserRoles.TA, UserRoles.STUDENT],
  [UserRoles.STUDENT]: [UserRoles.STUDENT]
}

/**
 * Check if a user has permission to access a route based on their role
 * 
 * @param {string} userRole - Current user's role
 * @param {string[]} allowedRoles - Array of roles allowed to access the route
 * @returns {boolean} True if user has permission
 */
export function hasPermission(userRole, allowedRoles) {
  if (!userRole || !allowedRoles || allowedRoles.length === 0) {
    return false
  }

  // Check if user's role is in the allowed roles
  if (allowedRoles.includes(userRole)) {
    return true
  }

  // Check if user's role hierarchy includes any of the allowed roles
  const userAccessibleRoles = roleHierarchy[userRole] || []
  return allowedRoles.some(role => userAccessibleRoles.includes(role))
}

/**
 * Get the default redirect path for a given role
 * 
 * @param {string} role - User role
 * @returns {string} Default dashboard path for the role
 */
export function getDefaultRouteForRole(role) {
  const roleRoutes = {
    [UserRoles.STUDENT]: '/student/dashboard',
    [UserRoles.TA]: '/ta/dashboard',
    [UserRoles.INSTRUCTOR]: '/instructor/dashboard',
    [UserRoles.ADMIN]: '/admin/dashboard'
  }
  
  return roleRoutes[role] || '/'
}

/**
 * Extract the base role from a route path
 * For example: /student/dashboard -> student
 * 
 * @param {string} path - Route path
 * @returns {string|null} Role name or null
 */
export function extractRoleFromPath(path) {
  const match = path.match(/^\/(student|ta|instructor|admin)/)
  return match ? match[1] : null
}

/**
 * Navigation guard to check authentication and authorization
 * Use this as a beforeEach guard in Vue Router
 * 
 * @param {Object} to - Target route
 * @param {Object} from - Current route
 * @param {Function} next - Navigation callback
 */
export function authGuard(to, from, next) {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated
  const userRole = userStore.role

  // Public routes that don't require authentication
  const publicRoutes = ['/', '/login', '/register']
  const isPublicRoute = publicRoutes.includes(to.path)

  // If route doesn't require auth, allow access
  if (isPublicRoute) {
    // If authenticated user tries to access login/register, redirect to dashboard
    if (isAuthenticated && (to.path === '/login' || to.path === '/register')) {
      return next(getDefaultRouteForRole(userRole))
    }
    return next()
  }

  // Check if user is authenticated
  if (!isAuthenticated) {
    // Store the intended destination
    return next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }

  // Check if route requires specific roles (from route meta)
  const allowedRoles = to.meta?.allowedRoles

  // If no specific roles required, allow access to authenticated users
  if (!allowedRoles || allowedRoles.length === 0) {
    return next()
  }

  // Check if user has permission to access this route
  if (hasPermission(userRole, allowedRoles)) {
    return next()
  }

  // User doesn't have permission - redirect to unauthorized page or their dashboard
  console.warn(`Access denied: User with role "${userRole}" tried to access route requiring roles: ${allowedRoles.join(', ')}`)
  
  return next({
    path: '/unauthorized',
    query: { 
      from: to.fullPath,
      requiredRole: allowedRoles[0] // Show the primary required role
    }
  })
}

/**
 * Check if the current route path matches the user's role
 * This is a stricter check - user must access their own role section
 * 
 * @param {string} path - Route path
 * @param {string} userRole - User's role
 * @returns {boolean} True if path matches user role
 */
export function isRoleRoute(path, userRole) {
  const routeRole = extractRoleFromPath(path)
  if (!routeRole) return true // Non-role-specific routes are allowed
  
  return routeRole === userRole
}

/**
 * Middleware to enforce strict role-based routing
 * This prevents students from accessing /ta routes even by URL manipulation
 * 
 * @param {Object} to - Target route
 * @param {Object} from - Current route
 * @param {Function} next - Navigation callback
 */
export function strictRoleGuard(to, from, next) {
  const userStore = useUserStore()
  const userRole = userStore.role
  const isAuthenticated = userStore.isAuthenticated

  // Public routes
  const publicRoutes = ['/', '/login', '/register', '/unauthorized', '/not-found']
  if (publicRoutes.includes(to.path)) {
    return next()
  }

  // Must be authenticated
  if (!isAuthenticated) {
    return next('/login')
  }

  // Extract role from path
  const routeRole = extractRoleFromPath(to.path)
  
  // If route is not role-specific, check meta.allowedRoles
  if (!routeRole) {
    const allowedRoles = to.meta?.allowedRoles
    if (!allowedRoles || hasPermission(userRole, allowedRoles)) {
      return next()
    }
    return next('/unauthorized')
  }

  // Strict check: route role must match user role
  if (routeRole !== userRole) {
    console.warn(`Role mismatch: User with role "${userRole}" tried to access "${routeRole}" route`)
    return next(getDefaultRouteForRole(userRole))
  }

  return next()
}

/**
 * Export a composable for use in components
 */
export function useAuth() {
  const userStore = useUserStore()

  return {
    isAuthenticated: userStore.isAuthenticated,
    user: userStore.user,
    role: userStore.role,
    hasRole: (role) => userStore.role === role,
    hasAnyRole: (roles) => roles.includes(userStore.role),
    hasPermission: (allowedRoles) => hasPermission(userStore.role, allowedRoles),
    logout: () => userStore.logout(),
    getDefaultRoute: () => getDefaultRouteForRole(userStore.role)
  }
}

export default {
  authGuard,
  strictRoleGuard,
  hasPermission,
  getDefaultRouteForRole,
  useAuth,
  UserRoles
}
