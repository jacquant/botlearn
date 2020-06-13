<template>
  <v-app>
    <!-- ============================================================================================== ----
      ---- Navbar
      ---- ============================================================================================== -->
    <v-card>
      <v-app-bar :clipped-left="clipped" fixed app>
        <v-app-bar-nav-icon @click="drawer = !drawer" />

        <v-toolbar-title>Botlearn</v-toolbar-title>

        <v-spacer />
        <v-btn
          v-if="admin"
          color="red accent-1"
          class="ma-2"
          href="/admin/bot" target="_blank"
        >
          Paramétrer le ChatBot
        </v-btn>

        <v-btn
          v-if="admin"
          color="red"
          href="/administration"
          class="ma-0 font-weight-bold"
        >
          Administrer
        </v-btn>
        <v-btn icon href="/administration" class="d-flex d-sm-none">
          <v-icon color="red">
            mdi-border-color
          </v-icon>
        </v-btn>
      </v-app-bar>
      <v-navigation-drawer v-model="drawer" fixed :clipped="clipped" app>
        <v-list>
          <div v-for="(item, i) in items" :key="i" router exact>
            <v-list-item
              v-if="
                (loggedIn &&
                  item.title !== 'Se connecter' &&
                  item.title !== 'S\'inscrire') ||
                  (!loggedIn && item.title !== 'Se déconnecter')
              "
              :to="item.to"
              @click="item.title === 'Se déconnecter' ? logout() : false"
            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-text="item.title" />
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
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
    import store from "./store/store";

    export default {
        name: "App",
        components: {},
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            clipped: false,
            drawer: false,
            fixed: false,
            items: [
                {
                    icon: "mdi-apps",
                    title: "Accueil",
                    to: "/"
                },
                {
                    icon: "mdi-login-variant",
                    title: "Se connecter",
                    to: "/login"
                },
                {
                    icon: "mdi-account-edit",
                    title: "S'inscrire",
                    to: "/register"
                },
                {
                    icon: "mdi-logout-variant",
                    title: "Se déconnecter",
                    to: null,
                },
            ]
        }),


        // ================================================================================================== ==
        // Computed
        // ================================================================================================== =

        computed: {
            //Check if user is logged to display information differently
            loggedIn() {
                return store.getters.isConnected;
            },
            //Check if a user is in the staff
            admin() {
                return store.getters.isStaff;
            },
        },

        // ================================================================================================== ==
        // Methods
        // ================================================================================================== ==
        methods: {
            logout() {
                store.commit("logout");
            }
        }
    };
</script>
