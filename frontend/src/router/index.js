import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/hotels', name: 'Hotels', component: () => import('../views/HotelManage.vue') },
  { path: '/platforms', name: 'Platforms', component: () => import('../views/PlatformManage.vue') },
  { path: '/sales', name: 'Sales', component: () => import('../views/SalesData.vue') },
  { path: '/expenses', name: 'Expenses', component: () => import('../views/ExpenseManage.vue') },
  { path: '/reconciliation', name: 'Reconciliation', component: () => import('../views/Reconciliation.vue') },
  { path: '/reports', name: 'Reports', component: () => import('../views/ReportView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
