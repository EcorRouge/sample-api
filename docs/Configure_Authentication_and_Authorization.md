# Configure Authentication and Authorization

1. Create an Auth0 account at auth0.com

![auth0_signup](./images/auth0_signup.png)
![auth0_signup_2](./images/auth0_signup_2.png)

2. While signing up, we would be creating a domain (e.g. `projectname.auth0.com`).

![auth0_domain](./images/auth0_domain.png)

3. Under `Applications` to create new app, click on `Create Application` and give it a name (`projectname`). Select `Single Page Web Application` (SPA).

![auth0_create_app](./images/auth0_create_app.png)
![auth0_create_app_2](./images/auth0_create_app_2.png)

4. Under the current app's `settings` tab, scroll down and click on `Show Advanced settings` and click on `Certificates` to get the public key with which the serverless service is going to sign the tokens.
Copy the contents on signing `Signing Certificate` and paste in a local file named `public_key` in the project folder.

![auth0_signing_cert](./images/auth0_signing_cert.png)

5. Click on `Grant Types` and check `Password`, uncheck all the other grant types and save changes.

![auth0_grant_types](./images/auth0_grant_types.png)

6. To configure the database to be used, click on `Connections > Database` and click on the default database `Username-Password-Authentication`.

![auth0_database](./images/auth0_database.png)

a. Settings like min and max password length, password policy, can be configured here.

b. Under applications tab we should see `projectname` enabled, if not please `enable` application.

![auth0_database_app_enabled](./images/auth0_database_app_enabled.png)

c. clicking `Try connection` should work with a login screen.

![auth0_try_connection_works](./images/auth0_try_connection_works.png)

7. To make password grant work, we have to set `Default Audience` and `Default Directory`, to do that:

a. Go to account settings (top right under your username)

![auth0_account_settings](./images/auth0_account_settings.png)

b. On the general tab scroll down to the API Authorization Settings section

![auth0_api_settings](./images/auth0_api_settings.png)

c. Default Audience would be your API identifier. This can be found under `APIs > Auth0 Management API`. `API Audience` is the identifier (`https://projectname.auth0.com/api/v2/`) 

d. Default Directory would be your connection such as database connection name (`Username-Password-Authentication`)

e. Paste values and save.
Ref: https://stackoverflow.com/questions/41626602/how-to-make-a-username-password-request-with-auth0-custom-api-getting-error-un

![auth0_audience](./images/auth0_audience.png)


8. CORS URLs: Under `Applications > projectname > Settings` scroll down to `Allowed Origins (CORS)` and enter any valid URL from which Auth0 endpoints are accessed (`http://localhost:8080/signin`).

Allowed Origins are URLs that will be allowed to make requests from JavaScript to Auth0 API (typically used with CORS). By default, all your callback URLs will be allowed.

Leave it empty, if you are in development.

![auth0_cors](./images/auth0_cors.png)

9. To enable users ability to create/delete their accounts, we need to setup another application which is a machine-to-machine application. To do that:

 a. Click on applications and create a new application

 b. Name it (`projectname-management`), select application type to be `machine-to-machine` (M2M), select `Auth0 API` and add scopes. Required scopes are `update:users, delete:users, create:users, read:users`.
 
 ![auth0_m2m](./images/auth0_m2m.png)
 ![auth0_scopes](./images/auth0_scopes.png)
 
 
 10. Copy credentials like SPA client_id, client_secret, M2M client_id, client_secret, audience, domain, certificate from Auth0 to your `config.{stage}.json` file.