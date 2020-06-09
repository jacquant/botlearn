<template>
  <v-layout align-center column justify-center>
    <v-flex md6 sm8 xs12>
      <div class="text-center">
        <v-img class="center" aspect-ratio="1.3283" src="../assets/bot_image.png" alt="Image accueil Botlearn"></v-img>
      </div>
      <v-card v-if="userInformation.eid !== null">
        <v-card-title class="headline">
          Salut {{ userInformation.first_name }} !
        </v-card-title>
        <v-card-text>
          <p>
            Bienvenue sur le site du bot de bac 1. Sur ce site tu trouveras
            pas mal d'informations 😉.
          </p>

          <v-card raised>
            <v-app-bar color="green" dark flat>
              <v-toolbar-title color="green" dark flat>
                Tes informations:
              </v-toolbar-title>
              <v-spacer />
              <v-icon size="40">
                mdi-account-card-details
              </v-icon>
            </v-app-bar>
            <v-card-text>
              <v-list disabled>
                <v-list-item-group flat>
                  <v-list-item :key="n" v-for="(info, n) in userInformation">
                    <v-list-item-icon>
                      <v-icon>mdi-checkbox-blank-circle</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ getInformation(n, info) }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
              <hr />
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
    import store from "../store/store";

    export default {
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            userInformation: {
                mail: null,
                last_name: null,
                first_name: null,
                student: null,
                student_card: null,
                eid: null,
                is_staff: null
            },
            userMapping: {
                last_name: "Nom: ",
                first_name: "Prénom: ",
                mail: "E-mail: ",
                eid: "Eid: "
            }
        }),

        // ================================================================================================== ==
        // Mounted
        // ================================================================================================== ==
        mounted() {
            //Get User informations
            this.userInformation = store.state.userInformation;
            delete this.userInformation.is_staff;
            delete this.userInformation.student_card;
            delete this.userInformation.student;
        },
        methods: {

            getInformation(mapper, info) {
                return this.userMapping[mapper] + info;
            }

        }
    };
</script>
