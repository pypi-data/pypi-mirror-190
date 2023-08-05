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
    'GetTagAtScopeResult',
    'AwaitableGetTagAtScopeResult',
    'get_tag_at_scope',
    'get_tag_at_scope_output',
]

@pulumi.output_type
class GetTagAtScopeResult:
    """
    Wrapper resource for tags API requests and responses.
    """
    def __init__(__self__, id=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the tags wrapper resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the tags wrapper resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.TagsResponse':
        """
        The set of tags.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the tags wrapper resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetTagAtScopeResult(GetTagAtScopeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTagAtScopeResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_tag_at_scope(scope: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTagAtScopeResult:
    """
    Wrapper resource for tags API requests and responses.


    :param str scope: The resource scope.
    """
    __args__ = dict()
    __args__['scope'] = scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:resources/v20200601:getTagAtScope', __args__, opts=opts, typ=GetTagAtScopeResult).value

    return AwaitableGetTagAtScopeResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_tag_at_scope)
def get_tag_at_scope_output(scope: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTagAtScopeResult]:
    """
    Wrapper resource for tags API requests and responses.


    :param str scope: The resource scope.
    """
    ...
