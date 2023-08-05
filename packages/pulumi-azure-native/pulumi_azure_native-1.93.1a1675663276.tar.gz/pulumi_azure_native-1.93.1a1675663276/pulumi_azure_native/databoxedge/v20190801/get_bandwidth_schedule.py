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
    'GetBandwidthScheduleResult',
    'AwaitableGetBandwidthScheduleResult',
    'get_bandwidth_schedule',
    'get_bandwidth_schedule_output',
]

warnings.warn("""Version 2019-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetBandwidthScheduleResult:
    """
    The bandwidth schedule details.
    """
    def __init__(__self__, days=None, id=None, name=None, rate_in_mbps=None, start=None, stop=None, type=None):
        if days and not isinstance(days, list):
            raise TypeError("Expected argument 'days' to be a list")
        pulumi.set(__self__, "days", days)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rate_in_mbps and not isinstance(rate_in_mbps, int):
            raise TypeError("Expected argument 'rate_in_mbps' to be a int")
        pulumi.set(__self__, "rate_in_mbps", rate_in_mbps)
        if start and not isinstance(start, str):
            raise TypeError("Expected argument 'start' to be a str")
        pulumi.set(__self__, "start", start)
        if stop and not isinstance(stop, str):
            raise TypeError("Expected argument 'stop' to be a str")
        pulumi.set(__self__, "stop", stop)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def days(self) -> Sequence[str]:
        """
        The days of the week when this schedule is applicable.
        """
        return pulumi.get(self, "days")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="rateInMbps")
    def rate_in_mbps(self) -> int:
        """
        The bandwidth rate in Mbps.
        """
        return pulumi.get(self, "rate_in_mbps")

    @property
    @pulumi.getter
    def start(self) -> str:
        """
        The start time of the schedule in UTC.
        """
        return pulumi.get(self, "start")

    @property
    @pulumi.getter
    def stop(self) -> str:
        """
        The stop time of the schedule in UTC.
        """
        return pulumi.get(self, "stop")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")


class AwaitableGetBandwidthScheduleResult(GetBandwidthScheduleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBandwidthScheduleResult(
            days=self.days,
            id=self.id,
            name=self.name,
            rate_in_mbps=self.rate_in_mbps,
            start=self.start,
            stop=self.stop,
            type=self.type)


def get_bandwidth_schedule(device_name: Optional[str] = None,
                           name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBandwidthScheduleResult:
    """
    The bandwidth schedule details.


    :param str device_name: The device name.
    :param str name: The bandwidth schedule name.
    :param str resource_group_name: The resource group name.
    """
    pulumi.log.warn("""get_bandwidth_schedule is deprecated: Version 2019-08-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20190801:getBandwidthSchedule', __args__, opts=opts, typ=GetBandwidthScheduleResult).value

    return AwaitableGetBandwidthScheduleResult(
        days=__ret__.days,
        id=__ret__.id,
        name=__ret__.name,
        rate_in_mbps=__ret__.rate_in_mbps,
        start=__ret__.start,
        stop=__ret__.stop,
        type=__ret__.type)


@_utilities.lift_output_func(get_bandwidth_schedule)
def get_bandwidth_schedule_output(device_name: Optional[pulumi.Input[str]] = None,
                                  name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBandwidthScheduleResult]:
    """
    The bandwidth schedule details.


    :param str device_name: The device name.
    :param str name: The bandwidth schedule name.
    :param str resource_group_name: The resource group name.
    """
    pulumi.log.warn("""get_bandwidth_schedule is deprecated: Version 2019-08-01 will be removed in v2 of the provider.""")
    ...
