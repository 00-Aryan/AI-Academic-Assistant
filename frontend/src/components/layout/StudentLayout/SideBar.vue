<script setup>
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()

// Navigation structure for student (you could make this role-based later)
const mainNav = [
  { name: 'Dashboard', path: '/student/dashboard', icon: 'bi-speedometer2' },
  { name: 'AI Assistant', path: '/student/AI-assistant', icon: 'bi-robot' },
  { name: 'My Courses & Resources', path: '/student/resources', icon: 'bi-journal-text' },
  { name: 'My Queries', path: '/student/queries', icon: 'bi-question-circle' },
  { name: 'Profile', path: '/student/profile', icon: 'bi-gear' },
]

const quickActions = [
  { name: 'New Query', path: '/student/my-query', icon: 'bi-plus-circle' },
  { name: 'Video Summary', path: '/student/summary', icon: 'bi-calendar-check' },
]

function signOut() {
  alert('Signed out successfully!')
  router.push('/login')
}
</script>

<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 text-white vh-100"
    style="width: 250px; background-color: #0d1b2a; height: 100vh; position: fixed; top: 0; left: 0; z-index: 100;">
    <RouterLink to="/" class="d-flex align-items-center mb-3 text-white text-decoration-none"
      style="color: #fff; opacity: 1; font-weight: 600;">
      <span class="fs-4 fw-semibold">AURA</span>
    </RouterLink>
    <hr class="border-light opacity-25" />

    <!-- Main nav -->
    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="item in mainNav" :key="item.path">
        <RouterLink :to="item.path" class="nav-link text-white" active-class="active-link"
          style="color: white !important; opacity: 1; font-weight: 500;">
          <i :class="`${item.icon} me-2`" style="color: #fff; opacity: 1;"></i> {{ item.name }}
        </RouterLink>
      </li>
    </ul>

    <hr class="border-light opacity-25" />

    <!-- Quick Actions -->
    <p class="text-secondary text-uppercase small mb-2"
      style="color: #e0e7ff !important; opacity: 0.85; font-weight: 400;">Quick Actions</p>
    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="action in quickActions" :key="action.path">
        <RouterLink :to="action.path" class="nav-link text-white" active-class="active-link"
          style="color: white !important; opacity: 1; font-weight: 500;">
          <i :class="`${action.icon} me-2`" style="color: white !important; opacity: 1;"></i> {{ action.name }}
        </RouterLink>
      </li>
    </ul>

    <!-- Sign Out -->
    <div class="pb-2 mt-auto">
      <button @click="signOut" class="btn btn-outline-light w-100 mt-3"
        style="background: #2563eb; color: #fff; font-weight: 500;">
        <i class="bi bi-box-arrow-right me-2" style="color: #fff; opacity: 1;"></i> Sign Out
      </button>
      <p class="small text-secondary text-center mt-2 mb-0" style="color: #e0e7ff; opacity: 0.85; font-weight: 400;">
        Logged in as Student</p>
    </div>
  </div>
</template>

<style scoped>
/* This rule is missing in your student sidebar */
.nav-link {
  color: white !important;
}

.nav-link:hover {
  background-color: #1b263b !important;
  color: white !important;
  /* Added for safety */
}

.active-link {
  background-color: #1b263b !important;
  color: white !important;
  /* Added for safety */
}
</style>
