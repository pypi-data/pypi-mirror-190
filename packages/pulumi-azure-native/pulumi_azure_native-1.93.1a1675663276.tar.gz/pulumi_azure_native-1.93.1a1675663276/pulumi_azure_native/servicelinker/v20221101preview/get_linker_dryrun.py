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
    'GetLinkerDryrunResult',
    'AwaitableGetLinkerDryrunResult',
    'get_linker_dryrun',
    'get_linker_dryrun_output',
]

@pulumi.output_type
class GetLinkerDryrunResult:
    """
    a dryrun job resource
    """
    def __init__(__self__, id=None, name=None, operation_previews=None, parameters=None, prerequisite_results=None, provisioning_state=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if operation_previews and not isinstance(operation_previews, list):
            raise TypeError("Expected argument 'operation_previews' to be a list")
        pulumi.set(__self__, "operation_previews", operation_previews)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if prerequisite_results and not isinstance(prerequisite_results, list):
            raise TypeError("Expected argument 'prerequisite_results' to be a list")
        pulumi.set(__self__, "prerequisite_results", prerequisite_results)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
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
    @pulumi.getter(name="operationPreviews")
    def operation_previews(self) -> Sequence['outputs.DryrunOperationPreviewResponse']:
        """
        the preview of the operations for creation
        """
        return pulumi.get(self, "operation_previews")

    @property
    @pulumi.getter
    def parameters(self) -> Optional['outputs.CreateOrUpdateDryrunParametersResponse']:
        """
        The parameters of the dryrun
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="prerequisiteResults")
    def prerequisite_results(self) -> Sequence[Any]:
        """
        the result of the dryrun
        """
        return pulumi.get(self, "prerequisite_results")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state. 
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetLinkerDryrunResult(GetLinkerDryrunResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkerDryrunResult(
            id=self.id,
            name=self.name,
            operation_previews=self.operation_previews,
            parameters=self.parameters,
            prerequisite_results=self.prerequisite_results,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_linker_dryrun(dryrun_name: Optional[str] = None,
                      resource_uri: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkerDryrunResult:
    """
    a dryrun job resource


    :param str dryrun_name: The name of dryrun.
    :param str resource_uri: The fully qualified Azure Resource manager identifier of the resource to be connected.
    """
    __args__ = dict()
    __args__['dryrunName'] = dryrun_name
    __args__['resourceUri'] = resource_uri
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:servicelinker/v20221101preview:getLinkerDryrun', __args__, opts=opts, typ=GetLinkerDryrunResult).value

    return AwaitableGetLinkerDryrunResult(
        id=__ret__.id,
        name=__ret__.name,
        operation_previews=__ret__.operation_previews,
        parameters=__ret__.parameters,
        prerequisite_results=__ret__.prerequisite_results,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_linker_dryrun)
def get_linker_dryrun_output(dryrun_name: Optional[pulumi.Input[str]] = None,
                             resource_uri: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinkerDryrunResult]:
    """
    a dryrun job resource


    :param str dryrun_name: The name of dryrun.
    :param str resource_uri: The fully qualified Azure Resource manager identifier of the resource to be connected.
    """
    ...
