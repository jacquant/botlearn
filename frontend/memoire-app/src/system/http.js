import Axios from "axios";
import Router from "./router";
import Store from "../store/store";
import JwtDecode from "jwt-decode";
import router from "./router"

/**
 * Base url of the server.
 * @private
 * @constant {string} Http#baseUrl
 */
const baseUrl = "http://localhost:8080/api/";

/**
 * Public instance of axios to manage request send in the application.
 * @private
 * @constant {AxiosInstance} Http#publicInstance
 */
const publicInstance = Axios.create();


/**
 * Updates if necessary the access token of the user.
 * @private
 * @function Http#renewAccessToken
 * @returns {Promise}
 */
function renewAccessToken() {

    const access = Store.state.accessToken;
    if (access != null && JwtDecode(access).exp * 1000 - Date.now() <= 0) {
        const refresh = Store.state.refreshToken;

        if (refresh === null || JwtDecode(refresh).exp * 1000 - Date.now() <= 0){
            Store.commit("logout"); 
            return Promise.reject();
        }else{
             return Axios.post(baseUrl+"token/refresh/", {"refresh": refresh})
            .then(response => {
                Store.commit("accessToken", response.data.access);
                return Promise.resolve();
            })
            .catch(() => {
                Store.commit("logout"); 
                return Promise.reject();
            });
        }
    } else return Promise.resolve();
}
//After each load of a page, try to reload the token
renewAccessToken();



// ================================================================================================================== ==
// PUBLIC METHODS
// ================================================================================================================== ==

export default {

    //HttpResponseManager,
    //renewAccessToken,

    /**
     * Executes a delete request on the server.
     * @function Http#delete
     * @param {string} route - The relative route for the request.
     * @param {Http.HttpResponseManager} manager - Manager of request response.
     * @param {object} [config] - Additional configuration for the request.
     * @returns {Promise<void>}
     */
    delete (route, manager, config = {}) {
        publicInstance.delete(baseUrl+route, config)
            .then(response => manager.execute(response.status, response.data))
            .catch(error => {
                if (Axios.isCancel(error)) return;
                manager.execute(error.response.status, error.response.data)
            });
    },

    /**
     * Executes a get request on the server.
     * @function Http#get
     * @param {string} route - The relative route for the request.
     * @param {Http.HttpResponseManager} manager - Manager of request response.
     * @param {object} [config] - Additional configuration for the request.
     * @returns {Promise<void>}
     */
    get (route, config = {}) {
        let data=null
        //Get info User
        if(route.includes("user")){
            publicInstance.get(baseUrl+route, config)
                .then(response => Store.commit.userInformation(response.data))
                .catch(error => {
                    Store.commit("internalError", true)
                });
        //Get All Tps        
        }else if(route.includes("sessions/all/")){
            data = publicInstance.get(baseUrl+route, config)
                .then(response => {return response})
                .catch(error => {
                    Store.commit("internalError", true)
                });
        }else if(route.includes("exercises/by_session/")){
            data = publicInstance.get(baseUrl+route, config)
                .then(response => {return response})
                .catch(error => {
                    Store.commit("internalError", true)
                });
        }
        return data;
    },

    /**
     * Executes a post request on the server.
     * @function Http#post
     * @param {string} route - The relative route for the request.
     * @param {object} data - The data to send in the request.
     * @param {Http.HttpResponseManager} manager - Manager of request response.
     * @param {object} [config] - Additional configuration for the request.
     * @returns {Promise<void>}
     */
    post (route, data, config = {}) {
        //Login Requests
        if(route.includes("token") && !route.includes("validate")){
            publicInstance.post(baseUrl+route, data, config)
                .then(function(response){
                    Store.commit("login",response.data)
                    publicInstance.get(baseUrl + "user/get/", {headers:{ 'Authorization': 'Bearer '+ Store.state.accessToken}})
                    .then(function(responseUser){
                        Store.commit("userInformation", responseUser.data);
                        //router.push("/");
                        router.back();
                    })
                })
                .catch(error => {
                    //if (Axios.isCancel(error)) return;
                    Store.commit("internalError", true)
                });

        }else if(route.includes("password_reset") && route.includes("confirm")){
            publicInstance.post(baseUrl+route, data, config)
            .then(function(response){
                Store.commit("internalSucceed", true)
                router.push("/login");
            })
            .catch(error => {
                Store.commit("internalError", true)
            });

        }else if(route.includes("password_reset") && route.includes("validate_token")){
            publicInstance.post(baseUrl+route, data, config)
            .then(function(response){
                Store.commit("internalSucceed", true)
            })
            .catch(error => {
                router.push("/login");
            });

        }else if(route.includes("password_reset")){
            publicInstance.post(baseUrl+route, data, config)
            .then(response => {Store.commit("internalSucceed", true)})
            .catch(error => {
                Store.commit("internalError", true)
            });
        }
    },

    /**
     * Executes a put request on the server.
     * @function Http#put
     * @param {string} route - The relative route for the request.
     * @param {object} data - The data to send in the request.
     * @param {Http.HttpResponseManager} manager - Manager of request response.
     * @param {object} [config] - Additional configuration for the request.
     * @returns {Promise<void>}
     */
    put (route, data, manager, config = {}) {
        publicInstance.put(baseUrl+route, data, config)
            .then(response => manager.execute(response.status, response.data))
            .catch(error => {
                if (Axios.isCancel(error)) return;
                manager.execute(error.response.status, error.response.data)
            });
    }

};
