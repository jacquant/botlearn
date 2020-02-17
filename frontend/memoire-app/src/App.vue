<template>
  <v-app>
      <!-- ============================================================================================== ----
        ---- Navbar
        ---- ============================================================================================== -->
        <v-card
        >
         <v-app-bar
          :clipped-left="clipped"
          fixed
          app
        >
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

            <v-toolbar-title>My learning</v-toolbar-title>
          </v-app-bar>
          <v-navigation-drawer
              v-model="drawer"
              fixed
              :clipped="clipped"
              app
              >
              <v-list>
                  <div 
                  v-for="(item, i) in items"         
                  :key="i"
                  router
                  exact
                  >
                  <v-list-item 
                  v-if="(loggedIn && item.title !='Se connecter') || (!loggedIn && item.title !='Se déconnecter')"
                  :to="item.to"
                  @click="item.title =='Se déconnecter' ? logout() : false"
                  >
                      <v-list-item-action>
                      <v-icon >{{ item.icon }}</v-icon>
                      </v-list-item-action>
                      <v-list-item-content>
                      <v-list-item-title v-text="item.title"/>
                      </v-list-item-content>
                  </v-list-item>
                  </div>
              </v-list>
          </v-navigation-drawer>
        </v-card>
        <!-- ============================================================================================== ----
        ---- Page's content
        ---- ============================================================================================== -->
        <v-content class="mt-10">
          <router-view></router-view>
        </v-content>
    </v-app>
</template>

<script>
import store from './store/store';

export default {

  name: 'App',
  components: {

  },
  // ================================================================================================== ==
  // Data
  // ================================================================================================== ==
  data: () => ({
        clipped: false,
        drawer: false,
        fixed: false,
        items: [
            {
                icon: 'mdi-apps',
                title: 'Acceuil',
                to: '/'
            },
            {
                icon: 'mdi-chart-bubble',
                title: 'Inspire',
                to: '/reset'
            },
            {
                icon: 'mdi-forum',
                title: 'bot',
                to: '/bot'
            },
            {
                icon: 'mdi-login-variant',
                title: 'Se connecter',
                to: '/login'
            },
            {
                icon: 'mdi-logout-variant',
                title: 'Se déconnecter',
                to: null,
            }
            ]
    }),

    // ================================================================================================== ==
    // Computed
    // ================================================================================================== ==

    computed:{
        //Check if user is logged to display information differently
        loggedIn(){
            return store.getters.isConnected;
        }
    },

    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods:{
        logout(){
            store.commit("logout");
        }
    }
};
</script>
