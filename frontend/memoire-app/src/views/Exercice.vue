<template>
  <v-layout>
    <v-flex>
      <v-row>
        <!--Détails des exerices-->
        <v-col class="ml-10 mr-10">
          <h1>Détails de l'exerice</h1>
          <v-card class="mx-auto">
            <v-toolbar color="green" dark flat>
              <v-toolbar-title>{{ exercice.name }}</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <div style="font-weight:bold">
                    Consigne
                  </div>
                  : {{ exercice.instruction }}
                </v-list-item>
                <v-list-item>
                  <div style="font-weight:bold">
                    Difficulté (1 à 4)
                  </div>
                  : {{ exercice.difficulty.name }}
                </v-list-item>
                <v-list-item v-for="tag in exercice.tags" :key="tag">
                  <div style="font-weight:bold">
                    Tag: 
                  </div>
                   {{ tag.name }}
                </v-list-item>
                <v-list-item>
                  <div style="font-weight:bold">
                    Nombre de soumissions
                  </div>
                  : 120
                </v-list-item>
                <v-list-item>
                  Nombre de soumissions distinctes: 71
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
                    'http://localhost:8080/admin/exercises/exercise/' +
                      exercice.id +
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
          <h1>Statistique de l'exercice</h1>
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
                  <v-card>
                    <v-toolbar color="green" dark flat>
                      <v-card-title class="subheading">
                        {{ item.name }}
                      </v-card-title>
                    </v-toolbar>

                    <v-divider />
                    <v-list dense>
                      <v-list-item>
                        <v-list-item-content>Date:</v-list-item-content>
                        <v-list-item-content>{{
                          printDate(item.date)
                        }}</v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content
                          >Nombre d'erreurs:</v-list-item-content
                        >
                        <v-list-item-content>{{
                          item.erreurs
                        }}</v-list-item-content>
                      </v-list-item>
                    </v-list>
                    <v-divider />
                    <v-card-actions class="d-flex align-center justify-center">
                      <p class="ma-0">
                        <v-btn color="green" class="white--text">
                          Afficher
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
import { GChart } from "vue-google-charts";

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
    //Detail exercice
    exercice: {
      id: 0,
      difficulty: {
        id: 0,
        number: 0,
        name: "string"
      },
      tags: [
        {
          id: 0,
          name: "string"
        }
      ],
      session: {
        id: 0,
        in_charge_persons: [
          {
            mail: "user@example.com",
            last_name: "string",
            first_name: "string"
          }
        ],
        target: {
          id: 0,
          name: "string"
        },
        name: "string",
        date: "2020-03-15T12:42:53.355Z",
        visibility: true,
        activated: true
      },
      section: {
        id: 0,
        academic_year: "string",
        name: "string",
        number: 0,
        parent: 0
      },
      author: {
        mail: "user@example.com",
        last_name: "string",
        first_name: "string"
      },
      name: "string",
      due_date: "2020-03-15T12:42:53.355Z",
      instruction: "string",
      project_files: "string",
      docker_image: 0,
      requirements: [0]
    },

    //Stats de l'exercice
    chartData: [
      ["Year", "Soumissions"],
      ["2014", 1000],
      ["2015", 1678],
      ["2016", 660],
      ["2017", 1030]
    ],
    chartOptions: {
      colors: ["green"],
      legend: { position: "none" }
    },

    //chart in PNG
    png: "",

    //Solutions des étudiants _ Data
    itemsPerPageArray: [4, 12, 24],
    search: "",
    filter: {},
    sortDesc: false,
    page: 1,
    itemsPerPage: 4,
    sortBy: "Le plus récent",
    keys: [
      "Le plus ancien",
      "Le plus récent",
      "Le plus d'erreurs",
      "Le moins d'erreurs"
    ],
    items: [
      {
        id: 1,
        name: "Dalla Valle Maxime",
        date: new Date("2020-02-24"),
        erreurs: 6
      },
      {
        id: 2,
        name: "Jacques Antoine",
        date: new Date("2020-02-25"),
        erreurs: 4
      },
      {
        id: 3,
        name: "Bonird Marc",
        date: new Date("2020-01-25"),
        erreurs: 1
      },
      {
        id: 4,
        name: "Constant Léopold",
        date: new Date("2020-02-01"),
        erreurs: 2
      },
      {
        id: 5,
        name: "Tripod John",
        date: new Date("2019-01-10"),
        erreurs: 9
      },
      {
        id: 6,
        name: "Tulit Marco",
        date: new Date("2020-01-24"),
        erreurs: 35
      }
    ]
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
  async created() {
    //Redirect if user is not staff -> Call API to get information to be sure that localstorage wasn't change manually
    const is_staff = await http.get("user/get/", {
      headers: { Authorization: "Bearer " + store.state.accessToken }
    });

    if (!is_staff) {
      let new_json = store.state.userInformation;
      new_json["is_staff"] = false;
      localStorage.setItem("infoUser", JSON.stringify(new_json));
      await this.$router.push("/");
    }

    //Redirect if there is no id for an exercice
    let id = null;
    if (this.$route.query.id === undefined || this.$route.query.id === "") {
      await this.$router.push("/administration");
    } else {
      id = this.$route.query.id;
    }

    //Get Details exercice
    this.exercice = (
      await http.get("exercises/" + id, {
        headers: { Authorization: "Bearer " + store.state.accessToken }
      })
    ).data;

    //Get Solutions
    //Waiting API

    //Filtering Exerice:
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
      if (this.sortBy.includes("récent")) {
        this.items = this.items.slice().sort((a, b) => b.date - a.date);
      } else if (this.sortBy.includes("ancien")) {
        this.items = this.items.slice().sort((a, b) => a.date - b.date);
      } else if (this.sortBy.includes("plus d'erreurs")) {
        this.items = this.items.slice().sort((a, b) => b.erreurs - a.erreurs);
      } else {
        this.items = this.items.slice().sort((a, b) => a.erreurs - b.erreurs);
      }
    },

    /**
     * Function to print the date correctly
     * @param {Date} date
     * @returns {String}
     * */
    printDate(date) {
      var monthNames = [
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

      var day = date.getDate();
      var monthIndex = date.getMonth();
      var year = date.getFullYear();

      return day + " " + monthNames[monthIndex] + " " + year;
    },

    //Transform Chart to PNG
    onChartReady(chart, google) {
      var self = this;
      google.visualization.events.addListener(chart, "ready", function() {
        self.png = chart.getImageURI();
      });
    },

    //Print the Graph
    print() {
      var WinPrint = window.open(
        "",
        "",
        "left=0,top=0,width=1000,height=900,toolbar=0,scrollbars=0,status=0"
      );
      WinPrint.document.write("<html><head>");
      WinPrint.document.write(
        '<link rel= "stylesheet", href= "../css/print.css">'
      );
      WinPrint.document.write("</head><body>");
      WinPrint.document.write('<img src="' + this.png + '">');
      //WinPrint.document.write('<h1>'+this.title+'</h1>')
      WinPrint.document.write("</body></html>");
      WinPrint.document.close();
      WinPrint.focus();
      WinPrint.print();
    }
  }
};
</script>
