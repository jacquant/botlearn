"use strict";

import Vue from "vue";
import Vuex from "vuex";
import router from "../system/router";

Vue.use(Vuex);

// ================================================================================================================== ==
// Constantes
// ================================================================================================================== ==

const KEY_ACCESS_TOKEN = "accessToken";
const KEY_REFRESH_TOKEN = "refreshToken";
const KEY_USER_INFORMATION = "infoUser";

// ================================================================================================================== ==
// Méthodes privées
// ================================================================================================================== ==

/**
 * Loads a token from the local storage and verify its validity.
 * @private
 * @function Store#loadToken
 * @param {string} key - The key associated to the token.
 * @returns {string|null}
 */
function loadToken(key) {
    return localStorage.getItem(key);
}

// ---------------------------------------------------------------------------------------------------------- --
// Store
// ---------------------------------------------------------------------------------------------------------- --
export default new Vuex.Store({
    // ---------------------------------------------------------------------------------------------------------- --
    // State
    // ---------------------------------------------------------------------------------------------------------- --
    state: {
        /**
         * Token used for each call to the API that requires a connection key.
         * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
         * @readonly
         * @member {string|null} Store#accessToken
         */
        accessToken: loadToken(KEY_ACCESS_TOKEN),

        /**
         * [STATE] Indicates if an error occurs on the server during an API call.
         * @readonly
         * @member {boolean} Store#internalError
         */
        internalError: false,

        /**
         * [STATE] Indicates the error's type during an API call.
         * @readonly
         * @member {object} Store#typeError
         */
        typeError: null,

        /**
         * [STATE] Indicates if an API call succeed.
         * @readonly
         * @member {boolean} Store#internalSucceed
         */
        internalSucceed: false,

        /**
         * Token used to renew the access token once it expires.
         * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
         * @readonly
         * @member {string|null} Store#refreshToken
         */
        refreshToken: loadToken(KEY_REFRESH_TOKEN),

        /**
         * Contains the user's information.
         * It's primarily saved in the JavaScript local store to avoid losing it when reloading the page.
         * @readonly
         * @member {UserInfo|null} Store#userInformation
         */
        userInformation: JSON.parse(localStorage.getItem("infoUser") || "{}")
    },

    // ---------------------------------------------------------------------------------------------------------- --
    // MUTATIONS
    // ---------------------------------------------------------------------------------------------------------- --
    mutations: {
        /**
         * [MUTATION] Updates the access token.
         * @function Store#accessToken
         * @param state
         * @param {string|null} payload - The new access token.
         */
        accessToken(state, payload) {
            localStorage.setItem(KEY_ACCESS_TOKEN, payload);
            state.accessToken = payload;
        },

        /**
         * [MUTATION] Change the state of the *internalError* member of the store.
         * @function Store#internalError
         * @param state
         * @param {boolean} payload - The new state of the *internalError* member.
         */
        internalError(state, payload) {
            state.internalError = payload;
            //reset the succeed if it occurred before
            state.internalSucceed = false;
        },

        /**
         * [MUTATION] Change the state of the *TypeError* member of the store.
         * @function Store#typeError
         * @param state
         * @param {object} payload - The new state of the *typeError* member.
         */
        typeError(state, payload) {
            state.typeError = payload;
        },

        /**
         * [MUTATION] Change the state of the *internalSucceed* member of the store.
         * @function Store#internalSucceed
         * @param state
         * @param {boolean} payload - The new state of the *internalSucceed* member.
         */
        internalSucceed(state, payload) {
            state.internalSucceed = payload;
            //reset the error if it occurred before
            state.internalError = false;
        },

        /**
         * [MUTATION] Updates the access token and the refresh token to login the user.
         * @function Store#login
         * @param state
         * @param {object} payload - The login information.
         * @param {string} payload.access - The access token.
         * @param {string} payload.refresh - The refresh token.
         */
        login(state, payload) {
            // Update the local storage to preserve in case of reloading page
            localStorage.setItem(KEY_ACCESS_TOKEN, payload.access);
            localStorage.setItem(KEY_REFRESH_TOKEN, payload.refresh);

            // Update the store to actualise the information
            state.accessToken = payload.access;
            state.refreshToken = payload.refresh;
        },

        /**
         * [MUTATION] Removes the access token, the refresh token and the user's information to logout him.
         * @function Store#logout
         */
        async logout(state) {
            // Update the local storage to preserve in case of reloading page
            localStorage.removeItem(KEY_ACCESS_TOKEN);
            localStorage.removeItem(KEY_REFRESH_TOKEN);
            localStorage.removeItem(KEY_USER_INFORMATION);

            // Update the store to actualise the information
            state.accessToken = undefined;
            state.refreshToken = undefined;
            state.userInformation = undefined;

            await router.push("/login")
        },

        /**
         * [MUTATION] Updates the user's information.
         * @function Store#userInformation
         * @param state
         * @param {UserInfo} payload - The new user's information.
         */
        userInformation(state, payload) {
            // Update the local storage to preserve in case of reloading page
            localStorage.setItem(KEY_USER_INFORMATION, JSON.stringify(payload));

            // Update the store to actualise the information
            state.userInformation = payload;
        }
    },

    // ---------------------------------------------------------------------------------------------------------- --
    // Getters
    // ---------------------------------------------------------------------------------------------------------- --
    getters: {
        /**
         * [GETTER] Indicates if the user is connected.
         * @function Store#isConnected
         * @returns {boolean}
         */
        isConnected: state => state.accessToken != null,

    /**
     * [GETTER] Indicates if the user is in the satff.
     * @function Store#isStaff
     * @returns {boolean}
     */
    isStaff: state =>
      state.userInformation !== null && state.userInformation.is_staff
        ? true
        : false
  }
});
