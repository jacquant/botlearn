import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store'

import Home from '../views/Home.vue'
import Bot from '../views/Bot.vue'
import Login from '../views/Login.vue'
import Reset from '../views/Reset.vue'
import Register from '../views/Register.vue'
import Admin from '../views/Admin.vue'


Vue.use(Router)

/**
 * Define a variable to redirect if user is not logged in
 * @private
 * @returns {null}
 */
const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isConnected) {
    next()
    return
  }
  next('/')
}

/**
 * Define a variable to redirect if user is logged in
 * @private
 * @returns {null}
 */
const ifAuthenticated = (to, from, next) => {
  if (store.getters.isConnected) {
    next()
    return
  }
  next('/login')
}

let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/reset',
      name: 'reset',
      component: Reset,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/bot',
      name: 'bot',
      component: Bot,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/administration',
      name: 'admin',
      component: Admin,
      beforeEnter: ifAuthenticated
    },
    { path: "*", 
      redirect: "/" 
    }
  ]
})

export default router