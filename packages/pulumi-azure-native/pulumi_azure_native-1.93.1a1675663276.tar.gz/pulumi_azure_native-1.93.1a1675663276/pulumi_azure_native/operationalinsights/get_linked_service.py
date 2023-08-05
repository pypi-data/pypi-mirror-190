# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetLinkedServiceResult',
    'AwaitableGetLinkedServiceResult',
    'get_linked_service',
    'get_linked_service_output',
]

@pulumi.output_type
class GetLinkedServiceResult:
    """
    The top level Linked service resource container.
    """
    def __init__(__self__, id=None, name=None, provisioning_state=None, resource_id=None, tags=None, type=None, write_access_resource_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if write_access_resource_id and not isinstance(write_access_resource_id, str):
            raise TypeError("Expected argument 'write_access_resource_id' to be a str")
        pulumi.set(__self__, "write_access_resource_id", write_access_resource_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning state of the linked service.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The resource id of the resource that will be linked to the workspace. This should be used for linking resources which require read access
        """
        return pulumi.get(self, "resource_id")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="writeAccessResourceId")
    def write_access_resource_id(self) -> Optional[str]:
        """
        The resource id of the resource that will be linked to the workspace. This should be used for linking resources which require write access
        """
        return pulumi.get(self, "write_access_resource_id")


class AwaitableGetLinkedServiceResult(GetLinkedServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkedServiceResult(
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            resource_id=self.resource_id,
            tags=self.tags,
            type=self.type,
            write_access_resource_id=self.write_access_resource_id)


def get_linked_service(linked_service_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       workspace_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkedServiceResult:
    """
    The top level Linked service resource container.
    API Version: 2020-08-01.


    :param str linked_service_name: Name of the linked service.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['linkedServiceName'] = linked_service_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:operationalinsights:getLinkedService', __args__, opts=opts, typ=GetLinkedServiceResult).value

    return AwaitableGetLinkedServiceResult(
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        resource_id=__ret__.resource_id,
        tags=__ret__.tags,
        type=__ret__.type,
        write_access_resource_id=__ret__.write_access_resource_id)


@_utilities.lift_output_func(get_linked_service)
def get_linked_service_output(linked_service_name: Optional[pulumi.Input[str]] = None,
                              resource_group_name: Optional[pulumi.Input[str]] = None,
                              workspace_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinkedServiceResult]:
    """
    The top level Linked service resource container.
    API Version: 2020-08-01.


    :param str linked_service_name: Name of the linked service.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
