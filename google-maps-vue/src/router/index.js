// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import InstructionsPage from '../views/InstructionsPage.vue'
import AboutUsPage from '../views/AboutUsPage.vue'
import ContactUsPage from '../views/ContactUsPage.vue'
import Sitemap from '@/views/Sitemap.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/instructions', component: InstructionsPage },
  { path: '/about', component: AboutUsPage },
  { path: '/contact', component: ContactUsPage },
  { path: '/sitemap', component: Sitemap }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
