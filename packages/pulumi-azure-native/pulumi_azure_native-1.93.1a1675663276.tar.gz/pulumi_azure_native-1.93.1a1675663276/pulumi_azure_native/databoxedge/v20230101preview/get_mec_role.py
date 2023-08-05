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
    'GetMECRoleResult',
    'AwaitableGetMECRoleResult',
    'get_mec_role',
    'get_mec_role_output',
]

@pulumi.output_type
class GetMECRoleResult:
    """
    MEC role.
    """
    def __init__(__self__, connection_string=None, controller_endpoint=None, id=None, kind=None, name=None, resource_unique_id=None, role_status=None, system_data=None, type=None):
        if connection_string and not isinstance(connection_string, dict):
            raise TypeError("Expected argument 'connection_string' to be a dict")
        pulumi.set(__self__, "connection_string", connection_string)
        if controller_endpoint and not isinstance(controller_endpoint, str):
            raise TypeError("Expected argument 'controller_endpoint' to be a str")
        pulumi.set(__self__, "controller_endpoint", controller_endpoint)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_unique_id and not isinstance(resource_unique_id, str):
            raise TypeError("Expected argument 'resource_unique_id' to be a str")
        pulumi.set(__self__, "resource_unique_id", resource_unique_id)
        if role_status and not isinstance(role_status, str):
            raise TypeError("Expected argument 'role_status' to be a str")
        pulumi.set(__self__, "role_status", role_status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional['outputs.AsymmetricEncryptedSecretResponse']:
        """
        Activation key of the MEC.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter(name="controllerEndpoint")
    def controller_endpoint(self) -> Optional[str]:
        """
        Controller Endpoint.
        """
        return pulumi.get(self, "controller_endpoint")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Role type.
        Expected value is 'MEC'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceUniqueId")
    def resource_unique_id(self) -> Optional[str]:
        """
        Unique Id of the Resource.
        """
        return pulumi.get(self, "resource_unique_id")

    @property
    @pulumi.getter(name="roleStatus")
    def role_status(self) -> str:
        """
        Role status.
        """
        return pulumi.get(self, "role_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of Role
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")


class AwaitableGetMECRoleResult(GetMECRoleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMECRoleResult(
            connection_string=self.connection_string,
            controller_endpoint=self.controller_endpoint,
            id=self.id,
            kind=self.kind,
            name=self.name,
            resource_unique_id=self.resource_unique_id,
            role_status=self.role_status,
            system_data=self.system_data,
            type=self.type)


def get_mec_role(device_name: Optional[str] = None,
                 name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMECRoleResult:
    """
    MEC role.


    :param str device_name: The device name.
    :param str name: The role name.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20230101preview:getMECRole', __args__, opts=opts, typ=GetMECRoleResult).value

    return AwaitableGetMECRoleResult(
        connection_string=__ret__.connection_string,
        controller_endpoint=__ret__.controller_endpoint,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        resource_unique_id=__ret__.resource_unique_id,
        role_status=__ret__.role_status,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_mec_role)
def get_mec_role_output(device_name: Optional[pulumi.Input[str]] = None,
                        name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMECRoleResult]:
    """
    MEC role.


    :param str device_name: The device name.
    :param str name: The role name.
    :param str resource_group_name: The resource group name.
    """
    ...
