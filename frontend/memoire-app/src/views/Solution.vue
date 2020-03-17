<template>
  <v-layout>
    <v-flex>
      <v-row>
        <!--Détails des exerices-->
        <v-col
          offset="1"
          offset-sm="3"
          cols="10"
          sm="6"
        >
          <v-card
            class="mx-auto"
          >
            <v-toolbar
              color="green"
              dark
              flat
            >
              <v-toolbar-title>Ma solution</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-flex>
                <pre style="text-align:center">
                    <code class="language-python">
                        {{ sourcecode }}
                    </code>
                </pre>
              </v-flex>
            </v-card-text>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <v-btn
                  color="green"
                  class="white--text"
                >
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
          <v-timeline :dense="$vuetify.breakpoint.smAndDown">
            <v-timeline-item
              color="cyan lighten-2"
              fill-dot
              left
            >
              <v-card>
                <v-card-title class="cyan lighten-2">
                  <v-icon
                    dark
                    size="42"
                    class="mr-4"
                  >
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack du Bot
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus. Commune scaevola imperdiet nec ut, sed euismod
                      convenire principes at. Est et nobis iisque percipit.
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-timeline-item>

            <v-timeline-item
              color="green lighten-1"
              fill-dot
              right
            >
              <v-card>
                <v-card-title class="green lighten-1">
                  <v-icon
                    class="mr-4"
                    dark
                    size="42"
                  >
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack Assistant
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus. Commune scaevola imperdiet nec ut, sed euismod
                      convenire principes at. Est et nobis iisque percipit, an vim zril disputando voluptatibus, vix an
                      salutandi sententiae.
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-timeline-item>

            <v-timeline-item
              color="cyan lighten-2"
              fill-dot
              left
            >
              <v-card>
                <v-card-title class="cyan lighten-2">
                  <v-icon
                    dark
                    size="42"
                    class="mr-4"
                  >
                    mdi-information-outline
                  </v-icon>
                  <h2 class="display-1 white--text font-weight-light">
                    FeedBack du Bot
                  </h2>
                </v-card-title>
                <v-container>
                  <v-row>
                    <v-col>
                      Lorem ipsum dolor sit amet, no nam oblique veritus. Commune scaevola imperdiet nec ut, sed euismod
                      convenire principes at. Est et nobis iisque percipit.
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
    //import python_code from "../static/python/exe.py"

    export default {

        // ================================================================================================== ==
        // Compents
        // ================================================================================================== ==
        components: {},
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            sourcecode: `my_var = 8

if(my_var < 10):
    print("Hello World")
else:
    print("It\'s not working ! ")


my_tab = [1,2,4,8,16,32,64]

for i in my_tab:
    print(i)`

        }),

        // ================================================================================================== ==
        // Mounted
        // ================================================================================================== ==
        mounted() {
            //Render the HighLight for the code
            Prism.highlightAll();
        },

        methods: {}
    };
</script>