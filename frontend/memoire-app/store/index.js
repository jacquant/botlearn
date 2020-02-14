"use strict";
//We can delete it, not use it
import Vuex from 'vuex';
import VuexPersist from 'vuex-persist'

// ================================================================================================================== ==
// Usefull Constants
// ================================================================================================================== ==

const KEY_ACCESS_TOKEN = "accessToken";
const KEY_REFRESH_TOKEN = "refreshToken";
const KEY_USER_INFORMATION = "infoUser";

let vuexLocalStorage = null;

if (process.browser) {
    vuexLocalStorage = new VuexPersist({
      key: 'vuex', // The key to store the state on in the storage provider.
      storage: window.localStorage, // or window.sessionStorage or localForage
    })
}


/**
 * Check the validity of the token
 * @private
 * @param {string} key - The key associated to the token.
 * @returns {string|null}
 */
function loadToken (key) {}

const createStore = () => {
    return new Vuex.Store({

        // ---------------------------------------------------------------------------------------------------------- --
        // STATE
        // ---------------------------------------------------------------------------------------------------------- --
        state: {

            /**
             * Token used for each call to the API that requires a connection key.
             * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
             * @readonly
             * @member {string|null} Store#accessToken
             */
            accessToken: null,


            /**
             * Token used to renew the access token once it expires.
             * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
             * @readonly
             * @member {string|null} Store#refreshToken
             */
            refreshToken: null,

            /**
             * Contains the user's information.
             * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
             * @readonly
             * @member {UserInfo|null} Store#userInformation
             */
            userInformation: null

        },

        mutations: {
            /*
            *
            *
            * */
            accessToken (state, payload) {
                //this.$store.state.auth.user.setLocalStorage(KEY_ACCESS_TOKEN, payload);
                state.accessToken = payload;
            },

            /**
             * Update tokens' user
             * @param {object} payload - The login information.
             * @param {string} payload.access - The access token.
             * @param {string} payload.refresh - The refresh token.
             */
            login (state, payload) {

                // Update the store to actualise the information
                state.accessToken = payload.access;
                state.refreshToken = payload.refresh;
                state.userInformation = {permissions: []};
            },

        },

        getters: {
            /**
             * Check if the user is connected
             * @returns {boolean}
             */
            isConnected: state => state.accessToken !== null,

            isAuthenticated(state) {
                return state.auth.loggedIn
              },
            
              loggedInUser(state) {
                return state.auth.user
              }

        },
        plugins: process.browser ? [vuexLocalStorage.plugin] : []


    });
}

export default createStore