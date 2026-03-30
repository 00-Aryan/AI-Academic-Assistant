import AssessmentWorkspace from '@/components/shared/assessment/AssessmentWorkspace.vue'
import TADashboard from '@/components/TA/TADashboard.vue'
import QueryTracker from '@/components/TA/QueryTracker.vue'
import SlideDeckConfig from '@/components/shared/slideDeck/SlideDeckConfig.vue'
import SlideDeckPreview from '@/components/shared/slideDeck/SlideDeckPreview.vue'
import SlideDeckViewer from '@/components/shared/slideDeck/SlideDeckViewer.vue'
import DoubtSummarizer from '../components/TA/DoubtSummarizer.vue'
import OnboardingMentor from '../components/TA/OnboardingMentor.vue'
import TaResourseshub from '@/components/TA/TaResourses_hub.vue'
import TaProfile from '../components/TA/TaProfile.vue'
import QuizDetails from '@/components/shared/assessment/QuizDetail.vue'
import QuizList from '@/components/shared/assessment/QuizList.vue'


export default [
    { 
      path: 'dashboard', 
      name: 'TaDashboard', 
      component: TADashboard,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    {
      path: 'query-tracker', 
      name: 'TaQueryTracker', 
      component: QueryTracker,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'assessment-generator', 
      name: 'TaAssessmentWorkspace', 
      component: AssessmentWorkspace, 
      props: () => ({ role:'ta' }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'quiz-list', 
      name: 'TaQuizList', 
      component: QuizList, 
      props: () => ({ role:'ta' }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'quiz-details/:id', 
      name: 'TaQuizDetails', 
      component: QuizDetails, 
      props: (route) => ({ role:'ta', id: route.params.id }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'slide-deck-creator', 
      name: 'TaSlideDeckConfig', 
      component: SlideDeckConfig, 
      props: () => ({ role:'ta' }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'slide-deck-preview/:deckId?', 
      name: 'TaSlideDeckPreview', 
      component: SlideDeckPreview, 
      props: (route) => ({ role: 'ta', deckId: route.params.deckId }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'slide-decks', 
      name: 'TaSlideDeckViewer', 
      component: SlideDeckViewer, 
      props: () => ({ role:'ta' }),
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'doubt-summarizer', 
      name: 'DoubtSummarizer', 
      component: DoubtSummarizer,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'onboarding-mentor', 
      name: 'OnboardingMentor', 
      component: OnboardingMentor,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
    { 
      path: 'resource', 
      name: 'TaResoursesHub', 
      component: TaResourseshub,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    }, 
    { 
      path: 'profile', 
      name: 'TaProfile', 
      component: TaProfile,
      meta: { requiresAuth: true, allowedRoles: ['ta', 'instructor', 'admin'] }
    },
]
