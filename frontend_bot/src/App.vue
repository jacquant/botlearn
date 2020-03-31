<template>
  <v-app>
    <!-- ============================================================================================== ----
        ---- Page's content
        ---- ============================================================================================== -->
    <v-content class="mt-10">
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {},

  data: () => ({
    //
  })
};
</script>
