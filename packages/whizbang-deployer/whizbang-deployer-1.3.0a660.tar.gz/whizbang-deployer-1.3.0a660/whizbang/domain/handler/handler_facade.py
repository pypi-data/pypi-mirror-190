from abc import ABC, abstractmethod

from whizbang.domain.handler.account_handler import AccountHandler
from whizbang.domain.handler.active_directory_handler import ActiveDirectoryHandler
from whizbang.domain.handler.app_registration_handler import IAppRegistrationHandler
from whizbang.domain.handler.bicep_handler import IBicepHandler
from whizbang.domain.handler.container_registry_handler import ContainerRegistryHandler
from whizbang.domain.handler.databricks_handler import IDatabricksHandler
from whizbang.domain.handler.datafactory_handler import DatafactoryHandler
from whizbang.domain.handler.keyvault_handler import IKeyVaultHandler
from whizbang.domain.handler.lock_handler import LockHandler
from whizbang.domain.handler.management_partner_handler import ManagementPartnerHandler
from whizbang.domain.handler.rbac_handler import IRbacHandler
from whizbang.domain.handler.resource_group_handler import ResourceGroupHandler
from whizbang.domain.handler.security_handler import SecurityHandler
from whizbang.domain.handler.service_principal_handler import ServicePrincipalHandler
from whizbang.domain.handler.sql_server_handler import ISqlServerHandler
from whizbang.domain.handler.storage_handler import IStorageHandler
from whizbang.domain.handler.webapp_handler import WebappHandler


class IHandlerFacade(ABC):
    """The HandlerFacade interface"""

    @property
    @abstractmethod
    def databricks_handler(self):
        """"""

    @property
    @abstractmethod
    def sql_server_handler(self) -> ISqlServerHandler:
        """"""

    @property
    @abstractmethod
    def rbac_handler(self):
        """"""

    @property
    @abstractmethod
    def bicep_handler(self):
        """"""

    @property
    @abstractmethod
    def keyvault_handler(self) -> IKeyVaultHandler:
        """"""

    @property
    @abstractmethod
    def storage_handler(self) -> IStorageHandler:
        """"""

    @property
    @abstractmethod
    def app_registration_handler(self) -> IAppRegistrationHandler:
        """"""

    @property
    @abstractmethod
    def account_handler(self) -> AccountHandler:
        """"""
    
    @property
    @abstractmethod
    def service_principal_handler(self) -> ServicePrincipalHandler:
        """"""

    @property
    @abstractmethod
    def webapp_handler(self) -> WebappHandler:
        """"""

    @property
    @abstractmethod
    def datafactory_handler(self) -> DatafactoryHandler:
        """"""

    @property
    @abstractmethod
    def container_registry_handler(self) -> ContainerRegistryHandler:
        """"""

    @property
    @abstractmethod
    def resource_group_handler(self) -> ResourceGroupHandler:
        """"""

    @property
    @abstractmethod
    def management_partner_handler(self) -> ManagementPartnerHandler:
        """"""
    @property
    @abstractmethod
    def security_handler(self) -> SecurityHandler:
        """"""

    @property
    @abstractmethod
    def lock_handler(self) -> LockHandler:
        """"""

    @property
    @abstractmethod
    def active_directory_handler(self) -> ActiveDirectoryHandler:
        """"""


class HandlerFacade(IHandlerFacade):
    def __init__(
            self,
            keyvault_handler: IKeyVaultHandler,
            bicep_handler: IBicepHandler,
            rbac_handler: IRbacHandler,
            sql_server_handler: ISqlServerHandler,
            databricks_handler: IDatabricksHandler,
            storage_handler: IStorageHandler,
            app_registration_handler: IAppRegistrationHandler,
            account_handler: AccountHandler,
            service_principal_handler: ServicePrincipalHandler,
            webapp_handler: WebappHandler,
            datafactory_handler: DatafactoryHandler,
            container_registry_handler: ContainerRegistryHandler,
            resource_group_handler: ResourceGroupHandler,
            management_partner_handler: ManagementPartnerHandler,
            security_handler: SecurityHandler,
            lock_handler: LockHandler,
            active_directory_handler: ActiveDirectoryHandler
    ):
        self.__account_handler = account_handler
        self.__service_principal_handler = service_principal_handler
        self.__app_registration_handler = app_registration_handler
        self.__storage_handler = storage_handler
        self.__databricks_handler = databricks_handler
        self.__sql_server_handler = sql_server_handler
        self.__rbac_handler = rbac_handler
        self.__bicep_handler = bicep_handler
        self.__keyvault_handler = keyvault_handler
        self.__webapp_handler = webapp_handler
        self.__datafactory_handler = datafactory_handler
        self.__container_registry_handler = container_registry_handler
        self.__resource_group_handler = resource_group_handler
        self.__management_partner_handler = management_partner_handler
        self.__security_handler = security_handler
        self.__lock_handler = lock_handler
        self.__active_directory_handler = active_directory_handler


    @property
    def storage_handler(self): return self.__storage_handler

    @property
    def databricks_handler(self): return self.__databricks_handler

    @property
    def sql_server_handler(self): return self.__sql_server_handler

    @property
    def rbac_handler(self): return self.__rbac_handler

    @property
    def bicep_handler(self): return self.__bicep_handler

    @property
    def keyvault_handler(self): return self.__keyvault_handler

    @property
    def app_registration_handler(self): return self.__app_registration_handler

    @property
    def account_handler(self): return self.__account_handler

    @property
    def service_principal_handler(self): return self.__service_principal_handler

    @property
    def webapp_handler(self): return self.__webapp_handler

    @property
    def datafactory_handler(self): return self.__datafactory_handler

    @property
    def container_registry_handler(self): return self.__container_registry_handler

    @property
    def resource_group_handler(self): return self.__resource_group_handler

    @property
    def management_partner_handler(self): return self.__management_partner_handler

    @property    
    def security_handler(self): return self.__security_handler

    @property
    def lock_handler(self): return self.__lock_handler

    @property
    def active_directory_handler(self): return self.__active_directory_handler
