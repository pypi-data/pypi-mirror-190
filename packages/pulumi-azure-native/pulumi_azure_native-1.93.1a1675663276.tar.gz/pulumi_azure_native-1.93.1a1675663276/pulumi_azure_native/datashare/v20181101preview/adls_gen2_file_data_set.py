# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ADLSGen2FileDataSetArgs', 'ADLSGen2FileDataSet']

@pulumi.input_type
class ADLSGen2FileDataSetArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 file_path: pulumi.Input[str],
                 file_system: pulumi.Input[str],
                 kind: pulumi.Input[str],
                 resource_group: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 share_name: pulumi.Input[str],
                 storage_account_name: pulumi.Input[str],
                 subscription_id: pulumi.Input[str],
                 data_set_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ADLSGen2FileDataSet resource.
        :param pulumi.Input[str] account_name: The name of the share account.
        :param pulumi.Input[str] file_path: File path within the file system.
        :param pulumi.Input[str] file_system: File system to which the file belongs.
        :param pulumi.Input[str] kind: Kind of data set.
               Expected value is 'AdlsGen2File'.
        :param pulumi.Input[str] resource_group: Resource group of storage account
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] share_name: The name of the share to add the data set to.
        :param pulumi.Input[str] storage_account_name: Storage account name of the source data set
        :param pulumi.Input[str] subscription_id: Subscription id of storage account
        :param pulumi.Input[str] data_set_name: The name of the dataSet.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "file_path", file_path)
        pulumi.set(__self__, "file_system", file_system)
        pulumi.set(__self__, "kind", 'AdlsGen2File')
        pulumi.set(__self__, "resource_group", resource_group)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "share_name", share_name)
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        pulumi.set(__self__, "subscription_id", subscription_id)
        if data_set_name is not None:
            pulumi.set(__self__, "data_set_name", data_set_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the share account.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> pulumi.Input[str]:
        """
        File path within the file system.
        """
        return pulumi.get(self, "file_path")

    @file_path.setter
    def file_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "file_path", value)

    @property
    @pulumi.getter(name="fileSystem")
    def file_system(self) -> pulumi.Input[str]:
        """
        File system to which the file belongs.
        """
        return pulumi.get(self, "file_system")

    @file_system.setter
    def file_system(self, value: pulumi.Input[str]):
        pulumi.set(self, "file_system", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Kind of data set.
        Expected value is 'AdlsGen2File'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Input[str]:
        """
        Resource group of storage account
        """
        return pulumi.get(self, "resource_group")

    @resource_group.setter
    def resource_group(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group", value)

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
    @pulumi.getter(name="shareName")
    def share_name(self) -> pulumi.Input[str]:
        """
        The name of the share to add the data set to.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> pulumi.Input[str]:
        """
        Storage account name of the source data set
        """
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_name", value)

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Input[str]:
        """
        Subscription id of storage account
        """
        return pulumi.get(self, "subscription_id")

    @subscription_id.setter
    def subscription_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subscription_id", value)

    @property
    @pulumi.getter(name="dataSetName")
    def data_set_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the dataSet.
        """
        return pulumi.get(self, "data_set_name")

    @data_set_name.setter
    def data_set_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_set_name", value)


class ADLSGen2FileDataSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 data_set_name: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 file_system: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_account_name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An ADLS Gen 2 file data set.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the share account.
        :param pulumi.Input[str] data_set_name: The name of the dataSet.
        :param pulumi.Input[str] file_path: File path within the file system.
        :param pulumi.Input[str] file_system: File system to which the file belongs.
        :param pulumi.Input[str] kind: Kind of data set.
               Expected value is 'AdlsGen2File'.
        :param pulumi.Input[str] resource_group: Resource group of storage account
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] share_name: The name of the share to add the data set to.
        :param pulumi.Input[str] storage_account_name: Storage account name of the source data set
        :param pulumi.Input[str] subscription_id: Subscription id of storage account
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ADLSGen2FileDataSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An ADLS Gen 2 file data set.

        :param str resource_name: The name of the resource.
        :param ADLSGen2FileDataSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ADLSGen2FileDataSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 data_set_name: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 file_system: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_account_name: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ADLSGen2FileDataSetArgs.__new__(ADLSGen2FileDataSetArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["data_set_name"] = data_set_name
            if file_path is None and not opts.urn:
                raise TypeError("Missing required property 'file_path'")
            __props__.__dict__["file_path"] = file_path
            if file_system is None and not opts.urn:
                raise TypeError("Missing required property 'file_system'")
            __props__.__dict__["file_system"] = file_system
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'AdlsGen2File'
            if resource_group is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group'")
            __props__.__dict__["resource_group"] = resource_group
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if share_name is None and not opts.urn:
                raise TypeError("Missing required property 'share_name'")
            __props__.__dict__["share_name"] = share_name
            if storage_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_account_name'")
            __props__.__dict__["storage_account_name"] = storage_account_name
            if subscription_id is None and not opts.urn:
                raise TypeError("Missing required property 'subscription_id'")
            __props__.__dict__["subscription_id"] = subscription_id
            __props__.__dict__["data_set_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:datashare:ADLSGen2FileDataSet"), pulumi.Alias(type_="azure-native:datashare/v20191101:ADLSGen2FileDataSet"), pulumi.Alias(type_="azure-native:datashare/v20200901:ADLSGen2FileDataSet"), pulumi.Alias(type_="azure-native:datashare/v20201001preview:ADLSGen2FileDataSet"), pulumi.Alias(type_="azure-native:datashare/v20210801:ADLSGen2FileDataSet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ADLSGen2FileDataSet, __self__).__init__(
            'azure-native:datashare/v20181101preview:ADLSGen2FileDataSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ADLSGen2FileDataSet':
        """
        Get an existing ADLSGen2FileDataSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ADLSGen2FileDataSetArgs.__new__(ADLSGen2FileDataSetArgs)

        __props__.__dict__["data_set_id"] = None
        __props__.__dict__["file_path"] = None
        __props__.__dict__["file_system"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["resource_group"] = None
        __props__.__dict__["storage_account_name"] = None
        __props__.__dict__["subscription_id"] = None
        __props__.__dict__["type"] = None
        return ADLSGen2FileDataSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataSetId")
    def data_set_id(self) -> pulumi.Output[str]:
        """
        Unique id for identifying a data set resource
        """
        return pulumi.get(self, "data_set_id")

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> pulumi.Output[str]:
        """
        File path within the file system.
        """
        return pulumi.get(self, "file_path")

    @property
    @pulumi.getter(name="fileSystem")
    def file_system(self) -> pulumi.Output[str]:
        """
        File system to which the file belongs.
        """
        return pulumi.get(self, "file_system")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of data set.
        Expected value is 'AdlsGen2File'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the azure resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Output[str]:
        """
        Resource group of storage account
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> pulumi.Output[str]:
        """
        Storage account name of the source data set
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Output[str]:
        """
        Subscription id of storage account
        """
        return pulumi.get(self, "subscription_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the azure resource
        """
        return pulumi.get(self, "type")

