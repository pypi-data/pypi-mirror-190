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
    'GetDeploymentResult',
    'AwaitableGetDeploymentResult',
    'get_deployment',
    'get_deployment_output',
]

warnings.warn("""Version 2016-02-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetDeploymentResult:
    """
    Deployment information.
    """
    def __init__(__self__, id=None, name=None, properties=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the deployment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the deployment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.DeploymentPropertiesExtendedResponse':
        """
        Deployment properties.
        """
        return pulumi.get(self, "properties")


class AwaitableGetDeploymentResult(GetDeploymentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeploymentResult(
            id=self.id,
            name=self.name,
            properties=self.properties)


def get_deployment(deployment_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeploymentResult:
    """
    Deployment information.


    :param str deployment_name: The name of the deployment.
    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    """
    pulumi.log.warn("""get_deployment is deprecated: Version 2016-02-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['deploymentName'] = deployment_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:resources/v20160201:getDeployment', __args__, opts=opts, typ=GetDeploymentResult).value

    return AwaitableGetDeploymentResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties)


@_utilities.lift_output_func(get_deployment)
def get_deployment_output(deployment_name: Optional[pulumi.Input[str]] = None,
                          resource_group_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeploymentResult]:
    """
    Deployment information.


    :param str deployment_name: The name of the deployment.
    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    """
    pulumi.log.warn("""get_deployment is deprecated: Version 2016-02-01 will be removed in v2 of the provider.""")
    ...
