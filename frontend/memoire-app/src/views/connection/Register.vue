<template>
  <v-layout>
    <v-flex class="text-center">
      <v-col offset="1" offset-sm="3" cols="8" sm="6">
        <v-card class="elevation-12">
          <v-toolbar color="green" dark flat>
            <v-toolbar-title>S'inscrire</v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="text"
                :error-messages="emailErrors"
                @input="$v.email.$touch()"
                @blur="$v.email.$touch()"
              />

              <v-text-field
                v-model="firstname"
                label="Prénom"
                name="prenom"
                prepend-icon="mdi-account"
                type="text"
                :error-messages="firstNameErrors"
                @input="$v.firstname.$touch()"
                @blur="$v.firstname.$touch()"
              />

              <v-text-field
                v-model="lastname"
                label="Nom"
                name="nom"
                prepend-icon="mdi-account"
                type="text"
                :error-messages="lastNameErrors"
                @input="$v.lastname.$touch()"
                @blur="$v.lastname.$touch()"
              />

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
                id="conf_password"
                v-model="password_conf"
                label="Confirmation du mot de passe"
                name="conf_password"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="passwordConfErrors"
                @input="$v.password_conf.$touch()"
                @blur="$v.password_conf.$touch()"
              />

              <v-text-field
                v-model="eid"
                label="Ton Eid"
                name="eid"
                prepend-icon="mdi-account-search"
                type="text"
                :error-messages="eidErrors"
                @input="$v.eid.$touch()"
                @blur="$v.eid.$touch()"
              >
                <v-tooltip slot="append" bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon color="green" dark v-on="on">
                      mdi-information-outline
                    </v-icon>
                  </template>
                  <span
                    >En indiquant ton eid, tu pourras te connecter avec tes
                    identifiants UNamur.</span
                  >
                </v-tooltip>
              </v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="green"
              class="white--text"
              :disabled="
                $v.password.$invalid ||
                  $v.password_conf.$invalid ||
                  $v.eid.$invalid ||
                  $v.email.$invalid ||
                  $v.firstname.$invalid ||
                  $v.lastname.$invalid ||
                  password !== password_conf
              "
              @click="submit"
            >
              Se connecter
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-flex>
  </v-layout>
</template>

<script>
    import {validationMixin} from "vuelidate";
    import {email, maxLength, minLength, required} from "vuelidate/lib/validators";

    export default {
  mixins: [validationMixin],

  // ================================================================================================== ==
  // Validations
  // Rules for each input
  // ================================================================================================== ==
  validations: {
    email: { required, email },
    firstname: { required },
    lastname: { required },
    password: { required, minLength: minLength(8) },
    password_conf: { required, minLength: minLength(8) },
    eid: { required, maxLength: maxLength(10) }
  },

  // ================================================================================================== ==
  // Data
  // ================================================================================================== ==
  data: () => ({
    //User's data
    email: "",
    firstname: "",
    lastname: "",
    password: "",
    password_conf: "",
    eid: "",

    //If emails are not the same
    error: false,
    succeed: false
  }),

  // ================================================================================================== ==
  // Computed
  // ================================================================================================== ==
  computed: {
    /**
     * Indicates if the identifiers are not correct.
     * @private
     * @returns errors: {Array}
     */
    emailErrors() {
      const errors = [];
      if (!this.this.$v.email.$dirty) return errors;
      !this.this.$v.email.email &&
        errors.push("Une adresse email valide est requise !");
      !this.this.$v.email.required &&
        errors.push("Une adresse email doit être indiquée");
      return errors;
    },

    /**
     * Indicates if there is a first name.
     * @private
     * @returns errors: {Array}
     */
    firstNameErrors() {
      const errors = [];
      if (!this.this.$v.firstname.$dirty) return errors;
      !this.this.$v.firstname.required && errors.push("Un prénom doit être indiqué");
      return errors;
    },

    /**
     * Indicates if there is a last name.
     * @private
     * @returns  errors: {Array}
     */
    lastNameErrors() {
      const errors = [];
      if (!this.this.$v.lastname.$dirty) return errors;
      !this.this.$v.lastname.required &&
        errors.push("Un nom doit être indiqué");
      return errors;
    },

    /**
     * Indicates if there is a password written.
     * @private
     * @returns  errors: {Array}
     */
    passwordErrors() {
      const errors = [];
      if (!this.this.$v.password.$dirty) return errors;
      !this.this.$v.password.minLength &&
        errors.push("Le mot de passe doit faire au minimum 8 caractères");
      !this.this.$v.password.required && errors.push("Un mot de passe est requis !");
      return errors;
    },

    /**
     * Indicates if there is a password written.
     * @private
     * @returns  errors: {Array}
     */
    passwordConfErrors() {
      const errors = [];
      if (!this.$v.password_conf.$dirty) return errors;
      !this.$v.password_conf.minLength &&
        errors.push("Le mot de passe doit faire minimum 8 caractères");
      !this.$v.password_conf.required &&
        errors.push("Un mot de passe est requis !");
      //!this.this.$v.password_conf.samePassword && errors.push("Le mot de passe ne correspond pas")
      if (this.password !== this.password_conf) {
        errors.push("Le mot de passe ne correspond pas");
      }
      return errors;
    },

    /**
     * Indicates if the eid is not correct.
     * @private
     * @returns  errors: {Array}
     */
    eidErrors() {
      const errors = [];
      if (!this.$v.eid.$dirty) return errors;
      !this.$v.eid.maxLength && errors.push("L'eid fait au maximum 10 caractères");
      !this.$v.eid.required && errors.push("Un eid est requis");
      return errors;
    }
  },

  // ================================================================================================== ==
  // Methods
  // ================================================================================================== ==
  methods: {
    async submit() {
      //Checking if user filled correctly the form
      this.$v.$touch();

      //toDo Axios
    }
  }
};
</script>
