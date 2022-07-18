import { createRouter, createWebHashHistory } from 'vue-router'

import HomeView from '@/views/HomeView'
import FlashCards from '@/views/FlashCards'
import DashView from '@/views/DashView'
import LoginView from '@/views/LoginView'
import CardView from '@/views/CardView'
import DeckView from '@/views/DeckView'

const routes = [

  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: function () {
  //     return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  //   }
  // }
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashView
  },
  {
    path: '/flashcards',
    name: 'Flashcards',
    component: FlashCards
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/card/:did',
    name: 'Card',
    component: CardView
  },
  {
    path: '/deck/:did',
    name: 'Deck',
    component: DeckView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
