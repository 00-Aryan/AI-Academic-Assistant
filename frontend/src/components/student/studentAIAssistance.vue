<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import BottomBar from '@/components/layout/StudentLayout/BottomBar.vue'
import ChatBubble from '@/components/shared/ChatBubble.vue'
import { sendEnhancedChatMessage, getChatbotStatus } from '@/api/chatbot'

// State
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const conversationId = ref(null)
const chatMode = ref('academic')
const chatMessagesContainer = ref(null)
const isChatbotAvailable = ref(true)

const themeStore = useThemeStore()

// Suggested prompts
const suggestedPrompts = [
  'Summarize last CS 301 lecture',
  'Explain Dijkstra with example',
  'Draft study plan for finals',
  'Help me understand recursion'
]

// Initialize with welcome message
onMounted(async () => {
  // Check chatbot status
  try {
    await getChatbotStatus()
    isChatbotAvailable.value = true
  } catch (error) {
    console.error('Chatbot not available:', error)
    isChatbotAvailable.value = false
  }

  // Add welcome message
  messages.value.push({
    type: 'assistant',
    content: 'Welcome! Ask about deadlines, resources, or concepts. I can summarize lectures and draft study plans.',
    timestamp: new Date()
  })
})

// Send message
const sendMessage = async () => {
  const messageText = userInput.value.trim()

  if (!messageText) return

  // Add user message to chat
  messages.value.push({
    type: 'user',
    content: messageText,
    timestamp: new Date()
  })

  // Clear input
  userInput.value = ''

  // Scroll to bottom
  await nextTick()
  scrollToBottom()

  // Show loading state
  isLoading.value = true

  // Add loading message
  const loadingMessageIndex = messages.value.length
  messages.value.push({
    type: 'assistant',
    content: 'Thinking...',
    isLoading: true,
    timestamp: new Date()
  })

  try {
    // Send to backend using enhanced endpoint with query detection
    const response = await sendEnhancedChatMessage({
      message: messageText,
      mode: chatMode.value,
      conversation_id: conversationId.value,
      use_knowledge_base: true
    })

    // Store conversation ID
    if (response.conversation_id) {
      conversationId.value = response.conversation_id
    }

    // Replace loading message with actual response
    messages.value[loadingMessageIndex] = {
      type: 'assistant',
      content: response.answer || 'I received your message but couldn\'t generate a response.',
      timestamp: new Date(),
      sources: response.sources || [],
      knowledgeSourcesUsed: response.knowledge_sources_used || 0
    }

  } catch (error) {
    console.error('Failed to send message:', error)

    // Replace loading message with error
    messages.value[loadingMessageIndex] = {
      type: 'assistant',
      content: 'Sorry, I encountered an error. Please try again.',
      isError: true,
      timestamp: new Date()
    }
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

// Handle suggested prompt click
const useSuggestedPrompt = (prompt) => {
  userInput.value = prompt
  sendMessage()
}

// Scroll to bottom of chat
const scrollToBottom = () => {
  if (chatMessagesContainer.value) {
    chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight
  }
}

// Handle Enter key
const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

// Clear conversation
const clearChat = () => {
  messages.value = [{
    type: 'assistant',
    content: 'Conversation cleared. How can I help you today?',
    timestamp: new Date()
  }]
  conversationId.value = null
}

// Change chat mode
const changeChatMode = (mode) => {
  chatMode.value = mode
}

// Handle BottomBar send event
const onBottomBarSend = async ({ message, file }) => {
  if (!message?.trim()) return;
  userInput.value = message.trim();
  // Handle file if needed (upload logic here)
  await sendMessage();
};
</script>

<template>
  <div class="h-screen w-full flex" :style="{ background: 'var(--bg-primary)' }">
    <!-- Sidebar -->
    <Sidebar class="fixed top-0 left-0 h-screen w-48 z-20" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col ml-56 min-w-0">
      <!-- Mode Selection Header -->
      <header class="sticky top-0 z-10 px-9 py-3" :style="{ background: 'var(--bg-primary)' }">
        <div class="flex items-center justify-between">
          <!-- Conversation Topic Name -->
          <div class="flex items-center gap-3">
            <h1 class="text-lg font-semibold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
              AI Assistant - {{ chatMode.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
            </h1>
          </div>

          <!-- Clear Chat Button -->
          <button
            @click="clearChat"
            class="px-3 py-1.5 rounded-md transition-colors text-sm font-medium flex items-center gap-2 whitespace-nowrap hover:bg-gray-100"
            :style="{ color: '#ef4444' }"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear Chat
          </button>
        </div>
      </header>

      <!-- Content -->
      <div class="flex-1 flex overflow-hidden">
        <!-- Central Chat Section -->
        <section class="flex flex-col flex-1 overflow-hidden relative">
          <div ref="chatMessagesContainer" class="flex-1 overflow-y-auto px-5 py-3 space-y-4 pb-24">
            <!-- Message Loop -->
            <div class="space-y-3">
              <ChatBubble
                v-for="(message, index) in messages"
                :key="index"
                :message="message"
                :isUser="message.type === 'user'"
                :isDark="themeStore.currentTheme === 'dark'"
              />
            </div>

            <!-- Empty state -->
            <div
              v-if="messages.length === 1"
              class="flex flex-col items-center justify-center py-12"
              :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
            >
              <svg
                class="w-16 h-16 mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
              <p class="text-sm">Start a conversation with AURA AI Assistant</p>
            </div>
          </div>

          <!-- Fixed Bottom Bar for message input -->
          <BottomBar @send="onBottomBarSend" />
        </section>

        <!-- Right Sidebar -->
        <aside
          class="w-80 flex-shrink-0 flex flex-col gap-5 p-4 overflow-y-auto"
          :style="{ maxHeight: 'calc(100vh - 140px)' }"
        >
          <!-- Current Mode -->
          <div class="rounded-2xl shadow p-5" :style="{ background: 'var(--card-bg)' }">
            <h3 class="text-base font-semibold mb-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Current Mode</h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                @click="changeChatMode('academic')"
                :class="[
                  'px-2 py-3 rounded-lg text-xs transition-all text-center min-h-[44px] flex items-center justify-center border-2',
                  chatMode === 'academic'
                    ? 'bg-blue-600 border-blue-600 shadow-lg font-semibold'
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="chatMode === 'academic' 
                  ? { color: themeStore.currentTheme === 'dark' ? 'white' : 'black' } 
                  : { backgroundColor: 'var(--card-bg)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
              >
                Academic
              </button>
              <button
                @click="changeChatMode('study_help')"
                :class="[
                  'px-2 py-3 rounded-lg text-xs transition-all text-center min-h-[44px] flex items-center justify-center border-2',
                  chatMode === 'study_help'
                    ? 'bg-blue-600 border-blue-600 shadow-lg font-semibold'
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="chatMode === 'study_help' 
                  ? { color: themeStore.currentTheme === 'dark' ? 'white' : 'black' } 
                  : { backgroundColor: 'var(--card-bg)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
              >
                Study Help
              </button>
              <button
                @click="changeChatMode('doubt_clarification')"
                :class="[
                  'px-2 py-3 rounded-lg text-xs transition-all text-center min-h-[44px] flex items-center justify-center border-2',
                  chatMode === 'doubt_clarification'
                    ? 'bg-blue-600 border-blue-600 shadow-lg font-semibold'
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="chatMode === 'doubt_clarification' 
                  ? { color: themeStore.currentTheme === 'dark' ? 'white' : 'black' } 
                  : { backgroundColor: 'var(--card-bg)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
              >
                <span class="leading-tight">Doubt<br>Clarification</span>
              </button>
              <button
                @click="changeChatMode('general')"
                :class="[
                  'px-2 py-3 rounded-lg text-xs transition-all text-center min-h-[44px] flex items-center justify-center border-2',
                  chatMode === 'general'
                    ? 'bg-blue-600 border-blue-600 shadow-lg font-semibold'
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="chatMode === 'general' 
                  ? { color: themeStore.currentTheme === 'dark' ? 'white' : 'black' } 
                  : { backgroundColor: 'var(--card-bg)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
              >
                General
              </button>
            </div>
            <p class="text-xs mt-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
              <span v-if="chatMode === 'academic'">
                Get clear, educational explanations with examples.
              </span>
              <span v-else-if="chatMode === 'doubt_clarification'">
                Step-by-step help to clarify your doubts.
              </span>
              <span v-else-if="chatMode === 'study_help'">
                Study strategies, time management, and learning techniques.
              </span>
              <span v-else>
                General helpful responses for any question.
              </span>
            </p>
          </div>

          <!-- Suggested Prompts -->
          <div class="rounded-2xl shadow p-5" :style="{ background: 'var(--card-bg)' }">
            <h3 class="text-base font-semibold mb-3" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Suggested Prompts</h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(prompt, index) in suggestedPrompts"
                :key="index"
                @click="useSuggestedPrompt(prompt)"
                class="bg-black hover:bg-gray-800 text-white text-xs px-3 py-2 rounded-full transition border border-gray-600 shadow-md"
                :disabled="isLoading"
              >
                {{ prompt }}
              </button>
            </div>
            <p class="text-xs mt-3" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
              Click to use these prompts or type your own question.
            </p>
          </div>

          <!-- Conversation Info -->
          <div class="rounded-2xl shadow p-5" :style="{ background: 'var(--card-bg)' }">
            <h3 class="text-base font-semibold mb-3" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Conversation</h3>
            <div class="flex flex-col gap-2 text-sm">
              <div class="flex items-center justify-between">
                <span class="font-medium" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Messages:</span>
                <span class="font-semibold" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ messages.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="font-medium" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Status:</span>
                <span
                  :class="[
                    'font-semibold px-2 py-1 rounded-full text-xs',
                    isChatbotAvailable
                      ? 'bg-green-50 text-green-700'
                      : 'bg-red-50 text-red-700'
                  ]"
                >
                  {{ isChatbotAvailable ? 'Connected' : 'Disconnected' }}
                </span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scroll for chat section */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background-color: var(--border-default);
  border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
  background-color: var(--border-dark);
}

/* Textarea auto-resize */
textarea {
  min-height: 48px;
  line-height: 1.5;
}

/* Animation for loading dots */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}

.blue-shadow {
  box-shadow: 0 4px 24px 0 rgba(37, 99, 235, 0.25), 0 1.5px 6px 0 rgba(37, 99, 235, 0.18);
}
.default-shadow {
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
}
</style>
