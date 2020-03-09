<template>
  <v-layout>
      <pre>{{data_from_iframe}}</pre>
    <v-flex class="text-center">
      <div id="bot">
        <v-btn color="#72c288" @click="interactIframe()"> Exécuter </v-btn>
        <div id="chatBotCommandDescription" class="mt-2"></div>
          <input id="humanInput" type="text" class="mt-5"/>
          <div id="chatBot">
              <div id="chatBotThinkingIndicator"></div>
              <div id="chatBotHistory"></div>
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>



<script>

import {ChatBot} from '../static/js/chatbot'
import axios from "axios"

export default {
    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
    data: () => ({

        url: "http://localhost:8080/api/",

        token: null,

        //Code Iframe
        data_from_iframe: ""
    }),

    // ================================================================================================== ==
    // Mounted
    // ================================================================================================== ==
    mounted(){

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
            this.data_from_iframe = evt.data.code;
        },
    },

    // ================================================================================================== ==
    // Created
    // ================================================================================================== ==
    created(){

        //Call function to check token's validity
        this.startInterval();

        //Listening if a code is submitted from the iframe
        window.addEventListener("message", this.listeningIframe);

    }
    
}
</script>

<style>
#bot {
      /*background-color: #ffffff;*/
      width: 90%;
      max-width: 1200px;
      margin-left: auto;
      margin-right: auto;
      padding: 20px;

      background-color: #F8F8F8;
      border: 1px solid #ccc;
      box-shadow: 0 0 10px #999;
      line-height: 1.4em;
      font: 13px helvetica,arial,freesans,clean,sans-serif;
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
      float: right;
  }
  #chatBotCommandDescription {
      /*display: none;*/
      margin-bottom: 20px;
  }
  input:focus {
      outline: none;
  }
  .chatBotChatEntry {
      /*display: none;*/
  }
</style>
