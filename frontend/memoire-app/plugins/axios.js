// ================================================================================================== ==
// Managing expired token
// ================================================================================================== ==

export default function ({ $axios, app, redirect }) {
    $axios.onRequest(config => {
      console.log('Making request to ' + config.url)
    })
  
    $axios.onError((error) => {
        const code = parseInt(error.response && error.response.status)
        if (code === 401) {
          app.$auth.logout()
          redirect('/login')
        }
      })
  }