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
from ._enums import *
from ._inputs import *

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 details: Optional[pulumi.Input[Union['DataBoxDiskJobDetailsArgs', 'DataBoxHeavyJobDetailsArgs', 'DataBoxJobDetailsArgs']]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name
        :param pulumi.Input['SkuArgs'] sku: The sku type.
        :param pulumi.Input[Union['DataBoxDiskJobDetailsArgs', 'DataBoxHeavyJobDetailsArgs', 'DataBoxJobDetailsArgs']] details: Details of a job run. This field will only be sent for expand details filter.
        :param pulumi.Input[str] job_name: The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
        :param pulumi.Input[str] location: The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if details is not None:
            pulumi.set(__self__, "details", details)
        if job_name is not None:
            pulumi.set(__self__, "job_name", job_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The Resource Group Name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The sku type.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input[Union['DataBoxDiskJobDetailsArgs', 'DataBoxHeavyJobDetailsArgs', 'DataBoxJobDetailsArgs']]]:
        """
        Details of a job run. This field will only be sent for expand details filter.
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: Optional[pulumi.Input[Union['DataBoxDiskJobDetailsArgs', 'DataBoxHeavyJobDetailsArgs', 'DataBoxJobDetailsArgs']]]):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter(name="jobName")
    def job_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
        """
        return pulumi.get(self, "job_name")

    @job_name.setter
    def job_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2018-01-01 will be removed in v2 of the provider.""", DeprecationWarning)


class Job(pulumi.CustomResource):
    warnings.warn("""Version 2018-01-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 details: Optional[pulumi.Input[Union[pulumi.InputType['DataBoxDiskJobDetailsArgs'], pulumi.InputType['DataBoxHeavyJobDetailsArgs'], pulumi.InputType['DataBoxJobDetailsArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Job Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['DataBoxDiskJobDetailsArgs'], pulumi.InputType['DataBoxHeavyJobDetailsArgs'], pulumi.InputType['DataBoxJobDetailsArgs']]] details: Details of a job run. This field will only be sent for expand details filter.
        :param pulumi.Input[str] job_name: The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
        :param pulumi.Input[str] location: The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku type.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Job Resource.

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 details: Optional[pulumi.Input[Union[pulumi.InputType['DataBoxDiskJobDetailsArgs'], pulumi.InputType['DataBoxHeavyJobDetailsArgs'], pulumi.InputType['DataBoxJobDetailsArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Job is deprecated: Version 2018-01-01 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = JobArgs.__new__(JobArgs)

            __props__.__dict__["details"] = details
            __props__.__dict__["job_name"] = job_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["cancellation_reason"] = None
            __props__.__dict__["error"] = None
            __props__.__dict__["is_cancellable"] = None
            __props__.__dict__["is_deletable"] = None
            __props__.__dict__["is_shipping_address_editable"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["start_time"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databox:Job"), pulumi.Alias(type_="azure-native:databox/v20190901:Job"), pulumi.Alias(type_="azure-native:databox/v20200401:Job"), pulumi.Alias(type_="azure-native:databox/v20201101:Job"), pulumi.Alias(type_="azure-native:databox/v20210301:Job"), pulumi.Alias(type_="azure-native:databox/v20210501:Job"), pulumi.Alias(type_="azure-native:databox/v20210801preview:Job"), pulumi.Alias(type_="azure-native:databox/v20211201:Job"), pulumi.Alias(type_="azure-native:databox/v20220201:Job"), pulumi.Alias(type_="azure-native:databox/v20220901:Job"), pulumi.Alias(type_="azure-native:databox/v20221001:Job")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Job, __self__).__init__(
            'azure-native:databox/v20180101:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobArgs.__new__(JobArgs)

        __props__.__dict__["cancellation_reason"] = None
        __props__.__dict__["details"] = None
        __props__.__dict__["error"] = None
        __props__.__dict__["is_cancellable"] = None
        __props__.__dict__["is_deletable"] = None
        __props__.__dict__["is_shipping_address_editable"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["start_time"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cancellationReason")
    def cancellation_reason(self) -> pulumi.Output[str]:
        """
        Reason for cancellation.
        """
        return pulumi.get(self, "cancellation_reason")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[Any]]:
        """
        Details of a job run. This field will only be sent for expand details filter.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def error(self) -> pulumi.Output['outputs.ErrorResponse']:
        """
        Top level error for the job.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter(name="isCancellable")
    def is_cancellable(self) -> pulumi.Output[bool]:
        """
        Describes whether the job is cancellable or not.
        """
        return pulumi.get(self, "is_cancellable")

    @property
    @pulumi.getter(name="isDeletable")
    def is_deletable(self) -> pulumi.Output[bool]:
        """
        Describes whether the job is deletable or not.
        """
        return pulumi.get(self, "is_deletable")

    @property
    @pulumi.getter(name="isShippingAddressEditable")
    def is_shipping_address_editable(self) -> pulumi.Output[bool]:
        """
        Describes whether the shipping address is editable or not.
        """
        return pulumi.get(self, "is_shipping_address_editable")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the object.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        The sku type.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[str]:
        """
        Time at which the job was started in UTC ISO 8601 format.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Name of the stage which is in progress.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the object.
        """
        return pulumi.get(self, "type")

