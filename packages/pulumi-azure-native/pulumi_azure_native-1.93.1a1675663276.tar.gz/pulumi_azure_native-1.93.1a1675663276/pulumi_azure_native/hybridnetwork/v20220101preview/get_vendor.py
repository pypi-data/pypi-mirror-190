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
    'GetVendorResult',
    'AwaitableGetVendorResult',
    'get_vendor',
    'get_vendor_output',
]

@pulumi.output_type
class GetVendorResult:
    """
    Vendor resource.
    """
    def __init__(__self__, id=None, name=None, provisioning_state=None, skus=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if skus and not isinstance(skus, list):
            raise TypeError("Expected argument 'skus' to be a list")
        pulumi.set(__self__, "skus", skus)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

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
    def provisioning_state(self) -> str:
        """
        The provisioning state of the vendor resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def skus(self) -> Sequence['outputs.SubResourceResponse']:
        """
        A list of IDs of the vendor skus offered by the vendor.
        """
        return pulumi.get(self, "skus")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetVendorResult(GetVendorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVendorResult(
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            skus=self.skus,
            system_data=self.system_data,
            type=self.type)


def get_vendor(vendor_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVendorResult:
    """
    Vendor resource.


    :param str vendor_name: The name of the vendor.
    """
    __args__ = dict()
    __args__['vendorName'] = vendor_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:hybridnetwork/v20220101preview:getVendor', __args__, opts=opts, typ=GetVendorResult).value

    return AwaitableGetVendorResult(
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        skus=__ret__.skus,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_vendor)
def get_vendor_output(vendor_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVendorResult]:
    """
    Vendor resource.


    :param str vendor_name: The name of the vendor.
    """
    ...
