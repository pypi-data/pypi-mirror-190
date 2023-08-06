from typing import Callable

from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import HandlerBase
from whizbang.domain.manager.az.az_account_manager import AzAccountManager
from whizbang.domain.manager.az.az_login_manager import AzLoginManager
from whizbang.domain.models.active_directory.account import LoginInfo
from whizbang.domain.models.active_directory.az_account import AzAccount
from whizbang.util.logger import logger


class AccountHandler(HandlerBase):
    def __init__(self, app_config: AppConfig, az_account_manager: AzAccountManager,
                 az_login_manager: AzLoginManager):
        HandlerBase.__init__(self, app_config=app_config)
        self.__az_account_manager = az_account_manager
        self.__az_login_manager = az_login_manager

    def get_account(self) -> AzAccount:
        return self.__az_account_manager.get_account()

    def switch_subscription(self, subscription_id: str):
        result = self.__az_account_manager.set_subscription(subscription_id=subscription_id)
        logger.info(result)
        return result


    def login_service_principal(self, client_id, tenant_id, key):
        """
        login to azure cli as a service principal
        :param client_id: aka app id
        :param tenant_id: the tenant_id you wish to target
        :param key: service principal key
        :return:
        """
        result = self.__az_login_manager.login_service_principal(client_id, tenant_id, key)
        logger.info(result)
        return result

    def login_user(self, username, tenant_id, key):
        """
        login to azure cli as a service principal
        :param username: e.g. john@username.com
        :param tenant_id: the tenant_id you wish to target
        :param key: service principal key
        :return:
        """
        result = self.__az_login_manager.login_user(username, tenant_id, key)
        logger.info(result)
        return result

    def list_subscriptions(self) -> dict:
        """
        Returns a list of all available subscriptions
        :return: dict
        """
        return self.__az_account_manager.list_subscriptions()

    def run_external_command(self, external_account: LoginInfo,
                             current_account: LoginInfo,
                             callable: Callable,
                             **kwargs) -> any:
        """
        Run a callable as a user in an external tenant and subscription
        :param external_account: The external scope details
        :param current_account: The current scope details
        :param callable: The callable to run
        :param kwargs: The callables kwargs
        :return:
        """
        self.login_service_principal(client_id=external_account.user_id,
                                     tenant_id=external_account.tenant_id,
                                     key=external_account.user_key)
        self.switch_subscription(subscription_id=external_account.subscription_id)
        results = callable(**kwargs)
        self.login_service_principal(client_id=current_account.user_id,
                                     tenant_id=current_account.tenant_id,
                                     key=current_account.user_key)
        self.switch_subscription(subscription_id=current_account.subscription_id)
        return results
