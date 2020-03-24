<template>
  <v-container
    fluid
    class="fill-height"
  >
    <v-row align="center">
      <v-col
        offset="1"
        offset-sm="3"
        cols="10"
        sm="6"
      >
        <!-- Classic Login -->
        <transition
          name="fade"
          mode="out-in"
        >
          <v-card
            v-if="!unamur"
            key="classique"
            class="elevation-12"
          >
            <v-toolbar
              color="green"
              dark
              flat
            >
              <v-toolbar-title>Connexion</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-alert
              v-if="error"
              text
              prominent
              type="error"
              icon="mdi-alert"
            >
              Il semblerait que les identifiants ne soient pas bons.
            </v-alert>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="email"
                  label="Email"
                  name="email"
                  prepend-icon="mdi-account"
                  type="text"
                  :error-messages="emailErrors"
                  @input="$v.email.$touch()"
                  @blur="$v.email.$touch()"
                  @keyup.enter="submit()"
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
                  @keyup.enter="submit()"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <a @click="forget_pwd=true">Mot de passe oublié ?</a>
              <v-spacer />
              <v-btn
                color="green"
                class="white--text"
                :disabled="$v.email.$invalid || $v.password.$invalid"
                @click="submit"
              >
                Se connecter
              </v-btn>
            </v-card-actions>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <a @click="unamur= !unamur">Se connecter avec ses identifiants UNamur</a>
              </p>
            </v-card-actions>
          </v-card>

          <!--Unamur Login>-->

          <v-card
            v-if="unamur"
            key="unamur"
            class="elevation-12"
          >
            <v-toolbar
              color="green"
              dark
              flat
            >
              <v-toolbar-title>Connexion UNamur</v-toolbar-title>
              <v-spacer />
            </v-toolbar>

            <v-alert
              v-if="error"
              text
              prominent
              type="error"
              icon="mdi-alert"
            >
              Il semblerait que les identifiants ne soient pas bons.
            </v-alert>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="eid_unamur"
                  label="Eid"
                  name="eid"
                  prepend-icon="mdi-account"
                  type="text"
                  :error-messages="eidErrors"
                  @input="$v.eid_unamur.$touch()"
                  @blur="$v.eid_unamur.$touch()"
                  @keyup.enter="submit()"
                />

                <v-text-field
                  id="password"
                  v-model="password_unamur"
                  label="Mot de passe"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  :error-messages="passwordUnamurErrors"
                  @input="$v.password_unamur.$touch()"
                  @blur="$v.password_unamur.$touch()"
                  @keyup.enter="submit()"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="green"
                class="white--text"
                :disabled="$v.eid_unamur.$invalid || $v.password_unamur.$invalid"
                @click="submit"
              >
                Se connecter
              </v-btn>
            </v-card-actions>
            <v-divider />
            <v-card-actions class="d-flex align-center justify-center">
              <p class="ma-0">
                <a @click="unamur= !unamur">Se connecter avec son propre compte.</a>
              </p>
            </v-card-actions>
          </v-card>
        </transition>

        <!--Reset password-->
        <v-dialog
          v-model="forget_pwd"
          width="500"
          class="elevation-12"
        >
          <v-card class="elevation-12">
            <v-toolbar
              color="green"
              dark
              flat
            >
              <v-toolbar-title>Réinitialiser son mot de passe</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-alert
              v-if="error"
              text
              prominent
              type="error"
              icon="mdi-alert"
            >
              L'adresse email n'existe pas.
            </v-alert>
            <v-alert
              v-if="succeed"
              text
              prominent
              type="success"
              icon="mdi-email"
            >
              Un email a été envoyé !
            </v-alert>

            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="email"
                  label="Email"
                  name="email"
                  prepend-icon="mdi-account"
                  type="text"
                  :error-messages="emailErrors"
                  @input="$v.email.$touch()"
                  @blur="$v.email.$touch()"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="green"
                class="white--text"
                :disabled="$v.email.$invalid"
                @click="reset"
              >
                Réinitialiser
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
    import {validationMixin} from "vuelidate";
    import {required, maxLength, email} from "vuelidate/lib/validators";
    import http from "../system/http";
    import store from "../store/store";

    export default {

        mixins: [validationMixin],

        // ================================================================================================== ==
        // Validations
        // Rules for each input
        // ================================================================================================== ==
        validations: {

            email: {required, email},
            eid_unamur: {required, between: maxLength(10)},
            password: {required},
            password_unamur: {required}

        },

        // ================================================================================================== ==
        // Data
        // ================================================================================================== ==
        data: () => ({

            //User's data
            email: "",
            password: "",

            eid_unamur: "",
            password_unamur: "",

            //Boolean
            forget_pwd: false,
            unamur: false,

        }),

        // ================================================================================================== ==
        // Computed
        // ================================================================================================== ==
        computed: {
            /**
             * Indicates if the identifiers are not correct.
             * @private
             * @returns {errors: tab}
             */
            emailErrors() {
                const errors = [];
                if (!this.$v.email.$dirty) return errors;
                !this.$v.email.email && errors.push("Une adresse email valide est requise !");
                !this.$v.email.required && errors.push("Une adresse email doit être indiquée");
                return errors;
            },

            /**
             * Indicates if there is a password written.
             * @private
             * @returns {errors: tab}
             */
            passwordErrors() {
                const errors = [];
                if (!this.$v.password.$dirty) return errors;
                !this.$v.password.required && errors.push("un mot de passe est requis");
                return errors;
            },

            /**
             * Indicates if the eid is not correct.
             * @private
             * @returns {errors: tab}
             */
            eidErrors() {
                const errors = [];
                if (!this.$v.eid_unamur.$dirty) return errors;
                !this.$v.eid_unamur.between && errors.push("L'eid fait maximum 10 caractères");
                !this.$v.eid_unamur.required && errors.push("Un eid est requis");
                return errors;
            },
            /**
             * Indicates if there is a password written.
             * @private
             * @returns {errors: tab}
             */
            passwordUnamurErrors() {
                const errors = [];
                if (!this.$v.password_unamur.$dirty) return errors;
                !this.$v.password_unamur.required && errors.push("un mot de passe est requis");
                return errors;
            },

            //Error message if user didn't enter good information
            error() {
                return store.state.internalError;
            },

            //Error message if user didn't register yet
            succeed() {
                return store.state.internalSucceed;
            },


        },

        // ================================================================================================== ==
        // Methods
        // ================================================================================================== ==
        methods: {
            async submit() {

                //Checking if user filled correctly the form
                this.$v.$touch();

                //Axios request to check if data is correct
                if (!this.unamur) {
                    //This condition is here to prevent from enter key pressed without filling the form
                    if (!this.$v.email.$invalid && !this.$v.password.$invalid) {
                        let data = {"mail": this.email, "password": this.password};
                        await http.post("token/login/", data);
                    }
                } else {
                    //This condition is here to prevent from enter key pressed without filling the form
                    if (!this.$v.eid_unamur.$invalid && !this.$v.password_unamur.$invalid) {
                        let data = {"eid": this.eid_unamur, "password": this.password_unamur};
                        await http.post("token/login_by_unamur/", data);
                    }
                }

            },

            async reset() {
                let data = {"email": this.email};
                await http.post("password_reset/", data);
                //console.log(store.state.typeError);
            }
        },
    };
</script>

<style>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.4s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
  {
    opacity: 0;
  }
</style>