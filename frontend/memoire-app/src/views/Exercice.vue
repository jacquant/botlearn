<template>
  <v-layout>
    <v-flex>
      <v-row>
        <!--Détails des exerices-->
        <v-col class="ml-10 mr-10">
          <h1>Détails de l'exercice</h1>
          <v-card class="mx-auto">
            <v-toolbar color="green" dark flat>
              <v-toolbar-title>{{ exercise.name }}</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-list dense>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title style="font-weight:bold">Consignes:</v-list-item-title>
                    {{ exercise.instruction }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title style="font-weight:bold">
                    Difficulté (1 à 4): {{ exercise.difficulty.name + " ("+exercise.difficulty.number+")" }}
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title style="font-weight:bold" v-if="exercise.tags.length > 1">Tags:
                    </v-list-item-title>
                    <v-list-item-title style="font-weight:bold" v-else>Tag:</v-list-item-title>
                    <v-list-item-group>
                      <v-list-item v-for="tag in exercise.tags" :key="tag.name" dense>
                        <v-list-item-content>
                          {{ tag.name }}
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title style="font-weight:bold">
                    Nombre de soumissions: {{ all_items.length }}
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title style="font-weight:bold">
                    Nombre de soumissions finales: {{ items.length }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <v-btn
                  color="green"
                  class="white--text"
                  :href="
                    'https://memoire.jacquant.be/admin/exercises/exercise/' +
                      exercise.id +
                      '/change/'
                  "
                  target="_blank"
                >
                  Modifier
                </v-btn>
              </p>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-divider />
      <!--Partie statistique des solutions des étudiants-->
      <v-row class="mr-10 ml-10">
        <v-container fluid>
          <h1>Statistiques de l'exercice
            <v-btn icon href="https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes"
                   target="_blank">
              <v-icon>
                mdi-information-outline
              </v-icon>
            </v-btn>
          </h1>
          <v-card>
            <GChart
              id="Chart"
              type="ColumnChart"
              :data="chartData"
              :options="chartOptions"
              @ready="onChartReady"
            />
            <v-card-actions class="justify-center">
              <v-btn block text @click="print()">
                Imprimer graphe
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-container>
      </v-row>

      <v-divider />
      <!--Réponse des étudiants-->
      <h1 class="mr-10 ml-10">
        Solutions des étudiants
      </h1>
      <v-row class="mr-10 ml-10">
        <v-container fluid>
          <v-data-iterator
            :items="items"
            :items-per-page.sync="itemsPerPage"
            :page="page"
            :search="search"
            :sort-desc="sortDesc"
            hide-default-footer
          >
            <!--Partie Filtre-->
            <template v-slot:header>
              <v-toolbar dark color="green darken-3" class="mb-1">
                <v-text-field
                  v-model="search"
                  clearable
                  flat
                  solo-inverted
                  hide-details
                  prepend-inner-icon="mdi-magnify"
                  label="Filtrer par nom"
                />
                <template v-if="$vuetify.breakpoint.mdAndUp">
                  <v-spacer />
                  <v-select
                    v-model="sortBy"
                    flat
                    hide-details
                    :items="keys"
                    prepend-inner-icon="mdi-magnify"
                    label="Trier par"
                    @change="filtering()"
                  />
                </template>
                <v-spacer />
                <v-switch class="d-none d-sm-flex mt-5" label="Finale" v-model="switch1"
                          @change="modify()"></v-switch>
                <v-spacer />
                <v-btn
                  class="d-none d-sm-flex"
                  color="#9c6013"
                  depressed
                  medium
                  @click="
                    search = '';
                    sortBy = 'Le plus récent';
                    filtering();
                  "
                >
                  Réinitialiser les filtres
                </v-btn>
                <v-btn
                  icon
                  class="d-flex d-sm-none"
                  @click="
                    search = '';
                    sortBy = 'Le plus récent';
                    filtering();
                  "
                >
                  <v-icon color="#9c6013">
                    mdi-eraser
                  </v-icon>
                </v-btn>
              </v-toolbar>
            </template>
            <!--Partie Affichage des solutions-->
            <template v-slot:default="props">
              <v-row>
                <v-col
                  v-for="item in props.items"
                  :key="item.id"
                  cols="12"
                  sm="6"
                  md="4"
                  lg="3"
                >
                  <v-card color="green">
                    <v-card-title color="green" class="subheading">
                      {{ item.name }}
                    </v-card-title>
                    <v-card-subtitle>
                      {{item.date[1]}}
                    </v-card-subtitle>

                    <v-divider />
                    <v-list dense>
                      <v-list-item>
                        <v-list-item-content>Nombre d'erreurs:
                        </v-list-item-content>
                        <v-list-item-content>{{ item.errors }}
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                    <v-divider />
                    <v-card-actions class="d-flex align-center justify-center">
                      <p class="ma-0">
                        <v-btn color="#9c6013" class="white--text"
                               :href='"/solution?id="+item.id' target="_blank"
                               v-if="item.code.length < 70">
                          Afficher
                        </v-btn>
                        <v-btn color="#9c6013" class="white--text"
                               :href='"/solution?id="+item.id' v-else>
                          Afficher la suite
                        </v-btn>
                      </p>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </template>

            <template v-slot:footer>
              <v-row class="mt-2" align="center" justify="center">
                <span class="grey--text">Nombre de solutions par page</span>
                <v-menu offset-y>
                  <template v-slot:activator="{ on }">
                    <v-btn dark text color="#0f5920" class="ml-2" v-on="on">
                      {{ itemsPerPage }}
                      <v-icon>mdi-chevron-down</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      v-for="(number, index) in itemsPerPageArray"
                      :key="index"
                      @click="updateItemsPerPage(number)"
                    >
                      <v-list-item-title>{{ number }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>

                <v-spacer />

                <span
                  class="mr-4
                            grey--text"
                >
                  Page {{ page }} sur {{ numberOfPages }}
                </span>
                <v-btn
                  fab
                  dark
                  color="green darken-3"
                  class="mr-1"
                  @click="formerPage"
                >
                  <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <v-btn
                  fab
                  dark
                  color="green darken-3"
                  class="ml-1"
                  @click="nextPage"
                >
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-row>
            </template>
          </v-data-iterator>
        </v-container>
      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>
    import http from "../system/http";
    import store from "../store/store";
    import {printDate} from "../utils/date";
    import {onChartReady, print} from "../utils/print";
    import {tooltipGenerator} from "../utils/graph";
    //import { component as VueCodeHighlight } from 'vue-code-highlight';

    export default {
        // ================================================================================================== ==
        // Components
        // ================================================================================================== ==
        components: {},
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            //Detail exercise
            exercise: {
                "id": 0,
                "difficulty": {
                    "id": 0,
                    "number": 0,
                    "name": ""
                },
                "tags": [
                    {
                        "id": 0,
                        "name": ""
                    },
                ],
                "session": {
                    "id": 0,
                    "in_charge_persons": [
                        {
                            "mail": "",
                            "last_name": "",
                            "first_name": ""
                        }
                    ],
                    "target": {
                        "id": 0,
                        "name": ""
                    },
                    "name": "",
                    "date": "",
                    "visibility": true,
                    "activated": true
                },
                "section": {
                    "id": 0,
                    "academic_year": "",
                    "name": "",
                    "number": 0,
                    "parent": 0
                },
                "author": {
                    "mail": "",
                    "last_name": "",
                    "first_name": ""
                },
                "name": "",
                "due_date": "",
                "instruction": "",
                "project_files": "",
                "docker_image": 0,
                "requirements": []
            },

            //Stats de l'exercice
            chartData: [["Code de l'erreur",
                "Nombre de fois rencontrée",
                {
                    role: "style"
                },
                {
                    type: "string",
                    role: "tooltip",
                    "p": {"html": true}
                }]],
            chartOptions: {
                colors: ["green"],
                legend: {position: "none"},
                tooltip: {
                    isHtml: true,
                    trigger: "selection"
                },
            },

            //chart in PNG
            png: "",

            //Solutions des étudiants _ Data
            itemsPerPageArray: [20, 40, 60],
            search: "",
            filter: {},
            switch1: true,
            sortDesc: false,
            page: 1,
            itemsPerPage: 20,
            sortBy: "Le plus récent",
            keys: [
                "Le plus ancien",
                "Le plus récent",
                "Le plus d'erreurs",
                "Le moins d'erreurs"
            ],
            items: [{
                id: 0,
                name: "Exemple structure",
                date: [Date(), ""],
                errors: 0,
                code: ""
            }],
            all_items: [{
                id: 0,
                name: "Exemple structure",
                date: [new Date("0-0-0"), ""],
                errors: 0,
                code: ""
            }],
            current_items: [],
            get_stats: {
                "number_submissions": 0,
                "errors": [
                    {
                        "counter": 0,
                        "message": "",
                        "type": "",
                        "submissions_list": [
                            0
                        ],
                        "code": ""
                    }
                ]
            }

        }),

        // ================================================================================================== ==
        // Computed
        // ================================================================================================== ==
        computed: {
            //Manage the pagination
            numberOfPages() {
                return Math.ceil(this.items.length / this.itemsPerPage);
            },
            filteredKeys() {
                return this.keys.filter(key => key !== `Name`);
            }
        },

        // ================================================================================================== ==
        // Created
        // ================================================================================================== ==
        created: async function () {
            //Redirect if user is not staff -> Call API to get information to be sure that localstorage wasn't change manually
            const is_staff = await http.get("user/get/", {
                headers: {Authorization: "Bearer " + store.state.accessToken}
            });

            if (!is_staff) {
                let new_json = store.state.userInformation;
                new_json["is_staff"] = false;
                localStorage.setItem("infoUser", JSON.stringify(new_json));
                await this.$router.push("/");
            }

            //Redirect if there is no id for an exercise
            let id = null;
            if (this.$route.query.id === undefined || this.$route.query.id === "") {
                await this.$router.push("/administration");
            } else {
                id = this.$route.query.id;
            }

            //Get Details exercise
            this.exercise = (
                await http.get("exercises/" + id, {
                    headers: {Authorization: "Bearer " + store.state.accessToken}
                })
            ).data;

            //Get All final submissions from exercises
            this.submissions = (
                await http.get("submissions/?&exercises=" + this.exercise.id, {
                    headers: {Authorization: "Bearer " + store.state.accessToken}
                })
            ).data;
            //Format display
            this.items = [];
            this.all_items = [];
            this.submissions.forEach(submission => {
                const date = new Date(submission.submission_date.substring(0, 19));
                const item = {
                    id: submission.id,
                    name: submission.author.last_name + " " + submission.author.first_name,
                    date: [date, printDate(date)],
                    errors: submission.errors.reduce((a, b) => a + b.counter, 0),
                    code: submission.code_input
                };
                if (submission.final) {
                    this.items.push(item);
                }
                this.all_items.push(item);
            });

            //Get Stats

            this.get_stats = (await http.get("stats/errors_by_exercise/" + id, {
                    headers: {Authorization: "Bearer " + store.state.accessToken}
                })
            ).data;

            tooltipGenerator(this.get_stats.errors).forEach(tooltip => {
                this.chartData.push(tooltip);
            });
            //Filtering Exercises:
            this.filtering();

        },

        // ================================================================================================== ==
        // Methods
        // ================================================================================================== ==
        methods: {
            //Methods to manage the pagination
            nextPage() {
                if (this.page + 1 <= this.numberOfPages) this.page += 1;
            },
            formerPage() {
                if (this.page - 1 >= 1) this.page -= 1;
            },
            updateItemsPerPage(number) {
                this.itemsPerPage = number;
            },
            //Filtering by date or by errors
            filtering() {
                if (this.sortBy === "Le plus récent") {
                    this.items = this.items.slice().sort((a, b) => b.date[0] - a.date[0]);
                } else if (this.sortBy === "Le plus ancien") {
                    this.items = this.items.slice().sort((a, b) => a.date[0] - b.date[0]);
                } else if (this.sortBy === "Le plus d'erreurs") {
                    this.items = this.items.slice().sort((a, b) => b.errors - a.errors);
                } else {
                    this.items = this.items.slice().sort((a, b) => a.errors - b.errors);
                }
            },

            printDate,

            /**
             * Display all submissions
             */
            modify() {
                if (this.switch1) {
                    this.items = this.previous_items;
                    this.previous_items = this.items;
                } else {
                    this.previous_items = this.items;
                    this.items = this.all_items;
                }

            },


            //Transform Chart to PNG
            onChartReady,

            //Print the Graph
            print
        }
    };
</script>
