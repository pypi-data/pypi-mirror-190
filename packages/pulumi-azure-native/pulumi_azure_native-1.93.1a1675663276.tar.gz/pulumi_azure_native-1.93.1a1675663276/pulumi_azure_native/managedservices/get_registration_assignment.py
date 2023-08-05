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
    'GetRegistrationAssignmentResult',
    'AwaitableGetRegistrationAssignmentResult',
    'get_registration_assignment',
    'get_registration_assignment_output',
]

@pulumi.output_type
class GetRegistrationAssignmentResult:
    """
    Registration assignment.
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
        The fully qualified path of the registration assignment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the registration assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.RegistrationAssignmentPropertiesResponse':
        """
        Properties of a registration assignment.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetRegistrationAssignmentResult(GetRegistrationAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistrationAssignmentResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_registration_assignment(expand_registration_definition: Optional[bool] = None,
                                registration_assignment_id: Optional[str] = None,
                                scope: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistrationAssignmentResult:
    """
    Registration assignment.
    API Version: 2019-09-01.


    :param bool expand_registration_definition: Tells whether to return registration definition details also along with registration assignment details.
    :param str registration_assignment_id: Guid of the registration assignment.
    :param str scope: Scope of the resource.
    """
    __args__ = dict()
    __args__['expandRegistrationDefinition'] = expand_registration_definition
    __args__['registrationAssignmentId'] = registration_assignment_id
    __args__['scope'] = scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:managedservices:getRegistrationAssignment', __args__, opts=opts, typ=GetRegistrationAssignmentResult).value

    return AwaitableGetRegistrationAssignmentResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_registration_assignment)
def get_registration_assignment_output(expand_registration_definition: Optional[pulumi.Input[Optional[bool]]] = None,
                                       registration_assignment_id: Optional[pulumi.Input[str]] = None,
                                       scope: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegistrationAssignmentResult]:
    """
    Registration assignment.
    API Version: 2019-09-01.


    :param bool expand_registration_definition: Tells whether to return registration definition details also along with registration assignment details.
    :param str registration_assignment_id: Guid of the registration assignment.
    :param str scope: Scope of the resource.
    """
    ...
