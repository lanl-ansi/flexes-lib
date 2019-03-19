import os, pytest, sys

import json
from asyncio import get_event_loop
from mock import MagicMock
from flexes_lib import async_job

os.environ['LANLYTICS_API_KEY'] = '123456testapikey'
os.environ['LANLYTICS_API_SECRET_KEY'] = 'testapisecretkey123456'

def _run(coro):
    return get_event_loop().run_until_complete(coro)


def AsyncMock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, *kwargs)

    mock_coro.mock = m
    return mock_coro


@pytest.fixture
def mock_get(mocker):
    mock_get_request = AsyncMock()
    mocker.patch('flexes_lib.async_job.get_request', new=mock_get_request)
    return mock_get_request.mock


@pytest.fixture
def mock_post(mocker):
    mock_post_request = AsyncMock()
    mocker.patch('flexes_lib.async_job.post_request', new=mock_post_request)
    return mock_post_request.mock


class TestAsyncJob:
    def setup_method(self, _):
        self.url = 'https://test.com'
        self.body = {'service': 'test', 'test':True}

    def test_Job(self):
        j = async_job.AsyncJob(self.url, self.body)
        assert(j.url == self.url)
        assert(j.body == self.body)

    def test_Job_ssl(self):
        j = async_job.AsyncJob('http://test.com', self.body)
        assert(j.url == self.url)
        assert(j.body == self.body)

    def test_Job_submit(self, mock_post):
        mock_post.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = _run(j.submit())
        assert(job_id == 'test1234')

    def test_job_check_status(self, mock_get, mock_post):
        mock_post.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value = {'status': 'running', 'job_id': 'test1234'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = _run(j.submit())
        status = _run(j.check_status())
        assert(status == 'running')


    def test_job_result(self, mock_get, mock_post):
        mock_post.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value = {'status': 'complete', 'job_id': 'test1234', 'result': 'success'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = _run(j.submit())
        result = _run(j.result())
        assert(result['status'] == 'complete')
        assert(result['job_id'] == 'test1234')
        assert(result['result'] == 'success')

    def test_ensure_ssl(self):
        url = 'http://foo.bar.com'
        assert(async_job.AsyncJob.ensure_ssl(url) == 'https://foo.bar.com')

    def test_create_headers(self):
        headers_post = async_job.AsyncJob.create_headers(json.dumps(self.body))
        headers_get = async_job.AsyncJob.create_headers('test1234')
        assert(headers_post is not None)
        assert(headers_get is not None)

    def test_run_task(self, mock_get, mock_post):
        mock_post.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.side_effect = [{'status': 'running', 'job_id': 'test1234'},
                                {'status': 'running', 'job_id': 'test1234'},
                                {'status': 'complete', 'job_id': 'test1234'},
                                {'status': 'complete', 'job_id': 'test1234', 'result': 'success'}]
        result = _run(async_job.run_task(self.body))
        assert(result['result'] == 'success')

    def test_run_task_fail(self, mock_get, mock_post):
        mock_post.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.side_effect = [{'status': 'running', 'job_id': 'test1234'},
                                {'status': 'running', 'job_id': 'test1234'},
                                {'status': 'failed', 'job_id': 'test1234'},
                                {'status': 'failed', 'job_id': 'test1234', 'result': 'success'}]
        with pytest.raises(ValueError):
            _run(async_job.run_task(self.body))
