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
                                                                    ({{printDate(new Date(sourcecode.submission_date.substring(0, 19)))}})
                            </v-toolbar-title>
                            <v-spacer />
                        </v-toolbar>
                        <v-card-text class="justify-center">
                            <vue-code-highlight language="python">{{sourcecode.code_input}}</vue-code-highlight>
                        </v-card-text>
                        <v-divider />
                        <v-card-text class="justify-center">
                            <v-flex>
                                <v-list-item>
                                    <v-list-item-content>
                                        <v-list-item-title v-for="{error} in sourcecode.errors"
                                                           :key="error.code">
                                            {{error.code + error.message}}
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
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
import {component as VueCodeHighlight} from "vue-code-highlight";

export default {
    // ================================================================================================== ==
    // Compents
    // ================================================================================================== ==
    components: {VueCodeHighlight},
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
        this.source.code.code_input = "a = 1\n b = 1\n c = 1U+0020\tprint (a+b+c)";
        console.log(this.sourcecode);
    },

    methods: {

        /**
         * Function to print the date correctly
         * @param {Date} date
         * @returns {String}
         * */
        printDate(date) {
            const monthNames = [
                "janvier",
                "février",
                "mars",
                "avril",
                "mai",
                "juin",
                "juillet",
                "août",
                "septembre",
                "octobre",
                "novembre",
                "décembre"
            ];

            let day = date.getDate();
            let monthIndex = date.getMonth();
            let year = date.getFullYear();
            let hour = date.getHours();
            let minute = date.getMinutes();
            let second = date.getSeconds();

            if (minute.toString().length === 1) {
                minute = "0" + minute;
            }

            return day + " " + monthNames[monthIndex] + " " + year + " à " + hour + ":" + minute + ":" + second + "";
        },
    },
};
</script>
