# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetSqlMigrationServiceResult',
    'AwaitableGetSqlMigrationServiceResult',
    'get_sql_migration_service',
    'get_sql_migration_service_output',
]

@pulumi.output_type
class GetSqlMigrationServiceResult:
    """
    A SQL Migration Service.
    """
    def __init__(__self__, id=None, integration_runtime_state=None, location=None, name=None, provisioning_state=None, system_data=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if integration_runtime_state and not isinstance(integration_runtime_state, str):
            raise TypeError("Expected argument 'integration_runtime_state' to be a str")
        pulumi.set(__self__, "integration_runtime_state", integration_runtime_state)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="integrationRuntimeState")
    def integration_runtime_state(self) -> str:
        """
        Current state of the Integration runtime.
        """
        return pulumi.get(self, "integration_runtime_state")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state to track the async operation status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")


class AwaitableGetSqlMigrationServiceResult(GetSqlMigrationServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlMigrationServiceResult(
            id=self.id,
            integration_runtime_state=self.integration_runtime_state,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_sql_migration_service(resource_group_name: Optional[str] = None,
                              sql_migration_service_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlMigrationServiceResult:
    """
    A SQL Migration Service.


    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_migration_service_name: Name of the SQL Migration Service.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlMigrationServiceName'] = sql_migration_service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:datamigration/v20211030preview:getSqlMigrationService', __args__, opts=opts, typ=GetSqlMigrationServiceResult).value

    return AwaitableGetSqlMigrationServiceResult(
        id=__ret__.id,
        integration_runtime_state=__ret__.integration_runtime_state,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_sql_migration_service)
def get_sql_migration_service_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                     sql_migration_service_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlMigrationServiceResult]:
    """
    A SQL Migration Service.


    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_migration_service_name: Name of the SQL Migration Service.
    """
    ...
