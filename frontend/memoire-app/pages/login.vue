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
                    <v-card-text>
                        <v-form>
                        <v-text-field
                            v-model="email"
                            label="email"
                            name="email"
                            prepend-icon="mdi-account"
                            type="text"
                            :error-messages="emailErrors"
                            @input="$v.email.$touch()"
                            @blur="$v.email.$touch()"
                        />

                        <v-text-field
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
                        <v-btn color="green" class="white--text"  @click="submit" :disabled="$v.$invalid">Login</v-btn>
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

        forget_pwd: false,
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
      submit () {
        this.$v.$touch()
        //console.log(this.$v.$touch());
      }
    }
    
}
</script>