<template>
  <v-layout>
    <v-flex>
      <v-row class="mr-10 ml-10">
        <!--Détails des exerices-->
        <v-col offset="1" offset-sm="3" cols="10" sm="6">
          <v-card class="mx-auto">
            <v-toolbar color="green" dark flat>
              <v-toolbar-title>Ma solution</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-flex>
<vue-code-highlight>
{{sourcecode}}
</vue-code-highlight>
              </v-flex>
            </v-card-text>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <v-btn color="green" class="white--text">
                  Modifier
                </v-btn>
              </p>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!--Partie FeedBack-->
      <v-row>
        <v-col class="ml-10 mr-10">
          <v-card>
            <v-overlay
            :absolute="true"
            :opacity="0.70"
            :value="true"
            >
            <h3>Disponible plus tard</h3>
          </v-overlay>
            <v-card-title class="red lighten-2">
              <v-icon dark size="42" class="mr-4">
                mdi-pencil
              </v-icon>
              <h2 class="display-1 white--text font-weight-light">
                Donner un feedback
              </h2>
            </v-card-title>
            <v-container>
              <v-row>
                <v-col>
                  <v-textarea v-model="feedback" color="teal">
                    <template v-slot:label>
                      <div>
                        FeedBack
                      </div>
                    </template>
                  </v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
          <v-timeline :dense="$vuetify.breakpoint.smAndDown">
            <v-overlay
            :absolute="true"
            :opacity="0.70"
            :value="true"
            >
          </v-overlay>
            <v-timeline-item color="cyan lighten-2" fill-dot left>
              <v-card>
                <v-card-title class="cyan lighten-2">
                  <v-icon dark size="42" class="mr-4">
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack du Bot
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus.
                      Commune scaevola imperdiet nec ut, sed euismod convenire
                      principes at. Est et nobis iisque percipit.
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-timeline-item>

            <v-timeline-item color="green lighten-1" fill-dot right>
              <v-card>
                <v-card-title class="green lighten-1">
                  <v-icon class="mr-4" dark size="42">
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack Assistant
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus.
                      Commune scaevola imperdiet nec ut, sed euismod convenire
                      principes at. Est et nobis iisque percipit, an vim zril
                      disputando voluptatibus, vix an salutandi sententiae.
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-timeline-item>

            <v-timeline-item color="cyan lighten-2" fill-dot left>
              <v-card>
                <v-card-title class="cyan lighten-2">
                  <v-icon dark size="42" class="mr-4">
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack du Bot
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus.
                      Commune scaevola imperdiet nec ut, sed euismod convenire
                      principes at. Est et nobis iisque percipit.
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </v-col>
      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>
import http from "../system/http";
import store from "../store/store";
import { component as VueCodeHighlight } from 'vue-code-highlight';

export default {
  // ================================================================================================== ==
  // Compents
  // ================================================================================================== ==
  components: {VueCodeHighlight},
  // ================================================================================================== ==
  // Data
  // ================================================================================================== ==
  data: () => ({
    sourcecode: "",

    feedback: "",
  }),

  // ================================================================================================== ==
  // Mounted
  // ================================================================================================== ==
  mounted() {
  },

  // ================================================================================================== ==
  // Created
  // ================================================================================================== ==
  async created() {
    //Redirect if there is no id for a solution
    let id = null;
    if (this.$route.query.id === undefined || this.$route.query.id === "") {
      await this.$router.push("/");
    } else {
      id = this.$route.query.id;
    }

    this.sourcecode = (
       await http.get("submissions/" + id, {
        headers: { Authorization: "Bearer " + store.state.accessToken }
      })
    ).data.code_input
  },

  methods: {},
};
</script>
