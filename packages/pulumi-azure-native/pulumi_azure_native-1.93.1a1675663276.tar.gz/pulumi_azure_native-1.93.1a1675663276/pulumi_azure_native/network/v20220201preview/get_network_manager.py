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
    'GetNetworkManagerResult',
    'AwaitableGetNetworkManagerResult',
    'get_network_manager',
    'get_network_manager_output',
]

@pulumi.output_type
class GetNetworkManagerResult:
    """
    The Managed Network resource
    """
    def __init__(__self__, description=None, etag=None, id=None, location=None, name=None, network_manager_scope_accesses=None, network_manager_scopes=None, provisioning_state=None, system_data=None, tags=None, type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_manager_scope_accesses and not isinstance(network_manager_scope_accesses, list):
            raise TypeError("Expected argument 'network_manager_scope_accesses' to be a list")
        pulumi.set(__self__, "network_manager_scope_accesses", network_manager_scope_accesses)
        if network_manager_scopes and not isinstance(network_manager_scopes, dict):
            raise TypeError("Expected argument 'network_manager_scopes' to be a dict")
        pulumi.set(__self__, "network_manager_scopes", network_manager_scopes)
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
    def description(self) -> Optional[str]:
        """
        A description of the network manager.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkManagerScopeAccesses")
    def network_manager_scope_accesses(self) -> Sequence[str]:
        """
        Scope Access.
        """
        return pulumi.get(self, "network_manager_scope_accesses")

    @property
    @pulumi.getter(name="networkManagerScopes")
    def network_manager_scopes(self) -> 'outputs.NetworkManagerPropertiesResponseNetworkManagerScopes':
        """
        Scope of Network Manager.
        """
        return pulumi.get(self, "network_manager_scopes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the scope assignment resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetNetworkManagerResult(GetNetworkManagerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkManagerResult(
            description=self.description,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            network_manager_scope_accesses=self.network_manager_scope_accesses,
            network_manager_scopes=self.network_manager_scopes,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_network_manager(network_manager_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkManagerResult:
    """
    The Managed Network resource


    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['networkManagerName'] = network_manager_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220201preview:getNetworkManager', __args__, opts=opts, typ=GetNetworkManagerResult).value

    return AwaitableGetNetworkManagerResult(
        description=__ret__.description,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        network_manager_scope_accesses=__ret__.network_manager_scope_accesses,
        network_manager_scopes=__ret__.network_manager_scopes,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_network_manager)
def get_network_manager_output(network_manager_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkManagerResult]:
    """
    The Managed Network resource


    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    """
    ...
