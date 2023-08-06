from abc import ABC, abstractmethod

from whizbang.config.environment_config import EnvironmentConfig
from whizbang.domain.exceptions import AzCliResourceDoesNotExist
from whizbang.domain.handler.handler_facade import IHandlerFacade
from whizbang.domain.models.template_deployment_result import TemplateDeploymentResult
from whizbang.domain.models.template_parameters_base import TemplateParametersBase

import logging

_log = logging.getLogger(__name__)

DEFAULT_US_PARTNER_ID = "577246"
DEFAULT_CA_PARTNER_ID = "550088"


class DeploymentSolutionBase(ABC):
    def __init__(self, environment_config: EnvironmentConfig, handler: IHandlerFacade):
        self.__handler = handler
        self.environment_config = environment_config
        self.deployment_data = {}

    @property
    def handler(self):
        return self.__handler

    @property
    def solution_name(self) -> str:
        return type(self).__name__.lower().replace('solution', '')

    def deploy(self):
        # todo: support solutions with multiple resource groups/templates
        self.__handler.account_handler.switch_subscription(subscription_id=self.environment_config.subscription_id)
        self.__set_partner_id()
        pre_deploy_output = self.pre_deploy()

        parameters = self.set_template_parameters(pre_deploy_output)
        self.__handler.account_handler.switch_subscription(subscription_id=self.environment_config.subscription_id)
        result: TemplateDeploymentResult = self.handler.bicep_handler.deploy_bicep_template(
            solution_name=self.solution_name,
            parameters=parameters,
            environment_config=self.environment_config
        )

        self.deployment_data['deploy_output'] = result.outputs

        self.__handler.account_handler.switch_subscription(subscription_id=self.environment_config.subscription_id)
        self.post_deploy(result.outputs, pre_deploy_output=pre_deploy_output)
        # TODO save solution object to internal storage

    @abstractmethod
    def pre_deploy(self) -> dict:
        """Anything that should be run before the bicep deployment."""

    # steps taken after a bicep solution
    @abstractmethod
    def post_deploy(self, deploy_output: dict, pre_deploy_output: dict):
        """Anything that needs to be run after the bicep deployment. Has access to pre-deploy and bicep deployment outputs."""

    @abstractmethod
    def set_template_parameters(self, pre_deploy_output: dict) -> TemplateParametersBase:
        """
        Build and return a TemplateParameter class to be used with the bicep deployment.
        Your TemplateParameter class should inherit TemplateParametersBase from whizbang.domain.models.template_parameters_base.
        """

    def set_rbac_policies(self):
        deployed_resource_ids = self._get_deployed_resource_ids(method_name='set_rbac_policies')

        if deployed_resource_ids is not None:
            self.handler.rbac_handler.set_rbac(resource_ids=deployed_resource_ids)

    def set_keyvault_access_policies(self):
        deployed_resource_ids = self._get_deployed_resource_ids(method_name='set_keyvault_access_policies')

        if deployed_resource_ids is not None:
            self.handler.keyvault_handler.set_keyvault_access_policies(resource_ids=deployed_resource_ids)

    def _get_deployed_resource_ids(self, method_name: str):
        if 'resourceIds' in self.deployment_data is False:
            _log.warning(
                f'no deployment resource_ids found...note: "{method_name}" can only be run in  the "post_deploy" '
                f'step, skipping "{method_name}"')
            return None
        if self.deployment_data \
                and self.deployment_data['deploy_output'] \
                and self.deployment_data['deploy_output']['resourceIds']:
            deployed_resource_ids = self.deployment_data['deploy_output']['resourceIds']['value']
            return deployed_resource_ids

    def __set_partner_id(self):
        partner_id = self.environment_config.properties.get("partner_id") or DEFAULT_US_PARTNER_ID
        try:
            current_partner_id: str = self.__handler.management_partner_handler.get_partner_id().get("partnerId")
            if current_partner_id == partner_id or current_partner_id == DEFAULT_CA_PARTNER_ID:
                return
            _log.info("Partner ID doesn't match provided ID. Updating partner ID.")
            self.__handler.management_partner_handler.update_partner_id(partner_id=partner_id)
        except AzCliResourceDoesNotExist:
            _log.info("Partner ID is not set. Setting partner ID.")
            self.__handler.management_partner_handler.create_partner_id(partner_id=partner_id)
