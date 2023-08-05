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

__all__ = ['WebAppSlotConfigurationNamesArgs', 'WebAppSlotConfigurationNames']

@pulumi.input_type
class WebAppSlotConfigurationNamesArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 app_setting_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 azure_storage_config_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 connection_string_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WebAppSlotConfigurationNames resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] app_setting_names: List of application settings names.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] azure_storage_config_names: List of external Azure storage account identifiers.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connection_string_names: List of connection string names.
        :param pulumi.Input[str] kind: Kind of resource.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if app_setting_names is not None:
            pulumi.set(__self__, "app_setting_names", app_setting_names)
        if azure_storage_config_names is not None:
            pulumi.set(__self__, "azure_storage_config_names", azure_storage_config_names)
        if connection_string_names is not None:
            pulumi.set(__self__, "connection_string_names", connection_string_names)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the app.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="appSettingNames")
    def app_setting_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of application settings names.
        """
        return pulumi.get(self, "app_setting_names")

    @app_setting_names.setter
    def app_setting_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "app_setting_names", value)

    @property
    @pulumi.getter(name="azureStorageConfigNames")
    def azure_storage_config_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of external Azure storage account identifiers.
        """
        return pulumi.get(self, "azure_storage_config_names")

    @azure_storage_config_names.setter
    def azure_storage_config_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "azure_storage_config_names", value)

    @property
    @pulumi.getter(name="connectionStringNames")
    def connection_string_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of connection string names.
        """
        return pulumi.get(self, "connection_string_names")

    @connection_string_names.setter
    def connection_string_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "connection_string_names", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)


class WebAppSlotConfigurationNames(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_setting_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 azure_storage_config_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 connection_string_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Slot Config names azure resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] app_setting_names: List of application settings names.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] azure_storage_config_names: List of external Azure storage account identifiers.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connection_string_names: List of connection string names.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebAppSlotConfigurationNamesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Slot Config names azure resource.

        :param str resource_name: The name of the resource.
        :param WebAppSlotConfigurationNamesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppSlotConfigurationNamesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_setting_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 azure_storage_config_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 connection_string_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebAppSlotConfigurationNamesArgs.__new__(WebAppSlotConfigurationNamesArgs)

            __props__.__dict__["app_setting_names"] = app_setting_names
            __props__.__dict__["azure_storage_config_names"] = azure_storage_config_names
            __props__.__dict__["connection_string_names"] = connection_string_names
            __props__.__dict__["kind"] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20150801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20160801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20180201:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20181101:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20190801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20200601:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20201001:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20201201:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20210101:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20210115:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20210201:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20210301:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-native:web/v20220301:WebAppSlotConfigurationNames")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSlotConfigurationNames, __self__).__init__(
            'azure-native:web/v20200901:WebAppSlotConfigurationNames',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppSlotConfigurationNames':
        """
        Get an existing WebAppSlotConfigurationNames resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebAppSlotConfigurationNamesArgs.__new__(WebAppSlotConfigurationNamesArgs)

        __props__.__dict__["app_setting_names"] = None
        __props__.__dict__["azure_storage_config_names"] = None
        __props__.__dict__["connection_string_names"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return WebAppSlotConfigurationNames(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appSettingNames")
    def app_setting_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of application settings names.
        """
        return pulumi.get(self, "app_setting_names")

    @property
    @pulumi.getter(name="azureStorageConfigNames")
    def azure_storage_config_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of external Azure storage account identifiers.
        """
        return pulumi.get(self, "azure_storage_config_names")

    @property
    @pulumi.getter(name="connectionStringNames")
    def connection_string_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of connection string names.
        """
        return pulumi.get(self, "connection_string_names")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

