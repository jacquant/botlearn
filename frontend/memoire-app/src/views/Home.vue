<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-center">
        <img src="../assets/bot_image.png" height="250px" class="center" />
      </div>
      <v-card v-if="userInformation.eid !== null">
        <v-card-title class="headline">
          Salut {{ userInformation.first_name }} !
        </v-card-title>
        <v-card-text>
          <p>
            Bienvenue sur le site du bot de bac 1. Sur ce site tu retrouveras
            pas mal d'informations 😉.
          </p>

          <v-card raised>
            <v-app-bar dark flat color="green">
              <v-toolbar-title color="green" dark flat>
                Tes informations:
              </v-toolbar-title>
              <v-spacer />
              <v-icon size="40">
                mdi-account-card-details
              </v-icon>
            </v-app-bar>
            <v-card-text>
              <v-list-item v-for="(info, n) in userInformation" :key="n">
                <v-icon size="15">
                  mdi-checkbox-blank-circle
                </v-icon>
                <div v-if="n === 'mail'">Email : {{ info }}</div>
                <div v-else-if="n === 'first_name'">Prénom : {{ info }}</div>
                <div v-else-if="n === 'last_name'">Nom: {{ info }}</div>
                <div v-else>Eid: {{ info }}</div>
              </v-list-item>
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
  }
};
</script>
