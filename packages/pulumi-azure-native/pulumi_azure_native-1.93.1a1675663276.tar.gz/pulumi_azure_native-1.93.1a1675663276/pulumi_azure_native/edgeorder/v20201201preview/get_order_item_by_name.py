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
    'GetOrderItemByNameResult',
    'AwaitableGetOrderItemByNameResult',
    'get_order_item_by_name',
    'get_order_item_by_name_output',
]

warnings.warn("""Version 2020-12-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetOrderItemByNameResult:
    """
    Represents order item contract
    """
    def __init__(__self__, address_details=None, id=None, location=None, name=None, order_id=None, order_item_details=None, start_time=None, system_data=None, tags=None, type=None):
        if address_details and not isinstance(address_details, dict):
            raise TypeError("Expected argument 'address_details' to be a dict")
        pulumi.set(__self__, "address_details", address_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if order_id and not isinstance(order_id, str):
            raise TypeError("Expected argument 'order_id' to be a str")
        pulumi.set(__self__, "order_id", order_id)
        if order_item_details and not isinstance(order_item_details, dict):
            raise TypeError("Expected argument 'order_item_details' to be a dict")
        pulumi.set(__self__, "order_item_details", order_item_details)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
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
    @pulumi.getter(name="addressDetails")
    def address_details(self) -> 'outputs.AddressDetailsResponse':
        """
        Represents shipping and return address for order item
        """
        return pulumi.get(self, "address_details")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orderId")
    def order_id(self) -> str:
        """
        Id of the order to which order item belongs to
        """
        return pulumi.get(self, "order_id")

    @property
    @pulumi.getter(name="orderItemDetails")
    def order_item_details(self) -> 'outputs.OrderItemDetailsResponse':
        """
        Represents order item details.
        """
        return pulumi.get(self, "order_item_details")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        Start time of order item
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Represents resource creation and update time
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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetOrderItemByNameResult(GetOrderItemByNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrderItemByNameResult(
            address_details=self.address_details,
            id=self.id,
            location=self.location,
            name=self.name,
            order_id=self.order_id,
            order_item_details=self.order_item_details,
            start_time=self.start_time,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_order_item_by_name(expand: Optional[str] = None,
                           order_item_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrderItemByNameResult:
    """
    Represents order item contract


    :param str expand: $expand is supported on device details, forward shipping details and reverse shipping details parameters. Each of these can be provided as a comma separated list. Device Details for order item provides details on the devices of the product, Forward and Reverse Shipping details provide forward and reverse shipping details respectively.
    :param str order_item_name: The name of the order item
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_order_item_by_name is deprecated: Version 2020-12-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['expand'] = expand
    __args__['orderItemName'] = order_item_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:edgeorder/v20201201preview:getOrderItemByName', __args__, opts=opts, typ=GetOrderItemByNameResult).value

    return AwaitableGetOrderItemByNameResult(
        address_details=__ret__.address_details,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        order_id=__ret__.order_id,
        order_item_details=__ret__.order_item_details,
        start_time=__ret__.start_time,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_order_item_by_name)
def get_order_item_by_name_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                  order_item_name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrderItemByNameResult]:
    """
    Represents order item contract


    :param str expand: $expand is supported on device details, forward shipping details and reverse shipping details parameters. Each of these can be provided as a comma separated list. Device Details for order item provides details on the devices of the product, Forward and Reverse Shipping details provide forward and reverse shipping details respectively.
    :param str order_item_name: The name of the order item
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_order_item_by_name is deprecated: Version 2020-12-01-preview will be removed in v2 of the provider.""")
    ...
