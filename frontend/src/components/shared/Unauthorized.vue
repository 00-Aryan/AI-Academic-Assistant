<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5 text-center">
              <!-- Error Icon -->
              <div class="mb-4">
                <i class="bi bi-shield-x text-danger" style="font-size: 5rem;"></i>
              </div>

              <!-- Error Code -->
              <h1 class="display-1 fw-bold text-danger mb-3">403</h1>

              <!-- Error Message -->
              <h2 class="h4 mb-3">Access Denied</h2>
              <p class="text-muted mb-2">
                You don't have permission to access this page.
              </p>
              
              <!-- Role Information -->
              <div v-if="userRole" class="alert alert-info d-inline-block mt-3 mb-4">
                <i class="bi bi-info-circle me-2"></i>
                <strong>Your Role:</strong> {{ roleDisplay }}
                <span v-if="requiredRole" class="d-block mt-1 small">
                  <strong>Required Role:</strong> {{ requiredRole }}
                </span>
              </div>

              <!-- Action Buttons -->
              <div class="d-flex gap-3 justify-content-center flex-wrap">
                <button 
                  @click="goBack" 
                  class="btn btn-outline-secondary"
                >
                  <i class="bi bi-arrow-left me-2"></i>Go Back
                </button>
                <button 
                  @click="goToDashboard" 
                  class="btn btn-primary"
                >
                  <i class="bi bi-house-door me-2"></i>Go to My Dashboard
                </button>
              </div>

              <!-- Additional Information -->
              <div class="mt-4 pt-4 border-top">
                <p class="text-muted small mb-2">
                  <strong>Why am I seeing this?</strong>
                </p>
                <ul class="text-muted small text-start d-inline-block">
                  <li>You may have clicked a link meant for a different role</li>
                  <li>The page might require higher privileges</li>
                  <li>Your session may need to be refreshed</li>
                </ul>
              </div>

              <!-- Contact Support -->
              <div class="mt-3">
                <p class="text-muted small mb-0">
                  If you believe you should have access, please contact your administrator.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/middleware/auth'

const router = useRouter()
const route = useRoute()
const { getDefaultRoute, role: userRole } = useAuth()

const requiredRole = computed(() => route.query.requiredRole || null)

const roleDisplay = computed(() => {
  const roleNames = {
    student: 'Student',
    ta: 'Teaching Assistant',
    instructor: 'Instructor',
    admin: 'Administrator'
  }
  return roleNames[userRole] || userRole || 'Unknown'
})

const goBack = () => {
  // Try to go back, but if there's no history, go to dashboard
  if (window.history.length > 2) {
    router.go(-1)
  } else {
    goToDashboard()
  }
}

const goToDashboard = () => {
  router.push(getDefaultRoute())
}
</script>

<style scoped>
.card {
  border-radius: 1rem;
  transition: transform 0.2s;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.alert {
  border-radius: 0.5rem;
  border: none;
  background-color: #e7f3ff;
  color: #004085;
}

ul {
  text-align: left;
  max-width: 350px;
}

.bi {
  vertical-align: middle;
}
</style>
