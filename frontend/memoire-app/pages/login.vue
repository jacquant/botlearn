<template>
    <v-container fluid class="fill-height">
        <v-row align="center">
            <v-col offset="1" offset-sm="3" cols="10" sm="6">
                <v-card class="elevation-12">
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
                        v-if="error !=null"
                        >
                        {{error}}
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
                            label="Password"
                            name="password"
                            prepend-icon="mdi-lock"
                            type="password"
                        />
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer />
                        <v-btn color="green" class="white--text"  @click="submit" :disabled="$v.$invalid" >Login</v-btn>
                    </v-card-actions>
                    <v-divider></v-divider>
                    <v-card-actions class="d-flex align-center justify-center">
                        <p class="ma-0"><a @click="forget_pwd=true">Mot de passe oublié ?</a></p>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
export default {

    mixins: [validationMixin],

    // ================================================================================================== ==
    // Validations
    // Rules for each input
    // ================================================================================================== ==
    validations: {

        email: { required, email },

    },

    // ================================================================================================== ==
    // Data
    // ================================================================================================== ==
    data: () => ({

        email: '',
        password: '',

        forget_pwd: false,

        error: null
    }),

    // ================================================================================================== ==
    // Computed
    // ================================================================================================== ==
    computed:{
        /**
         * Indicates if the identifiers are not correct.
         * @private
         * @returns errors: tab
        */
        emailErrors () {
        const errors = []
        if (!this.$v.email.$dirty) return errors
        !this.$v.email.email && errors.push('Une adresse email valide est requise !')
        !this.$v.email.required && errors.push('Une adresse email doit être indiquée')
        return errors
      }
    },

    // ================================================================================================== ==
    // Methods
    // ================================================================================================== ==
    methods: {
      async submit () {

        this.$v.$touch()

        let data = {"mail": this.email, "password": this.password}

        try {
            await this.$auth.loginWith('local',{data: data})
        } catch (e) {    
            this.error = "Il semblerait que les identifiants ne soient pas corrects"
        }

      

        //https://auth.nuxtjs.org/api/storage.html#local-state
        //Save context
        /*await this.$axios.$post("token/login/", data)  
            .then(function(response) {
                self.$auth.$storage.setLocalStorage("refresh", response.refresh, false);
                self.$auth.$storage.setLocalStorage("access", response.access, false);
                //self.$router.push('/')
            })
            .catch(error => {
                    console.log(error)
                });*/
        //https://auth.nuxtjs.org/api/auth.html#loggedin

        }
    }
    
}
</script>