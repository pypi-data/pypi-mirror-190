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
    'GetSubscriptionAliasResult',
    'AwaitableGetSubscriptionAliasResult',
    'get_subscription_alias',
    'get_subscription_alias_output',
]

warnings.warn("""Version 2019-10-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSubscriptionAliasResult:
    """
    Subscription Information with the alias.
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
        Fully qualified ID for the alias resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Alias ID.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.PutAliasResponsePropertiesResponse':
        """
        Put Alias response properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type, Microsoft.Subscription/aliases.
        """
        return pulumi.get(self, "type")


class AwaitableGetSubscriptionAliasResult(GetSubscriptionAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionAliasResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_subscription_alias(alias_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionAliasResult:
    """
    Subscription Information with the alias.


    :param str alias_name: Name for this subscription creation request also known as alias. Note that this is not the same as subscription name and this doesn’t have any other lifecycle need beyond the request for subscription creation.
    """
    pulumi.log.warn("""get_subscription_alias is deprecated: Version 2019-10-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['aliasName'] = alias_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:subscription/v20191001preview:getSubscriptionAlias', __args__, opts=opts, typ=GetSubscriptionAliasResult).value

    return AwaitableGetSubscriptionAliasResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_subscription_alias)
def get_subscription_alias_output(alias_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSubscriptionAliasResult]:
    """
    Subscription Information with the alias.


    :param str alias_name: Name for this subscription creation request also known as alias. Note that this is not the same as subscription name and this doesn’t have any other lifecycle need beyond the request for subscription creation.
    """
    pulumi.log.warn("""get_subscription_alias is deprecated: Version 2019-10-01-preview will be removed in v2 of the provider.""")
    ...
