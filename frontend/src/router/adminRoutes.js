import AdminDashboard from '../components/Admin/AdminDashboard.vue'

export default {
  path: '/admin',
  meta: { requiresAuth: true, allowedRoles: ['admin'] },
  children: [
    { path: '', redirect: '/admin/dashboard' },
    { 
      path: 'dashboard', 
      name: 'AdminDashboard', 
      component: AdminDashboard,
      meta: { requiresAuth: true, allowedRoles: ['admin'] }
    }
  ],
}
