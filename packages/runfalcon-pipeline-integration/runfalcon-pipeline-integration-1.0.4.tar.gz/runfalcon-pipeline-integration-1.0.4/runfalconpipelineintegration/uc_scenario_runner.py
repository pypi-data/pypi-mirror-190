import time
import urllib.parse
from runfalconpipelineintegration.model_job import JobStatus
from runfalconpipelineintegration.util_configuration import Configuration
from runfalconpipelineintegration.util_http import get_error_from_response
from runfalconpipelineintegration.util_http_client import HttpClient
from runfalconpipelineintegration.util_logger import print_debug, print_info

class ScenarioRunner:

    __client_name__:str
    __application_name__:str
    __scenario_code__:str
    __token__:str

    def __init__(self, client_name:str, application_name:str, scenario_code:str, token:str) -> None:
        self.__client_name__ = client_name
        self.__application_name__ = application_name
        self.__scenario_code__ = scenario_code
        self.__token__ = token

    def run_async(self) -> int:
        print_info('Running scenario "{}" ...'.format(self.__scenario_code__))
        url:str = Configuration.instance().get_config_value('RUNFALCON-ENDPOINTS', 'run')
        url = url.format( \
                    client = urllib.parse.quote(self.__client_name__), \
                    application = urllib.parse.quote(self.__application_name__), \
                    scenario = urllib.parse.quote(self.__scenario_code__) \
                    )
        print_debug('Runner url: {}'.format(url))
        http_client:HttpClient = HttpClient(self.__token__)
        response:any = http_client.get(url)

        if response.status_code != 200:
            raise Exception(get_error_from_response(response))

        json_response:any = response.json()
        job_id:int = int(json_response['jobId'])
        print_info('Job {} created.'.format(job_id))
        return job_id

    def __get_job_info__(self, job_id:int) -> str:
        print_info('Getting job {} information ...'.format(job_id))
        url:str = Configuration.instance().get_config_value('RUNFALCON-ENDPOINTS', 'get-job')
        url = url.format(client = self.__client_name__, application = self.__application_name__, scenario = self.__scenario_code__, job = job_id)
        print_debug('Url to get job information "{}" ...'.format(url))

        http_client:HttpClient = HttpClient(self.__token__)
        response:any = http_client.get(url)

        if response.status_code != 200:
            raise Exception(get_error_from_response(response))

        return response.json()

    def __is_final_status__(self, status:str) -> bool:
        if status:
            return status != JobStatus.RUNNING.value
        return True

    def run_sync(self) -> dict:
        job_status:str = JobStatus.RUNNING.value
        job_info:dict = None
        wait_seconds:int = Configuration.instance().get_config_value('INVOKER', 'wait-to-get-status')
        max_wait_cycles:int = Configuration.instance().get_config_value('INVOKER', 'max-wait-cycles')
        cycles_count:int = 0

        job_id:int = self.run_async()
        while job_status == JobStatus.RUNNING.value:
            print_debug('Wating ultil job {} finish ...'.format(job_id))
            time.sleep(wait_seconds)
            cycles_count = cycles_count + 1
            if cycles_count >= max_wait_cycles:
                raise Exception('The job {} did not finish in a reasonable time'.format(job_id))
            job_info = self.__get_job_info__(job_id)
            job_status = job_info['status']
            print_info('Job {job_id} status: "{status}"'.format(job_id = job_id, status = job_status))

        return job_info
