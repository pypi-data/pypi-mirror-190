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
from ._enums import *
from ._inputs import *

__all__ = ['TaskArgs', 'Task']

@pulumi.input_type
class TaskArgs:
    def __init__(__self__, *,
                 registry_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 agent_configuration: Optional[pulumi.Input['AgentPropertiesArgs']] = None,
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['CredentialsArgs']] = None,
                 identity: Optional[pulumi.Input['IdentityPropertiesArgs']] = None,
                 is_system_task: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_template: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input['PlatformPropertiesArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'TaskStatus']]] = None,
                 step: Optional[pulumi.Input[Union['DockerBuildStepArgs', 'EncodedTaskStepArgs', 'FileTaskStepArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 task_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input['TriggerPropertiesArgs']] = None):
        """
        The set of arguments for constructing a Task resource.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input['AgentPropertiesArgs'] agent_configuration: The machine configuration of the run agent.
        :param pulumi.Input[str] agent_pool_name: The dedicated agent pool for the task.
        :param pulumi.Input['CredentialsArgs'] credentials: The properties that describes a set of credentials that will be used when this run is invoked.
        :param pulumi.Input['IdentityPropertiesArgs'] identity: Identity for the resource.
        :param pulumi.Input[bool] is_system_task: The value of this property indicates whether the task resource is system task or not.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[str] log_template: The template that describes the repository and tag information for run log artifact.
        :param pulumi.Input['PlatformPropertiesArgs'] platform: The platform properties against which the run has to happen.
        :param pulumi.Input[Union[str, 'TaskStatus']] status: The current status of task.
        :param pulumi.Input[Union['DockerBuildStepArgs', 'EncodedTaskStepArgs', 'FileTaskStepArgs']] step: The properties of a task step.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] task_name: The name of the container registry task.
        :param pulumi.Input[int] timeout: Run timeout in seconds.
        :param pulumi.Input['TriggerPropertiesArgs'] trigger: The properties that describe all triggers for the task.
        """
        pulumi.set(__self__, "registry_name", registry_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if agent_configuration is not None:
            pulumi.set(__self__, "agent_configuration", agent_configuration)
        if agent_pool_name is not None:
            pulumi.set(__self__, "agent_pool_name", agent_pool_name)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if is_system_task is None:
            is_system_task = False
        if is_system_task is not None:
            pulumi.set(__self__, "is_system_task", is_system_task)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if log_template is not None:
            pulumi.set(__self__, "log_template", log_template)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if step is not None:
            pulumi.set(__self__, "step", step)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if task_name is not None:
            pulumi.set(__self__, "task_name", task_name)
        if timeout is None:
            timeout = 3600
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if trigger is not None:
            pulumi.set(__self__, "trigger", trigger)

    @property
    @pulumi.getter(name="registryName")
    def registry_name(self) -> pulumi.Input[str]:
        """
        The name of the container registry.
        """
        return pulumi.get(self, "registry_name")

    @registry_name.setter
    def registry_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "registry_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group to which the container registry belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="agentConfiguration")
    def agent_configuration(self) -> Optional[pulumi.Input['AgentPropertiesArgs']]:
        """
        The machine configuration of the run agent.
        """
        return pulumi.get(self, "agent_configuration")

    @agent_configuration.setter
    def agent_configuration(self, value: Optional[pulumi.Input['AgentPropertiesArgs']]):
        pulumi.set(self, "agent_configuration", value)

    @property
    @pulumi.getter(name="agentPoolName")
    def agent_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The dedicated agent pool for the task.
        """
        return pulumi.get(self, "agent_pool_name")

    @agent_pool_name.setter
    def agent_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_pool_name", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['CredentialsArgs']]:
        """
        The properties that describes a set of credentials that will be used when this run is invoked.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['CredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityPropertiesArgs']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityPropertiesArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="isSystemTask")
    def is_system_task(self) -> Optional[pulumi.Input[bool]]:
        """
        The value of this property indicates whether the task resource is system task or not.
        """
        return pulumi.get(self, "is_system_task")

    @is_system_task.setter
    def is_system_task(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_system_task", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="logTemplate")
    def log_template(self) -> Optional[pulumi.Input[str]]:
        """
        The template that describes the repository and tag information for run log artifact.
        """
        return pulumi.get(self, "log_template")

    @log_template.setter
    def log_template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_template", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input['PlatformPropertiesArgs']]:
        """
        The platform properties against which the run has to happen.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input['PlatformPropertiesArgs']]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'TaskStatus']]]:
        """
        The current status of task.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'TaskStatus']]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def step(self) -> Optional[pulumi.Input[Union['DockerBuildStepArgs', 'EncodedTaskStepArgs', 'FileTaskStepArgs']]]:
        """
        The properties of a task step.
        """
        return pulumi.get(self, "step")

    @step.setter
    def step(self, value: Optional[pulumi.Input[Union['DockerBuildStepArgs', 'EncodedTaskStepArgs', 'FileTaskStepArgs']]]):
        pulumi.set(self, "step", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="taskName")
    def task_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container registry task.
        """
        return pulumi.get(self, "task_name")

    @task_name.setter
    def task_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "task_name", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        Run timeout in seconds.
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter
    def trigger(self) -> Optional[pulumi.Input['TriggerPropertiesArgs']]:
        """
        The properties that describe all triggers for the task.
        """
        return pulumi.get(self, "trigger")

    @trigger.setter
    def trigger(self, value: Optional[pulumi.Input['TriggerPropertiesArgs']]):
        pulumi.set(self, "trigger", value)


class Task(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_configuration: Optional[pulumi.Input[pulumi.InputType['AgentPropertiesArgs']]] = None,
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['CredentialsArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]] = None,
                 is_system_task: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_template: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[pulumi.InputType['PlatformPropertiesArgs']]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'TaskStatus']]] = None,
                 step: Optional[pulumi.Input[Union[pulumi.InputType['DockerBuildStepArgs'], pulumi.InputType['EncodedTaskStepArgs'], pulumi.InputType['FileTaskStepArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 task_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input[pulumi.InputType['TriggerPropertiesArgs']]] = None,
                 __props__=None):
        """
        The task that has the ARM resource and task properties.
        The task will have all information to schedule a run against it.
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AgentPropertiesArgs']] agent_configuration: The machine configuration of the run agent.
        :param pulumi.Input[str] agent_pool_name: The dedicated agent pool for the task.
        :param pulumi.Input[pulumi.InputType['CredentialsArgs']] credentials: The properties that describes a set of credentials that will be used when this run is invoked.
        :param pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']] identity: Identity for the resource.
        :param pulumi.Input[bool] is_system_task: The value of this property indicates whether the task resource is system task or not.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[str] log_template: The template that describes the repository and tag information for run log artifact.
        :param pulumi.Input[pulumi.InputType['PlatformPropertiesArgs']] platform: The platform properties against which the run has to happen.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[Union[str, 'TaskStatus']] status: The current status of task.
        :param pulumi.Input[Union[pulumi.InputType['DockerBuildStepArgs'], pulumi.InputType['EncodedTaskStepArgs'], pulumi.InputType['FileTaskStepArgs']]] step: The properties of a task step.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] task_name: The name of the container registry task.
        :param pulumi.Input[int] timeout: Run timeout in seconds.
        :param pulumi.Input[pulumi.InputType['TriggerPropertiesArgs']] trigger: The properties that describe all triggers for the task.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TaskArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The task that has the ARM resource and task properties.
        The task will have all information to schedule a run against it.
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param TaskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TaskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_configuration: Optional[pulumi.Input[pulumi.InputType['AgentPropertiesArgs']]] = None,
                 agent_pool_name: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['CredentialsArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]] = None,
                 is_system_task: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_template: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[pulumi.InputType['PlatformPropertiesArgs']]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'TaskStatus']]] = None,
                 step: Optional[pulumi.Input[Union[pulumi.InputType['DockerBuildStepArgs'], pulumi.InputType['EncodedTaskStepArgs'], pulumi.InputType['FileTaskStepArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 task_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 trigger: Optional[pulumi.Input[pulumi.InputType['TriggerPropertiesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TaskArgs.__new__(TaskArgs)

            __props__.__dict__["agent_configuration"] = agent_configuration
            __props__.__dict__["agent_pool_name"] = agent_pool_name
            __props__.__dict__["credentials"] = credentials
            __props__.__dict__["identity"] = identity
            if is_system_task is None:
                is_system_task = False
            __props__.__dict__["is_system_task"] = is_system_task
            __props__.__dict__["location"] = location
            __props__.__dict__["log_template"] = log_template
            __props__.__dict__["platform"] = platform
            if registry_name is None and not opts.urn:
                raise TypeError("Missing required property 'registry_name'")
            __props__.__dict__["registry_name"] = registry_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["status"] = status
            __props__.__dict__["step"] = step
            __props__.__dict__["tags"] = tags
            __props__.__dict__["task_name"] = task_name
            if timeout is None:
                timeout = 3600
            __props__.__dict__["timeout"] = timeout
            __props__.__dict__["trigger"] = trigger
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerregistry/v20180201preview:Task"), pulumi.Alias(type_="azure-native:containerregistry/v20180901:Task"), pulumi.Alias(type_="azure-native:containerregistry/v20190401:Task"), pulumi.Alias(type_="azure-native:containerregistry/v20190601preview:Task")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Task, __self__).__init__(
            'azure-native:containerregistry:Task',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Task':
        """
        Get an existing Task resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TaskArgs.__new__(TaskArgs)

        __props__.__dict__["agent_configuration"] = None
        __props__.__dict__["agent_pool_name"] = None
        __props__.__dict__["creation_date"] = None
        __props__.__dict__["credentials"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["is_system_task"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["log_template"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["platform"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["step"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["timeout"] = None
        __props__.__dict__["trigger"] = None
        __props__.__dict__["type"] = None
        return Task(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentConfiguration")
    def agent_configuration(self) -> pulumi.Output[Optional['outputs.AgentPropertiesResponse']]:
        """
        The machine configuration of the run agent.
        """
        return pulumi.get(self, "agent_configuration")

    @property
    @pulumi.getter(name="agentPoolName")
    def agent_pool_name(self) -> pulumi.Output[Optional[str]]:
        """
        The dedicated agent pool for the task.
        """
        return pulumi.get(self, "agent_pool_name")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of task.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.CredentialsResponse']]:
        """
        The properties that describes a set of credentials that will be used when this run is invoked.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityPropertiesResponse']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="isSystemTask")
    def is_system_task(self) -> pulumi.Output[Optional[bool]]:
        """
        The value of this property indicates whether the task resource is system task or not.
        """
        return pulumi.get(self, "is_system_task")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logTemplate")
    def log_template(self) -> pulumi.Output[Optional[str]]:
        """
        The template that describes the repository and tag information for run log artifact.
        """
        return pulumi.get(self, "log_template")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[Optional['outputs.PlatformPropertiesResponse']]:
        """
        The platform properties against which the run has to happen.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the task.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        The current status of task.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def step(self) -> pulumi.Output[Optional[Any]]:
        """
        The properties of a task step.
        """
        return pulumi.get(self, "step")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Output[Optional[int]]:
        """
        Run timeout in seconds.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def trigger(self) -> pulumi.Output[Optional['outputs.TriggerPropertiesResponse']]:
        """
        The properties that describe all triggers for the task.
        """
        return pulumi.get(self, "trigger")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

