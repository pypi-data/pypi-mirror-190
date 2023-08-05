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
from ._inputs import *

__all__ = ['MonitoringConfigArgs', 'MonitoringConfig']

@pulumi.input_type
class MonitoringConfigArgs:
    def __init__(__self__, *,
                 device_name: pulumi.Input[str],
                 metric_configurations: pulumi.Input[Sequence[pulumi.Input['MetricConfigurationArgs']]],
                 resource_group_name: pulumi.Input[str],
                 role_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a MonitoringConfig resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Sequence[pulumi.Input['MetricConfigurationArgs']]] metric_configurations: The metrics configuration details
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] role_name: The role name.
        """
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "metric_configurations", metric_configurations)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter(name="metricConfigurations")
    def metric_configurations(self) -> pulumi.Input[Sequence[pulumi.Input['MetricConfigurationArgs']]]:
        """
        The metrics configuration details
        """
        return pulumi.get(self, "metric_configurations")

    @metric_configurations.setter
    def metric_configurations(self, value: pulumi.Input[Sequence[pulumi.Input['MetricConfigurationArgs']]]):
        pulumi.set(self, "metric_configurations", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Input[str]:
        """
        The role name.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_name", value)


warnings.warn("""Version 2020-09-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class MonitoringConfig(pulumi.CustomResource):
    warnings.warn("""Version 2020-09-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 metric_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetricConfigurationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The metric setting details for the role

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetricConfigurationArgs']]]] metric_configurations: The metrics configuration details
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] role_name: The role name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MonitoringConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The metric setting details for the role

        :param str resource_name: The name of the resource.
        :param MonitoringConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MonitoringConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 metric_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MetricConfigurationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""MonitoringConfig is deprecated: Version 2020-09-01-preview will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MonitoringConfigArgs.__new__(MonitoringConfigArgs)

            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            if metric_configurations is None and not opts.urn:
                raise TypeError("Missing required property 'metric_configurations'")
            __props__.__dict__["metric_configurations"] = metric_configurations
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if role_name is None and not opts.urn:
                raise TypeError("Missing required property 'role_name'")
            __props__.__dict__["role_name"] = role_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20210201preview:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20220401preview:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20221201preview:MonitoringConfig"), pulumi.Alias(type_="azure-native:databoxedge/v20230101preview:MonitoringConfig")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MonitoringConfig, __self__).__init__(
            'azure-native:databoxedge/v20200901preview:MonitoringConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MonitoringConfig':
        """
        Get an existing MonitoringConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MonitoringConfigArgs.__new__(MonitoringConfigArgs)

        __props__.__dict__["metric_configurations"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return MonitoringConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="metricConfigurations")
    def metric_configurations(self) -> pulumi.Output[Sequence['outputs.MetricConfigurationResponse']]:
        """
        The metrics configuration details
        """
        return pulumi.get(self, "metric_configurations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

