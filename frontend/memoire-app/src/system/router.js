import Vue from "vue";
import Router from "vue-router";
import store from "../store/store";

//Login Parts
import Login from "../views/Login.vue";
import Reset from "../views/Reset.vue";
import Register from "../views/Register.vue";

//General Parts
import Home from "../views/Home.vue";

//Students parts
import AllSolutions from "../views/AllSolutions.vue";
import Solution from "../views/Solution.vue";

//Admin Parts
import Admin from "../views/Admin.vue";
import Exercice from "../views/Exercice.vue";

Vue.use(Router);

/**
 * Define a variable to redirect if user is not logged in
 * @private
 * @returns {null}
 */
const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isConnected) {
    next();
    return;
  }
  next("/");
};

/**
 * Define a variable to redirect if user is logged in
 * @private
 * @returns {null}
 */
const ifAuthenticated = (to, from, next) => {
  if (store.getters.isConnected) {
    next();
    return;
  }
  next("/login");
};

let router = new Router({
  mode: "history",
  // eslint-disable-next-line no-undef
  base: process.env.BASE_URL,
  routes: [
    //Login Parts
    {
      path: "/register",
      name: "register",
      component: Register,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/reset",
      name: "reset",
      component: Reset,
      beforeEnter: ifNotAuthenticated
    },

    //General Parts
    {
      path: "/",
      name: "home",
      component: Home,
      beforeEnter: ifAuthenticated
    },

    //Students Parts
    {
      path: "/mysolutions",
      name: "allsolution",
      component: AllSolutions,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/solution",
      name: "solution",
      component: Solution,
      beforeEnter: ifAuthenticated
    },

    //Admin Parts
    {
      path: "/administration",
      name: "admin",
      component: Admin,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/administration/exercice",
      name: "exercice",
      component: Exercice,
      beforeEnter: ifAuthenticated
    },
    { path: "*", redirect: "/" }
  ]
});

export default router;
