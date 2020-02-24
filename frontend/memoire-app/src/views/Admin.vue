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
                            <v-list>
                            <!--Loop for the sections-->
                                <v-list-group
                                    prepend-icon=""
                                    value="true"
                                    v-for="info in sections.data"
                                    :key="info.number"
                                    sub-group
                                >
                                    <template v-slot:activator>
                                        <v-list-item-title>
                                            <b>{{info.number}}: {{info.title}}</b>
                                        </v-list-item-title>
                                    </template>
                                    <v-list-item
                                        v-for=" exe in exercices.data"
                                        :key="exe.number"
                                        link
                                        @click="getInfo(exe.number)"
                                    >
                                        <v-list-item-title> {{exe.number}} - {{exe.title}}</v-list-item-title>
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
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
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
                            <GChart
                                type="ColumnChart"
                                :data="chartData"
                                :options="chartOptions"
                            />
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
                        <div class="display-1">Nombre de soumissions des exercices</div>
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

export default {
    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
   data: () => ({
       //List exercices
      sections: {data: [{number:"Section 1", title:"Les variables"},
                        {number:"Section 2", title:"Les conditions"}
      
      ]},
      exercices: {data:[{number:"Exercice 1.1",title:"Donne-moi une valeur", consigne: "Tu dois faire ça"},
                        {number:"Exercice 1.2",title:"Additione-nous !", consigne: "Tu dois faire comme ceci"}
      ]},

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
      }
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
    created(){
        if(!store.state.userInformation.is_staff){
            router.push("/");
        }
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
        },
        
        //Print the Graph
        print(){
            window.print();
        }
    }
    
}
</script>