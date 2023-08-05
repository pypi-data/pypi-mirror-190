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

__all__ = ['DataVersionArgs', 'DataVersion']

@pulumi.input_type
class DataVersionArgs:
    def __init__(__self__, *,
                 data_version_base_details: pulumi.Input[Union['MLTableDataArgs', 'UriFileDataVersionArgs', 'UriFolderDataVersionArgs']],
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataVersion resource.
        :param pulumi.Input[Union['MLTableDataArgs', 'UriFileDataVersionArgs', 'UriFolderDataVersionArgs']] data_version_base_details: [Required] Additional attributes of the entity.
        :param pulumi.Input[str] name: Container name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        :param pulumi.Input[str] version: Version identifier.
        """
        pulumi.set(__self__, "data_version_base_details", data_version_base_details)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="dataVersionBaseDetails")
    def data_version_base_details(self) -> pulumi.Input[Union['MLTableDataArgs', 'UriFileDataVersionArgs', 'UriFolderDataVersionArgs']]:
        """
        [Required] Additional attributes of the entity.
        """
        return pulumi.get(self, "data_version_base_details")

    @data_version_base_details.setter
    def data_version_base_details(self, value: pulumi.Input[Union['MLTableDataArgs', 'UriFileDataVersionArgs', 'UriFolderDataVersionArgs']]):
        pulumi.set(self, "data_version_base_details", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Container name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        Name of Azure Machine Learning workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version identifier.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class DataVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_version_base_details: Optional[pulumi.Input[Union[pulumi.InputType['MLTableDataArgs'], pulumi.InputType['UriFileDataVersionArgs'], pulumi.InputType['UriFolderDataVersionArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Azure Resource Manager resource envelope.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['MLTableDataArgs'], pulumi.InputType['UriFileDataVersionArgs'], pulumi.InputType['UriFolderDataVersionArgs']]] data_version_base_details: [Required] Additional attributes of the entity.
        :param pulumi.Input[str] name: Container name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] version: Version identifier.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Azure Resource Manager resource envelope.

        :param str resource_name: The name of the resource.
        :param DataVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_version_base_details: Optional[pulumi.Input[Union[pulumi.InputType['MLTableDataArgs'], pulumi.InputType['UriFileDataVersionArgs'], pulumi.InputType['UriFolderDataVersionArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataVersionArgs.__new__(DataVersionArgs)

            if data_version_base_details is None and not opts.urn:
                raise TypeError("Missing required property 'data_version_base_details'")
            __props__.__dict__["data_version_base_details"] = data_version_base_details
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["version"] = version
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:machinelearningservices:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20210301preview:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20220501:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20220601preview:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20221001:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20221001preview:DataVersion"), pulumi.Alias(type_="azure-native:machinelearningservices/v20221201preview:DataVersion")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DataVersion, __self__).__init__(
            'azure-native:machinelearningservices/v20220201preview:DataVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DataVersion':
        """
        Get an existing DataVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DataVersionArgs.__new__(DataVersionArgs)

        __props__.__dict__["data_version_base_details"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return DataVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataVersionBaseDetails")
    def data_version_base_details(self) -> pulumi.Output[Any]:
        """
        [Required] Additional attributes of the entity.
        """
        return pulumi.get(self, "data_version_base_details")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

