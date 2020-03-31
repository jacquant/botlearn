<template>
  <v-container fluid class="fill-height">
    <v-row align="center">
      <v-col offset="1" offset-sm="3" cols="10" sm="6">
        <!-- Classic Login -->
        <v-card class="elevation-12">
          <v-toolbar color="green" dark flat>
            <v-toolbar-title>Réinitialiser son mot de passe</v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-alert v-if="error" text prominent type="error" icon="mdi-alert">
            Les mots de passe ne correspondent pas.
          </v-alert>
          <v-alert
            v-if="succeed"
            text
            prominent
            type="success"
            icon="mdi-checkbox-marked-circle"
          >
            Le mot de passe a été changé (<a href="/login">Se connecter</a>).
          </v-alert>
          <v-card-text>
            <v-form>
              <v-text-field
                id="password"
                v-model="password"
                label="Mot de passe"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="passwordErrors"
                @input="$v.password.$touch()"
                @blur="$v.password.$touch()"
              />

              <v-text-field
                v-model="password_conf"
                label="Confirmation du mot de passe"
                name="conf_password"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="passwordConfErrors"
                @input="$v.password_conf.$touch()"
                @blur="$v.password_conf.$touch()"
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="green"
              class="white--text"
              :disabled="$v.password.$invalid || $v.password_conf.$invalid"
              @click="submit"
            >
              Se connecter
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, minLength } from "vuelidate/lib/validators";
import http from "../system/http";

export default {
  mixins: [validationMixin],

  // ================================================================================================== ==
  // Validations
  // Rules for each input
  // ================================================================================================== ==
  validations: {
    password: { required, minLength: minLength(8) },
    password_conf: { required, minLength: minLength(8) }
  },

  // ================================================================================================== ==
  // Data
  // ================================================================================================== ==
  data: () => ({
    //User's data
    password: "",
    password_conf: "",

    //If emails are not the same
    error: false,
    succeed: false
  }),

  // ================================================================================================== ==
  // Computed
  // ================================================================================================== ==
  computed: {
    /**
     * Indicates if there is a password written.
     * @private
     * @returns {errors: tab}
     */
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push("Le mot de passe doit faire minimum 8 caractères");
      !this.$v.password.required && errors.push("un mot de passe est requis");
      return errors;
    },

    /**
     * Indicates if there is a password written.
     * @private
     * @returns {errors: tab}
     */
    passwordConfErrors() {
      const errors = [];
      if (!this.$v.password_conf.$dirty) return errors;
      !this.$v.password_conf.minLength &&
        errors.push("Le mot de passe doit faire minimum 8 caractères");
      !this.$v.password_conf.required &&
        errors.push("un mot de passe est requis");
      return errors;
    }
  },

  // ================================================================================================== ==
  // Mounted
  // ================================================================================================== ==
  async mounted() {
    //Verify the token

    if (this.$route.query.token === undefined) {
      this.$router.push("/login");
    } else {
      let data = { token: this.$route.query.token };
      await http.post("password_reset/validate_token/", data);
    }
  },

  // ================================================================================================== ==
  // Methods
  // ================================================================================================== ==
  methods: {
    async submit() {
      //Checking if user filled correctly the form
      this.$v.$touch();

      //Axios request to check if data is correct
      if (this.password != this.password_conf) {
        this.error = true;
        this.succeed = false;
      } else {
        this.error = false;
        this.succeed = true;
        let data = { password: this.password, token: this.$route.query.token };
        await http.post("password_reset/confirm/", data);
      }
    }
  }
};
</script>
