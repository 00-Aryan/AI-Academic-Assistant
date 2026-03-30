<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5 text-center">
              <!-- Error Icon -->
              <div class="mb-4">
                <i class="bi bi-exclamation-triangle-fill text-warning" style="font-size: 5rem;"></i>
              </div>

              <!-- Error Code -->
              <h1 class="display-1 fw-bold text-primary mb-3">404</h1>

              <!-- Error Message -->
              <h2 class="h4 mb-3">Page Not Found</h2>
              <p class="text-muted mb-4">
                The page you are looking for doesn't exist or has been moved.
              </p>

              <!-- Action Buttons -->
              <div class="d-flex gap-3 justify-content-center flex-wrap">
                <button 
                  @click="goBack" 
                  class="btn btn-outline-primary"
                >
                  <i class="bi bi-arrow-left me-2"></i>Go Back
                </button>
                <button 
                  @click="goHome" 
                  class="btn btn-primary"
                >
                  <i class="bi bi-house-door me-2"></i>Go to Dashboard
                </button>
              </div>

              <!-- Additional Help -->
              <div class="mt-4 pt-4 border-top">
                <p class="text-muted small mb-0">
                  If you believe this is an error, please contact support.
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
import { useRouter } from 'vue-router'
import { useAuth } from '@/middleware/auth'

const router = useRouter()
const { getDefaultRoute, isAuthenticated } = useAuth()

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  if (isAuthenticated) {
    router.push(getDefaultRoute())
  } else {
    router.push('/')
  }
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

.bi {
  vertical-align: middle;
}
</style>
