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

__all__ = ['VirtualharddiskRetrieveArgs', 'VirtualharddiskRetrieve']

@pulumi.input_type
class VirtualharddiskRetrieveArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 block_size_bytes: Optional[pulumi.Input[int]] = None,
                 disk_size_bytes: Optional[pulumi.Input[float]] = None,
                 dynamic: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input['ExtendedLocationArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 physical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtualharddisks_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VirtualharddiskRetrieve resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[float] disk_size_bytes: diskSizeBytes - size of the disk in GB
        :param pulumi.Input[bool] dynamic: Boolean for enabling dynamic sizing on the virtual hard disk
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: The extendedLocation of the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_name: name of the object to be used in moc
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if block_size_bytes is not None:
            pulumi.set(__self__, "block_size_bytes", block_size_bytes)
        if disk_size_bytes is not None:
            pulumi.set(__self__, "disk_size_bytes", disk_size_bytes)
        if dynamic is not None:
            pulumi.set(__self__, "dynamic", dynamic)
        if extended_location is not None:
            pulumi.set(__self__, "extended_location", extended_location)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if logical_sector_bytes is not None:
            pulumi.set(__self__, "logical_sector_bytes", logical_sector_bytes)
        if physical_sector_bytes is not None:
            pulumi.set(__self__, "physical_sector_bytes", physical_sector_bytes)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtualharddisks_name is not None:
            pulumi.set(__self__, "virtualharddisks_name", virtualharddisks_name)

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
    @pulumi.getter(name="blockSizeBytes")
    def block_size_bytes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "block_size_bytes")

    @block_size_bytes.setter
    def block_size_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "block_size_bytes", value)

    @property
    @pulumi.getter(name="diskSizeBytes")
    def disk_size_bytes(self) -> Optional[pulumi.Input[float]]:
        """
        diskSizeBytes - size of the disk in GB
        """
        return pulumi.get(self, "disk_size_bytes")

    @disk_size_bytes.setter
    def disk_size_bytes(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "disk_size_bytes", value)

    @property
    @pulumi.getter
    def dynamic(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean for enabling dynamic sizing on the virtual hard disk
        """
        return pulumi.get(self, "dynamic")

    @dynamic.setter
    def dynamic(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dynamic", value)

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> Optional[pulumi.Input['ExtendedLocationArgs']]:
        """
        The extendedLocation of the resource.
        """
        return pulumi.get(self, "extended_location")

    @extended_location.setter
    def extended_location(self, value: Optional[pulumi.Input['ExtendedLocationArgs']]):
        pulumi.set(self, "extended_location", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="logicalSectorBytes")
    def logical_sector_bytes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "logical_sector_bytes")

    @logical_sector_bytes.setter
    def logical_sector_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "logical_sector_bytes", value)

    @property
    @pulumi.getter(name="physicalSectorBytes")
    def physical_sector_bytes(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "physical_sector_bytes")

    @physical_sector_bytes.setter
    def physical_sector_bytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "physical_sector_bytes", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the object to be used in moc
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="virtualharddisksName")
    def virtualharddisks_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "virtualharddisks_name")

    @virtualharddisks_name.setter
    def virtualharddisks_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtualharddisks_name", value)


class VirtualharddiskRetrieve(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_size_bytes: Optional[pulumi.Input[int]] = None,
                 disk_size_bytes: Optional[pulumi.Input[float]] = None,
                 dynamic: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 physical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtualharddisks_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The virtualharddisks resource definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] disk_size_bytes: diskSizeBytes - size of the disk in GB
        :param pulumi.Input[bool] dynamic: Boolean for enabling dynamic sizing on the virtual hard disk
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: The extendedLocation of the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: name of the object to be used in moc
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualharddiskRetrieveArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The virtualharddisks resource definition.

        :param str resource_name: The name of the resource.
        :param VirtualharddiskRetrieveArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualharddiskRetrieveArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_size_bytes: Optional[pulumi.Input[int]] = None,
                 disk_size_bytes: Optional[pulumi.Input[float]] = None,
                 dynamic: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 physical_sector_bytes: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtualharddisks_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualharddiskRetrieveArgs.__new__(VirtualharddiskRetrieveArgs)

            __props__.__dict__["block_size_bytes"] = block_size_bytes
            __props__.__dict__["disk_size_bytes"] = disk_size_bytes
            __props__.__dict__["dynamic"] = dynamic
            __props__.__dict__["extended_location"] = extended_location
            __props__.__dict__["location"] = location
            __props__.__dict__["logical_sector_bytes"] = logical_sector_bytes
            __props__.__dict__["physical_sector_bytes"] = physical_sector_bytes
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["tags"] = tags
            __props__.__dict__["virtualharddisks_name"] = virtualharddisks_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:azurestackhci/v20210901preview:virtualharddiskRetrieve")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualharddiskRetrieve, __self__).__init__(
            'azure-native:azurestackhci/v20210701preview:virtualharddiskRetrieve',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualharddiskRetrieve':
        """
        Get an existing VirtualharddiskRetrieve resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualharddiskRetrieveArgs.__new__(VirtualharddiskRetrieveArgs)

        __props__.__dict__["block_size_bytes"] = None
        __props__.__dict__["disk_size_bytes"] = None
        __props__.__dict__["dynamic"] = None
        __props__.__dict__["extended_location"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["logical_sector_bytes"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["physical_sector_bytes"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return VirtualharddiskRetrieve(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blockSizeBytes")
    def block_size_bytes(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "block_size_bytes")

    @property
    @pulumi.getter(name="diskSizeBytes")
    def disk_size_bytes(self) -> pulumi.Output[Optional[float]]:
        """
        diskSizeBytes - size of the disk in GB
        """
        return pulumi.get(self, "disk_size_bytes")

    @property
    @pulumi.getter
    def dynamic(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean for enabling dynamic sizing on the virtual hard disk
        """
        return pulumi.get(self, "dynamic")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> pulumi.Output[Optional['outputs.ExtendedLocationResponse']]:
        """
        The extendedLocation of the resource.
        """
        return pulumi.get(self, "extended_location")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logicalSectorBytes")
    def logical_sector_bytes(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "logical_sector_bytes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="physicalSectorBytes")
    def physical_sector_bytes(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "physical_sector_bytes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Output[Optional[str]]:
        """
        name of the object to be used in moc
        """
        return pulumi.get(self, "resource_name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.VirtualHardDiskStatusResponse']:
        """
        VirtualHardDiskStatus defines the observed state of VirtualHardDisk
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

