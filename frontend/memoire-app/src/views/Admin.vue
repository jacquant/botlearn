<template>
    <v-layout>
        <v-flex>
            <v-row>
                <v-col offset="1" mb="6" lg="6" xl="6">
                        <h1>Liste des exercices</h1>
                        <v-card
                            class="mx-auto mr-xs-10"
                            max-width="100%"
                        >                            
                            <v-text-field color="success" loading disabled v-if="loading"></v-text-field>
                            <v-list v-else>
                            <!--Loop for the sections-->
                                <v-list-group
                                    prepend-icon=""
                                    value="true"
                                    v-for="info in tps"
                                    :key="info.id"
                                    sub-group
                                >
                                    <template v-slot:activator>
                                        <v-list-item-title>
                                            <b>{{info.name}}</b>
                                        </v-list-item-title>
                                    </template>
                                    <v-list-item
                                        v-for=" exe in info.exercices"
                                        :key="exe.id"
                                        link
                                        @click="getInfo(exe.id)"
                                    >
                                        <v-list-item-title> {{exe.name}}</v-list-item-title>
                                        <v-list-item-icon>
                                        <v-icon></v-icon>
                                        </v-list-item-icon>
                                    </v-list-item>
                                </v-list-group>
                            </v-list>
                        </v-card>
                </v-col>
                <v-col offset="1">
                    <h1>Informations</h1>
                        <v-alert type="info" class="mx-auto mr-10" v-if="current_data == null">
                            Sélectionne un exercice pour en avoir un résumé.
                        </v-alert>
                    <v-card
                        class="mx-auto mr-10"
                        v-else
                    >
                        <v-toolbar
                            color="green"
                            dark
                            flat
                        >
                            <v-toolbar-title>{{current_data}}</v-toolbar-title>
                            <v-spacer />
                        </v-toolbar>
                        <v-card-text>
                            <v-list>
                                <v-list-item >
                                    <div style="font-weight:bold">Nombre de soumissions: </div> 120
                                </v-list-item>
                                <v-list-item>
                                    Nombre de soumissions distinctes: 71
                                </v-list-item>
                            </v-list>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions class="d-flex align-center justify-center">
                            <p class="ma-0"> 
                                <v-btn color="green" class="white--text">Afficher l'exercice en détails</v-btn>
                            </p>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col >
                    <v-divider></v-divider>
                    <v-card
                    class="mx-auto text-center mt-10"
                    color="white"
                    max-width="800px"
                    >
                    <v-tabs
                        v-model="tab"
                        background-color="green"
                        dark
                        class="mb-5"
                        show-arrows
                        >
                        <v-tab
                            v-for="item in items"
                            :key="item.tab"
                            @click="changeData()"
                        >
                            {{ item.tab }}
                        </v-tab>
                    </v-tabs>
                    <v-tabs-items v-model="tab">
                        <v-tab-item
                            v-for="item in items"
                            :key="item.tab"
                        >
                            <v-card flat> 
                                <v-card-text>
   
                                </v-card-text>
                            </v-card>
                        </v-tab-item>
                    </v-tabs-items>
                        <v-card-text>
                            <div id="printMe">
                                <GChart
                                    type="ColumnChart"
                                    :data="chartData"
                                    :options="chartOptions"
                                />
                            </div>
                        <!--<v-sheet color="rgba(0, 0, 0, .12)">
                            <v-sparkline
                            :value="value"
                            color="rgba(255, 255, 255, .7)"
                            height="100"
                            padding="24"
                            stroke-linecap="round"
                            smooth
                            >
                            <template v-slot:label="item">
                                {{ item.value }}
                            </template>
                            </v-sparkline>
                        </v-sheet> -->
                        </v-card-text>

                        <v-card-text>
                        <div class="display-1">{{title}}</div>
                        </v-card-text>

                        <v-divider></v-divider>

                        <v-card-actions class="justify-center">
                        <v-btn block text @click="print()">Imprimer graphe</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-flex>
    </v-layout>
</template>

<script>
import store from "../store/store"
import router from "../system/router"
import { GChart } from 'vue-google-charts'
import http from '../system/http'
import Store from '../store/store'

export default {
    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
   data: () => ({
       //List exercices et tps
      tps:[],

      current_data:null,

        // Data for Tabs
      items: [
          { tab: 'One', content: 'Tab 1 Content' },
          { tab: 'Two', content: 'Tab 2 Content' },
          { tab: 'Three', content: 'Tab 3 Content' },
          { tab: 'Four', content: 'Tab 4 Content' },
          { tab: 'Five', content: 'Tab 5 Content' },
          { tab: 'Six', content: 'Tab 6 Content' },
        ],
        tab:null,

        //Data For Graph
        chartData: [
            ['Year', 'Soumissions'],
            ['2014', 1000],
            ['2015', 1678],
            ['2016', 660],
            ['2017', 1030]
        ],
        chartOptions: {
            colors: ['green'],
            legend:  { position: "none" }
        },
        title:'Nombre de soumissions des exercices',

        //loading

        loading: true
    }),

    // ================================================================================================== ==
    // Components
    // ================================================================================================== ==
    components: {
        GChart,
    },

    // ================================================================================================== ==
    // Created
    // ================================================================================================== ==
    async created(){
        //Redirect if user is not staff
        if(!store.state.userInformation.is_staff){
            router.push("/");
        }

        //Get All Tps
        this.tps = (await http.get("sessions/all/",{headers:{ 'Authorization': 'Bearer '+ Store.state.accessToken}})).data;
        //console.log(this.tps);

        var exercices = [];
        for (const key in this.tps) {
            exercices = (await (http.get("exercises/by_session/"+this.tps[key].id,{headers:{ 'Authorization': 'Bearer '+ Store.state.accessToken}}))).data;
            this.tps[key]["exercices"] = exercices
        }

        this.loading = false;
        
    },

    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods:{
        //Get details from an exercice
        getInfo(data){
            this.current_data = data;
        },
        //Get the data compared to the tab selectionned
        changeData(){
            this.chartData =[ 
                ['Type', 'Erreurs'],
                ['Boucle', 834],
                ['Condition', 435],
                ['Fonction', 501],
                ['Structure de données', 1030]
            ]
            this.title = "Nombre d'erreurs par type"
        },
        
        //Print the Graph
        print(){
            //window.print();
            this.$htmlToPaper('printMe');
        }
    }
    
}
</script>