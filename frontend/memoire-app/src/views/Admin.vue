<template>
    <v-layout>
        <v-flex>
            <v-row>
                <!--List of exercices by TP-->
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
                                        <v-list-item-icon>
                                            <v-icon>mdi-book</v-icon>
                                        </v-list-item-icon>
                                        <v-list-item-title> {{exe.name}}</v-list-item-title>
                                        <v-btn :href="'http://localhost:8080/admin/exercises/exercise/'+exe.id+'/change/'" target="_blank">
                                            <v-icon>mdi-lead-pencil</v-icon>
                                        </v-btn>
                                    </v-list-item>
                                    <v-list-item :href="'http://localhost:8080/admin/exercises/exercise/add?id='+info.id" target="_blank">
                                        <v-list-item-icon>
                                            <v-icon>mdi-book-plus</v-icon>
                                        </v-list-item-icon>
                                        <v-list-item-title style="color:red">Ajouter un exercice</v-list-item-title>
                                    </v-list-item>
                                    <v-divider></v-divider>
                                </v-list-group>
                            </v-list>
                        </v-card>
                </v-col>

                <!--Details for one exercice choosen-->
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
                                <v-btn color="green" class="white--text" :href="'/administration/exercice?id='+current_data" target="_blank">Afficher l'exercice en détails</v-btn>
                            </p>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>

            <!--Graph Part - Global view-->
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
                        </v-tab-item>
                    </v-tabs-items>
                        <v-card-text>
                            <GChart
                                id="Chart"
                                type="ColumnChart"
                                :data="chartData"
                                :options="chartOptions"
                                @ready="onChartReady"
                            />
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
        loading: true,

        //chart in PNG
        png:'',
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

        //Redirect if user is not staff -> Call API to get information to be sure that localstorage wasn't change manually
        var is_staff = await http.get("user/get/", {headers:{ 'Authorization': 'Bearer '+ store.state.accessToken}})

        if(!is_staff){
            var new_json = store.state.userInformation;
            new_json["is_staff"]=false;
            localStorage.setItem('infoUser', JSON.stringify(new_json));
            router.push("/");
        }

        //Get All Tps
        this.tps = (await http.get("sessions/all/",{headers:{ 'Authorization': 'Bearer '+ store.state.accessToken}})).data;
        //console.log(this.tps);

        var exercices = [];
        for (const key in this.tps) {
            exercices = (await (http.get("exercises/by_session/"+this.tps[key].id,{headers:{ 'Authorization': 'Bearer '+ store.state.accessToken}}))).data;
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

        //Transform Chart to PNG
        onChartReady (chart, google) {
            var self =this;
             google.visualization.events.addListener(chart, 'ready', function () {
                self.png= chart.getImageURI();
            });
            
        },
        
        //Print the Graph
        print(){
            var WinPrint = window.open('', '', 'left=0,top=0,width=1000,height=900,toolbar=0,scrollbars=0,status=0');
            WinPrint.document.write('<html><head>');
            WinPrint.document.write('<link rel= "stylesheet", href= "/css/print.css">');
            WinPrint.document.write('</head><body>');
            WinPrint.document.write('<img src="'+this.png+ '">');
            WinPrint.document.write('<h1>'+this.title+'</h1>');
            WinPrint.document.write('</body></html>');
            WinPrint.document.close();
            WinPrint.focus();
            WinPrint.print();
        }
    }
    
}
</script>