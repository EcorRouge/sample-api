# How to Run and Deploy

## Pre-requisites

1. NodeJS: Serverless project and its plugins depend upon node. Its good to update node to a latest stable version.

I use `nvm` to install and maintain multiple `npm` versions. Using `nvm` install `12.8.1` or above.

2. Docker

Docker is used to download and package python requirements and also for `localstack` which is useful in testing.

3. AWS CLI

```bash
pip3 install awscli --upgrade --user
```

## Installing project dependencies

** To install project dependencies, you can just run install.sh **

```sh install.sh```

## Deploy Project

To deploy the project please use the `deploy.py` script. It is a deployment manager and it can initialize a new environment
or look for updates and deploy updates to your environment.

```python deploy.py {stage}```

Here `stage` refers to the environment you wish to deploy to. Please make sure a `config.{stage}.json` file, (for example `config.test.json`)
exists and has key-value pairs similar to `config.example.json`.

### Install dependencies manually

1. Install Serverless plugin to manage python requirements:

`sls plugin install -n serverless-python-requirements`

2. Create a virtual environment and install python dependencies for local development

```bash
virtualenv -p /usr/bin/python3.6 ~/.virtualenv/prolanceEnv
source ~/.virtualenv/prolanceEnv/bin/activate
pip install -r requirements-dev.txt
```

3. Also install pseudo-parameters plugin which gives easy access to AWS Cloudformation variables like {AWS::AccountId}

`sls plugin install -n serverless-pseudo-parameters`

4. Install `sls plugin install -n serverless-prune-plugin`

This plugin helps purge previous versions of functions from AWS

## Create Tables

```bash
python data_dynamodb/create_tables.py prod
```

This creates all the tables in dynamodb and MySQL instance in AWS region in `config.prod.json`, for stage `prod`.

Please note, for mysql models defined under `tables/`, you can optionally add a `create_after` attribute in the class,
which can be set to the table name of another table, which has to be created before creating this table.