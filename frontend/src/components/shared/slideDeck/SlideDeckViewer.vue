<template>
  <div class="flex min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 font-sans text-slate-800">
    <component :is="role === 'ta' ? taSidebar : instructorSidebar" />

    <main class="flex-1 ml-64 p-6 lg:p-8">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8 flex items-center justify-between">
          <div>
            <h1 class="font-extrabold text-4xl text-slate-900 tracking-tight">My Slide Decks</h1>
            <p class="text-slate-500 mt-1">Browse and manage your AI-generated presentations</p>
          </div>
          <router-link
            :to="`/${props.role}/slide-deck-creator`"
            class="px-6 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
          >
            ✨ Create New Deck
          </router-link>
        </div>

        <!-- Filters -->
        <div class="mb-6 flex gap-3 flex-wrap">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search decks..."
            class="px-4 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          />
          <select
            v-model="filterCourse"
            class="px-4 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          >
            <option value="">All Courses</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.name }}
            </option>
          </select>
          <div class="flex-1"></div>
          <button
            @click="loadDecks"
            class="px-4 py-2 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition"
          >
            🔄 Refresh
          </button>
        </div>

        <!-- Decks Grid -->
        <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="bg-white rounded-xl border border-slate-200 p-6 animate-pulse">
            <div class="h-6 bg-slate-200 rounded w-2/3 mb-4"></div>
            <div class="h-4 bg-slate-200 rounded w-full mb-2"></div>
            <div class="h-4 bg-slate-200 rounded w-4/5"></div>
          </div>
        </div>

        <div v-else-if="filteredDecks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="deck in filteredDecks"
            :key="deck.id"
            class="bg-white rounded-xl border border-slate-200 hover:shadow-lg transition overflow-hidden group cursor-pointer"
            @click="openDeck(deck)"
          >
            <!-- Card Header -->
            <div class="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-slate-200">
              <h3 class="font-bold text-slate-900 truncate group-hover:text-blue-600 transition">
                {{ deck.title }}
              </h3>
              <p class="text-xs text-slate-500 mt-1">{{ formatDate(deck.created_at) }}</p>
            </div>

            <!-- Card Content -->
            <div class="p-4">
              <div class="grid grid-cols-2 gap-3 mb-4">
                <div class="text-center">
                  <p class="text-2xl font-bold text-blue-600">{{ deck.slides.length }}</p>
                  <p class="text-xs text-slate-500">Slides</p>
                </div>
                <div class="text-center">
                  <p class="text-2xl font-bold text-green-600">{{ deck.creator.id }}</p>
                  <p class="text-xs text-slate-500">Creator</p>
                </div>
              </div>

              <p v-if="deck.description" class="text-sm text-slate-600 line-clamp-2 mb-4">
                {{ deck.description }}
              </p>

              <!-- Tags -->
              <div class="flex flex-wrap gap-1 mb-4">
                <span class="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">
                  {{ deck.course_id }}
                </span>
              </div>
            </div>

            <!-- Card Actions -->
            <div class="p-4 bg-slate-50 border-t border-slate-200 flex gap-2">
              <button
                @click.stop="viewDeck(deck.id)"
                class="flex-1 px-3 py-2 bg-blue-100 text-blue-700 font-semibold rounded-lg hover:bg-blue-200 transition text-sm"
              >
                👁️ View
              </button>
              <button
                @click.stop="editDeck(deck.id)"
                class="flex-1 px-3 py-2 bg-amber-100 text-amber-700 font-semibold rounded-lg hover:bg-amber-200 transition text-sm"
              >
                ✏️ Preview
              </button>
              <button
                @click.stop="deleteDeck(deck.id)"
                class="flex-1 px-3 py-2 bg-red-100 text-red-700 font-semibold rounded-lg hover:bg-red-200 transition text-sm"
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20">
          <div class="inline-block">
            <p class="text-2xl mb-4">📊</p>
            <p class="text-lg font-semibold text-slate-900 mb-2">No slide decks yet</p>
            <p class="text-slate-500 mb-6">Create your first AI-generated slide deck to get started</p>
            <router-link
              :to="`/${props.role}/slide-deck-creator`"
              class="inline-block px-6 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition"
            >
              Create Your First Deck
            </router-link>
          </div>
        </div>
      </div>
    </main>

    <!-- Deck Detail Modal -->
    <div
      v-if="selectedDeck"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="selectedDeck = null"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-slate-200 sticky top-0 bg-white flex items-center justify-between">
          <h3 class="text-2xl font-bold text-slate-900">{{ selectedDeck.title }}</h3>
          <button
            @click="selectedDeck = null"
            class="text-slate-400 hover:text-slate-600 text-3xl"
          >
            ✕
          </button>
        </div>

        <div class="p-6">
          <!-- Deck Info -->
          <div class="grid grid-cols-3 gap-4 mb-6 p-4 bg-slate-50 rounded-lg">
            <div>
              <p class="text-xs font-bold text-slate-600 uppercase">Slides</p>
              <p class="text-2xl font-bold text-slate-900">{{ selectedDeck.slides.length }}</p>
            </div>
            <div>
              <p class="text-xs font-bold text-slate-600 uppercase">Created</p>
              <p class="text-sm font-semibold text-slate-900">{{ formatDate(selectedDeck.created_at) }}</p>
            </div>
            <div>
              <p class="text-xs font-bold text-slate-600 uppercase">Course</p>
              <p class="text-sm font-semibold text-slate-900">#{{ selectedDeck.course_id }}</p>
            </div>
          </div>

          <!-- Description -->
          <div v-if="selectedDeck.description" class="mb-6">
            <p class="text-sm font-bold text-slate-700 uppercase mb-2">Description</p>
            <p class="text-slate-700">{{ selectedDeck.description }}</p>
          </div>

          <!-- Slides Preview -->
          <div>
            <p class="text-sm font-bold text-slate-700 uppercase mb-3">Slides</p>
            <div class="space-y-2 max-h-96 overflow-y-auto">
              <div
                v-for="(slide, idx) in selectedDeck.slides"
                :key="idx"
                class="p-3 bg-slate-50 border border-slate-200 rounded-lg"
              >
                <p class="font-semibold text-slate-900">{{ idx + 1 }}. {{ slide.title }}</p>
                <p class="text-xs text-slate-600 line-clamp-2 mt-1">{{ slide.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 border-t border-slate-200 flex gap-3 justify-end bg-slate-50">
          <button
            @click="selectedDeck = null"
            class="px-4 py-2 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition"
          >
            Close
          </button>
          <router-link
            :to="`/${props.role}/slide-deck/${selectedDeck.id}`"
            class="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition"
          >
            Open Full View
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import taSidebar from '@/components/layout/TaLayout/TASidebar.vue'
import { api } from '@/api'

const props = defineProps({
  role: {
    type: String,
    default: 'instructor'
  }
})

const router = useRouter()

const decks = ref([])
const courses = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const filterCourse = ref('')
const selectedDeck = ref(null)

const filteredDecks = computed(() => {
  return decks.value.filter(deck => {
    const matchesSearch = deck.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCourse = !filterCourse.value || deck.course_id === parseInt(filterCourse.value)
    return matchesSearch && matchesCourse
  })
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

async function loadDecks() {
  isLoading.value = true
  try {
    const response = await api.get('/slide-decks/')
    decks.value = response.data
  } catch (error) {
    console.error('Failed to load decks:', error)
  } finally {
    isLoading.value = false
  }
}

function openDeck(deck) {
  selectedDeck.value = deck
}

function viewDeck(id) {
  router.push(`/${props.role}/slide-deck/${id}`)
}

function editDeck(id) {
  // Redirect to preview page to edit the deck
  router.push({
    name: props.role === 'ta' ? 'TaSlideDeckPreview' : 'InstructorSlideDeckPreview',
    params: { deckId: id }
  })
}

async function deleteDeck(id) {
  if (!confirm('Are you sure you want to delete this slide deck?')) return

  try {
    await api.delete(`/slide-decks/${id}`)
    await loadDecks()
    selectedDeck.value = null
  } catch (error) {
    console.error('Failed to delete deck:', error)
    alert('Failed to delete: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadDecks()
})
</script>

<style scoped></style>
