<template>
  <v-layout>
    <v-flex class="text-center" @click="onClickApp">

      <!--Dialog when the student wants to submit his code-->
      <v-dialog v-model="dialog_soumettre" persistent max-width="490">
        <v-card>
          <v-card-title class="headline" style="text-align:center;">
            Cette action n'est effectuable qu'une fois
          </v-card-title>
          <v-card-actions>
            <v-btn class="ma-2" tile outlined color="success" @click="dialog_soumettre = false">
              <v-icon left>mdi-pencil</v-icon> Modifier
            </v-btn>
            <v-spacer />
              <v-btn color="#28703d" @click="interactIframe(true); dialog_soumettre = false; disable_submit = true">
                Soumettre
              </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="anonym_alert" max-width="600">
        <v-alert type="warning" v-if="anonym_value">
          Tu es désormais <strong>anonyme</strong> ! Tous tes codes sont anonymes.
        </v-alert>
        <v-alert type="warning" v-else>
          Tu n'es <strong>plus anonyme</strong> ! Tous tes codes ne sont plus anonymes.
        </v-alert>
      </v-dialog>

      <!--Bot's interface-->
      <div id="bot">
        <v-btn color="#72c288" @click="interactIframe(false);" :disabled="disable_button">
          Exécuter <span v-if="countDown > 0 && disable_button"> ({{countDown}})</span>
        </v-btn>
        <v-btn color="#28703d" class="ml-5" @click="dialog_soumettre = true" v-if="current_exercise != null" :disabled="disable_submit">
          Soumettre
        </v-btn>
        <v-layout column align-center>
          <v-switch
            v-model="anonym_value"
            :label=" anonym_value ? 'Tu es anonyme' : 'Tu n\'es pas anonyme' "
            color="#28703d"
            @change="anonym_alert = true; anonym()"
          ></v-switch>
        </v-layout>
        <v-alert class="mt-2" type="error" v-show="alert">
          Une erreur est survenue durant l'exécution (probablement aucun exercice lié à la soumission).
        </v-alert>

        <!-- Show current exercise selected-->
        <v-card class="mt-4 justify-center" v-if="detail_exercise != null" color="green"> 
          <v-card-text>
            Tu es en train de répondre à l'exercice n°{{detail_exercise.id}} - {{detail_exercise.instruction}}
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn class="ma-2 text-center" x-small rounded outlined  @click="detail_exercise = null; current_exercise= null">
              Quitter l'exercice 
            </v-btn>
          </v-card-actions>
        </v-card>

        <div id="chatBotCommandDescription" class="mt-2" />
        <input id="humanInput" type="text" class="mt-5" />
        <div class="tooltip ml-10">
          <i class="fas fa-info" />
          <span class="tooltiptext">
            <p>Pour ouvrir un lien sur Mac OS: cmd + click</p>
            <p>Pour ouvrir un lien sur Windows: ctrl + click</p>
          </span>
        </div>
        <div id="chatBot">
          <div id="chatBotThinkingIndicator" />
          <div id="chatBotHistory" />
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import { ChatBot } from "../static/js/chatbot";
import axios from "axios";

export default {
    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
    data: () => ({

        url: "https://memoire.jacquant.be/api/",

        email: null,

        token: null,

        dialog_soumettre: false,

        //Code Iframe
        data_from_iframe: "",

        //get the current exercise selected
        current_exercise: null,
        detail_exercise: null,

        //Alert if there is an error from exectute api
        alert: false,
        final: true,

        //Countdown button
        countDown: 10,
        disable_button: false,
        disable_submit: true,

        //Anonym value
        anonym_value: null,
        anonym_alert: false,
    }),

    // ================================================================================================== ==
    // Mounted
    // ================================================================================================== ==
    mounted(){

        //Render the HighLight for the code
        //Prism.highlightAll()

        //Partie token

        if(this.$route.query.token === undefined) {
            this.$router.push("/login");
        }else{
            this.token = this.$route.query.token;
        }

        //Get email of a user when is connected and check if the user is anonym or not
         axios.get(this.url + 'user/get/', {headers: {"Authorization": "Bearer " + this.token}}
            ).then( response => {
              this.email = response.data.mail;
              this.anonym_value = response.data.anonymous;
            }).catch(() => { 
            });

        ///////////////////////////////////////////////////////////////////////////

        //Partie Bot
        let config = {
        // what inputs should the bot listen to? this selector should point to at least one input field
        inputs: '#humanInput',
        // if you want to show the capabilities of the bot under the search input
        inputCapabilityListing: true,
        // optionally, you can specify which conversation engines the bot should use, e.g. webknox, spoonacular, or duckduckgo
        engines: [ChatBot.Engines.backendinfo(this.token)],
        // you can specify what should happen to newly added messages
        addChatEntryCallback: function(entryDiv, text, origin) { //eslint-disable-line
        entryDiv.slideDown();
      }
    };
    ChatBot.init(config);
  },

  // ================================================================================================== ==
  // Created
  // ================================================================================================== ==
  created() {
    //Call function to check token's validity
    this.startInterval();

    //Listening if a code is submitted from the iframe
    window.addEventListener("message", this.listeningIframe);
  },
    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods:{
        //Catch when the user click on the exercice to get the id
        onClickApp(ev){
          if(!isNaN(parseInt(ev.target.id))){
            this.disable_submit = true;
            this.current_exercise = ev.target.id;

            //Get details of exercice to show it
            axios.get(this.url + 'exercises/' + this.current_exercise + "/", {headers: {"Authorization": "Bearer " + this.token}}
            
            ).then( response => {
              this.detail_exercise = response.data;
            }).catch(() => { 
              });

            //Check if user has already submitted the code
            axios.get(this.url + 'submissions/?author_mail=' + this.email + '&exercises=' + this.current_exercise + "&final=true",
                      {headers: {"Authorization": "Bearer " + this.token}}
            ).then(response => {
              if(response.data.length > 0){
                this.disable_submit = true;
              }else{
                this.disable_submit = false;
              }
            }).catch(() => { 
              });
          }
        },
        //Check token's validity every 20 minutes (1200000)
        startInterval() {
            let self = this;
            let timer = setInterval(() => {
                axios.post(this.url + 'token/verify/', {
                    "token": this.token,
                })
                .catch(function () {
                    //console.log(error);
                    clearInterval(timer);
                    self.$router.push("/login");
                });

            }, 1200000)
        },

        //Execute what the iframe requested
        interactIframe (bool) {
          this.final = bool;
          this.countDownTimer();
          parent.window.postMessage("run", "*");
        },
        
        //Listening what the iframe sent (code)
        listeningIframe (evt) {
            let name_file = evt.data.filename.split("/")

            let data = {"code_input": evt.data.code,
                        "final": this.final,
                        "exercise_id": this.current_exercise,
                        "filename": String(name_file[name_file.length - 1]),
                        }
            //modify url
            let url_execute = "execute/";

            if (this.current_exercise == null){
              url_execute = "lint/";
              data = {"code_input": evt.data.code,
                      "filename": String(name_file[name_file.length - 1]),
                      "translate": false
                      }
            }
            //exécute the code
            axios.post(this.url + 'code/'+ url_execute, data, {headers: {"Authorization": "Bearer " + this.token}}
            
            ).then(function (response) {
                //display code
                  let css_response = ""
                  let color= ""
                //If execution is correct
                  if(response.data.stderr == ""){
                    css_response = "<h2 style='font-weight: bold; text-align: left;'> Résultat:</h2>" 
                    if(response.data.stdout !=""){
                      css_response += "<p style='text-align: left;'>" +  response.data.stdout.replace(/\n/g,"<br>") + "</p>";
                    }else{
                      css_response += "<p style='text-align: left;'>Aucun résultat à montrer</p>"
                    }
                    color = '#419eba';

                //If execution is NOT correct
                }else{
                  css_response = "<h2 style='font-weight: bold; text-align: left;'>Oups ! L'exécution de ton code a eu un problème !</h2>"
                  css_response += "<p style='text-align: left;'>" +  response.data.stderr + "</p>";
                  color = "#e88f5f";

                }
                
                css_response += "<p style='text-align: left;'>------------------ </p>"
                css_response += "<h2 style='font-weight: bold; text-align: left;'> Amélioration du code ! </h2>" 
                css_response += "<ul style='text-align: left;'>"
                for (const key in response.data.lint_results) {
                    css_response += "<li> Ligne: " + response.data.lint_results[key].substring(response.data.lint_results[key].indexOf(":") + 1); + "</li>"
                }
                css_response += "</ul>"
                let entryDiv = $('<div class="chatBotChatEntry Bot" style="background-color:' + color + '"></div>'); //eslint-disable-line
                entryDiv.html('<span class="origin">' + 'Botlearn' + '</span>' + css_response);

                $('#chatBotHistory').prepend(entryDiv);//eslint-disable-line 
                
            }).catch(() => {
              this.alert = true;
                window.setInterval(() => {
                  this.alert = false;
                }, 3000)    
              });
        },
        //Create countdown to not spam the button
          countDownTimer() {
            this.disable_button = true;
              if(this.countDown > 0) {
                  setTimeout(() => {
                      this.countDown -= 1
                      this.countDownTimer()
                  }, 1000)
              }else{
                this.disable_button = false;
                this.countDown = 10;
              }
          },

        // change value of being anonym or not
        anonym(){
          axios.put(this.url + 'user/update', {anonymous:this.anonym_value} ,{headers: {"Authorization": "Bearer " + this.token}})
          
        }
    },
};
</script>

<style>
/*Partie Bot*/
#bot {
  /*background-color: #ffffff;*/
  width: 90%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;

  background-color: #f8f8f8;
  border: 1px solid #ccc;
  box-shadow: 0 0 10px #999;
  line-height: 1.4em;
  font: 13px helvetica, arial, freesans, clean, sans-serif;
  color: black;
}
#bot input {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  width: 400px;
}
.button {
  display: inline-block;
  background-color: darkcyan;
  color: #fff;
  padding: 8px;
  cursor: pointer;
}
#chatBotCommandDescription {
  /*display: none;*/
  margin-bottom: 20px;
}
input:focus {
  outline: none;
}
/*Partie Tooltip*/
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  width: 350px;
  top: 100%;
  left: 50%;
  margin-left: -300px;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
