<!-- 
  Example component demonstrating RBAC usage in Vue components
  This shows how to conditionally render content based on user roles
-->

<template>
  <div class="rbac-example">
    <h2>Role-Based Content Display Example</h2>
    
    <!-- Basic authentication check -->
    <div v-if="auth.isAuthenticated" class="mb-3">
      <p>✅ You are logged in as: <strong>{{ auth.userName }}</strong></p>
      <p>Role: <span class="badge bg-primary">{{ roleDisplay }}</span></p>
    </div>
    
    <div v-else class="alert alert-warning">
      ⚠️ Please login to view content
    </div>

    <!-- Role-specific content using store getters -->
    <div class="row mt-4">
      <!-- Student Content -->
      <div v-if="userStore.isStudent" class="col-md-6">
        <div class="card border-primary">
          <div class="card-header bg-primary text-white">
            Student Features
          </div>
          <div class="card-body">
            <ul>
              <li>View courses</li>
              <li>Submit queries</li>
              <li>Access AI assistant</li>
              <li>Study resources</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- TA Content -->
      <div v-if="userStore.isTA || userStore.isInstructor || userStore.isAdmin" class="col-md-6">
        <div class="card border-success">
          <div class="card-header bg-success text-white">
            TA Features
          </div>
          <div class="card-body">
            <ul>
              <li>Track student queries</li>
              <li>Create assessments</li>
              <li>Doubt summarizer</li>
              <li>Resource management</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Instructor Content -->
      <div v-if="userStore.isInstructor || userStore.isAdmin" class="col-md-6 mt-3">
        <div class="card border-info">
          <div class="card-header bg-info text-white">
            Instructor Features
          </div>
          <div class="card-body">
            <ul>
              <li>Discussion summaries</li>
              <li>Slide deck generator</li>
              <li>Advanced analytics</li>
              <li>Course management</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Admin Content -->
      <div v-if="userStore.isAdmin" class="col-md-6 mt-3">
        <div class="card border-danger">
          <div class="card-header bg-danger text-white">
            Admin Features
          </div>
          <div class="card-body">
            <ul>
              <li>User management</li>
              <li>System settings</li>
              <li>Full analytics</li>
              <li>Access all features</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Using hasRole method -->
    <div class="mt-4">
      <h4>Using hasRole Method</h4>
      <div class="d-flex gap-2">
        <button 
          v-if="auth.hasRole('student')" 
          class="btn btn-primary"
        >
          Student Action
        </button>
        <button 
          v-if="auth.hasRole('ta')" 
          class="btn btn-success"
        >
          TA Action
        </button>
        <button 
          v-if="auth.hasRole('instructor')" 
          class="btn btn-info"
        >
          Instructor Action
        </button>
        <button 
          v-if="auth.hasRole('admin')" 
          class="btn btn-danger"
        >
          Admin Action
        </button>
      </div>
    </div>

    <!-- Using hasAnyRole method -->
    <div class="mt-4">
      <h4>Using hasAnyRole Method</h4>
      <button 
        v-if="auth.hasAnyRole(['ta', 'instructor', 'admin'])" 
        class="btn btn-warning"
      >
        Staff Only Action
      </button>
      <button 
        v-if="auth.hasAnyRole(['instructor', 'admin'])" 
        class="btn btn-secondary"
      >
        Management Only Action
      </button>
    </div>

    <!-- Using hasPermission for custom role arrays -->
    <div class="mt-4">
      <h4>Using hasPermission Method</h4>
      <div v-if="auth.hasPermission(['admin'])" class="alert alert-danger">
        🔐 This is admin-only sensitive information
      </div>
      <div v-if="auth.hasPermission(['instructor', 'admin'])" class="alert alert-info">
        📊 This is visible to instructors and admins
      </div>
      <div v-if="auth.hasPermission(['ta', 'instructor', 'admin'])" class="alert alert-success">
        📚 This is visible to all staff members
      </div>
    </div>

    <!-- Navigation based on role -->
    <div class="mt-4">
      <h4>Quick Navigation</h4>
      <button @click="goToMyDashboard" class="btn btn-outline-primary">
        <i class="bi bi-house-door me-2"></i>
        Go to My Dashboard
      </button>
      <p class="text-muted small mt-2">
        Will redirect to: {{ auth.getDefaultRoute() }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/middleware/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const auth = useAuth()
const userStore = useUserStore()

const roleDisplay = computed(() => {
  const roleNames = {
    student: 'Student',
    ta: 'Teaching Assistant',
    instructor: 'Instructor',
    admin: 'Administrator'
  }
  return roleNames[auth.role] || auth.role || 'Unknown'
})

const goToMyDashboard = () => {
  router.push(auth.getDefaultRoute())
}
</script>

<style scoped>
.rbac-example {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.badge {
  font-size: 1rem;
  padding: 0.5rem 1rem;
}

.btn {
  transition: all 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
}
</style>
