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
    'GetTriggerResult',
    'AwaitableGetTriggerResult',
    'get_trigger',
    'get_trigger_output',
]

warnings.warn("""Please use one of the variants: FileEventTrigger, PeriodicTimerEventTrigger.""", DeprecationWarning)

@pulumi.output_type
class GetTriggerResult:
    """
    Trigger details.
    """
    def __init__(__self__, id=None, kind=None, name=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
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
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Trigger Kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of Trigger
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")


class AwaitableGetTriggerResult(GetTriggerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTriggerResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            system_data=self.system_data,
            type=self.type)


def get_trigger(device_name: Optional[str] = None,
                name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTriggerResult:
    """
    Trigger details.


    :param str device_name: The device name.
    :param str name: The trigger name.
    :param str resource_group_name: The resource group name.
    """
    pulumi.log.warn("""get_trigger is deprecated: Please use one of the variants: FileEventTrigger, PeriodicTimerEventTrigger.""")
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20230101preview:getTrigger', __args__, opts=opts, typ=GetTriggerResult).value

    return AwaitableGetTriggerResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_trigger)
def get_trigger_output(device_name: Optional[pulumi.Input[str]] = None,
                       name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTriggerResult]:
    """
    Trigger details.


    :param str device_name: The device name.
    :param str name: The trigger name.
    :param str resource_group_name: The resource group name.
    """
    pulumi.log.warn("""get_trigger is deprecated: Please use one of the variants: FileEventTrigger, PeriodicTimerEventTrigger.""")
    ...
