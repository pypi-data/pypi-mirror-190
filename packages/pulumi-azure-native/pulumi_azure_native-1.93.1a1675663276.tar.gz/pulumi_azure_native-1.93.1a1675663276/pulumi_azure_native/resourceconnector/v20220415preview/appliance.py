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

__all__ = ['ApplianceArgs', 'Appliance']

@pulumi.input_type
class ApplianceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 distro: Optional[pulumi.Input[Union[str, 'Distro']]] = None,
                 identity: Optional[pulumi.Input['IdentityArgs']] = None,
                 infrastructure_config: Optional[pulumi.Input['AppliancePropertiesInfrastructureConfigArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Appliance resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Union[str, 'Distro']] distro: Represents a supported Fabric/Infra. (AKSEdge etc...).
        :param pulumi.Input['IdentityArgs'] identity: Identity for the resource.
        :param pulumi.Input['AppliancePropertiesInfrastructureConfigArgs'] infrastructure_config: Contains infrastructure information about the Appliance
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] public_key: Certificates pair used to download MSI certificate from HIS
        :param pulumi.Input[str] resource_name: Appliances name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] version: Version of the Appliance
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if distro is None:
            distro = 'AKSEdge'
        if distro is not None:
            pulumi.set(__self__, "distro", distro)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if infrastructure_config is not None:
            pulumi.set(__self__, "infrastructure_config", infrastructure_config)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if public_key is not None:
            pulumi.set(__self__, "public_key", public_key)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

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
    @pulumi.getter
    def distro(self) -> Optional[pulumi.Input[Union[str, 'Distro']]]:
        """
        Represents a supported Fabric/Infra. (AKSEdge etc...).
        """
        return pulumi.get(self, "distro")

    @distro.setter
    def distro(self, value: Optional[pulumi.Input[Union[str, 'Distro']]]):
        pulumi.set(self, "distro", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityArgs']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="infrastructureConfig")
    def infrastructure_config(self) -> Optional[pulumi.Input['AppliancePropertiesInfrastructureConfigArgs']]:
        """
        Contains infrastructure information about the Appliance
        """
        return pulumi.get(self, "infrastructure_config")

    @infrastructure_config.setter
    def infrastructure_config(self, value: Optional[pulumi.Input['AppliancePropertiesInfrastructureConfigArgs']]):
        pulumi.set(self, "infrastructure_config", value)

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
    @pulumi.getter(name="publicKey")
    def public_key(self) -> Optional[pulumi.Input[str]]:
        """
        Certificates pair used to download MSI certificate from HIS
        """
        return pulumi.get(self, "public_key")

    @public_key.setter
    def public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_key", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Appliances name.
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
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the Appliance
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class Appliance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 distro: Optional[pulumi.Input[Union[str, 'Distro']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 infrastructure_config: Optional[pulumi.Input[pulumi.InputType['AppliancePropertiesInfrastructureConfigArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Appliances definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'Distro']] distro: Represents a supported Fabric/Infra. (AKSEdge etc...).
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: Identity for the resource.
        :param pulumi.Input[pulumi.InputType['AppliancePropertiesInfrastructureConfigArgs']] infrastructure_config: Contains infrastructure information about the Appliance
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] public_key: Certificates pair used to download MSI certificate from HIS
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: Appliances name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] version: Version of the Appliance
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplianceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Appliances definition.

        :param str resource_name: The name of the resource.
        :param ApplianceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplianceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 distro: Optional[pulumi.Input[Union[str, 'Distro']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 infrastructure_config: Optional[pulumi.Input[pulumi.InputType['AppliancePropertiesInfrastructureConfigArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplianceArgs.__new__(ApplianceArgs)

            if distro is None:
                distro = 'AKSEdge'
            __props__.__dict__["distro"] = distro
            __props__.__dict__["identity"] = identity
            __props__.__dict__["infrastructure_config"] = infrastructure_config
            __props__.__dict__["location"] = location
            __props__.__dict__["public_key"] = public_key
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["tags"] = tags
            __props__.__dict__["version"] = version
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:resourceconnector:Appliance"), pulumi.Alias(type_="azure-native:resourceconnector/v20211031preview:Appliance"), pulumi.Alias(type_="azure-native:resourceconnector/v20221027:Appliance")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Appliance, __self__).__init__(
            'azure-native:resourceconnector/v20220415preview:Appliance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Appliance':
        """
        Get an existing Appliance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplianceArgs.__new__(ApplianceArgs)

        __props__.__dict__["distro"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["infrastructure_config"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_key"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["version"] = None
        return Appliance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def distro(self) -> pulumi.Output[Optional[str]]:
        """
        Represents a supported Fabric/Infra. (AKSEdge etc...).
        """
        return pulumi.get(self, "distro")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="infrastructureConfig")
    def infrastructure_config(self) -> pulumi.Output[Optional['outputs.AppliancePropertiesResponseInfrastructureConfig']]:
        """
        Contains infrastructure information about the Appliance
        """
        return pulumi.get(self, "infrastructure_config")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Output[Optional[str]]:
        """
        Certificates pair used to download MSI certificate from HIS
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Appliance’s health and state of connection to on-prem
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource
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

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        Version of the Appliance
        """
        return pulumi.get(self, "version")

