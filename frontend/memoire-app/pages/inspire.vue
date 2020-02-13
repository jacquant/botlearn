<template>
  <v-layout>
    <v-flex class="text-center">
      <img
        src="/v.png"
        alt="Vuetify.js"
        class="mb-5"
      >
      <blockquote class="blockquote">
        &#8220;First, solve the problem. Then, write the code.&#8221;
        <footer>
          <small>
            <em>&mdash;John Johnson</em>
          </small>
        </footer>
      </blockquote>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  async mounted(){

    //Try killing token if expired
    /*let data = {"token": this.$auth.getToken('local').slice(7)}
    console.log(data);
    await this.$axios.$post("token/verify/", data)  
            .then(function(response) {
                console.log("fonctionne")
                //self.$router.push('/')
            })
            .catch(error => {
                    console.log(error)
                });*/
  }

}
</script>
