import aiohttp
import json
import time
from urllib.parse import urlparse
from .utils import sign_request_payload

class AsyncJob:
    '''Asynchronous handler for API jobs

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

    async def submit(self):
        '''Submit job to API
        
        Returns:
            str: Unique ID for job

        Raises:
            ValueError: If submission fails
        '''
        headers = self.create_headers(json.dumps(self.body)) if self.sign is True else None
        response = await post_request(self.url, json=self.body, headers=headers)
        if response['status'] == 'submitted':
            self.job_id = response['job_id']
            self.headers = self.create_headers(self.job_id) if self.sign is True else None
            return self.job_id
        else:
            raise ValueError('Error submitting job: {}'.format(response['message']))

    async def check_status(self):
        '''Check status of job
        
        Returns:
            str: Status of the job

        Raises:
            ValueError: If `job_id` is `None`
        '''
        if self.job_id is not None:
            response = await get_request('{}/jobs/{}'.format(self.url, self.job_id), 
                                         headers=self.headers)
            return response['status']
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    async def result(self):
        '''Get job result
        
        Returns:
            dict: Job result

        Raises:
            ValueError: If `job_id` is `None`
        '''
        if self.job_id is not None:
            response = await get_request('{}/jobs/{}'.format(self.url, self.job_id), 
                                         headers=self.headers)
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


async def get_request(url, headers=None):
    '''Execute GET request asynchronously

    Args:
        url (str): Request URL
        headers (dict, optional): Authorization and Signature headers

    Returns:
        dict: JSON response
    '''
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def post_request(url, body, headers=None):
    '''Execute POST request with JSON body asynchronously

    Args:
        url (str): Request URL
        body (dict): JSON request body
        headers (dict, optional): Authorization and Signature headers

    Returns:
        dict: JSON response
    '''
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(url, json=body, headers=headers) as response:
            return await response.json()


async def run_task(body, poll_frequency=1, url='https://api.lanlytics.com'):
    '''Submit and execute job through the API

    Args:
        body (dict): Message body
        poll_frequency (int, optional): Status poll frequency in seconds, default 1
        url (str, optional): API endpoint, default https://api.lanlytics.com

    Returns:
        dict: Job result

    Raises:
        ValueError: If job fails
    '''
    job = AsyncJob(url, body)
    job_id = await job.submit()
    job_status = await job.check_status()

    while job_status in ['submitted', 'running']:
        job_status = await job.check_status()
        time.sleep(poll_frequency)
    result = await job.result()

    if job_status in ['complete', 'active']:
        return result
    else:
        raise ValueError('Job failed: {}'.format(result))
