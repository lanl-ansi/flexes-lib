import os, pytest, sys

sys.path.append('.')
import mock
import async_job
import json

os.environ['LANLYTICS_API_KEY'] = '123456testapikey'
os.environ['LANLYTICS_API_SECRET_KEY'] = 'testapisecretkey123456'

class TestJob:
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

    @mock.patch('requests.post')
    def test_Job_submit(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = j.submit()
        assert(job_id == 'test1234')

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_job_check_status(self, mock_get, mock_post):
        mock_post.return_value.json.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value.json.return_value = {'status': 'running', 'job_id': 'test1234'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = j.submit()
        status = j.check_status()
        assert(status == 'running')


    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_job_result(self, mock_get, mock_post):
        mock_post.return_value.json.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value.json.return_value = {'status': 'complete', 'job_id': 'test1234', 'result': 'success'}
        j = async_job.AsyncJob(self.url, self.body)
        job_id = j.submit()
        result = j.result()
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

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_run_task(self, mock_get, mock_post):
        mock_post.return_value.json.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value.json.side_effect = [{'status': 'running', 'job_id': 'test1234'},
                                                  {'status': 'running', 'job_id': 'test1234'},
                                                  {'status': 'complete', 'job_id': 'test1234'},
                                                  {'status': 'complete', 'job_id': 'test1234', 'result': 'success'}]
        result = async_job.run_task(self.url, self.body)
        assert(result['result'] == 'success')

    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_run_task_fail(self, mock_get, mock_post):
        mock_post.return_value.json.return_value = {'status': 'submitted', 'job_id': 'test1234'}
        mock_get.return_value.json.side_effect = [{'status': 'running', 'job_id': 'test1234'},
                                                  {'status': 'running', 'job_id': 'test1234'},
                                                  {'status': 'failed', 'job_id': 'test1234'},
                                                  {'status': 'failed', 'job_id': 'test1234', 'result': 'success'}]
        with pytest.raises(ValueError):
            async_job.run_task(self.url, self.body)
