/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'simoennova.eu', // the auth0 domain prefix
    audience: 'coffeeapi', // the audience set for the auth0 app
    clientId: 'SohP41DjGKBhd3pW2eL7GKwfR6dsrjEi', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
