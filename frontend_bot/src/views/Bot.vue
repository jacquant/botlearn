<template>
  <v-layout>
    <pre>{{ data_from_iframe }}</pre>
    <v-flex class="text-center">
      <v-dialog v-model="dialog_soumettre" persistent max-width="490">
        <v-card>
          <v-card-title class="headline" style="text-align:center;">
            Cette action n'est effectuable qu'une fois
          </v-card-title>
          <v-card-actions>
            <v-btn color="red" @click="dialog_soumettre = false">
              Modifier mon code
            </v-btn>
            <v-spacer />
            <v-btn color="#28703d">
              Soumettre
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <div id="bot">
        <v-btn color="#72c288" @click="interactIframe()">
          Exécuter
        </v-btn>
        <v-btn color="#28703d" class="ml-5" @click="dialog_soumettre = true">
          Soumettre
        </v-btn>
        <div id="chatBotCommandDescription" class="mt-2" />
        <input id="humanInput" type="text" class="mt-5" />
        <div class="tooltip ml-10">
          <i class="fas fa-info" />
          <span class="tooltiptext"
            ><p>Pour ouvrir un lien sur Mac OS: cmd + click</p></span
          >
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

        url: "http://localhost:8080/api/",

        token: null,

        dialog_soumettre: false,

        //Code Iframe
        data_from_iframe: "",
        id_execut: 1,
    }),

    // ================================================================================================== ==
    // Mounted
    // ================================================================================================== ==
    mounted(){

        //Render the HighLight for the code
        Prism.highlightAll()

        //Partie token

        if(this.$route.query.token === undefined) {
            this.$router.push("/login");
        }else{
            this.token = this.$route.query.token;
        }

        ///////////////////////////////////////////////////////////////////////////

        //Partie Bot
        var config = { 
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
  methods: {
    //Check token's validity every 20 minutes (1200000)
    startInterval() {
      let self = this;
      let timer = setInterval(() => {
        axios
          .post(this.url + "token/verify/", {
            token: this.token
          })
          .catch(function() {
            //console.log(error);
            clearInterval(timer);
            self.$router.push("/login");
          });
      }, 1200000);
    },

    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods:{
        //Check token's validity every 20 minutes (1200000)
        startInterval() {
            let self = this;
            let timer = setInterval(() => {
                axios.post(this.url + 'token/verify/', {
                    "token": this.token,
                })
                .catch(function (error) {
                    //console.log(error);
                    clearInterval(timer);
                    self.$router.push("/login");
                });

            }, 1200000)
        },

        //Execute what the iframe requested
        interactIframe (evt) {
            parent.window.postMessage("run", "*");
        },

        //Listening what the iframe sent (code)
        listeningIframe (evt) {
            let namefile = evt.data.filename.split("/")

            let data = {"code_input": evt.data.code,
                        "filename": String(namefile[namefile.length - 1]),
                        "translate": true
                        }
            axios.post(this.url + 'code/lint/', data, {headers: {"Authorization": "Bearer " + this.token}}
            
            ).then(function (response) {
                let css_response="<ul style='text-align: left;'>"
                for (const key in response.data.lint_results) {
                    css_response += "<li>" + response.data.lint_results[key] + "</li>"
                }
                css_response += "</ul>"
                var entryDiv = $('<div class="chatBotChatEntry Bot" style="background-color:#e88f5f"></div>');
                entryDiv.html('<span class="origin">' + 'Bot' + '</span>' + css_response);

                $('#chatBotHistory').prepend(entryDiv);
                
            })
        },
    },

    //Listening what the iframe sent (code)
    listeningIframe(evt) {
      this.data_from_iframe = evt.data.code;
    }
  }
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
