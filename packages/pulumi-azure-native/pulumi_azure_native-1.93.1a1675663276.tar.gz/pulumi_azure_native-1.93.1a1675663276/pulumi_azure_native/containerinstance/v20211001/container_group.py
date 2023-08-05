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

__all__ = ['ContainerGroupArgs', 'ContainerGroup']

@pulumi.input_type
class ContainerGroupArgs:
    def __init__(__self__, *,
                 containers: pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]],
                 os_type: pulumi.Input[Union[str, 'OperatingSystemTypes']],
                 resource_group_name: pulumi.Input[str],
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 diagnostics: Optional[pulumi.Input['ContainerGroupDiagnosticsArgs']] = None,
                 dns_config: Optional[pulumi.Input['DnsConfigurationArgs']] = None,
                 encryption_properties: Optional[pulumi.Input['EncryptionPropertiesArgs']] = None,
                 identity: Optional[pulumi.Input['ContainerGroupIdentityArgs']] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]] = None,
                 init_containers: Optional[pulumi.Input[Sequence[pulumi.Input['InitContainerDefinitionArgs']]]] = None,
                 ip_address: Optional[pulumi.Input['IpAddressArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 sku: Optional[pulumi.Input[Union[str, 'ContainerGroupSku']]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerGroupSubnetIdArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ContainerGroup resource.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]] containers: The containers within the container group.
        :param pulumi.Input[Union[str, 'OperatingSystemTypes']] os_type: The operating system type required by the containers in the container group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] container_group_name: The name of the container group.
        :param pulumi.Input['ContainerGroupDiagnosticsArgs'] diagnostics: The diagnostic information for a container group.
        :param pulumi.Input['DnsConfigurationArgs'] dns_config: The DNS config information for a container group.
        :param pulumi.Input['EncryptionPropertiesArgs'] encryption_properties: The encryption properties for a container group.
        :param pulumi.Input['ContainerGroupIdentityArgs'] identity: The identity of the container group, if configured.
        :param pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]] image_registry_credentials: The image registry credentials by which the container group is created from.
        :param pulumi.Input[Sequence[pulumi.Input['InitContainerDefinitionArgs']]] init_containers: The init containers for a container group.
        :param pulumi.Input['IpAddressArgs'] ip_address: The IP address type of the container group.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']] restart_policy: Restart policy for all containers within the container group. 
               - `Always` Always restart
               - `OnFailure` Restart on failure
               - `Never` Never restart
        :param pulumi.Input[Union[str, 'ContainerGroupSku']] sku: The SKU for a container group.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerGroupSubnetIdArgs']]] subnet_ids: The subnet resource IDs for a container group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]] volumes: The list of volumes that can be mounted by containers in this container group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: The zones for the container group.
        """
        pulumi.set(__self__, "containers", containers)
        pulumi.set(__self__, "os_type", os_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if container_group_name is not None:
            pulumi.set(__self__, "container_group_name", container_group_name)
        if diagnostics is not None:
            pulumi.set(__self__, "diagnostics", diagnostics)
        if dns_config is not None:
            pulumi.set(__self__, "dns_config", dns_config)
        if encryption_properties is not None:
            pulumi.set(__self__, "encryption_properties", encryption_properties)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if image_registry_credentials is not None:
            pulumi.set(__self__, "image_registry_credentials", image_registry_credentials)
        if init_containers is not None:
            pulumi.set(__self__, "init_containers", init_containers)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if restart_policy is not None:
            pulumi.set(__self__, "restart_policy", restart_policy)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if volumes is not None:
            pulumi.set(__self__, "volumes", volumes)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]]:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @containers.setter
    def containers(self, value: pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]]):
        pulumi.set(self, "containers", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Input[Union[str, 'OperatingSystemTypes']]:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: pulumi.Input[Union[str, 'OperatingSystemTypes']]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="containerGroupName")
    def container_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container group.
        """
        return pulumi.get(self, "container_group_name")

    @container_group_name.setter
    def container_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_group_name", value)

    @property
    @pulumi.getter
    def diagnostics(self) -> Optional[pulumi.Input['ContainerGroupDiagnosticsArgs']]:
        """
        The diagnostic information for a container group.
        """
        return pulumi.get(self, "diagnostics")

    @diagnostics.setter
    def diagnostics(self, value: Optional[pulumi.Input['ContainerGroupDiagnosticsArgs']]):
        pulumi.set(self, "diagnostics", value)

    @property
    @pulumi.getter(name="dnsConfig")
    def dns_config(self) -> Optional[pulumi.Input['DnsConfigurationArgs']]:
        """
        The DNS config information for a container group.
        """
        return pulumi.get(self, "dns_config")

    @dns_config.setter
    def dns_config(self, value: Optional[pulumi.Input['DnsConfigurationArgs']]):
        pulumi.set(self, "dns_config", value)

    @property
    @pulumi.getter(name="encryptionProperties")
    def encryption_properties(self) -> Optional[pulumi.Input['EncryptionPropertiesArgs']]:
        """
        The encryption properties for a container group.
        """
        return pulumi.get(self, "encryption_properties")

    @encryption_properties.setter
    def encryption_properties(self, value: Optional[pulumi.Input['EncryptionPropertiesArgs']]):
        pulumi.set(self, "encryption_properties", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ContainerGroupIdentityArgs']]:
        """
        The identity of the container group, if configured.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ContainerGroupIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @image_registry_credentials.setter
    def image_registry_credentials(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]]):
        pulumi.set(self, "image_registry_credentials", value)

    @property
    @pulumi.getter(name="initContainers")
    def init_containers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InitContainerDefinitionArgs']]]]:
        """
        The init containers for a container group.
        """
        return pulumi.get(self, "init_containers")

    @init_containers.setter
    def init_containers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InitContainerDefinitionArgs']]]]):
        pulumi.set(self, "init_containers", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input['IpAddressArgs']]:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input['IpAddressArgs']]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @restart_policy.setter
    def restart_policy(self, value: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]]):
        pulumi.set(self, "restart_policy", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[Union[str, 'ContainerGroupSku']]]:
        """
        The SKU for a container group.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[Union[str, 'ContainerGroupSku']]]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContainerGroupSubnetIdArgs']]]]:
        """
        The subnet resource IDs for a container group.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerGroupSubnetIdArgs']]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def volumes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]]):
        pulumi.set(self, "volumes", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The zones for the container group.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


class ContainerGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]]] = None,
                 diagnostics: Optional[pulumi.Input[pulumi.InputType['ContainerGroupDiagnosticsArgs']]] = None,
                 dns_config: Optional[pulumi.Input[pulumi.InputType['DnsConfigurationArgs']]] = None,
                 encryption_properties: Optional[pulumi.Input[pulumi.InputType['EncryptionPropertiesArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ContainerGroupIdentityArgs']]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]]] = None,
                 init_containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InitContainerDefinitionArgs']]]]] = None,
                 ip_address: Optional[pulumi.Input[pulumi.InputType['IpAddressArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OperatingSystemTypes']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 sku: Optional[pulumi.Input[Union[str, 'ContainerGroupSku']]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerGroupSubnetIdArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A container group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_group_name: The name of the container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]] containers: The containers within the container group.
        :param pulumi.Input[pulumi.InputType['ContainerGroupDiagnosticsArgs']] diagnostics: The diagnostic information for a container group.
        :param pulumi.Input[pulumi.InputType['DnsConfigurationArgs']] dns_config: The DNS config information for a container group.
        :param pulumi.Input[pulumi.InputType['EncryptionPropertiesArgs']] encryption_properties: The encryption properties for a container group.
        :param pulumi.Input[pulumi.InputType['ContainerGroupIdentityArgs']] identity: The identity of the container group, if configured.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]] image_registry_credentials: The image registry credentials by which the container group is created from.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InitContainerDefinitionArgs']]]] init_containers: The init containers for a container group.
        :param pulumi.Input[pulumi.InputType['IpAddressArgs']] ip_address: The IP address type of the container group.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'OperatingSystemTypes']] os_type: The operating system type required by the containers in the container group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']] restart_policy: Restart policy for all containers within the container group. 
               - `Always` Always restart
               - `OnFailure` Restart on failure
               - `Never` Never restart
        :param pulumi.Input[Union[str, 'ContainerGroupSku']] sku: The SKU for a container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerGroupSubnetIdArgs']]]] subnet_ids: The subnet resource IDs for a container group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]] volumes: The list of volumes that can be mounted by containers in this container group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: The zones for the container group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A container group.

        :param str resource_name: The name of the resource.
        :param ContainerGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]]] = None,
                 diagnostics: Optional[pulumi.Input[pulumi.InputType['ContainerGroupDiagnosticsArgs']]] = None,
                 dns_config: Optional[pulumi.Input[pulumi.InputType['DnsConfigurationArgs']]] = None,
                 encryption_properties: Optional[pulumi.Input[pulumi.InputType['EncryptionPropertiesArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ContainerGroupIdentityArgs']]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]]] = None,
                 init_containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InitContainerDefinitionArgs']]]]] = None,
                 ip_address: Optional[pulumi.Input[pulumi.InputType['IpAddressArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OperatingSystemTypes']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 sku: Optional[pulumi.Input[Union[str, 'ContainerGroupSku']]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerGroupSubnetIdArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerGroupArgs.__new__(ContainerGroupArgs)

            __props__.__dict__["container_group_name"] = container_group_name
            if containers is None and not opts.urn:
                raise TypeError("Missing required property 'containers'")
            __props__.__dict__["containers"] = containers
            __props__.__dict__["diagnostics"] = diagnostics
            __props__.__dict__["dns_config"] = dns_config
            __props__.__dict__["encryption_properties"] = encryption_properties
            __props__.__dict__["identity"] = identity
            __props__.__dict__["image_registry_credentials"] = image_registry_credentials
            __props__.__dict__["init_containers"] = init_containers
            __props__.__dict__["ip_address"] = ip_address
            __props__.__dict__["location"] = location
            if os_type is None and not opts.urn:
                raise TypeError("Missing required property 'os_type'")
            __props__.__dict__["os_type"] = os_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["restart_policy"] = restart_policy
            __props__.__dict__["sku"] = sku
            __props__.__dict__["subnet_ids"] = subnet_ids
            __props__.__dict__["tags"] = tags
            __props__.__dict__["volumes"] = volumes
            __props__.__dict__["zones"] = zones
            __props__.__dict__["instance_view"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerinstance:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20170801preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20171001preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20171201preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180201preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180401:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180601:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180901:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20181001:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20191201:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20201101:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210301:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210701:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210901:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20220901:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20221001preview:ContainerGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ContainerGroup, __self__).__init__(
            'azure-native:containerinstance/v20211001:ContainerGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ContainerGroup':
        """
        Get an existing ContainerGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ContainerGroupArgs.__new__(ContainerGroupArgs)

        __props__.__dict__["containers"] = None
        __props__.__dict__["diagnostics"] = None
        __props__.__dict__["dns_config"] = None
        __props__.__dict__["encryption_properties"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["image_registry_credentials"] = None
        __props__.__dict__["init_containers"] = None
        __props__.__dict__["instance_view"] = None
        __props__.__dict__["ip_address"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["os_type"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["restart_policy"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["subnet_ids"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["volumes"] = None
        __props__.__dict__["zones"] = None
        return ContainerGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Sequence['outputs.ContainerResponse']]:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter
    def diagnostics(self) -> pulumi.Output[Optional['outputs.ContainerGroupDiagnosticsResponse']]:
        """
        The diagnostic information for a container group.
        """
        return pulumi.get(self, "diagnostics")

    @property
    @pulumi.getter(name="dnsConfig")
    def dns_config(self) -> pulumi.Output[Optional['outputs.DnsConfigurationResponse']]:
        """
        The DNS config information for a container group.
        """
        return pulumi.get(self, "dns_config")

    @property
    @pulumi.getter(name="encryptionProperties")
    def encryption_properties(self) -> pulumi.Output[Optional['outputs.EncryptionPropertiesResponse']]:
        """
        The encryption properties for a container group.
        """
        return pulumi.get(self, "encryption_properties")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ContainerGroupIdentityResponse']]:
        """
        The identity of the container group, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> pulumi.Output[Optional[Sequence['outputs.ImageRegistryCredentialResponse']]]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @property
    @pulumi.getter(name="initContainers")
    def init_containers(self) -> pulumi.Output[Optional[Sequence['outputs.InitContainerDefinitionResponse']]]:
        """
        The init containers for a container group.
        """
        return pulumi.get(self, "init_containers")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> pulumi.Output['outputs.ContainerGroupPropertiesResponseInstanceView']:
        """
        The instance view of the container group. Only valid in response.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional['outputs.IpAddressResponse']]:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[str]:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the container group. This only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional[str]]:
        """
        The SKU for a container group.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[Optional[Sequence['outputs.ContainerGroupSubnetIdResponse']]]:
        """
        The subnet resource IDs for a container group.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def volumes(self) -> pulumi.Output[Optional[Sequence['outputs.VolumeResponse']]]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The zones for the container group.
        """
        return pulumi.get(self, "zones")

