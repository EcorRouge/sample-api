# SampleProject
The Serverless Python API for the web application.

# Quickstart

If you are already familiar with deploying the project, here is a quickstart guide to deploy and update your environment

```shell script
sh install.sh    # install pre-requisites
python deploy.py {stage}    # initialize or look for updates and deploy
```

Please make sure `config.{stage}.json` has required key-value pairs. Please refer to `config.example.json` to look at sample values.

Test API: [https://50ioygefti.execute-api.us-east-1.amazonaws.com/test](https://50ioygefti.execute-api.us-east-1.amazonaws.com/test)

# Contents

[How to Run and Deploy](docs/How_to_Run_and_Deploy.md)

[Configuring Deployment and How to Deploy Services](docs/Configuring_Deployment_and_How_to_Deploy_Services.md)

[Configure Authentication and Authorization](docs/Configure_Authentication_and_Authorization.md)

[cURL statements](docs/cURL_Statements.md)

[Troubleshooting](#Troubleshooting)

[Implementation](#Implementation)

[Deployment Scripts](#Deployment-Scripts)

[Testing](#Testing)

[Next Steps](#Next-Steps)

[Conclusion](#Conclusion)