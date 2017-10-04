import json
import requests
import time
from urllib.parse import urlparse
from utils import sign_request_payload

class Job:
    def __init__(self, url, body):
        self.url = self.ensure_ssl(url)
        self.body = body
        self.job_id = None
        self.headers = None

    def submit(self):
        headers = self.create_headers(json.dumps(self.body))
        response = requests.post(self.url, json=self.body, headers=headers).json()
        if response['status'] == 'submitted':
            self.job_id = response['job_id']
            self.headers = self.create_headers(self.job_id) 
            return self.job_id
        else:
            raise ValueError('Error submitting job: {}'.format(response['message']))

    def check_status(self):
        if self.job_id is not None:
            response = requests.get('{}/jobs/{}'.format(self.url, self.job_id), 
                                    self.headers=headers).json()
            return response['status']
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    def result(self):
        if self.job_id is not None:
            response = requests.get('{}/jobs/{}'.format(self.url, self.job_id), 
                                    self.headers=headers).json()
            return response 
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    @staticmethod
    def ensure_ssl(url):
        parsed = urlparse(url)
        parsed._replace(scheme='https')
        return parsed.geturl()

    @staticmethod
    def create_headers(payload):
        api_key, signature = sign_request_payload(payload)
        headers = {'Authorization': api_key, 'Signature': signature}
        return headers


def run_task(url, body):
    job = Job(url, body)
    job_id = job.submit()
    job_status = job.check_status()

    while job_status in ['submitted', 'running']:
        job_status = job.check_status()
        time.sleep(1)
    result = job.result()

    if job_status in ['complete', 'active']:
        return result
    else:
        raise ValueError('Job failed: {}'.format(result))
