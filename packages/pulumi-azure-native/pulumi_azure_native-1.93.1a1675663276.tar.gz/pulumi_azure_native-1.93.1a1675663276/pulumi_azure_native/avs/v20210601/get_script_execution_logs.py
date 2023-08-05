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
    'GetScriptExecutionLogsResult',
    'AwaitableGetScriptExecutionLogsResult',
    'get_script_execution_logs',
    'get_script_execution_logs_output',
]

@pulumi.output_type
class GetScriptExecutionLogsResult:
    """
    An instance of a script executed by a user - custom or AVS
    """
    def __init__(__self__, errors=None, failure_reason=None, finished_at=None, hidden_parameters=None, id=None, information=None, name=None, named_outputs=None, output=None, parameters=None, provisioning_state=None, retention=None, script_cmdlet_id=None, started_at=None, submitted_at=None, timeout=None, type=None, warnings=None):
        if errors and not isinstance(errors, list):
            raise TypeError("Expected argument 'errors' to be a list")
        pulumi.set(__self__, "errors", errors)
        if failure_reason and not isinstance(failure_reason, str):
            raise TypeError("Expected argument 'failure_reason' to be a str")
        pulumi.set(__self__, "failure_reason", failure_reason)
        if finished_at and not isinstance(finished_at, str):
            raise TypeError("Expected argument 'finished_at' to be a str")
        pulumi.set(__self__, "finished_at", finished_at)
        if hidden_parameters and not isinstance(hidden_parameters, list):
            raise TypeError("Expected argument 'hidden_parameters' to be a list")
        pulumi.set(__self__, "hidden_parameters", hidden_parameters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if information and not isinstance(information, list):
            raise TypeError("Expected argument 'information' to be a list")
        pulumi.set(__self__, "information", information)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if named_outputs and not isinstance(named_outputs, dict):
            raise TypeError("Expected argument 'named_outputs' to be a dict")
        pulumi.set(__self__, "named_outputs", named_outputs)
        if output and not isinstance(output, list):
            raise TypeError("Expected argument 'output' to be a list")
        pulumi.set(__self__, "output", output)
        if parameters and not isinstance(parameters, list):
            raise TypeError("Expected argument 'parameters' to be a list")
        pulumi.set(__self__, "parameters", parameters)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if retention and not isinstance(retention, str):
            raise TypeError("Expected argument 'retention' to be a str")
        pulumi.set(__self__, "retention", retention)
        if script_cmdlet_id and not isinstance(script_cmdlet_id, str):
            raise TypeError("Expected argument 'script_cmdlet_id' to be a str")
        pulumi.set(__self__, "script_cmdlet_id", script_cmdlet_id)
        if started_at and not isinstance(started_at, str):
            raise TypeError("Expected argument 'started_at' to be a str")
        pulumi.set(__self__, "started_at", started_at)
        if submitted_at and not isinstance(submitted_at, str):
            raise TypeError("Expected argument 'submitted_at' to be a str")
        pulumi.set(__self__, "submitted_at", submitted_at)
        if timeout and not isinstance(timeout, str):
            raise TypeError("Expected argument 'timeout' to be a str")
        pulumi.set(__self__, "timeout", timeout)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if warnings and not isinstance(warnings, list):
            raise TypeError("Expected argument 'warnings' to be a list")
        pulumi.set(__self__, "warnings", warnings)

    @property
    @pulumi.getter
    def errors(self) -> Sequence[str]:
        """
        Standard error output stream from the powershell execution
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> Optional[str]:
        """
        Error message if the script was able to run, but if the script itself had errors or powershell threw an exception
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter(name="finishedAt")
    def finished_at(self) -> str:
        """
        Time the script execution was finished
        """
        return pulumi.get(self, "finished_at")

    @property
    @pulumi.getter(name="hiddenParameters")
    def hidden_parameters(self) -> Optional[Sequence[Any]]:
        """
        Parameters that will be hidden/not visible to ARM, such as passwords and credentials
        """
        return pulumi.get(self, "hidden_parameters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def information(self) -> Sequence[str]:
        """
        Standard information out stream from the powershell execution
        """
        return pulumi.get(self, "information")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namedOutputs")
    def named_outputs(self) -> Optional[Mapping[str, Any]]:
        """
        User-defined dictionary.
        """
        return pulumi.get(self, "named_outputs")

    @property
    @pulumi.getter
    def output(self) -> Optional[Sequence[str]]:
        """
        Standard output stream from the powershell execution
        """
        return pulumi.get(self, "output")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Sequence[Any]]:
        """
        Parameters the script will accept
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of the script execution resource
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def retention(self) -> Optional[str]:
        """
        Time to live for the resource. If not provided, will be available for 60 days
        """
        return pulumi.get(self, "retention")

    @property
    @pulumi.getter(name="scriptCmdletId")
    def script_cmdlet_id(self) -> Optional[str]:
        """
        A reference to the script cmdlet resource if user is running a AVS script
        """
        return pulumi.get(self, "script_cmdlet_id")

    @property
    @pulumi.getter(name="startedAt")
    def started_at(self) -> str:
        """
        Time the script execution was started
        """
        return pulumi.get(self, "started_at")

    @property
    @pulumi.getter(name="submittedAt")
    def submitted_at(self) -> str:
        """
        Time the script execution was submitted
        """
        return pulumi.get(self, "submitted_at")

    @property
    @pulumi.getter
    def timeout(self) -> str:
        """
        Time limit for execution
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def warnings(self) -> Sequence[str]:
        """
        Standard warning out stream from the powershell execution
        """
        return pulumi.get(self, "warnings")


class AwaitableGetScriptExecutionLogsResult(GetScriptExecutionLogsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScriptExecutionLogsResult(
            errors=self.errors,
            failure_reason=self.failure_reason,
            finished_at=self.finished_at,
            hidden_parameters=self.hidden_parameters,
            id=self.id,
            information=self.information,
            name=self.name,
            named_outputs=self.named_outputs,
            output=self.output,
            parameters=self.parameters,
            provisioning_state=self.provisioning_state,
            retention=self.retention,
            script_cmdlet_id=self.script_cmdlet_id,
            started_at=self.started_at,
            submitted_at=self.submitted_at,
            timeout=self.timeout,
            type=self.type,
            warnings=self.warnings)


def get_script_execution_logs(private_cloud_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              script_execution_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScriptExecutionLogsResult:
    """
    An instance of a script executed by a user - custom or AVS


    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str script_execution_name: Name of the user-invoked script execution resource
    """
    __args__ = dict()
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['scriptExecutionName'] = script_execution_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:avs/v20210601:getScriptExecutionLogs', __args__, opts=opts, typ=GetScriptExecutionLogsResult).value

    return AwaitableGetScriptExecutionLogsResult(
        errors=__ret__.errors,
        failure_reason=__ret__.failure_reason,
        finished_at=__ret__.finished_at,
        hidden_parameters=__ret__.hidden_parameters,
        id=__ret__.id,
        information=__ret__.information,
        name=__ret__.name,
        named_outputs=__ret__.named_outputs,
        output=__ret__.output,
        parameters=__ret__.parameters,
        provisioning_state=__ret__.provisioning_state,
        retention=__ret__.retention,
        script_cmdlet_id=__ret__.script_cmdlet_id,
        started_at=__ret__.started_at,
        submitted_at=__ret__.submitted_at,
        timeout=__ret__.timeout,
        type=__ret__.type,
        warnings=__ret__.warnings)


@_utilities.lift_output_func(get_script_execution_logs)
def get_script_execution_logs_output(private_cloud_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     script_execution_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScriptExecutionLogsResult]:
    """
    An instance of a script executed by a user - custom or AVS


    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str script_execution_name: Name of the user-invoked script execution resource
    """
    ...
