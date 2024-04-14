import requests


def trigger_job_run_api(base_url, account_id, job_id, service_token, data):
    url = f'https://{base_url}/api/v2/accounts/{account_id}/jobs/{job_id}/run/'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {service_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    run = response.json()['data']
    return run


def get_job_run_api(base_url, account_id, run_id, include_related, service_token):
    url = f'https://{base_url}/api/v2/accounts/{account_id}/runs/{run_id}/'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {service_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'include_related': include_related
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['data']


def get_job_run_step_api(base_url, account_id, step_id, include_related, service_token):
    url = f'https://{base_url}/api/v2/accounts/{account_id}/steps/{step_id}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {service_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'include_related': include_related
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['data']
