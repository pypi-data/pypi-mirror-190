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
    'GetScalingPlanPooledScheduleResult',
    'AwaitableGetScalingPlanPooledScheduleResult',
    'get_scaling_plan_pooled_schedule',
    'get_scaling_plan_pooled_schedule_output',
]

@pulumi.output_type
class GetScalingPlanPooledScheduleResult:
    """
    Represents a ScalingPlanPooledSchedule definition.
    """
    def __init__(__self__, days_of_week=None, id=None, name=None, off_peak_load_balancing_algorithm=None, off_peak_start_time=None, peak_load_balancing_algorithm=None, peak_start_time=None, ramp_down_capacity_threshold_pct=None, ramp_down_force_logoff_users=None, ramp_down_load_balancing_algorithm=None, ramp_down_minimum_hosts_pct=None, ramp_down_notification_message=None, ramp_down_start_time=None, ramp_down_stop_hosts_when=None, ramp_down_wait_time_minutes=None, ramp_up_capacity_threshold_pct=None, ramp_up_load_balancing_algorithm=None, ramp_up_minimum_hosts_pct=None, ramp_up_start_time=None, system_data=None, type=None):
        if days_of_week and not isinstance(days_of_week, list):
            raise TypeError("Expected argument 'days_of_week' to be a list")
        pulumi.set(__self__, "days_of_week", days_of_week)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if off_peak_load_balancing_algorithm and not isinstance(off_peak_load_balancing_algorithm, str):
            raise TypeError("Expected argument 'off_peak_load_balancing_algorithm' to be a str")
        pulumi.set(__self__, "off_peak_load_balancing_algorithm", off_peak_load_balancing_algorithm)
        if off_peak_start_time and not isinstance(off_peak_start_time, dict):
            raise TypeError("Expected argument 'off_peak_start_time' to be a dict")
        pulumi.set(__self__, "off_peak_start_time", off_peak_start_time)
        if peak_load_balancing_algorithm and not isinstance(peak_load_balancing_algorithm, str):
            raise TypeError("Expected argument 'peak_load_balancing_algorithm' to be a str")
        pulumi.set(__self__, "peak_load_balancing_algorithm", peak_load_balancing_algorithm)
        if peak_start_time and not isinstance(peak_start_time, dict):
            raise TypeError("Expected argument 'peak_start_time' to be a dict")
        pulumi.set(__self__, "peak_start_time", peak_start_time)
        if ramp_down_capacity_threshold_pct and not isinstance(ramp_down_capacity_threshold_pct, int):
            raise TypeError("Expected argument 'ramp_down_capacity_threshold_pct' to be a int")
        pulumi.set(__self__, "ramp_down_capacity_threshold_pct", ramp_down_capacity_threshold_pct)
        if ramp_down_force_logoff_users and not isinstance(ramp_down_force_logoff_users, bool):
            raise TypeError("Expected argument 'ramp_down_force_logoff_users' to be a bool")
        pulumi.set(__self__, "ramp_down_force_logoff_users", ramp_down_force_logoff_users)
        if ramp_down_load_balancing_algorithm and not isinstance(ramp_down_load_balancing_algorithm, str):
            raise TypeError("Expected argument 'ramp_down_load_balancing_algorithm' to be a str")
        pulumi.set(__self__, "ramp_down_load_balancing_algorithm", ramp_down_load_balancing_algorithm)
        if ramp_down_minimum_hosts_pct and not isinstance(ramp_down_minimum_hosts_pct, int):
            raise TypeError("Expected argument 'ramp_down_minimum_hosts_pct' to be a int")
        pulumi.set(__self__, "ramp_down_minimum_hosts_pct", ramp_down_minimum_hosts_pct)
        if ramp_down_notification_message and not isinstance(ramp_down_notification_message, str):
            raise TypeError("Expected argument 'ramp_down_notification_message' to be a str")
        pulumi.set(__self__, "ramp_down_notification_message", ramp_down_notification_message)
        if ramp_down_start_time and not isinstance(ramp_down_start_time, dict):
            raise TypeError("Expected argument 'ramp_down_start_time' to be a dict")
        pulumi.set(__self__, "ramp_down_start_time", ramp_down_start_time)
        if ramp_down_stop_hosts_when and not isinstance(ramp_down_stop_hosts_when, str):
            raise TypeError("Expected argument 'ramp_down_stop_hosts_when' to be a str")
        pulumi.set(__self__, "ramp_down_stop_hosts_when", ramp_down_stop_hosts_when)
        if ramp_down_wait_time_minutes and not isinstance(ramp_down_wait_time_minutes, int):
            raise TypeError("Expected argument 'ramp_down_wait_time_minutes' to be a int")
        pulumi.set(__self__, "ramp_down_wait_time_minutes", ramp_down_wait_time_minutes)
        if ramp_up_capacity_threshold_pct and not isinstance(ramp_up_capacity_threshold_pct, int):
            raise TypeError("Expected argument 'ramp_up_capacity_threshold_pct' to be a int")
        pulumi.set(__self__, "ramp_up_capacity_threshold_pct", ramp_up_capacity_threshold_pct)
        if ramp_up_load_balancing_algorithm and not isinstance(ramp_up_load_balancing_algorithm, str):
            raise TypeError("Expected argument 'ramp_up_load_balancing_algorithm' to be a str")
        pulumi.set(__self__, "ramp_up_load_balancing_algorithm", ramp_up_load_balancing_algorithm)
        if ramp_up_minimum_hosts_pct and not isinstance(ramp_up_minimum_hosts_pct, int):
            raise TypeError("Expected argument 'ramp_up_minimum_hosts_pct' to be a int")
        pulumi.set(__self__, "ramp_up_minimum_hosts_pct", ramp_up_minimum_hosts_pct)
        if ramp_up_start_time and not isinstance(ramp_up_start_time, dict):
            raise TypeError("Expected argument 'ramp_up_start_time' to be a dict")
        pulumi.set(__self__, "ramp_up_start_time", ramp_up_start_time)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="daysOfWeek")
    def days_of_week(self) -> Optional[Sequence[str]]:
        """
        Set of days of the week on which this schedule is active.
        """
        return pulumi.get(self, "days_of_week")

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
    @pulumi.getter(name="offPeakLoadBalancingAlgorithm")
    def off_peak_load_balancing_algorithm(self) -> Optional[str]:
        """
        Load balancing algorithm for off-peak period.
        """
        return pulumi.get(self, "off_peak_load_balancing_algorithm")

    @property
    @pulumi.getter(name="offPeakStartTime")
    def off_peak_start_time(self) -> Optional['outputs.TimeResponse']:
        """
        Starting time for off-peak period.
        """
        return pulumi.get(self, "off_peak_start_time")

    @property
    @pulumi.getter(name="peakLoadBalancingAlgorithm")
    def peak_load_balancing_algorithm(self) -> Optional[str]:
        """
        Load balancing algorithm for peak period.
        """
        return pulumi.get(self, "peak_load_balancing_algorithm")

    @property
    @pulumi.getter(name="peakStartTime")
    def peak_start_time(self) -> Optional['outputs.TimeResponse']:
        """
        Starting time for peak period.
        """
        return pulumi.get(self, "peak_start_time")

    @property
    @pulumi.getter(name="rampDownCapacityThresholdPct")
    def ramp_down_capacity_threshold_pct(self) -> Optional[int]:
        """
        Capacity threshold for ramp down period.
        """
        return pulumi.get(self, "ramp_down_capacity_threshold_pct")

    @property
    @pulumi.getter(name="rampDownForceLogoffUsers")
    def ramp_down_force_logoff_users(self) -> Optional[bool]:
        """
        Should users be logged off forcefully from hosts.
        """
        return pulumi.get(self, "ramp_down_force_logoff_users")

    @property
    @pulumi.getter(name="rampDownLoadBalancingAlgorithm")
    def ramp_down_load_balancing_algorithm(self) -> Optional[str]:
        """
        Load balancing algorithm for ramp down period.
        """
        return pulumi.get(self, "ramp_down_load_balancing_algorithm")

    @property
    @pulumi.getter(name="rampDownMinimumHostsPct")
    def ramp_down_minimum_hosts_pct(self) -> Optional[int]:
        """
        Minimum host percentage for ramp down period.
        """
        return pulumi.get(self, "ramp_down_minimum_hosts_pct")

    @property
    @pulumi.getter(name="rampDownNotificationMessage")
    def ramp_down_notification_message(self) -> Optional[str]:
        """
        Notification message for users during ramp down period.
        """
        return pulumi.get(self, "ramp_down_notification_message")

    @property
    @pulumi.getter(name="rampDownStartTime")
    def ramp_down_start_time(self) -> Optional['outputs.TimeResponse']:
        """
        Starting time for ramp down period.
        """
        return pulumi.get(self, "ramp_down_start_time")

    @property
    @pulumi.getter(name="rampDownStopHostsWhen")
    def ramp_down_stop_hosts_when(self) -> Optional[str]:
        """
        Specifies when to stop hosts during ramp down period.
        """
        return pulumi.get(self, "ramp_down_stop_hosts_when")

    @property
    @pulumi.getter(name="rampDownWaitTimeMinutes")
    def ramp_down_wait_time_minutes(self) -> Optional[int]:
        """
        Number of minutes to wait to stop hosts during ramp down period.
        """
        return pulumi.get(self, "ramp_down_wait_time_minutes")

    @property
    @pulumi.getter(name="rampUpCapacityThresholdPct")
    def ramp_up_capacity_threshold_pct(self) -> Optional[int]:
        """
        Capacity threshold for ramp up period.
        """
        return pulumi.get(self, "ramp_up_capacity_threshold_pct")

    @property
    @pulumi.getter(name="rampUpLoadBalancingAlgorithm")
    def ramp_up_load_balancing_algorithm(self) -> Optional[str]:
        """
        Load balancing algorithm for ramp up period.
        """
        return pulumi.get(self, "ramp_up_load_balancing_algorithm")

    @property
    @pulumi.getter(name="rampUpMinimumHostsPct")
    def ramp_up_minimum_hosts_pct(self) -> Optional[int]:
        """
        Minimum host percentage for ramp up period.
        """
        return pulumi.get(self, "ramp_up_minimum_hosts_pct")

    @property
    @pulumi.getter(name="rampUpStartTime")
    def ramp_up_start_time(self) -> Optional['outputs.TimeResponse']:
        """
        Starting time for ramp up period.
        """
        return pulumi.get(self, "ramp_up_start_time")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetScalingPlanPooledScheduleResult(GetScalingPlanPooledScheduleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScalingPlanPooledScheduleResult(
            days_of_week=self.days_of_week,
            id=self.id,
            name=self.name,
            off_peak_load_balancing_algorithm=self.off_peak_load_balancing_algorithm,
            off_peak_start_time=self.off_peak_start_time,
            peak_load_balancing_algorithm=self.peak_load_balancing_algorithm,
            peak_start_time=self.peak_start_time,
            ramp_down_capacity_threshold_pct=self.ramp_down_capacity_threshold_pct,
            ramp_down_force_logoff_users=self.ramp_down_force_logoff_users,
            ramp_down_load_balancing_algorithm=self.ramp_down_load_balancing_algorithm,
            ramp_down_minimum_hosts_pct=self.ramp_down_minimum_hosts_pct,
            ramp_down_notification_message=self.ramp_down_notification_message,
            ramp_down_start_time=self.ramp_down_start_time,
            ramp_down_stop_hosts_when=self.ramp_down_stop_hosts_when,
            ramp_down_wait_time_minutes=self.ramp_down_wait_time_minutes,
            ramp_up_capacity_threshold_pct=self.ramp_up_capacity_threshold_pct,
            ramp_up_load_balancing_algorithm=self.ramp_up_load_balancing_algorithm,
            ramp_up_minimum_hosts_pct=self.ramp_up_minimum_hosts_pct,
            ramp_up_start_time=self.ramp_up_start_time,
            system_data=self.system_data,
            type=self.type)


def get_scaling_plan_pooled_schedule(resource_group_name: Optional[str] = None,
                                     scaling_plan_name: Optional[str] = None,
                                     scaling_plan_schedule_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScalingPlanPooledScheduleResult:
    """
    Represents a ScalingPlanPooledSchedule definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str scaling_plan_name: The name of the scaling plan.
    :param str scaling_plan_schedule_name: The name of the ScalingPlanSchedule
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['scalingPlanName'] = scaling_plan_name
    __args__['scalingPlanScheduleName'] = scaling_plan_schedule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:desktopvirtualization/v20220909:getScalingPlanPooledSchedule', __args__, opts=opts, typ=GetScalingPlanPooledScheduleResult).value

    return AwaitableGetScalingPlanPooledScheduleResult(
        days_of_week=__ret__.days_of_week,
        id=__ret__.id,
        name=__ret__.name,
        off_peak_load_balancing_algorithm=__ret__.off_peak_load_balancing_algorithm,
        off_peak_start_time=__ret__.off_peak_start_time,
        peak_load_balancing_algorithm=__ret__.peak_load_balancing_algorithm,
        peak_start_time=__ret__.peak_start_time,
        ramp_down_capacity_threshold_pct=__ret__.ramp_down_capacity_threshold_pct,
        ramp_down_force_logoff_users=__ret__.ramp_down_force_logoff_users,
        ramp_down_load_balancing_algorithm=__ret__.ramp_down_load_balancing_algorithm,
        ramp_down_minimum_hosts_pct=__ret__.ramp_down_minimum_hosts_pct,
        ramp_down_notification_message=__ret__.ramp_down_notification_message,
        ramp_down_start_time=__ret__.ramp_down_start_time,
        ramp_down_stop_hosts_when=__ret__.ramp_down_stop_hosts_when,
        ramp_down_wait_time_minutes=__ret__.ramp_down_wait_time_minutes,
        ramp_up_capacity_threshold_pct=__ret__.ramp_up_capacity_threshold_pct,
        ramp_up_load_balancing_algorithm=__ret__.ramp_up_load_balancing_algorithm,
        ramp_up_minimum_hosts_pct=__ret__.ramp_up_minimum_hosts_pct,
        ramp_up_start_time=__ret__.ramp_up_start_time,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_scaling_plan_pooled_schedule)
def get_scaling_plan_pooled_schedule_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                            scaling_plan_name: Optional[pulumi.Input[str]] = None,
                                            scaling_plan_schedule_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScalingPlanPooledScheduleResult]:
    """
    Represents a ScalingPlanPooledSchedule definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str scaling_plan_name: The name of the scaling plan.
    :param str scaling_plan_schedule_name: The name of the ScalingPlanSchedule
    """
    ...
