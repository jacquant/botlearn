<template>
  <v-layout>
    <v-flex>
      <h1 class="mr-10 ml-10">
        Mes solutions rendues
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
                  label="Filtrer par intitulé de l'exercice"
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

export default {
  // ================================================================================================== ==
  // Data
  // ================================================================================================== ==
  data: () => ({
    //Detail exercice
    exercice: {},

    //Solutions d'un étudiant _ Data
    itemsPerPageArray: [4, 12, 24],
    search: "",
    filter: {},
    sortDesc: false,
    page: 1,
    itemsPerPage: 20,
    sortBy: "Le plus récent",
    keys: ["Le plus ancien", "Le plus récent"],
    items: [
      {
        id: 1,
        name: "Exercice 1.1",
        date: new Date("2020-02-24"),
        erreurs: 6
      },
      {
        id: 2,
        name: "Exercice 1.2",
        date: new Date("2020-02-25"),
        erreurs: 4
      },
      {
        id: 3,
        name: "Exercice 2.1",
        date: new Date("2020-01-25"),
        erreurs: 1
      },
      {
        id: 4,
        name: "Exercice 3.1",
        date: new Date("2020-02-01"),
        erreurs: 2
      },
      {
        id: 5,
        name: "Exercice 3.2",
        date: new Date("2019-01-10"),
        erreurs: 9
      },
      {
        id: 6,
        name: "Exercice 3.3",
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
    //TO DO ! Get ALL SUBMISSIONS OF A USER
    //Get Details exercice
    this.exercice = (
      await http.get("submissions/", {
        headers: { Authorization: "Bearer " + store.state.accessToken }
      })
    ).data;
    console.log(this.exercice);
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
    }
  }
};
</script>
