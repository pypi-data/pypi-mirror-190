from abc import abstractmethod
import logging

from whizbang.config.app_config import AppConfig
from whizbang.domain.exceptions import DatabricksJobFailure
from whizbang.domain.handler.account_handler import AccountHandler
from whizbang.domain.manager.az.az_keyvault_manager import IAzKeyVaultManager
from whizbang.domain.manager.databricks.databricks_cluster_manager import IDatabricksClusterManager
from whizbang.domain.manager.databricks.databricks_filesystem_manager import DatabricksFilesystemManager
from whizbang.domain.manager.databricks.databricks_token_manager import DatabricksTokenManager
from whizbang.domain.models.databricks.databricks_cluster import DatabricksCluster
from whizbang.domain.models.databricks.databricks_file import DatabricksFile
from whizbang.domain.models.databricks.databricks_secret_scope import DatabricksSecretScope
from whizbang.domain.models.databricks.databricks_token import DatabricksToken
from whizbang.domain.models.keyvault.keyvault_resource import KeyVaultResource
from whizbang.data.databricks.databricks_client_args import DatabricksClientArgs
from whizbang.domain.handler.handler_base import IHandler, HandlerBase
from whizbang.domain.manager.databricks.databricks_job_manager import IDatabricksJobManager
from whizbang.domain.manager.databricks.databricks_workspace_manager import IDatabricksWorkspaceManager
from whizbang.domain.models.databricks.databricks_job_instance import DatabricksJobInstance
from whizbang.domain.models.databricks.databricks_state import DatabricksState
from whizbang.domain.workflow.databricks.databricks_deploy_workflow import IDatabricksDeployWorkflow
from whizbang.util import path_defaults
from whizbang.util.json_helpers import import_local_json
from whizbang.domain.models.databricks.databricks_notebook import DatabricksNotebook

_log = logging.getLogger(__name__)


class IDatabricksHandler(IHandler):
    """"""

    @abstractmethod
    def run_jobs(self, solution_name, databricks_url):
        """"""


class DatabricksHandler(HandlerBase, IDatabricksHandler):
    def __init__(
            self,
            app_config: AppConfig,
            databricks_deploy_workflow: IDatabricksDeployWorkflow,
            databricks_job_manager: IDatabricksJobManager,
            databricks_cluster_manager: IDatabricksClusterManager,
            account_handler: AccountHandler,
            az_keyvault_manager: IAzKeyVaultManager,
            databricks_token_manager: DatabricksTokenManager,
            databricks_filesystem_manager: DatabricksFilesystemManager,
            databricks_workspace_manager: IDatabricksWorkspaceManager
    ):
        HandlerBase.__init__(self, app_config)
        self.__databricks_token_manager = databricks_token_manager
        self.__databricks_deploy_workflow = databricks_deploy_workflow
        self.__databricks_job_manager = databricks_job_manager
        self.__databricks_cluster_manager = databricks_cluster_manager
        self.__databricks_filesystem_manager = databricks_filesystem_manager
        self.__account_handler = account_handler
        self.__az_keyvault_manager = az_keyvault_manager
        self.__databricks_workspace_manager = databricks_workspace_manager

    def deploy_databricks_state(self, solution_name,
                                databricks_url,
                                keyvault: KeyVaultResource,
                                cluster_env_variables: dict = None,
                                notebook_target_path: str = None) -> DatabricksState:
        databricks_state_path = path_defaults.get_databricks_state_path(app_config=self._app_config,
                                                                        solution_name=solution_name)

        databricks_cluster_path = f'{databricks_state_path}/Clusters/dv-clusters.json'
        databricks_library_path = f'{databricks_state_path}/Libraries/dv-libraries.json'
        databricks_notebook_path = f'{databricks_state_path}/Notebooks'
        databricks_job_path = f'{databricks_state_path}/Jobs/dv-jobs.json'
        databricks_sql_endpoint_path = f'{databricks_state_path}/Sql/sql-endpoints.json'

        databricks_pool_state = import_local_json(databricks_cluster_path)['instance_pools']
        databricks_cluster_state = import_local_json(databricks_cluster_path)['clusters']
        databricks_library_state = import_local_json(databricks_library_path)['clusters']
        databricks_notebook_state = databricks_notebook_path
        databricks_jobs_state = import_local_json(databricks_job_path)['jobs']
        databricks_sql_endpoint_state = import_local_json(databricks_sql_endpoint_path)['sql_endpoints']

        keyvault_json = self.__az_keyvault_manager.get_keyvault(keyvault=keyvault)
        databricks_secret_scope = DatabricksSecretScope(
            keyvault_name=keyvault_json['name'],
            keyvault_resource_id=keyvault_json['id'],
            keyvault_dns=keyvault_json['properties']['vaultUri']
        )

        client_args = DatabricksClientArgs(host=databricks_url)
        databricks_state = DatabricksState(client=client_args,
                                           pool_state=databricks_pool_state,
                                           cluster_state=databricks_cluster_state,
                                           library_state=databricks_library_state,
                                           notebook_state=databricks_notebook_state,
                                           job_state=databricks_jobs_state,
                                           secret_scope=databricks_secret_scope,
                                           new_cluster_fields=cluster_env_variables,
                                           sql_endpoint_state=databricks_sql_endpoint_state,
                                           notebook_target_path=notebook_target_path,
                                           )

        self.__databricks_deploy_workflow.run(request=databricks_state)
        return databricks_state

    def upload_databricks_notebooks(self, databricks_url: str, upload_source_path: str, upload_target_path: str = None):
        """"
        Upload Databricks workspace notebooks from a source directory.
        :param databricks_url: Databricks URL
        :param upload_source_path: Source path of the workspace notebooks to upload
        :param upload_target_path: Target path in the workspace to download
        """
        client_args = DatabricksClientArgs(host=databricks_url)
        notebook_object = DatabricksNotebook(source_path=upload_source_path, target_path=upload_target_path)
        self.__databricks_workspace_manager.save(client_args=client_args, t_object=notebook_object)

    def download_databricks_notebooks(self, databricks_url: str, notebook_source_path: str, download_notebooks_local_path: str = None):
        """"
        Downloads Databricks workspace notebooks from a source directory.
        :param databricks_url: Databricks URL
        :param notebook_source_path: Source path of the workspace notebooks
        :param download_notebooks_local_path: Local path of where to store the downloaded notebooks. Defaults to root ('/') directory if none specified.
        """
        client_args = DatabricksClientArgs(host=databricks_url)
        notebook_object = DatabricksNotebook(source_path=notebook_source_path, target_path=download_notebooks_local_path)
        self.__databricks_workspace_manager.download(client_args=client_args, t_object=notebook_object)

    def return_databricks_cluster_info(self, databricks_url) -> list[DatabricksCluster]:
        client_args = DatabricksClientArgs(host=databricks_url)
        return self.__databricks_cluster_manager.get(client_args=client_args)

    def run_jobs(self, solution_name, databricks_url):
        databricks_state_path = path_defaults.get_databricks_state_path(app_config=self._app_config,
                                                                        solution_name=solution_name)
        job_instances = import_local_json(f'{databricks_state_path}/Jobs/job-runs.json')['job_runs']
        client_args = DatabricksClientArgs(host=databricks_url)
        for job_instance in job_instances:
            to_run = DatabricksJobInstance(job_name=job_instance['name'],
                                           jar_params=job_instance['jar_params'],
                                           notebook_params=job_instance['notebook_params'],
                                           python_params=job_instance['python_params'],
                                           spark_submit_params=job_instance['spark_submit_params'])
            self.__databricks_job_manager.run_job(client_args=client_args, job_instance=to_run)

    def create_token(self, databricks_url, lifespan_seconds: int, comment: str = None):
        client_args = DatabricksClientArgs(host=databricks_url)
        token = DatabricksToken(
            token_lifespan_seconds=lifespan_seconds,
            comment=comment
        )
        return self.__databricks_token_manager.create(client_args=client_args,
                                                      token=token)

    def create_token_if_none_exists(self, databricks_url, lifespan_seconds: int, comment: str = None):
        client_args = DatabricksClientArgs(host=databricks_url)
        existing_token: dict = self.__databricks_token_manager.get(client_args=client_args)
        if 'token_infos' not in existing_token.keys():
            token = self.create_token(databricks_url=databricks_url, lifespan_seconds=lifespan_seconds, comment=comment)
            return token

    # todo: move the logging logic to manager
    def check_job_statuses(self, databricks_url: str, solution_name: str, raise_exception_on_error: bool = True):
        client_args = DatabricksClientArgs(host=databricks_url)
        databricks_state_path = path_defaults.get_databricks_state_path(app_config=self._app_config,
                                                                        solution_name=solution_name)
        jobs_to_check = import_local_json(f'{databricks_state_path}/Jobs/job-runs.json')['job_runs']
        for job in jobs_to_check:
            status = self.__databricks_job_manager.get_job_status(client_args=client_args,
                                                                  job_name=job["name"])
            if status == 'FAILED':
                _log.error(
                    f'The job {job["name"]} failed. Please check the logs in your databricks workspace. Ensure Secret Scope has been created')
                if raise_exception_on_error:
                    raise DatabricksJobFailure(
                        f'The job {job["name"]} failed. Please check the logs in your databricks workspace.')
            elif status == 'NOT RUN':
                _log.warning(f'The job {job["name"]} was not run.')
            else:
                _log.info(f'The job {job["name"]} Succeeded.')

    def upload_file_to_dbfs(self, databricks_url: str, source_path: str, destination_path: str, overwrite: bool):
        databricks_file = DatabricksFile(source_path=source_path,
                                         destination_path=destination_path,
                                         overwrite=overwrite)
        client_args = DatabricksClientArgs(host=databricks_url)
        result = self.__databricks_filesystem_manager.save(client_args=client_args, file=databricks_file)
        return result
