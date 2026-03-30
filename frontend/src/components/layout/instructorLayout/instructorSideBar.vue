<script setup>
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()

const mainNav = [
  { name: 'Dashboard', path: '/instructor/dashboard', icon: 'bi-speedometer2' },
  { name: 'Discussion Summaries', path: '/instructor/discussion-summaries', icon: 'bi-robot' },
  { name: 'Slides Workspace', path: '/instructor/slide-deck-generator', icon: 'bi-journal-text' },
  { name: 'My Slide Decks', path: '/instructor/slide-decks', icon: 'bi-collection-play' },
  { name: 'Question Paper Generator', path: '/instructor/assessment-generator', icon: 'bi-question-circle' },
  { name: 'Generated Quizzes', path: '/instructor/quiz-list', icon: 'bi-file-earmark-text' },
  { name: 'Profile', path: '/instructor/profile', icon: 'bi-gear' },
]

const quickActions = [
  { name: 'New Query', path: '/student/my-query', icon: 'bi-plus-circle' },
  { name: 'Book Office Hour', path: '/student/office-hour', icon: 'bi-calendar-check' },
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
      style="color: white !important;">
      <span class="fs-4 fw-semibold">AURA</span>
    </RouterLink>
    <hr class="border-light opacity-25" />

    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="item in mainNav" :key="item.path">
        <RouterLink :to="item.path" class="nav-link text-white" active-class="active-link"
          style="color: white !important;">
          <i :class="`${item.icon} me-2`" style="color: white !important;"></i> {{ item.name }}
        </RouterLink>
      </li>
    </ul>

    <div class="mt-auto">
      <button @click="signOut" class="btn btn-outline-light w-100 mt-3">
        <i class="bi bi-box-arrow-right me-2"></i> Sign Out
      </button>
      <p class="small text-secondary text-center mt-2 mb-0" style="color: #e0e7ff !important; opacity: 0.85;">Logged in
        as Instructor</p>
    </div>
  </div>
</template>



<style scoped>
/* Added rule to force white text */
.nav-link {
  color: white !important;
}

.nav-link:hover {
  background-color: #1b263b !important;
  color: white !important;
}

.active-link {
  background-color: #1b263b !important;
  color: white !important;
}
</style>

