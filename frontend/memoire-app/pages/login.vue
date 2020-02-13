<template>
    <v-container fluid class="fill-height">
        <v-row align="center">
            <v-col offset="1" offset-sm="3" cols="10" sm="6">
                <!-- Classic Login -->
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
                            :error-messages="passwordErrors"
                            @input="$v.password.$touch()"
                            @blur="$v.password.$touch()"
                        />
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <a @click="forget_pwd=true">Mot de passe oublié ?</a>
                        <v-spacer />
                        <v-btn color="green" class="white--text"  @click="submit" :disabled="$v.email.$invalid || $v.password.$invalid" >Se connecter</v-btn>
                    </v-card-actions>
                    <v-divider></v-divider>
                    <v-card-actions class="d-flex align-center justify-center">
                        <p class="ma-0"> 
                            <a @click="unamur=true">Se connecter avec ses identifiants UNamur</a>
                        </p>
                    </v-card-actions>
                </v-card>

                <!--Unamur Login-->
                <v-dialog
                    v-model="unamur"
                    width="500"
                    class="elevation-12">
                    <v-card class="elevation-12">
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
                        v-if="error !=null"
                        >
                        {{error}}
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
                            label="Password"
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
                </v-card>
    </v-dialog>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, email } from 'vuelidate/lib/validators'
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

        //User's data
        email: '',
        password: '',

        eid_unamur:'',
        password_unamur: '',

        //Boolean
        forget_pwd: false,
        unamur: false,

        //Error message
        error: null
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
            console.log(this.$v.$invalid);
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
        //Checking if user filled correctly the form
            this.$v.$touch();

            console.log(this.$v.$touch())

            //Axios request to check if data is correct
            if(!this.unamur){
                let data = {"mail": this.email, "password": this.password}
                try {
                    await this.$auth.loginWith('local',{data: data})
                } catch (e) {    
                    this.error = "Il semblerait que les identifiants ne soient pas corrects"
                }
            }else{
                let data = {"eid": this.eid_unamur, "password": this.password_unamur}
                try {
                    await this.$auth.loginWith('unamur',{data: data});
                } catch (e) {    
                    this.error = "Il semblerait que les identifiants ne soient pas corrects"
                }
            }

        }
    },
    
}
</script>