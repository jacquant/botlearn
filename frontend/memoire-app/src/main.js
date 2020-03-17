import Vue from "vue";
import router from "./system/router";
import App from "./App.vue";

//Plugins
import vuetify from "./plugins/vuetify";
import VueHtmlToPaper from "vue-html-to-paper";
//import Prism from 'prismjs';

Vue.config.productionTip = false;

const options = {
    name: "_blank",
    specs: [
        "fullscreen=yes",
        "titlebar=yes",
        "scrollbars=yes"
    ]
};

//Vue.use(Prism);
Vue.use(VueHtmlToPaper);


new Vue({
    vuetify,
    router,
    render: h => h(App)
}).$mount("#app");
