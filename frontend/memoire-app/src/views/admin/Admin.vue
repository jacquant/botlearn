<template>
  <v-layout>
    <v-flex>
      <v-row>
        <!--List of exercices by TP-->
        <v-col offset="1" mb="6" lg="6" xl="6">
          <h1>Liste des exercices</h1>
          <v-card class="mx-auto mr-xs-10" max-width="100%">
            <v-text-field v-if="loading" color="success" loading disabled />
            <v-list v-else>
              <!--Loop for the sections-->
              <v-list-group
                v-for="info in tps"
                :key="info.id"
                prepend-icon=""
                value="true"
                sub-group
              >
                <template v-slot:activator>
                  <v-list-item-title>
                    <b>{{ info.name }}</b>
                  </v-list-item-title>
                </template>
                <v-list-item
                  v-for="exe in info.exercices"
                  :key="exe.id"
                  link
                  @click="getInfo(exe)"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-book</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title> {{ exe.name }}</v-list-item-title>
                  <v-btn
                    :href="
                      'https://memoire.jacquant.be/admin/exercises/exercise/' +
                        exe.id +
                        '/change/'
                    "
                    target="_blank"
                  >
                    <v-icon>mdi-lead-pencil</v-icon>
                  </v-btn>
                </v-list-item>
                <v-list-item
                  :href="
                    'https://memoire.jacquant.be/admin/exercises/exercise/add?id=' +
                      info.id
                  "
                  target="_blank"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-book-plus</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title style="color:red">
                    Ajouter un exercice
                  </v-list-item-title>
                </v-list-item>
                <v-divider />
              </v-list-group>
            </v-list>
          </v-card>
        </v-col>
        <!--Details for one exercice choosen-->
        <v-col offset="1">
          <h1>Informations</h1>
          <v-alert
            v-if="current_data == null"
            type="info"
            class="mx-auto mr-10"
          >
            Sélectionne un exercice pour en avoir un résumé.
          </v-alert>
          <v-card v-else class="mx-auto mr-10">
            <v-toolbar color="green" dark flat>
              <v-toolbar-title>{{ current_data.name }}</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <div style="font-weight:bold">
                    Nombre de soumissions totales:
                  </div>
                  {{current_data.total_sub}}
                </v-list-item>
                <v-list-item>
                  <div style="font-weight:bold">
                    Nombre de soumissions finales:
                  </div>
                  {{current_data.final_sub}}
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <v-btn
                  color="green"
                  class="white--text"
                  :href="'/administration/exercice?id=' + current_data.id"
                  target="_blank"
                >
                  Afficher l'exercice en détails
                </v-btn>
              </p>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!--Graph Part - Global view-->
      <v-row>
        <v-col>
          <v-divider />
          <v-card
            class="mx-auto text-center mt-10"
            color="white"
            max-width="800px"
          >
            <v-tabs
              v-model="current_tab"
              background-color="green"
              dark
              class="mb-5"
              show-arrows
              @change="changeData()"
            >
              <v-tab
                v-for="item in items"
                :key="item.tab"
                :value="item"
              >
                {{ item.tab }}
              </v-tab>
            </v-tabs>
            <v-tabs-items v-model="current_tab">
              <v-tab-item v-for="item in items" :key="item.tab" />
            </v-tabs-items>
            <v-card-text>
              <v-col class="d-flex" cols="12" sm="6">
                <v-select
                  :items="tps"
                  item-text="name"
                  item-value="exercices"
                  label="Choix du TP"
                  v-model="current_tp"
                  color="green"
                  outlined
                  @change="changeData()"
                ></v-select>
              </v-col>
              <GChart
                id="Chart"
                type="ColumnChart"
                :data="chartData"
                :options="chartOptions"
                :events="chartEvents"
                @ready="onChartReady"
                ref="gChart"
              />
            </v-card-text>

            <v-card-text>
              <div class="display-1">
                {{ title }}
                <v-btn icon href="https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes" target="_blank">
                  <v-icon>
                    mdi-information-outline
                  </v-icon>
                </v-btn>
              </div>
            </v-card-text>

            <v-divider />

            <v-card-actions class="justify-center">
              <v-btn block text @click="print(title, current_tp[0].session.name)">
                Imprimer graphe
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>
    import store from "../../store/store";
    import router from "../../system/router";
    import {GChart} from "vue-google-charts";
    import http from "../../system/http";
    import {tooltipGenerator} from "../../utils/graph";
    import {onChartReady, print} from "../../utils/print";

    export default {
        // ================================================================================================== ==
        // Components
        // ================================================================================================== ==
        components: {
            GChart
        },
        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({
            //List exercices et tps
            tps: [],

            current_tp: null,

            exercices: [],

            current_data: null,

            // Data for Tabs
            items: [
                {tab: "Soumissions finales", content: "finales"},
                {tab: "Soumissions totales", content: "totales"},
                {tab: "Nombre d'erreurs", content: "erreurs"},
                {tab: "Type d'erreurs", content: "types"},
            ],
            current_tab: null,

            //Data For Graph
            chartData: [],
            chartOptions: {
                colors: ["green"],
                legend: {position: "none"},
                tooltip: {
                    isHtml: true,
                    trigger: "selection"
                },
            },
            title: "Nombre de soumissions finales par exercice par TP",

            //loading
            loading: true,

            //chart in PNG
            png: "",

            //Handling Event for chart
            chartEvents: {
                select: () => {
                }
            },

            get_stats: {
                "number_submissions": 0,
                "errors": [
                    {
                        "counter": 0,
                        "submissions_list": [
                            0
                        ],
                        "code": ""
                    }
                ]
            }

        }),

        // ================================================================================================== ==
        // Created
        // ================================================================================================== ==
        async created() {

            //Redirect if user is not staff -> Call API to get information to be sure that localstorage wasn't change manually
            let is_staff = await http.get("user/get/", {
                headers: {Authorization: "Bearer " + store.state.accessToken}
            });

            if (!is_staff) {
                let new_json = store.state.userInformation;
                new_json["is_staff"] = false;
                localStorage.setItem("infoUser", JSON.stringify(new_json));
                await router.push("/");
            }

            //Get All Tps
            this.tps = (
                await http.get("sessions/", {
                    headers: {Authorization: "Bearer " + store.state.accessToken}
                })
            ).data;


            let exercices = [];
            for (const key in this.tps) {
                exercices = (
                    await http.get("exercises/?session=" + this.tps[key].id, {
                        headers: {Authorization: "Bearer " + store.state.accessToken}
                    })
                ).data;
                this.tps[key]["exercices"] = exercices;
                for (const exe in this.tps[key]["exercices"]) {

                    //Get all subsmissions
                    this.tps[key]["exercices"][exe]["total_sub"] = (await http.get("submissions/?&exercises=" + this.tps[key]["exercices"][exe].id, {
                            headers: {Authorization: "Bearer " + store.state.accessToken}
                        })
                    ).data.length;

                    //Get all final subsmissions
                    this.tps[key]["exercices"][exe]["final_sub"] = (await http.get("submissions/?&final=true&exercises=" + this.tps[key]["exercices"][exe].id, {
                            headers: {Authorization: "Bearer " + store.state.accessToken}
                        })
                    ).data.length;
                }

            }

            this.loading = false;
        },

        // ================================================================================================== ==
        // Methods
        // ================================================================================================== ==
        methods: {

            //Get details from an exercice
            async getInfo(data) {
                this.current_data = data;
            },

            //Get the data compared to the tab selectionned
            async changeData() {
                if (this.current_tp !== null) {

                    //Get All submissions for every exercice
                    if (this.items[this.current_tab].content === "totales") {
                        this.title = "Nombre de soumissions totales par exercice par TP";

                        this.chartData = [["Exercice", "Nombre de soumissions totales"]];
                        for (const exercice in this.current_tp) {
                            this.chartData.push([this.current_tp[exercice].name, (
                                await http.get("submissions/?&exercises=" + this.current_tp[exercice].id, {
                                    headers: {Authorization: "Bearer " + store.state.accessToken}
                                })
                            ).data.length]);
                        }

                        //Get All final submissions for every exercice
                    } else if (this.items[this.current_tab].content === "finales") {
                        this.title = "Nombre de soumissions finales par exercice par TP";

                        this.chartData = [["Exercice",
                            "Nombre de soumissions finales", {
                                type: "string",
                                role: "tooltip",
                                "p": {"html": true}
                            }]];
                        for (const exercice in this.current_tp) {
                            this.chartData.push([this.current_tp[exercice].name, (
                                await http.get("submissions/?&final=true&exercises=" + this.current_tp[exercice].id, {
                                    headers: {Authorization: "Bearer " + store.state.accessToken}
                                })
                            ).data.length, "<b>" + this.current_tp[exercice].name + "</b><br>Nombre de soumissions finales: " + 4 + "<br><a href=/solution?id=55 target='_blank'>voir exemples</a>"]);
                        }

                        //Get stats from students' errors by error
                    } else if (this.items[this.current_tab].content === "types") {
                        this.title = "Nombre d'erreurs par type par TP";

                        this.chartData = [["Numéro de l'erreur",
                            "Nombre de fois rencontrée", {
                                type: "string",
                                role: "tooltip",
                                "p": {"html": true}
                            }]];

                        this.get_stats = (await http.get("stats/errors_by_session/" + this.current_tp[0].session.id, {
                                headers: {Authorization: "Bearer " + store.state.accessToken}
                            })
                        ).data;

                        tooltipGenerator(this.get_stats.errors).forEach(tooltip => {
                            this.chartData.push(tooltip);
                        });

                        //Get stats from students' errors by exercice
                    } else {
                        this.title = "Nombre d'erreurs par exercice par TP";

                        this.chartData = [["Exercice", "Nombre d'erreurs par exercice"]];
                        for (const exercice in this.current_tp) {
                            let submissions = (await http.get("submissions/?&exercises=" + this.current_tp[exercice].id, {
                                    headers: {Authorization: "Bearer " + store.state.accessToken}
                                })
                            ).data;

                            let total_errors = 0;
                            for (const nb in submissions) {
                                total_errors += submissions[nb].errors.reduce((acc, value) => value.counter + acc, 0);
                            }
                            this.chartData.push([this.current_tp[exercice].name, total_errors]);
                        }
                    }
                }
            },

            //Transform Chart to PNG
            onChartReady,

            //Print the Graph
            print
        }
    };
</script>
