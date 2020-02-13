import colors from 'vuetify/es5/util/colors'

export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: process.env.npm_package_description || ''}
    ],
    script:[
      { src:"https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"},
      { src: "js/chatbot.js"},
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
      {rel: "stylesheet", href: "css/chatbot.css" }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: {color: '#fff'},
  /*
  ** Global CSS
  */
  css: [],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~/plugins/auth',
    '~/plugins/axios',
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxt/typescript-build',
    '@nuxtjs/vuetify',
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxt/http'
  ],
  /*
  ** Auth module configuration
  ** See https://auth.nuxtjs.org/
  ** https://github.com/nuxt-community/auth-module/pull/361
  */

  auth: {
    plugins: ['~/plugins/auth.js'],
    strategies: {
      local: {
        _scheme: 'local',
        endpoints: {
          login: { url: 'token/login/', method: 'post', propertyName: 'access', refresh_token:'refresh'},
          refresh: { url: '/token/refresh', method: 'post' },
          logout: false,
          user: false,
        },
        tokenRequired: true,
        // tokenType: 'bearer'
      },
      unamur: {
        _scheme: 'local',
        endpoints: {
          login: { url: 'token/login_by_unamur/', method: 'post', propertyName: 'access', refresh_token:'refresh'},
          logout: false,
          user: false,
        },
        tokenRequired: true,
        // tokenType: 'bearer'
      }
    },
    watchLoggedIn: true,
    resetOnError: true,
    rewriteRedirects: true,
    cookie: {
      prefix: 'auth.',
      options: {
        path: '/',
      },
    },
  },

  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: "http://localhost:8080/api/"
  },
  /*
  ** Http module configuration
  ** See https://http.nuxtjs.org/api/
  */
  http: {
    baseURL: "http://localhost:8080/api/"
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  }
}
