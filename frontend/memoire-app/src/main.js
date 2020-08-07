import Vue from "vue";
import router from "./system/router";
import App from "./App.vue";
//Plugins
import vuetify from "./plugins/vuetify";
import VueGoogleCharts from "vue-google-charts";
import Vuelidate from "vuelidate/src";
import VueHtmlToPaper from "vue-html-to-paper";
import VuePrism from "vue-prism";
import "vue-code-highlight/themes/prism.css";
import "prism-es6/components/prism-python";

Vue.use(Vuelidate);

Vue.use(VueGoogleCharts);

Vue.use(VueHtmlToPaper);

Vue.use(VuePrism);

Vue.config.productionTip = false;
// eslint-disable-next-line no-unused-vars
const options = {
    name: "_blank",
    specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"]
};


new Vue({
    vuetify,
    router,
    render: h => h(App)
}).$mount("#app");
