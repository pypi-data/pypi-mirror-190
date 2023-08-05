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

__all__ = ['ConfigurationAssignmentParentArgs', 'ConfigurationAssignmentParent']

@pulumi.input_type
class ConfigurationAssignmentParentArgs:
    def __init__(__self__, *,
                 provider_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 resource_parent_name: pulumi.Input[str],
                 resource_parent_type: pulumi.Input[str],
                 resource_type: pulumi.Input[str],
                 configuration_assignment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ConfigurationAssignmentParent resource.
        :param pulumi.Input[str] provider_name: Resource provider name
        :param pulumi.Input[str] resource_group_name: Resource group name
        :param pulumi.Input[str] resource_name: Resource identifier
        :param pulumi.Input[str] resource_parent_name: Resource parent identifier
        :param pulumi.Input[str] resource_parent_type: Resource parent type
        :param pulumi.Input[str] resource_type: Resource type
        :param pulumi.Input[str] configuration_assignment_name: Configuration assignment name
        :param pulumi.Input[str] location: Location of the resource
        :param pulumi.Input[str] maintenance_configuration_id: The maintenance configuration Id
        :param pulumi.Input[str] resource_id: The unique resourceId
        """
        pulumi.set(__self__, "provider_name", provider_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        pulumi.set(__self__, "resource_parent_name", resource_parent_name)
        pulumi.set(__self__, "resource_parent_type", resource_parent_type)
        pulumi.set(__self__, "resource_type", resource_type)
        if configuration_assignment_name is not None:
            pulumi.set(__self__, "configuration_assignment_name", configuration_assignment_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_configuration_id is not None:
            pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> pulumi.Input[str]:
        """
        Resource provider name
        """
        return pulumi.get(self, "provider_name")

    @provider_name.setter
    def provider_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "provider_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Resource group name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        Resource identifier
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="resourceParentName")
    def resource_parent_name(self) -> pulumi.Input[str]:
        """
        Resource parent identifier
        """
        return pulumi.get(self, "resource_parent_name")

    @resource_parent_name.setter
    def resource_parent_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_parent_name", value)

    @property
    @pulumi.getter(name="resourceParentType")
    def resource_parent_type(self) -> pulumi.Input[str]:
        """
        Resource parent type
        """
        return pulumi.get(self, "resource_parent_type")

    @resource_parent_type.setter
    def resource_parent_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_parent_type", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        Resource type
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter(name="configurationAssignmentName")
    def configuration_assignment_name(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration assignment name
        """
        return pulumi.get(self, "configuration_assignment_name")

    @configuration_assignment_name.setter
    def configuration_assignment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_assignment_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location of the resource
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        The maintenance configuration Id
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @maintenance_configuration_id.setter
    def maintenance_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_configuration_id", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique resourceId
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


class ConfigurationAssignmentParent(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_assignment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 resource_parent_name: Optional[pulumi.Input[str]] = None,
                 resource_parent_type: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Configuration Assignment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_assignment_name: Configuration assignment name
        :param pulumi.Input[str] location: Location of the resource
        :param pulumi.Input[str] maintenance_configuration_id: The maintenance configuration Id
        :param pulumi.Input[str] provider_name: Resource provider name
        :param pulumi.Input[str] resource_group_name: Resource group name
        :param pulumi.Input[str] resource_id: The unique resourceId
        :param pulumi.Input[str] resource_name_: Resource identifier
        :param pulumi.Input[str] resource_parent_name: Resource parent identifier
        :param pulumi.Input[str] resource_parent_type: Resource parent type
        :param pulumi.Input[str] resource_type: Resource type
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationAssignmentParentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Configuration Assignment

        :param str resource_name: The name of the resource.
        :param ConfigurationAssignmentParentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationAssignmentParentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_assignment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 resource_parent_name: Optional[pulumi.Input[str]] = None,
                 resource_parent_type: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationAssignmentParentArgs.__new__(ConfigurationAssignmentParentArgs)

            __props__.__dict__["configuration_assignment_name"] = configuration_assignment_name
            __props__.__dict__["location"] = location
            __props__.__dict__["maintenance_configuration_id"] = maintenance_configuration_id
            if provider_name is None and not opts.urn:
                raise TypeError("Missing required property 'provider_name'")
            __props__.__dict__["provider_name"] = provider_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_id"] = resource_id
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            if resource_parent_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_parent_name'")
            __props__.__dict__["resource_parent_name"] = resource_parent_name
            if resource_parent_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_parent_type'")
            __props__.__dict__["resource_parent_type"] = resource_parent_type
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:maintenance:ConfigurationAssignmentParent"), pulumi.Alias(type_="azure-native:maintenance/v20210401preview:ConfigurationAssignmentParent"), pulumi.Alias(type_="azure-native:maintenance/v20210901preview:ConfigurationAssignmentParent"), pulumi.Alias(type_="azure-native:maintenance/v20221101preview:ConfigurationAssignmentParent")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConfigurationAssignmentParent, __self__).__init__(
            'azure-native:maintenance/v20220701preview:ConfigurationAssignmentParent',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConfigurationAssignmentParent':
        """
        Get an existing ConfigurationAssignmentParent resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConfigurationAssignmentParentArgs.__new__(ConfigurationAssignmentParentArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["maintenance_configuration_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["resource_id"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return ConfigurationAssignmentParent(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Location of the resource
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[Optional[str]]:
        """
        The maintenance configuration Id
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The unique resourceId
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

