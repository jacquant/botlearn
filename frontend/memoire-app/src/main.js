import Vue from "vue";
import router from "./system/router";
import App from "./App.vue";

//Plugins
import vuetify from "./plugins/vuetify";
import VueHtmlToPaper from "vue-html-to-paper";
import VuePrism from "vue-prism";
import "prismjs/themes/prism.css";

Vue.config.productionTip = false;
// eslint-disable-next-line no-unused-vars
const options = {
  name: "_blank",
  specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"]
};

Vue.use(VuePrism);
Vue.use(VueHtmlToPaper);

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount("#app");
