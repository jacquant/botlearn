import Vue from 'vue'
import Router from 'vue-router'
import Bot from "../views/Bot.vue"
import Login from "../views/Login.vue"

Vue.use(Router)


let router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
      {
        path: '/bot',
        name: 'Bot',
        component: Bot,
      },
      {
        path: '/login',
        name: 'login',
        component: Login,
      },
      { 
        path: "*", 
        redirect: "/bot" 
        }
    ]
})

export default router