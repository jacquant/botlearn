<template>
    <v-container fluid class="fill-height">
        <v-row align="center">
            <v-col offset="1" offset-sm="3" cols="10" sm="6">
                <!-- Classic Login -->
            <transition name="fade"  mode="out-in">
                <v-card class="elevation-12"
                        v-if="!unamur"
                        key="classique"
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
                        text
                        prominent
                        type="error"
                        icon="mdi-alert"
                        v-if="error"
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
                        />

                        <v-text-field
                            v-model="password"
                            id="password"
                            label="Mot de passe"
                            name="password"
                            prepend-icon="mdi-lock"
                            type="password"
                            :error-messages="passwordErrors"
                            @input="$v.password.$touch()"
                            @blur="$v.password.$touch()"
                        />
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on }">
                                <v-icon color="green" dark v-on="on">mdi-information-outline</v-icon>
                            </template>
                            <span>Si tu as oublié ton mot de passe, tu prux aller le modifier sur le <b>site</b>.</span>
                        </v-tooltip>
                        <v-spacer />
                        <v-btn color="green" class="white--text"  @click="submit" :disabled="$v.email.$invalid || $v.password.$invalid" >Se connecter</v-btn>
                    </v-card-actions>
                    <v-divider></v-divider>
                    <v-card-actions class="d-flex align-center justify-center">
                        <p class="ma-0"> 
                            <a @click="unamur= !unamur">Se connecter avec ses identifiants UNamur</a>
                        </p>
                    </v-card-actions>
                </v-card>

                <!--Unamur Login>-->
                
                <v-card class="elevation-12"
                        v-if="unamur"
                        key="unamur"
                        
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
                    text
                    prominent
                    type="error"
                    icon="mdi-alert"
                    v-if="error"
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
                    />

                    <v-text-field
                        v-model="password_unamur"
                        id="password"
                        label="Mot de passe"
                        name="password"
                        prepend-icon="mdi-lock"
                        type="password"
                        :error-messages="passwordUnamurErrors"
                        @input="$v.password_unamur.$touch()"
                        @blur="$v.password_unamur.$touch()"
                        
                    />
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn color="green" class="white--text"  @click="submit" :disabled="$v.eid_unamur.$invalid || $v.password_unamur.$invalid">Se connecter</v-btn>
                </v-card-actions>
                    <v-divider></v-divider>
                <v-card-actions class="d-flex align-center justify-center">
                    <p class="ma-0"> 
                        <a @click="unamur= !unamur">Se connecter avec son propre compte.</a>
                    </p>
                </v-card-actions>
                </v-card>
             </transition>

                <v-overlay :value="overlay">
                    <v-progress-circular indeterminate size="64"></v-progress-circular>
                </v-overlay>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, email } from 'vuelidate/lib/validators'
import axios from "axios"



export default {

    mixins: [validationMixin],

    // ================================================================================================== ==
    // Validations
    // Rules for each input
    // ================================================================================================== ==
    validations: {

        email: { required, email },
        eid_unamur: {required, between: maxLength(10)},
        password:{required},
        password_unamur:{required}

    },

    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
    data: () => ({

        //url
        url: "http://localhost:8080/api/",

        //User's data
        email: '',
        password: '',

        eid_unamur:'',
        password_unamur: '',

        //Boolean
        forget_pwd: false,
        unamur: false,

        error: false,

        overlay:false,

    }),

    // ================================================================================================== ==
    // Computed
    // ================================================================================================== ==
    computed:{
        /**
         * Indicates if the identifiers are not correct.
         * @private
         * @returns {errors: tab}
        */
        emailErrors () {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Une adresse email valide est requise !')
            !this.$v.email.required && errors.push('Une adresse email doit être indiquée')
            return errors
      },

        /**
         * Indicates if there is a password written.
         * @private
         * @returns {errors: tab}
        */
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push("un mot de passe est requis")
            return errors
        },

        /**
         * Indicates if the eid is not correct.
         * @private
         * @returns {errors: tab}
        */
        eidErrors () {
            const errors = []
            if (!this.$v.eid_unamur.$dirty) return errors
            !this.$v.eid_unamur.between && errors.push("L'eid fait maximum 10 caractères")
            !this.$v.eid_unamur.required && errors.push('Un eid est requis')
            return errors
        },
        /**
         * Indicates if there is a password written.
         * @private
         * @returns {errors: tab}
        */
        passwordUnamurErrors () {
            const errors = []
            if (!this.$v.password_unamur.$dirty) return errors
            !this.$v.password_unamur.required && errors.push("un mot de passe est requis")
            return errors
        },
           
    },

    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods: {
        async submit () {
            this.overlay = !this.overlay;
            let self = this;
            if (!this.unamur){
                await axios.post(this.url + 'token/login/', {
                    "mail": this.email,
                    "password": this.password
                })
                .then(function (response) {
                    self.error = false;
                    self.$router.push("/bot?token="+response.data.access);
                })
                .catch(function (error) {
                    self.overlay = !self.overlay;
                    self.error = true;
                    console.log(error);
                });
            }else{
                await axios.post(this.url + 'token/login_by_unamur/', {
                    "eid": this.eid_unamur,
                    "password": this.password_unamur
                })
                .then(function (response) {
                    self.error = false,
                    self.$router.push("/bot?token="+response.data.access);
                })
                .catch(function (error) {
                    self.overlay = !self.overlay;
                    self.error = true;
                    console.log(error);
                });
            }

        },
    },
}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>