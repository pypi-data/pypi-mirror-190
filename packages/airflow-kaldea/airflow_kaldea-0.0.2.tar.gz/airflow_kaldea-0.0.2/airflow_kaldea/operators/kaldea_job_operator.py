import requests
import tenacity
from airflow.models import BaseOperator
from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook


class KaldeaJobOperator(BaseOperator):
    """Changes the status of target airflow task in Kaldea to success.

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :<https://www.kaldea.com/docs/getting-started/integrations/airflow>`

    :param task_id: A unique, meaningful id for the task
    :param kaldea_job_id: Kaldea job id
    :param kaldea_task_id: Kaldea task id
    :param kaldea_conn_id: Connection that has Kaldea host, id and password, default = "kaldea_default"
    """

    def __init__(
            self,
            task_id: str,
            kaldea_job_id: str,
            kaldea_task_id: str,
            kaldea_conn_id: str = 'kaldea_default',
            **kwargs,
    ) -> None:
        super().__init__(task_id=task_id, **kwargs)
        self.kaldea_conn_id = kaldea_conn_id
        self.kaldea_job_id = kaldea_job_id
        self.kaldea_task_id = kaldea_task_id

    def execute(self, context):
        http = self._HttpHook('POST', http_conn_id=self.kaldea_conn_id)
        conn = http.get_connection(self.kaldea_conn_id)
        response = http.run(
            endpoint='account/signin',
            json={
                'email': conn.login,
                'password': conn.get_password(),
            },
        )

        # It will retry up to 3 times because it can fail due to timing issues.
        schedule_time = context.get('next_execution_date') or context.get('execution_date')
        if schedule_time is None:
            raise AirflowException('This case is not supported. Please contact support@kaldea.com.')

        def is_not_found_error(r: requests.Response):
            return r.status_code == 404

        def return_last_value(retry_state: tenacity.RetryCallState):
            """return the result of the last call attempt"""
            return retry_state.outcome.result()

        response = http.run_with_advanced_retry(
            endpoint=f'scheduler/jobs/{self.kaldea_job_id}/instances/-/task_instances/-/exit',
            json={
                'task_id': self.kaldea_task_id,
                'schedule_time': schedule_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            },
            headers={
                'Authorization': f'Bearer {response.json().get("data", {}).get("auth_token", {}).get("access_token")}',
            },
            extra_options={
                'check_response': False,
            },
            _retry_args={
                'wait': tenacity.wait_fixed(60),
                'stop': tenacity.stop_after_attempt(3),
                'retry': tenacity.retry_if_result(is_not_found_error),
                'retry_error_callback': return_last_value,
            },
        )
        if response.status_code == 200:
            return

        if is_not_found_error(response):
            raise AirflowException(
                f'Task is not found. Please check `kaldea_job_id`, `kaldea_task_id` and `schedule_interval`.')

        raise AirflowException(
            f'An internal error({response.json().get("error_detail", {}).get("code", "0")}) has occurred. '
            f'Please retry your request.')

    class _HttpHook(HttpHook):
        def get_conn(self, headers: dict = None) -> requests.Session:
            """Returns http session for use with requests.

            :param headers: Additional headers to be passed through as a dictionary
            """
            session = requests.Session()

            if self.http_conn_id:
                conn = self.get_connection(self.http_conn_id)

                if conn.host and "://" in conn.host:
                    self.base_url = conn.host
                else:
                    # schema defaults to HTTP
                    schema = conn.schema if conn.schema else "http"
                    host = conn.host if conn.host else ""
                    self.base_url = schema + "://" + host

                if conn.port:
                    self.base_url = self.base_url + ":" + str(conn.port)
            if headers:
                session.headers.update(headers)

            return session
