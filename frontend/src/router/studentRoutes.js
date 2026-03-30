import StudentDashboard from '../components/student/StudentDashboard.vue'
import StudentQueries from '../components/student/studentQueries.vue'
import StudentResource from '../components/student/StudentResource.vue'
import AIassistant from '../components/student/studentAIAssistance.vue'
import StudentMyQuery from '../components/student/StudentNewQuery.vue'
import StudyBreak from '../components/student/StudyBreak.vue'
import Profile from '../components/student/Profile.vue'
import StudentSummary from '../components/student/StudentSummary.vue'

export default [
  { 
    path: 'dashboard', 
    name: 'StudentDashboard', 
    component: StudentDashboard,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'queries', 
    name: 'StudentQueries', 
    component: StudentQueries,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'resources', 
    name: 'StudentResource', 
    component: StudentResource,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'AI-assistant', 
    name: 'StudentAIAssistant', 
    component: AIassistant,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'my-query', 
    name: 'StudentMyQuery', 
    component: StudentMyQuery,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'new-query', 
    name: 'StudentNewQuery', 
    component: StudentMyQuery,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'study-break', 
    name: 'StudyBreak', 
    component: StudyBreak,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'Profile', 
    name: 'StudentProfile', 
    component: Profile,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
  { 
    path: 'summary', 
    name: 'StudentSummary', 
    component: StudentSummary,
    meta: { requiresAuth: true, allowedRoles: ['student'] }
  },
]
