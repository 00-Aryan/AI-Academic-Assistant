<template>
  <div class="header-section">

    <!--  Top Box -->
    <div class="top-box d-flex justify-content-between align-items-center p-3 rounded shadow-sm mb-2">
      <div class="d-flex align-items-center">
        <i class="bi bi-search text-muted me-2"></i>
        <input
          type="text"
          class="form-control form-control-sm rounded-pill"
          placeholder="Search courses, threads, or resources"
          style="width: 320px;"
        />
      </div>

      <div class="d-flex align-items-center">
        <!-- Ask AI button -->
        <!-- <button class="btn btn-outline-primary rounded-pill me-3 px-3 py-1 d-flex align-items-center hover-shadow">
          <i class="bi bi-stars me-2"></i> Ask AI
        </button> -->

        <!-- Notification -->
        <!-- <button class="btn btn-light border rounded-circle p-2 me-3 position-relative hover-shadow">
          <i class="bi bi-bell-fill"></i>
          <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 0.6rem;">
            3
          </span>
        </button> -->

        <!-- Profile dropdown -->
        <div class="dropdown">
          <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" data-bs-toggle="dropdown">
            <img :src="profileImage" alt="Profile" class="rounded-circle me-2" width="36" height="36" />
            <span class="fw-semibold text-dark"> Student </span>
          </a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#"><i class="bi bi-person-circle me-2"></i>Profile</a></li>
            <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i>Settings</a></li>
            <li><hr class="dropdown-divider" /></li>
            <li><a class="dropdown-item text-danger" href="#"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
          </ul>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import profileImage from '@/assets/profile.jpg'

export default {
  data() {
    return {
      profileImage
    }
  }
}
</script>

<style scoped>
.header-section {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--card-bg);
  padding-bottom: 0.5rem;
}

.top-box, .bottom-box {
  background-color: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.shadow-sm {
  box-shadow: 0 2px 6px var(--card-shadow);
}

.hover-shadow:hover {
  box-shadow: 0 2px 8px var(--card-shadow);
  transition: all 0.2s ease;
}

.active-btn {
  background-color: #0d6efd;
  color: white;
  border: none;
}

.active-btn:hover {
  background-color: #0b5ed7;
  color: white;
}
</style>
