import aiohttp
import json
import time
from urllib.parse import urlparse
from utils import sign_request_payload

class AsyncJob:
    def __init__(self, url, body):
        self.url = self.ensure_ssl(url)
        self.body = body
        self.job_id = None
        self.headers = None

    async def submit(self):
        headers = self.create_headers(json.dumps(self.body))
        headers['content-type'] = 'application/json'
        response = await post_request(self.url, json=self.body, headers=headers)
        if response['status'] == 'submitted':
            self.job_id = response['job_id']
            self.headers = self.create_headers(self.job_id) 
            return self.job_id
        else:
            raise ValueError('Error submitting job: {}'.format(response['message']))

    async def check_status(self):
        if self.job_id is not None:
            response = await get_request('{}/jobs/{}'.format(self.url, self.job_id), 
                                         headers=self.headers)
            return response['status']
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    async def result(self):
        if self.job_id is not None:
            response = await get_request('{}/jobs/{}'.format(self.url, self.job_id), 
                                         headers=self.headers)
            return response 
        else:
            raise ValueError('Job ID is None, has the job been submitted?')

    @staticmethod
    def ensure_ssl(url):
        parsed = urlparse(url)
        return parsed.geturl().replace(parsed.scheme, 'https', 1)

    @staticmethod
    def create_headers(payload):
        api_key, signature = sign_request_payload(payload)
        headers = {'Authorization': api_key, 'Signature': signature}
        return headers


async def get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def post_request(url, body, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=body, headers=headers) as response:
            return await response.json()


async def run_task(url, body, poll_frequency=1):
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
