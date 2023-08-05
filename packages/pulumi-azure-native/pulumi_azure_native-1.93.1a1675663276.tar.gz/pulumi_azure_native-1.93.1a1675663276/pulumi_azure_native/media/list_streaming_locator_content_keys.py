# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'ListStreamingLocatorContentKeysResult',
    'AwaitableListStreamingLocatorContentKeysResult',
    'list_streaming_locator_content_keys',
    'list_streaming_locator_content_keys_output',
]

@pulumi.output_type
class ListStreamingLocatorContentKeysResult:
    """
    Class of response for listContentKeys action
    """
    def __init__(__self__, content_keys=None):
        if content_keys and not isinstance(content_keys, list):
            raise TypeError("Expected argument 'content_keys' to be a list")
        pulumi.set(__self__, "content_keys", content_keys)

    @property
    @pulumi.getter(name="contentKeys")
    def content_keys(self) -> Optional[Sequence['outputs.StreamingLocatorContentKeyResponse']]:
        """
        ContentKeys used by current Streaming Locator
        """
        return pulumi.get(self, "content_keys")


class AwaitableListStreamingLocatorContentKeysResult(ListStreamingLocatorContentKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListStreamingLocatorContentKeysResult(
            content_keys=self.content_keys)


def list_streaming_locator_content_keys(account_name: Optional[str] = None,
                                        resource_group_name: Optional[str] = None,
                                        streaming_locator_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListStreamingLocatorContentKeysResult:
    """
    Class of response for listContentKeys action
    API Version: 2020-05-01.


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_locator_name: The Streaming Locator name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['streamingLocatorName'] = streaming_locator_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:media:listStreamingLocatorContentKeys', __args__, opts=opts, typ=ListStreamingLocatorContentKeysResult).value

    return AwaitableListStreamingLocatorContentKeysResult(
        content_keys=__ret__.content_keys)


@_utilities.lift_output_func(list_streaming_locator_content_keys)
def list_streaming_locator_content_keys_output(account_name: Optional[pulumi.Input[str]] = None,
                                               resource_group_name: Optional[pulumi.Input[str]] = None,
                                               streaming_locator_name: Optional[pulumi.Input[str]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListStreamingLocatorContentKeysResult]:
    """
    Class of response for listContentKeys action
    API Version: 2020-05-01.


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_locator_name: The Streaming Locator name.
    """
    ...
