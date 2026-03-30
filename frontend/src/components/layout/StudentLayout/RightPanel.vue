<template>
  <div class="border-start p-3 right-panel-theme" style="width: 300px; min-height: 100vh;" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
    <!-- Pinned Resources -->
    <div class="mb-4">
      <h6 class="fw-semibold mb-3 panel-heading" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
        <i class="bi bi-pin-angle me-2 panel-icon"></i>Pinned resources ({{ pinnedResources.length }})
      </h6>
      <div v-if="pinnedResources.length === 0" class="text-muted small text-center py-3">
        <i class="bi bi-pin-angle text-3xl"></i>
        <p class="mb-0 mt-2">No pinned resources</p>
      </div>
      <div v-else class="list-group small">
        <a 
          v-for="res in pinnedResources.slice(0, 3)" 
          :key="res.id"
          href="#" 
          class="list-group-item list-group-item-action border rounded mb-2 panel-item" 
          @click.prevent="openResource(res)"
          :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
        >
          <i :class="getResourceIcon(res.resource_type)" class="me-2 panel-item-icon"></i>
          {{ res.title }}
        </a>
        <button 
          v-if="pinnedResources.length > 3"
          @click="viewPinned"
          class="btn btn-sm panel-btn border w-100 text-start"
          :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
        >
          <i class="bi bi-three-dots me-2"></i>View all ({{ pinnedResources.length }})
        </button>
      </div>
    </div>

    <!-- ⚡ Quick Actions -->
    <div class="mb-4">
      <h6 class="fw-semibold mb-3 panel-heading" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
        <i class="bi bi-lightning-charge-fill me-2 panel-icon-warning"></i>Quick actions
      </h6>
      <div class="d-grid gap-2">
        <button type="button" class="btn panel-btn border text-start py-2" @click="viewDeadlines" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <i class="bi bi-calendar-check me-2 panel-icon-danger"></i>View deadlines
        </button>
        <button type="button" class="btn panel-btn border text-start py-2" @click="shareToClass" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <i class="bi bi-share me-2 panel-icon"></i>Share to class
        </button>
        <button type="button" class="btn panel-btn border text-start py-2" @click="viewPinned" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <i class="bi bi-pin-angle me-2 panel-icon-success"></i>Pinned resources ({{ pinnedResources.length }})
        </button>
      </div>
    </div>

    <!--  Continue Section -->
    <div>
      <h6 class="fw-semibold mb-3 panel-heading">
        <i class="bi bi-clock-history me-2 panel-icon-info"></i>Continue where you left
      </h6>
      <div class="list-group small">
        <a href="#" class="list-group-item list-group-item-action border rounded mb-2 d-flex align-items-center panel-item" @click="continueStudy('CS301 Thread • Graphs')" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <i class="bi bi-diagram-3-fill me-2 panel-item-icon"></i>
          CS301 Thread • Graphs
        </a>
        <a href="#" class="list-group-item list-group-item-action border rounded d-flex align-items-center panel-item" @click="continueStudy('Systems Lab • Setup')" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <i class="bi bi-cpu-fill me-2 panel-item-icon"></i>
          Systems Lab • Setup
        </a>
      </div>
    </div>

    <!-- Deadlines Modal -->
    <div class="modal fade" id="deadlinesModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow modal-theme">
          <div class="modal-header modal-header-danger text-white rounded-top-4">
            <h5 class="modal-title"><i class="bi bi-calendar-check me-2"></i>Upcoming Deadlines</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body modal-body-theme">
            <ul class="list-group small">
              <li class="list-group-item">CS301 Project • Due Nov 5</li>
              <li class="list-group-item">Linear Algebra Quiz • Due Nov 8</li>
              <li class="list-group-item">Systems Assignment • Due Nov 10</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div class="modal fade" id="shareModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 shadow modal-theme">
          <div class="modal-header modal-header-primary text-white rounded-top-4">
            <h5 class="modal-title"><i class="bi bi-share me-2"></i>Share Resource</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body modal-body-theme">
            <input type="text" class="form-control mb-3 modal-input" placeholder="Enter email or username" />
            <button class="btn modal-btn-primary w-100 rounded-pill" @click="shareNow">Share</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useThemeStore } from '@/stores/theme'

export default {
  props: {
    pinnedResources: {
      type: Array,
      default: () => []
    }
  },
  setup() {
    const themeStore = useThemeStore()
    return { themeStore }
  },
  methods: {
    openResource(resource) {
      if (resource.resource_type === 'link') {
        window.open(resource.url, '_blank')
      } else {
        this.$emit('open-resource', resource)
      }
    },
    getResourceIcon(type) {
      const icons = {
        document: 'bi bi-file-earmark-text',
        image: 'bi bi-image',
        link: 'bi bi-link-45deg',
        pdf: 'bi bi-file-earmark-pdf',
      }
      return icons[type] || 'bi bi-file-earmark'
    },
    viewDeadlines() {
      // TODO: Implement deadlines modal
      alert('View deadlines - Coming soon!')
    },
    shareToClass() {
      // TODO: Implement share modal
      alert('Share to class - Coming soon!')
    },
    viewPinned() {
      this.$emit('view-pinned')
    },
    continueStudy(topic) {
      alert(`Resuming: ${topic}`)
    },
    shareNow() {
      alert('Resource shared successfully ')
    }
  }
}
</script>

<style scoped>
.list-group-item {
  transition: background 0.2s ease, transform 0.2s ease;
}
.list-group-item:hover {
  background-color: var(--color-bg-hover, rgba(255,255,255,0.04));
  transform: translateY(-2px);
}
.panel-item {
  background: transparent;
  color: var(--color-text-on-panel);
}
.panel-item-icon {
  color: var(--color-icon-on-panel, var(--color-text-secondary));
}
.panel-heading {
  color: var(--color-text-on-panel);
}
.panel-icon {
  color: var(--color-icon-on-panel, var(--color-text-secondary));
}
.panel-icon-warning { color: var(--color-accent-yellow); }
.panel-icon-danger { color: var(--color-accent-red); }
.panel-icon-success { color: var(--color-accent-green); }
.panel-icon-info { color: var(--color-accent-blue); }
.panel-btn {
  background: var(--color-btn-bg);
  color: var(--color-btn-text);
}
.panel-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.right-panel-theme {
  background: var(--color-bg-card);
  color: var(--color-text-on-panel);
  transition: background 0.3s, color 0.3s;
}
.modal-theme {
  background: var(--color-bg-card);
  color: var(--color-text-on-panel);
}
.modal-header-danger { background: var(--color-accent-red); }
.modal-header-primary { background: var(--color-accent-blue); }
.modal-body-theme { background: var(--color-bg-card); color: var(--color-text-on-panel); }
.modal-input { background: var(--color-bg-card); color: var(--color-text-on-panel); border-color: var(--color-border); }
.modal-btn-primary { background: var(--color-accent-blue); color: var(--color-btn-blue-text); }
</style>
