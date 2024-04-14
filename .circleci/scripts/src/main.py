import argparse
import json
import sys

import domain, services


def main(config):
    job_type = config.get('job_type')
    base_url = config.get('base_url')
    account_id = config.get('account_id')
    ci_job_id = config.get('ci_job_id')
    cleanup_job_id = config.get('cleanup_job_id')
    service_token = config.get('service_token')
    git_branch = config.get('git_branch')
    schema_name = config.get('schema_name')

    run = None
    if job_type == domain.JobType.CI_JOB:
        print('Triggering CI job')
        run = services.trigger_ci_job_run_service(
            base_url=base_url, 
            account_id=account_id, 
            ci_job_id=ci_job_id, 
            service_token=service_token,
            git_branch=git_branch,
            schema_name=schema_name
        )
    elif job_type == domain.JobType.CLEANUP_JOB:
        print('Triggering cleanup job')
        run = services.trigger_cleanup_job_run_service(
            base_url=base_url, 
            account_id=account_id, 
            cleanup_job_id=cleanup_job_id, 
            service_token=service_token,
            git_branch=git_branch,
            schema_name=schema_name
        )

    print('Waiting for job to complete')
    services.wait_for_job_to_complete_service(
        base_url=base_url,
        account_id=account_id, 
        run_id=run['id'], 
        service_token=service_token,
    )

    run_is_success = services.get_is_job_run_success_service(
        base_url=base_url,
        account_id=account_id,
        run_id=run['id'],
        service_token=service_token
    )

    if run_is_success:
        print('Job run successful!')
        sys.exit(0)
    else:
        latest_step = services.get_latest_step_service(
            base_url=base_url,
            account_id=account_id,
            run_id=run['id'],
            service_token=service_token
        )

        print('Job run not successful.')
        print(latest_step['logs'])
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, help='The JSON configuration string')
    args = parser.parse_args()
    config = json.loads(args.config)
    main(config)
