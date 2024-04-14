import argparse
import json
import requests
import time

import api


def trigger_ci_job_run_service(base_url, account_id, ci_job_id, service_token, git_branch, schema_name):
    return api.trigger_job_run_api(
        base_url=base_url, 
        account_id=account_id, 
        job_id=ci_job_id, 
        service_token=service_token,
        data={
            'cause': 'Triggered by CircleCI',
            'git_branch': git_branch,
            'schema_override': schema_name,
            'threads_override': 4,
            'target_name_override': 'ci',
            'steps_override': [
                'dbt build --select state:modified+'
            ]
        }
    )


def trigger_cleanup_job_run_service(base_url, account_id, cleanup_job_id, service_token, git_branch, schema_name):
    return api.trigger_job_run_api(
        base_url=base_url, 
        account_id=account_id, 
        job_id=cleanup_job_id, 
        service_token=service_token,
        data={
            'cause': 'Triggered by CircleCI',
            'git_branch': git_branch,
            'schema_override': schema_name,
            'threads_override': 4,
            'target_name_override': 'ci',
            'steps_override': [
                f'dbt run-operation drop_schema_by_name --args "{{schema_name: {schema_name}}}"'
            ]
        }
    )


def wait_for_job_to_complete_service(base_url, account_id, run_id, service_token):
    is_complete = False
    while not is_complete:
        job_run = api.get_job_run_api(base_url, account_id, run_id, [], service_token)
        is_complete = job_run['is_complete']
        time.sleep(5)


def get_is_job_run_success_service(base_url, account_id, run_id, service_token):
    job_run = api.get_job_run_api(base_url, account_id, run_id, [], service_token)
    is_success = job_run['is_success']
    return is_success


def get_latest_step_service(base_url, account_id, run_id, service_token):
    job_run = api.get_job_run_api(base_url, account_id, run_id, ['run_steps'], service_token)
    step_ids = list(map(lambda x: x['id'], job_run['run_steps']))
    latest_step_id = max(step_ids)
    return api.get_job_run_step_api(base_url, account_id, latest_step_id, ['logs'], service_token)
