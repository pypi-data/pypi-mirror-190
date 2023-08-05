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
    'GetResourceGroupResult',
    'AwaitableGetResourceGroupResult',
    'get_resource_group',
    'get_resource_group_output',
]

@pulumi.output_type
class GetResourceGroupResult:
    """
    Resource group information.
    """
    def __init__(__self__, id=None, location=None, managed_by=None, name=None, properties=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_by and not isinstance(managed_by, str):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, "managed_by", managed_by)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource group. It cannot be changed after the resource group has been created. It must be one of the supported Azure locations.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> Optional[str]:
        """
        The ID of the resource that manages this resource group.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ResourceGroupPropertiesResponse':
        """
        The resource group properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags attached to the resource group.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource group.
        """
        return pulumi.get(self, "type")


class AwaitableGetResourceGroupResult(GetResourceGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceGroupResult(
            id=self.id,
            location=self.location,
            managed_by=self.managed_by,
            name=self.name,
            properties=self.properties,
            tags=self.tags,
            type=self.type)


def get_resource_group(resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceGroupResult:
    """
    Resource group information.


    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:resources/v20191001:getResourceGroup', __args__, opts=opts, typ=GetResourceGroupResult).value

    return AwaitableGetResourceGroupResult(
        id=__ret__.id,
        location=__ret__.location,
        managed_by=__ret__.managed_by,
        name=__ret__.name,
        properties=__ret__.properties,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_resource_group)
def get_resource_group_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourceGroupResult]:
    """
    Resource group information.


    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    """
    ...
