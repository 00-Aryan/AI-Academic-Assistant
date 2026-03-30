import AssessmentWorkspace from '../components/shared/assessment/AssessmentWorkspace.vue'
import InstructorDashboard from '../components/instructor/InstructorDashboard.vue'
import InstructorDiscussionSummaries from '../components/instructor/InstructorDiscussionSummaries.vue'
import SlideDeckConfig from '../components/shared/slideDeck/SlideDeckConfig.vue'
import SlideDeckPreview from '../components/shared/slideDeck/SlideDeckPreview.vue'
import InstructorProfile from '../components/instructor/InstructorProfile.vue'
import QuizDetails from '../components/shared/assessment/QuizDetail.vue'
import QuizList from '../components/shared/assessment/QuizList.vue'
import SlideDeckViewer from '../components/shared/slideDeck/SlideDeckViewer.vue'

export default {
  path: '/instructor',
  meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] },
  children: [
    { 
      path: 'dashboard', 
      name: 'InstructorDashboard', 
      component: InstructorDashboard,
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'assessment-generator', 
      name: 'InstructorAssessmentWorkspace', 
      component: AssessmentWorkspace, 
      props: () => ({ role:'instructor' }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'discussion-summaries', 
      name: 'InstructorDiscussionSummaries', 
      component: InstructorDiscussionSummaries,
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'slide-deck-generator', 
      name: 'InstructorSlideDeckConfig', 
      component: SlideDeckConfig, 
      props: () => ({ role:'instructor' }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'slide-deck-preview/:deckId?', 
      name: 'InstructorSlideDeckPreview', 
      component: SlideDeckPreview, 
      props: (route) => ({ role: 'instructor', deckId: route.params.deckId }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'slide-decks', 
      name: 'InstructorSlideDeckViewer', 
      component: SlideDeckViewer, 
      props: () => ({ role:'instructor' }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'quiz-list', 
      name: 'QuizList', 
      component: QuizList, 
      props: () => ({ role:'instructor' }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'quiz-details/:id', 
      name: 'QuizDetails', 
      component: QuizDetails, 
      props: (route) => ({ role:'instructor', id: route.params.id }),
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
    { 
      path: 'profile', 
      name: 'InstructorProfile', 
      component: InstructorProfile,
      meta: { requiresAuth: true, allowedRoles: ['instructor', 'admin'] }
    },
  ],
}
