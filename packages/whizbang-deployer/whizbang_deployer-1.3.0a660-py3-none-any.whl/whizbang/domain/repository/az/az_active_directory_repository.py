from abc import abstractmethod
from typing import List

from whizbang.data.az_cli_context import AzCliContext
from whizbang.domain.exceptions import AzCliException
from whizbang.domain.models.active_directory.ad_group_member import AdGroupMember
from whizbang.domain.repository.az.az_repository_base import AzRepositoryBase, IAzRepository

import logging
_log = logging.getLogger(__name__) 

class IAzActiveDirectoryRepository(IAzRepository):
    @abstractmethod
    def get_object_id(self, lookup_type: str, lookup_value: str) -> str:
        """The get_object_id interface"""

    @abstractmethod
    def get_display_name(self, object_id: str) -> str:
        """The get_display_name interface"""

    @abstractmethod
    def get_group_members(self, group_object_id: str) -> List[AdGroupMember]:
        """"""

    @abstractmethod
    def delete_service_principal(self, service_principal_id: str) -> None:
        """"""

    @abstractmethod
    def delete_app_registration(self, app_registration_id: str) -> None:
        """"""


class AzActiveDirectoryRepository(AzRepositoryBase, IAzActiveDirectoryRepository):
    def __init__(self, context: AzCliContext):
        AzRepositoryBase.__init__(self, context)

    @property
    def _resource_provider(self) -> str:
        return 'ad'

    def get_object_id(self, lookup_type: str, lookup_value: str) -> str:
        lookup_type = lookup_type.lower()

        # TODO: use shared types for strings
        if lookup_type == 'objectid':
            return lookup_value

        if lookup_type == 'email':
            return self._execute(f'user show --id {lookup_value} --query id').results

        if lookup_type == 'group':
            return self._execute(f'group show --group {lookup_value} --query id').results

        if lookup_type == 'serviceprincipal':
            # object_id = az_invoke(
            #     f'ad sp list --query "[?displayName=={lookup_value} && servicePrincipalType==ManagedIdentity].objectId" --all -o tsv')
            # if object_id is None:
            result = self._execute(f'sp list --display-name {lookup_value}').results

            if result is None or result.__len__() == 0:
                try:
                    return self._execute(f'sp show --id {lookup_value} --query id').results
                except AzCliException:
                    # TODO: should we be swallowing this exception?
                    return ''
            else:
                _log.info(result)
                object_id = result[0].get("id")
                if object_id is not None:
                    return object_id
                raise AzCliException(f"ad objectId for lookup value of {lookup_value} could not be found")

        if lookup_type == 'appregistration':
            result = self._execute(f'app list --display-name {lookup_value}').results
            if result is None or result.__len__() == 0:
                try:
                    return self._execute(f'app show --id {lookup_value} --query id').results
                except AzCliException:
                    # TODO: should we be swallowing this exception?
                    return ''
            else:
                _log.info(result)
                object_id = result[0].get("id")
                if object_id is not None:
                    return object_id
                raise AzCliException(f"ad objectId for lookup value of {lookup_value} could not be found")

        if lookup_type == 'self':
            object_id = self._execute(f'signed-in-user show').results['id']
            return object_id

    def get_display_name(self, object_id: str) -> str:
        query = 'displayName'
        
        # TODO: try/catch error handling if needed?
        # TODO: is this really the best way to do this?
        
        display_name = self._execute(f'user show --id {object_id} --only-show-errors --query {query} -o tsv').results
        if display_name is not None:
            return display_name

        display_name = self._execute(f'sp show --id {object_id} --only-show-errors --query {query} -o tsv').results
        if display_name is not None:
            return display_name

        display_name = self._execute(f'group show --id {object_id} --only-show-errors --query {query} -o tsv').results
        if display_name is not None:
            return display_name

        display_name = self._execute(f'app show --id {object_id} --only-show-errors --query {query} -o tsv').results
        if display_name is not None:
            return display_name

    def get_group_members(self, group_object_id: str) -> List[AdGroupMember]:
        result: List[dict] = self._execute(
            f'group member list --group {group_object_id}'
            ' --query "[].{object_id: objectId, display_name: displayName, object_type: objectType}"'
        ).results

        group_members: List[AdGroupMember] = []
        for group_member in result:
            group_members.append(AdGroupMember(**group_member))

        return group_members

    def delete_service_principal(self, service_principal_id: str) -> None:
        self._execute(f'sp delete --id {service_principal_id}')

    def delete_app_registration(self, app_registration_id: str) -> None:
        self._execute(f'app delete --id {app_registration_id}')
