import requests
import time

class Job:
    def __init__(self, url, body):
        self.url = url
        self.body = body
        self.job_id = None

    def submit(self):
        response = requests.post(self.url, json=self.body).json()
        if response['status'] == 'submitted':
            self.job_id = response['job_id']
            return self.job_id
        else:
            raise ValueError('Error submitting job: {}'.format(response['message']))

    def check_status(self):
        if self.job_id is not None:
            response = requests.get('{}/jobs/{}'.format(self.url, self.job_id)).json()
            return response['status']
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    def result(self):
        if self.job_id is not None:
            return requests.get('{}/jobs/{}'.format(self.url, self.job_id)).json()
        else:
            raise ValueError('Job ID is None, has the job been submitted?')


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
