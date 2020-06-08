# Configuring Deployment

Before deploying, a config file with secrets like the AUTH0_CLIENT_ID, can be created, which will be used to set Runtime OS environment variables used by the lambda functions.

This is an example content of the JSON file:

```json
{
  "REGION": "us-east-1",
  "AUTH0_CLIENT_ID": "ThABFIgh99ZideKcy-1WmNC8E6Js5Rn4",
  "AUTH0_CLIENT_SECRET": "hiY3oPJSO-ax5OtXjnbFiaNaup479qGWhTURwxCUNAukX3naPGutOTITpI4vUJV_",
  "AUTH0_MANAGEMENT_API_CLIENT_ID": "bfkODTJWm3O37eEokHzSChnQzu6gbkcS",
  "AUTH0_MANAGEMENT_API_CLIENT_SECRET": "ZiYd8fjhKl0MboUpK6BRwx0qcDKN9WS99Ab06_EKP3ABgrZRNMXUZxOn0Sf5BGvY",
  "AUTH0_AUDIENCE": "https://neotheicebird.auth0.com/api/v2/",
  "AUTH0_DOMAIN": "https://neotheicebird.auth0.com",
  "AUTH0_CONNECTION": "Username-Password-Authentication",
  "SIGNUP_ORIGIN_URL": "*",
  "S3_UPLOADS_BUCKET_NAME": "test-brand-logos-new",
  "ROLLBAR_SECRET": "7e87a2dcd94646818928277ac4700000",
  "EMAIL_TRANSMITTER_SOURCE": "project@email.com",
  "WEBAPP_BASE_URL": "http://localhost:8080"
}
```

`AUTH0_CLIENT_ID` and `AUTH0_CLIENT_SECRET` are found under `Applications > testfdc01` in our Apps' `settings` tab.

`AUTH0_MANAGEMENT_API_CLIENT_ID` and `AUTH0_MANAGEMENT_API_CLIENT_SECRET` are found under `Applications > testfdc01-management` in our Apps' `settings` tab.

`REGION` refers to `dynamodb` and `lambda` AWS region.

`USERS_MASTER_PASSWORD` is a secret that is used to generate Auth0 user profiles' passwords upon signup. If this info is lost or changed, exisiting users might have to go through a reset password flow (NotImplementedYet) to get access to prolance again.

`SIGNUP_ORIGIN_URL` is the URI from which `POST /signup` originates. If it is set to any value other than "*", the handler checks if the request originates from the same domain and raises error if not.

`S3_UPLOADS_BUCKET_NAME` is the S3 bucket to which supplier logo PNGs are uploaded. It can be used for other uploads with code changes to repository.

`ROLLBAR_SECRET` is the secret generated in Rollbar upon setup. Please refer to [How_to_Run_and_Deploy][./How_to_Run_and_Deploy.md]

`EMAIL_TRANSMITTER_SOURCE` email source of SES emails

`WEBAPP_BASE_URL` the URL of where the Vue app is deployed to (like https://www.projectname.com)

## Deploy Serverless Application to AWS

The simplest way to deploy is to use `deploy.py`. Before running `deploy.py`, please make sure `SampleProject/config.{stage}.json`
has all the environment variables defined. Also edit `public_key.{stage}` to add Auth0 public key data.

To deploy all services please run

`python deploy.py {stage}` where {stage} could be dev, test, prod etc based on the config.{stage}.json files generated.

SampleProject consists of multiple services, and they can be deployed all at once using the following command:

```bash
# For Dev or Staging or Test environments
python deploy_all_services.py --stage {stage}
```
The configuration of any stage can be done to the file `config.{STAGE}.json`. Please refer to the section [Configuring Deployment](#Configuring Deployment) for more details on how to configure a stage.

If you wish to deploy to production, we can set the AWS_PROFILE environment variable

```bash
AWS_PROFILE=PRODUCTION_PROFILE_NAME python deploy_all_services.py --stage prod
```

The above command takes some time to complete and always deploys all the services starting with the Auth API.

If changes were made only to one or few services, then they can be individually updated using the following command:

```bash
sls deploy -v --stage dev
```

Or for Production deployment

```bash
AWS_PROFILE=PRODUCTION_PROFILE_NAME sls deploy -v --stage prod
```

Pls note, adding environment variable `AWS_PROFILE` can help us choose the AWS Profile using which we deploy. This can help us deploy to multiple AWS Accounts.
Please ignore the AWS_PROFILE part if not required.