<template>
  <v-layout>
    <v-flex>
      <v-row class="mr-10 ml-10">
        <!--Détails des exerices-->
        <v-col offset="1" offset-sm="2" cols="10" sm="8">
          <v-card class="mx-auto justify-center" v-if="sourcecode.id !== 0">
            <v-toolbar color="green" dark flat>
              <v-toolbar-title class="justify-center">{{sourcecode.author.last_name}}
                                                      {{sourcecode.author.first_name}}
                                                      -
                                                      ({{printDate(new Date(sourcecode.submission_date.substring(0,
                                                      19)))}})
              </v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text class="justify-center">
              <pre class="language-python"><code v-text="sourcecode.code_input" class="no-before"></code></pre>
            </v-card-text>
            <v-divider />
            <v-card-text class="justify-center">
              <v-flex>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title v-for="{error} in sourcecode.errors"
                                       :key="error.code">
                      {{error.code + ": " + error.message}}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-flex>
            </v-card-text>
            <v-divider />
          </v-card>
        </v-col>
      </v-row>

      <!--Partie FeedBack-->
<!--      <Feedback></Feedback>-->
    </v-flex>
  </v-layout>
</template>

<script>
    import http from "../system/http";
    import {printDate} from "../utils/date";
    import store from "../store/store";
    //import Feedback from "../components/Feedback";

    export default {
        // ================================================================================================== ==
        // Compents
        // ================================================================================================== ==
        components: {
        //    Feedback
        },
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            sourcecode: {
                "id": 0,
                "author": {
                    "mail": "",
                    "last_name": "",
                    "first_name": ""
                },
                "errors": [{
                    "counter": 0,
                    "error": {
                        "id": 0,
                        "code": "",
                        "message": "",
                        "type_error": ""
                    }
                }],
                "submission_date": "",
                "code_input": "",
                "not_executed": false,
                "code_output": {
                    "stderr": "",
                    "stdout": "",
                    "timeout": false,
                    "duration": 0,
                    "exit_code": 0,
                    "oom_killed": false,
                    "lint_results": []
                },
                "final": false,
                "exercise": 0
            },

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
                    headers: {Authorization: "Bearer " + store.state.accessToken}
                })
            ).data;
        },

        methods: {

            printDate,
        },
    };
</script>
<style>
  .no-before::before{
    display: none;
    background: #272822;
  }
</style>
