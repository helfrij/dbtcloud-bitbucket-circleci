# dbtcloud-bitbucket-circleci

This is a first-pass project at implementing continuous integration (CI) for a dbt Cloud project using BitBucket managed code and CircleCI.

## dbt Cloud setup

We can manually setup a dbt Cloud environment and jobs with the following steps:

1. Create a Continuous Integration environment.
   - Environment type = deployment
   - Deployment type = general
   - dbt version = 1.7
2. Create a CI job in the environment and note the job ID in the url.
   - Commands = dbt build or anything (these will be overridden in the CircleCI script)
   - Defer to production = yes
   - Target name = ci or anything (this is overridden in the CircleCI script)
   - Run timeout = 0/Never
   - Threads = 4 or anything (this is overridden in the CircleCI script)
3. Create a cleanup job in the environment and note the job ID in the url.
   - Commands = dbt build or anything (these will be overridden in the CircleCI script)
   - Defer to production = yes
   - Target name = ci or anything (this is overridden in the CircleCI script)
   - Run timeout = 0/Never
   - Threads = 4 or anything (this is overridden in the CircleCI script)
4. Create a service token for CircleCI to use to be able to access the dbt Cloud api.

## CircleCI setup

We use CircleCI to trigger the dbt Cloud jobs through their api. We can setup the pipeline with the following steps:

1. Create a config.yml file that uses the dbt Cloud api to trigger job runs using the job ids of the created dbt Cloud jobs.
2. Log in to CircleCI and enable the integration with the BitBucket repository.
3. Add the following environment variables to the CircleCI project:
   - DBT_CLOUD_BASE_URL
   - DBT_CLOUD_ACCOUNT_ID
   - DBT_CLOUD_CI_JOB_ID
   - DBT_CLOUD_CLEANUP_JOB_ID
   - DBT_CLOUD_CIRCLECI_SERVICE_TOKEN
