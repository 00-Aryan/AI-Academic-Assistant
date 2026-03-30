import { createRouter, createWebHistory } from 'vue-router'
import { strictRoleGuard } from '@/middleware/auth'

// Auth / landing
import LandingPage from '../components/LandingPage.vue'
import RegisterPage from '../components/auth/RegisterPage.vue'
import LoginPage from '../components/auth/LoginPage.vue'

// Role-based route imports
import studentRoutes from './studentRoutes'
import instructorRoutes from './instructorRoutes'
import taRoutes from './TaRoutes'
import adminRoutes from './adminRoutes'

const routes = [
  { 
    path: '/', 
    component: LandingPage,
    meta: { requiresAuth: false }
  },
  { 
    path: '/register', 
    component: RegisterPage,
    meta: { requiresAuth: false }
  },
  { 
    path: '/login', 
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/student',
    meta: { requiresAuth: true, allowedRoles: ['student'] },
    children: [
      { path: '', redirect: '/student/dashboard' },
      ...studentRoutes
    ],
  },
  {
    path: '/ta',
    meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] },
    children: [
     { path: '', redirect: '/ta/dashboard' },
      ...taRoutes
    ],
  },
  instructorRoutes,
  adminRoutes,
  // Unauthorized access route
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('../components/shared/Unauthorized.vue'),
    meta: { requiresAuth: false }
  },
  // Catch-all 404 route
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../components/shared/NotFound.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Apply navigation guard to all routes
router.beforeEach(strictRoleGuard)

export default router
