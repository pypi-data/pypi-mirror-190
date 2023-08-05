# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWebAppHostKeysResult',
    'AwaitableListWebAppHostKeysResult',
    'list_web_app_host_keys',
    'list_web_app_host_keys_output',
]

@pulumi.output_type
class ListWebAppHostKeysResult:
    """
    Functions host level keys.
    """
    def __init__(__self__, function_keys=None, master_key=None, system_keys=None):
        if function_keys and not isinstance(function_keys, dict):
            raise TypeError("Expected argument 'function_keys' to be a dict")
        pulumi.set(__self__, "function_keys", function_keys)
        if master_key and not isinstance(master_key, str):
            raise TypeError("Expected argument 'master_key' to be a str")
        pulumi.set(__self__, "master_key", master_key)
        if system_keys and not isinstance(system_keys, dict):
            raise TypeError("Expected argument 'system_keys' to be a dict")
        pulumi.set(__self__, "system_keys", system_keys)

    @property
    @pulumi.getter(name="functionKeys")
    def function_keys(self) -> Optional[Mapping[str, str]]:
        """
        Host level function keys.
        """
        return pulumi.get(self, "function_keys")

    @property
    @pulumi.getter(name="masterKey")
    def master_key(self) -> Optional[str]:
        """
        Secret key.
        """
        return pulumi.get(self, "master_key")

    @property
    @pulumi.getter(name="systemKeys")
    def system_keys(self) -> Optional[Mapping[str, str]]:
        """
        System keys.
        """
        return pulumi.get(self, "system_keys")


class AwaitableListWebAppHostKeysResult(ListWebAppHostKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppHostKeysResult(
            function_keys=self.function_keys,
            master_key=self.master_key,
            system_keys=self.system_keys)


def list_web_app_host_keys(name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppHostKeysResult:
    """
    Functions host level keys.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20220301:listWebAppHostKeys', __args__, opts=opts, typ=ListWebAppHostKeysResult).value

    return AwaitableListWebAppHostKeysResult(
        function_keys=__ret__.function_keys,
        master_key=__ret__.master_key,
        system_keys=__ret__.system_keys)


@_utilities.lift_output_func(list_web_app_host_keys)
def list_web_app_host_keys_output(name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWebAppHostKeysResult]:
    """
    Functions host level keys.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
