"use strict";

import Axios from "axios";
import Store from "../store";

/**
 * Beginning of the server's url.
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

export default {
   
    post (route, data, config = {}) {
        console.log("couou");
        console.log(route);
        console.log(baseUrl);
        //console.assert(typeof route === "string");
        //console.assert(typeof data === "object" && data !== null);
        //console.assert(typeof config === "object" && config !== null);
        publicInstance.post(baseUrl+route, data, config)
            .then(response => console.log("oui"))
            .catch(error => {
                if (Axios.isCancel(error)) return;
                console.log("non")
            });
    }

};