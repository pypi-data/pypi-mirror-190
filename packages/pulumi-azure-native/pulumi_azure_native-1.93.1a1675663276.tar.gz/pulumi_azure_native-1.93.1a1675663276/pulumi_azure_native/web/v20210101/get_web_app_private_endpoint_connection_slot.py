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
    'GetWebAppPrivateEndpointConnectionSlotResult',
    'AwaitableGetWebAppPrivateEndpointConnectionSlotResult',
    'get_web_app_private_endpoint_connection_slot',
    'get_web_app_private_endpoint_connection_slot_output',
]

@pulumi.output_type
class GetWebAppPrivateEndpointConnectionSlotResult:
    """
    Remote Private Endpoint Connection ARM resource.
    """
    def __init__(__self__, id=None, ip_addresses=None, kind=None, name=None, private_endpoint=None, private_link_service_connection_state=None, provisioning_state=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_addresses and not isinstance(ip_addresses, list):
            raise TypeError("Expected argument 'ip_addresses' to be a list")
        pulumi.set(__self__, "ip_addresses", ip_addresses)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint and not isinstance(private_endpoint, dict):
            raise TypeError("Expected argument 'private_endpoint' to be a dict")
        pulumi.set(__self__, "private_endpoint", private_endpoint)
        if private_link_service_connection_state and not isinstance(private_link_service_connection_state, dict):
            raise TypeError("Expected argument 'private_link_service_connection_state' to be a dict")
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        Private IPAddresses mapped to the remote private endpoint
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.ArmIdWrapperResponse']:
        """
        PrivateEndpoint of a remote private endpoint connection
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkConnectionStateResponse']:
        """
        The state of a private link connection
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWebAppPrivateEndpointConnectionSlotResult(GetWebAppPrivateEndpointConnectionSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppPrivateEndpointConnectionSlotResult(
            id=self.id,
            ip_addresses=self.ip_addresses,
            kind=self.kind,
            name=self.name,
            private_endpoint=self.private_endpoint,
            private_link_service_connection_state=self.private_link_service_connection_state,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_web_app_private_endpoint_connection_slot(name: Optional[str] = None,
                                                 private_endpoint_connection_name: Optional[str] = None,
                                                 resource_group_name: Optional[str] = None,
                                                 slot: Optional[str] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppPrivateEndpointConnectionSlotResult:
    """
    Remote Private Endpoint Connection ARM resource.


    :param str name: Name of the site.
    :param str private_endpoint_connection_name: Name of the private endpoint connection.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the site deployment slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210101:getWebAppPrivateEndpointConnectionSlot', __args__, opts=opts, typ=GetWebAppPrivateEndpointConnectionSlotResult).value

    return AwaitableGetWebAppPrivateEndpointConnectionSlotResult(
        id=__ret__.id,
        ip_addresses=__ret__.ip_addresses,
        kind=__ret__.kind,
        name=__ret__.name,
        private_endpoint=__ret__.private_endpoint,
        private_link_service_connection_state=__ret__.private_link_service_connection_state,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_web_app_private_endpoint_connection_slot)
def get_web_app_private_endpoint_connection_slot_output(name: Optional[pulumi.Input[str]] = None,
                                                        private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                                        slot: Optional[pulumi.Input[str]] = None,
                                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppPrivateEndpointConnectionSlotResult]:
    """
    Remote Private Endpoint Connection ARM resource.


    :param str name: Name of the site.
    :param str private_endpoint_connection_name: Name of the private endpoint connection.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the site deployment slot.
    """
    ...
