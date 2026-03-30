<template>
  <div class="flex h-screen" :style="{ backgroundColor: 'var(--page-bg)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex flex-col flex-1 min-h-screen">
      <!-- HeaderBar with sidebar offset -->
      <div class="ml-[250px]">
        <HeaderBar />
      </div>

      <!-- Body Section -->
      <div class="d-flex flex-grow-1 overflow-hidden">
        <!-- Main content container -->
        <main class="flex-1 overflow-y-auto p-6 ml-[250px]">
          <!-- DASHBOARD PAGE -->
          <section v-show="activePage === 'dashboard'" class="space-y-6">
            <!-- Hero -->
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 shadow">
              <h2 class="text-2xl font-bold mb-1" style="color: white !important;">Welcome back, {{ userName }}! 👋</h2>
              <p class="opacity-90" style="color: white !important;">Here's what's happening with your academics today.</p>
            </div>

            <!-- Loading State -->
            <div v-if="isLoading" class="text-center py-12">
              <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p class="mt-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Loading your dashboard...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6">
              <h3 class="font-semibold mb-2" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Error Loading Dashboard</h3>
              <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ error }}</p>
              <button @click="loadDashboardData" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
                Retry
              </button>
            </div>

            <!-- Dashboard Content -->
            <template v-else>
              <!-- Stats -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="rounded-xl p-5" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <div class="flex items-center justify-between mb-2">
                    <BookOpen class="w-5 h-5 text-blue-600" />
                    <span class="text-2xl font-bold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ dashboardStats.total_knowledge_sources || 0 }}</span>
                  </div>
                  <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Available Resources</p>
                  <p class="text-green-600 text-xs mt-1">Knowledge Base</p>
                </div>

                <div class="rounded-xl p-5" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <div class="flex items-center justify-between mb-2">
                    <CheckCircle class="w-5 h-5 text-green-600" />
                    <span class="text-2xl font-bold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userStats.total_queries || 0 }}</span>
                  </div>
                  <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">My Queries</p>
                  <p class="text-green-600 text-xs mt-1">All time</p>
                </div>

                <div class="rounded-xl p-5" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <div class="flex items-center justify-between mb-2">
                    <FileText class="w-5 h-5 text-purple-600" />
                    <span class="text-2xl font-bold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ activeTasksCount || 0 }}</span>
                  </div>
                  <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Active Tasks</p>
                  <p class="text-green-600 text-xs mt-1">In Progress</p>
                </div>

                <div class="rounded-xl p-5" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <div class="flex items-center justify-between mb-2">
                    <Clock class="w-5 h-5 text-orange-600" />
                    <span class="text-2xl font-bold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ recentQueriesCount || 0 }}</span>
                  </div>
                  <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Recent Queries</p>
                  <p class="text-green-600 text-xs mt-1">This week</p>
                </div>
              </div>

              <!-- Two-column area -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Recent Queries -->
                <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <h3 class="text-lg font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">My Recent Queries</h3>
                  <div v-if="recentQueries.length === 0" class="text-center py-8" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                    <AlertCircle class="w-12 h-12 mx-auto mb-2 text-gray-400" />
                    <p>No queries yet. Start asking questions!</p>
                  </div>
                  <div v-else class="space-y-3">
                    <div v-for="q in recentQueries" :key="q.title" class="flex items-start p-3 bg-gray-50 rounded-lg">
                      <AlertCircle class="w-5 h-5 text-orange-600 mr-3 mt-1" />
                      <div class="flex-1">
                        <p class="font-medium" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ q.title }}</p>
                        <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ q.status }}</p>
                        <p class="text-xs mt-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ formatDate(q.created_at) }}</p>
                      </div>
                      <span class="px-2 py-1 rounded text-xs" :class="getStatusClass(q.status)">
                        {{ q.status }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Top Knowledge Sources -->
                <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                  <h3 class="text-lg font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Popular Resources</h3>
                  <div v-if="topSources.length === 0" class="text-center py-8" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                    <BookOpen class="w-12 h-12 mx-auto mb-2 text-gray-400" />
                    <p>No resources available yet.</p>
                  </div>
                  <div v-else class="space-y-3">
                    <div v-for="source in topSources" :key="source.id" class="flex items-start p-3 bg-gray-50 rounded-lg">
                      <Bell class="w-5 h-5 text-blue-600 mr-3 mt-1" />
                      <div class="flex-1">
                        <p class="font-medium" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ source.title }}</p>
                        <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ source.category }}</p>
                        <p class="text-xs mt-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ source.views || 0 }} views</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Knowledge Sources by Category -->
              <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
                <h3 class="text-lg font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Resources by Category</h3>
                <div v-if="sourcesByCategory.length === 0" class="text-center py-8" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  <p>Loading categories...</p>
                </div>
                <div v-else class="space-y-4">
                  <div v-for="cat in sourcesByCategory" :key="cat.category">
                    <div class="flex items-center justify-between mb-2">
                      <div>
                        <p class="font-medium" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ cat.category }}</p>
                        <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ cat.count }} resources</p>
                      </div>
                      <button
                        @click="viewCategory(cat.category)"
                        class="text-blue-600 hover:text-blue-700 text-sm font-medium"
                      >
                        View All →
                      </button>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-blue-600 h-2 rounded-full"
                        :style="{ width: getCategoryPercentage(cat.count) + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </section>

          <!-- AI ASSISTANT PAGE -->
          <section v-show="activePage === 'ai-assistant'" class="h-full flex flex-col gap-4">
            <div class="rounded-xl p-4" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
              <h3 class="font-semibold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Enhanced AI Assistant with Knowledge Base</h3>
              <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Ask questions and get answers from our knowledge base and AI.</p>
              <label class="inline-flex items-center mt-2">
                <input
                  type="checkbox"
                  v-model="useKnowledgeBase"
                  class="form-checkbox h-4 w-4 text-blue-600"
                />
                <span class="ml-2 text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Use Knowledge Base (RAG)</span>
              </label>
            </div>

            <div class="flex-1 rounded-xl p-4 flex flex-col" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
              <div id="chatMessages" class="flex-1 overflow-y-auto p-4 space-y-3">
                <div v-for="(m, i) in messages" :key="i"
                  :class="m.from === 'user' ? 'flex justify-end' : 'flex justify-start'">
                  <div :class="['max-w-xs lg:max-w-md px-4 py-3 rounded-lg', m.from === 'user' ? 'bg-blue-600 text-white' : 'text-primary']"
                    :style="m.from !== 'user' ? { backgroundColor: 'var(--color-bg-card)' } : {}">
                    <p class="text-sm whitespace-pre-wrap">{{ m.text }}</p>
                    <!-- Show sources if available -->
                    <div v-if="m.sources && m.sources.length > 0" class="mt-2 pt-2 border-t border-gray-300">
                      <p class="text-xs font-semibold mb-1">📚 Sources:</p>
                      <ul class="text-xs space-y-1">
                        <li v-for="source in m.sources" :key="source.title">
                          • {{ source.title }} ({{ source.category }})
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <!-- Typing indicator -->
                <div v-if="isTyping" class="flex justify-start">
                  <div class="bg-gray-100 px-4 py-3 rounded-lg">
                    <div class="flex space-x-2">
                      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                      <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="p-4 border-t border-gray-200">
                <div class="flex gap-2">
                  <input
                    v-model="chatInput"
                    @keyup.enter="sendMessage"
                    :disabled="isTyping"
                    placeholder="Ask a question..."
                    class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 disabled:bg-gray-100"
                  />
                  <button
                    @click="sendMessage"
                    :disabled="isTyping || !chatInput.trim()"
                    class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {{ isTyping ? 'Sending...' : 'Send' }}
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- KNOWLEDGE BASE PAGE -->
          <section v-show="activePage === 'knowledge-base'" class="space-y-6">
            <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
              <h3 class="text-lg font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Knowledge Base</h3>

              <!-- Search and Filter -->
              <div class="flex gap-4 mb-4">
                <input
                  v-model="knowledgeSearch"
                  @input="searchKnowledge"
                  placeholder="Search resources..."
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
                <select
                  v-model="selectedCategory"
                  @change="filterByCategory"
                  class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                >
                  <option value="">All Categories</option>
                  <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                </select>
              </div>

              <!-- Knowledge Sources List -->
              <div v-if="knowledgeSources.length === 0" class="text-center py-12" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                <BookOpen class="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p>No resources found.</p>
              </div>
              <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="source in knowledgeSources"
                  :key="source.id"
                  class="bg-gray-50 border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                  @click="viewSource(source)"
                >
                  <div class="flex items-start justify-between mb-2">
                    <h4 class="font-semibold text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ source.title }}</h4>
                    <span class="text-xs px-2 py-1 bg-blue-100 text-blue-600 rounded">
                      {{ source.category }}
                    </span>
                  </div>
                  <p class="text-sm line-clamp-2" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ source.description }}</p>
                  <p class="text-xs mt-2" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ formatDate(source.created_at) }}</p>
                </div>
              </div>
            </div>
          </section>

          <!-- MY QUERIES PAGE -->
          <section v-show="activePage === 'my-queries'" class="space-y-6">
            <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">My Queries</h3>
                <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  New Query
                </button>
              </div>

              <div v-if="userStats.recent_queries && userStats.recent_queries.length > 0" class="space-y-3">
                <div
                  v-for="query in userStats.recent_queries"
                  :key="query.title"
                  class="p-4 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <h4 class="font-semibold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ query.title }}</h4>
                      <p class="text-sm mt-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Status: {{ query.status }}</p>
                      <p class="text-xs mt-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ formatDate(query.created_at) }}</p>
                    </div>
                    <span class="px-3 py-1 rounded text-sm" :class="getStatusClass(query.status)">
                      {{ query.status }}
                    </span>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-12" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                <AlertCircle class="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p>No queries yet. Create your first query!</p>
              </div>
            </div>
          </section>

          <!-- PROFILE PAGE -->
          <section v-show="activePage === 'profile'" class="space-y-6">
            <div class="rounded-xl p-6" :style="{ backgroundColor: 'var(--color-bg-card)', borderColor: 'var(--color-border)'}">
              <h3 class="text-lg font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">My Profile</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Full Name</label>
                  <p :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userName }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Email</label>
                  <p :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userEmail }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Role</label>
                  <p class="capitalize" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userRole }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Total Queries</label>
                  <p :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userStats.total_queries || 0 }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Active Tasks</label>
                  <p :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ userStats.active_tasks_count || 0 }}</p>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import { ref, onMounted, computed } from 'vue'
import {
  Menu,
  Bell,
  LogOut,
  BookOpen,
  CheckCircle,
  FileText,
  Clock,
  AlertCircle,
} from 'lucide-vue-next'

// Import API services
import { dashboardAPI, knowledgeAPI, tasksAPI, chatbotAPI } from '@/api'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'

// User store
const themeStore = useThemeStore()
// User store
const userStore = useUserStore()
const userName = computed(() => userStore.user?.full_name || 'Student')
const userEmail = computed(() => userStore.user?.email || '')
const userRole = computed(() => userStore.user?.role || 'student')

// Page state
const activePage = ref('dashboard')
const pageTitle = ref('Dashboard')

// Dashboard data
const isLoading = ref(false)
const error = ref(null)
const dashboardStats = ref({})
const userStats = ref({})
const topSources = ref([])
const recentQueries = ref([])
const activeTasksCount = ref(0)
const recentQueriesCount = ref(0)
const sourcesByCategory = ref([])

// Knowledge base
const knowledgeSources = ref([])
const knowledgeSearch = ref('')
const selectedCategory = ref('')
const categories = ref([])

// Chatbot
const messages = ref([
  { from: 'bot', text: "Hello! I'm your AI Assistant powered by our knowledge base. How can I help you today?" },
])
const chatInput = ref('')
const isTyping = ref(false)
const useKnowledgeBase = ref(true)
const conversationId = ref(null)

// Computed
const getCategoryPercentage = (count) => {
  const total = dashboardStats.value.total_knowledge_sources || 1
  return Math.round((count / total) * 100)
}

const getStatusClass = (status) => {
  const statusMap = {
    'OPEN': 'bg-yellow-100 text-yellow-700',
    'IN_PROGRESS': 'bg-blue-100 text-blue-700',
    'RESOLVED': 'bg-green-100 text-green-700',
    'CLOSED': 'bg-gray-100 text-gray-700',
  }
  return statusMap[status] || 'bg-gray-100 text-gray-700'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Functions
const showPage = (id) => {
  activePage.value = id
  const titleMap = {
    dashboard: 'Dashboard',
    'ai-assistant': 'AI Assistant',
    'knowledge-base': 'Knowledge Base',
    'my-queries': 'My Queries',
    forum: 'Discussion Forum',
    profile: 'Profile',
  }
  pageTitle.value = titleMap[id] || 'Aura'

  // Load data for specific pages
  if (id === 'knowledge-base' && knowledgeSources.value.length === 0) {
    loadKnowledgeSources()
  }
}

const loadDashboardData = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Load dashboard statistics
    const stats = await dashboardAPI.getStatistics()
    dashboardStats.value = stats

    // Load top sources
    const topSourcesData = await dashboardAPI.getTopSources({ limit: 5 })
    topSources.value = topSourcesData.sources || []

    // Load user context
    const context = await chatbotAPI.getUserContext()
    userStats.value = context.user_context || {}
    recentQueries.value = userStats.value.recent_queries || []
    recentQueriesCount.value = recentQueries.value.length

    // Load task statistics
    const taskStats = await tasksAPI.getStatistics()
    activeTasksCount.value = taskStats.in_progress_count || 0

    // Load categories
    if (stats.sources_by_category) {
      sourcesByCategory.value = Object.entries(stats.sources_by_category).map(([category, count]) => ({
        category,
        count
      }))
    }

    // Load available categories
    const categoriesData = await knowledgeAPI.getCategories()
    categories.value = categoriesData.categories || []

  } catch (err) {
    console.error('Error loading dashboard:', err)
    error.value = err.message || 'Failed to load dashboard data. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const loadKnowledgeSources = async () => {
  try {
    const params = {
      limit: 50
    }
    if (knowledgeSearch.value) {
      params.search = knowledgeSearch.value
    }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }

    const data = await knowledgeAPI.getSources(params)
    knowledgeSources.value = data.sources || []
  } catch (err) {
    console.error('Error loading knowledge sources:', err)
  }
}

const searchKnowledge = () => {
  loadKnowledgeSources()
}

const filterByCategory = () => {
  loadKnowledgeSources()
}

const viewCategory = (category) => {
  selectedCategory.value = category
  showPage('knowledge-base')
  loadKnowledgeSources()
}

const viewSource = (source) => {
  alert(`Viewing: ${source.title}\n\n${source.description}\n\nCategory: ${source.category}`)
}

const sendMessage = async () => {
  const text = chatInput.value.trim()
  if (!text || isTyping.value) return

  // Add user message
  messages.value.push({ from: 'user', text })
  chatInput.value = ''
  isTyping.value = true

  try {
    // Always use enhanced chat with query detection
    const response = await chatbotAPI.sendEnhancedChatMessage({
      message: text,
      conversation_id: conversationId.value,
      use_knowledge_base: useKnowledgeBase.value,
      mode: 'academic'
    })

    conversationId.value = response.conversation_id

    // Add bot message with sources
    messages.value.push({
      from: 'bot',
      text: response.answer,
      sources: response.sources || []
    })
  } catch (err) {
    console.error('Chat error:', err)
    messages.value.push({
      from: 'bot',
      text: 'Sorry, I encountered an error. Please try again.'
    })
  } finally {
    isTyping.value = false

    // Scroll to bottom
    setTimeout(() => {
      const chatDiv = document.getElementById('chatMessages')
      if (chatDiv) {
        chatDiv.scrollTop = chatDiv.scrollHeight
      }
    }, 100)
  }
}

// Lifecycle
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
