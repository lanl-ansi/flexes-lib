import json
import requests
import time
from urllib.parse import urlparse
from utils import sign_request_payload

class Job:
    '''Handler for API jobs

    Attributes:
        url (str): API endpoint
        body (dict): Message body
        job_id (str): The instance's job ID, set during self.submit()
        headers (dict): Job request headers, set during self.submit()
        sign (bool): Use request signing for authentication, default False

    Args:
        url (str): API endpoint
        body (dict): Message body
        sign (bool, optional): Use request signing for authentication, default False
    '''
    def __init__(self, url, body, sign=False):
        self.url = self.ensure_ssl(url)
        self.body = body
        self.job_id = None
        self.headers = None
        self.sign = sign

    def submit(self):
        '''Submit job to API
        
        Returns:
            str: Unique ID for job

        Raises:
            ValueError: If submission fails
        '''
        if self.sign is True:
            headers = self.create_headers(json.dumps(self.body))
        else:
            headers = None
        response = requests.post(self.url, json=self.body, headers=headers).json()
        if response['status'] == 'submitted':
            self.job_id = response['job_id']
            if self.sign is True:
                self.headers = self.create_headers(self.job_id) 
            return self.job_id
        else:
            raise ValueError('Error submitting job: {}'.format(response['message']))

    def check_status(self):
        '''Check status of job
        
        Returns:
            str: Status of the job

        Raises:
            ValueError: If `job_id` is `None`
        '''
        if self.job_id is not None:
            response = requests.get('{}/jobs/{}'.format(self.url, self.job_id), 
                                    headers=self.headers).json()
            return response['status']
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    def result(self):
        '''Get job result
        
        Returns:
            dict: Job result

        Raises:
            ValueError: If `job_id` is `None`
        '''
        if self.job_id is not None:
            response = requests.get('{}/jobs/{}'.format(self.url, self.job_id), 
                                    headers=self.headers).json()
            return response 
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    @staticmethod
    def ensure_ssl(url):
        '''Ensure URL is using SSL

        Args:
            url (str): Request URL
        
        Returns:
            str: URL rewritten using SSL
        '''
        parsed = urlparse(url)
        return parsed.geturl().replace(parsed.scheme, 'https', 1)

    @staticmethod
    def create_headers(payload):
        '''Create Authorization and Signature request headers

        Args:
            payload (str): Request payload

        Returns:
            dict: Request headers
        '''
        api_key, signature = sign_request_payload(payload)
        headers = {'Authorization': api_key, 'Signature': signature}
        return headers


def run_task(url, body, poll_frequency=1):
    '''Submit and execute job through the API

    Args:
        url (str): API endpoint
        body (dict): Message body
        poll_frequency (int, optional): Status poll frequency in seconds, default 1

    Returns:
        dict: Job result

    Raises:
        ValueError: If job fails
    '''
    job = Job(url, body)
    job_id = job.submit()
    job_status = job.check_status()

    while job_status in ['submitted', 'running']:
        job_status = job.check_status()
        time.sleep(poll_frequency)
    result = job.result()

    if job_status in ['complete', 'active']:
        return result
    else:
        raise ValueError('Job failed: {}'.format(result))
