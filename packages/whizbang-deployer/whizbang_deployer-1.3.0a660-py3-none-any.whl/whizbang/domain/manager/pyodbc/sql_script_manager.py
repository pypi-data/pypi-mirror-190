import abc
import logging

from whizbang.data.pyodbc.pyodbc_context_args import SqlServerContextArgs
from whizbang.domain.manager.pyodbc.pyodbc_manager_base import PyodbcManager, IPyodbcManager
from whizbang.domain.repository.sql_server.sql_script_repository import ISqlScriptRepository

_log = logging.getLogger(__name__)

class ISqlScriptManager(IPyodbcManager, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute_script(self, context_args: SqlServerContextArgs, sql_script: str, catch_errors: bool = False):
        """the execute_script interface"""


class SqlScriptManager(PyodbcManager, ISqlScriptManager):
    def __init__(self, repository: ISqlScriptRepository):
        PyodbcManager.__init__(self, repository)
        self._repository: ISqlScriptRepository

    def execute_script(self, context_args: SqlServerContextArgs, sql_script: str, catch_errors: bool = False):
        try:
            return self._repository.execute_script(context_args, sql_script)
        except Exception as ex:
            if catch_errors is True:
                return None
            raise ex

    def execute_script_path(self, context_args, file_path):
        file = open(file_path)
        script = file.read()
        file.close()
        return self.execute_script(context_args, script)
