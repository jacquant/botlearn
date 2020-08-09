<template>
  <v-layout>
    <v-flex class="text-center">
      <div id="bot">
        <div id="chatBotCommandDescription" />
        <label for="humanInput" />
        <input id="humanInput" type="text" />
        <div id="chatBot">
          <div id="chatBotThinkingIndicator" />
          <div id="chatBotHistory" />
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
    import {ChatBot} from "../static/js/chatbot";

    export default {
  mounted() {
    const config = {
      // what inputs should the bot listen to? this selector should point to at least one input field
      inputs: "#humanInput",
      // if you want to show the capabilities of the bot under the search input
      inputCapabilityListing: true,
      // optionally, you can specify which conversation engines the bot should use, e.g. webknox, spoonacular, or duckduckgo
      engines: [ChatBot.Engines.duckduckgo()],
      // you can specify what should happen to newly added messages
                addChatEntryCallback: function (entryDiv, text, origin) { //eslint-disable-line
        entryDiv.slideDown();
      }
    };
    ChatBot.init(config);
  }
};
</script>

<style>
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

/*.button {
  display: inline-block;
  background-color: darkcyan;
  color: #fff;
  padding: 8px;
  cursor: pointer;
}*/

#chatBotCommandDescription {
  /*display: none;*/
  margin-bottom: 20px;
}

input:focus {
  outline: none;
}
</style>
