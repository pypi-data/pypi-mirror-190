# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'GuestOSCustomizationArgs',
    'GuestOSNICCustomizationArgs',
    'ResourcePoolArgs',
    'SkuArgs',
    'VirtualDiskArgs',
    'VirtualNetworkArgs',
    'VirtualNicArgs',
]

@pulumi.input_type
class GuestOSCustomizationArgs:
    def __init__(__self__, *,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Guest OS Customization properties
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: List of dns servers to use
        :param pulumi.Input[str] host_name: Virtual Machine hostname
        :param pulumi.Input[str] password: Password for login
        :param pulumi.Input[str] policy_id: id of customization policy
        :param pulumi.Input[str] username: Username for login
        """
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if host_name is not None:
            pulumi.set(__self__, "host_name", host_name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of dns servers to use
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> Optional[pulumi.Input[str]]:
        """
        Virtual Machine hostname
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for login
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        id of customization policy
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Username for login
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class GuestOSNICCustomizationArgs:
    def __init__(__self__, *,
                 allocation: Optional[pulumi.Input[str]] = None,
                 dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 gateway: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 mask: Optional[pulumi.Input[str]] = None,
                 primary_wins_server: Optional[pulumi.Input[str]] = None,
                 secondary_wins_server: Optional[pulumi.Input[str]] = None):
        """
        Guest OS nic customization
        :param pulumi.Input[str] allocation: IP address allocation method
        :param pulumi.Input[Sequence[pulumi.Input[str]]] dns_servers: List of dns servers to use
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateway: Gateway addresses assigned to nic
        :param pulumi.Input[str] ip_address: Static ip address for nic
        :param pulumi.Input[str] mask: Network mask for nic
        :param pulumi.Input[str] primary_wins_server: primary WINS server for Windows
        :param pulumi.Input[str] secondary_wins_server: secondary WINS server for Windows
        """
        if allocation is not None:
            pulumi.set(__self__, "allocation", allocation)
        if dns_servers is not None:
            pulumi.set(__self__, "dns_servers", dns_servers)
        if gateway is not None:
            pulumi.set(__self__, "gateway", gateway)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if mask is not None:
            pulumi.set(__self__, "mask", mask)
        if primary_wins_server is not None:
            pulumi.set(__self__, "primary_wins_server", primary_wins_server)
        if secondary_wins_server is not None:
            pulumi.set(__self__, "secondary_wins_server", secondary_wins_server)

    @property
    @pulumi.getter
    def allocation(self) -> Optional[pulumi.Input[str]]:
        """
        IP address allocation method
        """
        return pulumi.get(self, "allocation")

    @allocation.setter
    def allocation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allocation", value)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of dns servers to use
        """
        return pulumi.get(self, "dns_servers")

    @dns_servers.setter
    def dns_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "dns_servers", value)

    @property
    @pulumi.getter
    def gateway(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Gateway addresses assigned to nic
        """
        return pulumi.get(self, "gateway")

    @gateway.setter
    def gateway(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateway", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Static ip address for nic
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def mask(self) -> Optional[pulumi.Input[str]]:
        """
        Network mask for nic
        """
        return pulumi.get(self, "mask")

    @mask.setter
    def mask(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mask", value)

    @property
    @pulumi.getter(name="primaryWinsServer")
    def primary_wins_server(self) -> Optional[pulumi.Input[str]]:
        """
        primary WINS server for Windows
        """
        return pulumi.get(self, "primary_wins_server")

    @primary_wins_server.setter
    def primary_wins_server(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_wins_server", value)

    @property
    @pulumi.getter(name="secondaryWinsServer")
    def secondary_wins_server(self) -> Optional[pulumi.Input[str]]:
        """
        secondary WINS server for Windows
        """
        return pulumi.get(self, "secondary_wins_server")

    @secondary_wins_server.setter
    def secondary_wins_server(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_wins_server", value)


@pulumi.input_type
class ResourcePoolArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str]):
        """
        Resource pool model
        :param pulumi.Input[str] id: resource pool id (privateCloudId:vsphereId)
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        resource pool id (privateCloudId:vsphereId)
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 capacity: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        The purchase SKU for CloudSimple paid resources
        :param pulumi.Input[str] name: The name of the SKU for VMWare CloudSimple Node
        :param pulumi.Input[str] capacity: The capacity of the SKU
        :param pulumi.Input[str] description: dedicatedCloudNode example: 8 x Ten-Core Intel® Xeon® Processor E5-2640 v4 2.40GHz 25MB Cache (90W); 12 x 64GB PC4-19200 2400MHz DDR4 ECC Registered DIMM, ...
        :param pulumi.Input[str] family: If the service has different generations of hardware, for the same SKU, then that can be captured here
        :param pulumi.Input[str] tier: The tier of the SKU
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SKU for VMWare CloudSimple Node
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[str]]:
        """
        The capacity of the SKU
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        dedicatedCloudNode example: 8 x Ten-Core Intel® Xeon® Processor E5-2640 v4 2.40GHz 25MB Cache (90W); 12 x 64GB PC4-19200 2400MHz DDR4 ECC Registered DIMM, ...
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        If the service has different generations of hardware, for the same SKU, then that can be captured here
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        The tier of the SKU
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class VirtualDiskArgs:
    def __init__(__self__, *,
                 controller_id: pulumi.Input[str],
                 independence_mode: pulumi.Input['DiskIndependenceMode'],
                 total_size: pulumi.Input[int],
                 virtual_disk_id: Optional[pulumi.Input[str]] = None):
        """
        Virtual disk model
        :param pulumi.Input[str] controller_id: Disk's Controller id
        :param pulumi.Input['DiskIndependenceMode'] independence_mode: Disk's independence mode type
        :param pulumi.Input[int] total_size: Disk's total size
        :param pulumi.Input[str] virtual_disk_id: Disk's id
        """
        pulumi.set(__self__, "controller_id", controller_id)
        pulumi.set(__self__, "independence_mode", independence_mode)
        pulumi.set(__self__, "total_size", total_size)
        if virtual_disk_id is not None:
            pulumi.set(__self__, "virtual_disk_id", virtual_disk_id)

    @property
    @pulumi.getter(name="controllerId")
    def controller_id(self) -> pulumi.Input[str]:
        """
        Disk's Controller id
        """
        return pulumi.get(self, "controller_id")

    @controller_id.setter
    def controller_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "controller_id", value)

    @property
    @pulumi.getter(name="independenceMode")
    def independence_mode(self) -> pulumi.Input['DiskIndependenceMode']:
        """
        Disk's independence mode type
        """
        return pulumi.get(self, "independence_mode")

    @independence_mode.setter
    def independence_mode(self, value: pulumi.Input['DiskIndependenceMode']):
        pulumi.set(self, "independence_mode", value)

    @property
    @pulumi.getter(name="totalSize")
    def total_size(self) -> pulumi.Input[int]:
        """
        Disk's total size
        """
        return pulumi.get(self, "total_size")

    @total_size.setter
    def total_size(self, value: pulumi.Input[int]):
        pulumi.set(self, "total_size", value)

    @property
    @pulumi.getter(name="virtualDiskId")
    def virtual_disk_id(self) -> Optional[pulumi.Input[str]]:
        """
        Disk's id
        """
        return pulumi.get(self, "virtual_disk_id")

    @virtual_disk_id.setter
    def virtual_disk_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_disk_id", value)


@pulumi.input_type
class VirtualNetworkArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str]):
        """
        Virtual network model
        :param pulumi.Input[str] id: virtual network id (privateCloudId:vsphereId)
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        virtual network id (privateCloudId:vsphereId)
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class VirtualNicArgs:
    def __init__(__self__, *,
                 network: pulumi.Input['VirtualNetworkArgs'],
                 nic_type: pulumi.Input['NICType'],
                 customization: Optional[pulumi.Input['GuestOSNICCustomizationArgs']] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 power_on_boot: Optional[pulumi.Input[bool]] = None,
                 virtual_nic_id: Optional[pulumi.Input[str]] = None):
        """
        Virtual NIC model
        :param pulumi.Input['VirtualNetworkArgs'] network: Virtual Network
        :param pulumi.Input['NICType'] nic_type: NIC type
        :param pulumi.Input['GuestOSNICCustomizationArgs'] customization: guest OS customization for nic
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: NIC ip address
        :param pulumi.Input[str] mac_address: NIC MAC address
        :param pulumi.Input[bool] power_on_boot: Is NIC powered on/off on boot
        :param pulumi.Input[str] virtual_nic_id: NIC id
        """
        pulumi.set(__self__, "network", network)
        pulumi.set(__self__, "nic_type", nic_type)
        if customization is not None:
            pulumi.set(__self__, "customization", customization)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if power_on_boot is not None:
            pulumi.set(__self__, "power_on_boot", power_on_boot)
        if virtual_nic_id is not None:
            pulumi.set(__self__, "virtual_nic_id", virtual_nic_id)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input['VirtualNetworkArgs']:
        """
        Virtual Network
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input['VirtualNetworkArgs']):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="nicType")
    def nic_type(self) -> pulumi.Input['NICType']:
        """
        NIC type
        """
        return pulumi.get(self, "nic_type")

    @nic_type.setter
    def nic_type(self, value: pulumi.Input['NICType']):
        pulumi.set(self, "nic_type", value)

    @property
    @pulumi.getter
    def customization(self) -> Optional[pulumi.Input['GuestOSNICCustomizationArgs']]:
        """
        guest OS customization for nic
        """
        return pulumi.get(self, "customization")

    @customization.setter
    def customization(self, value: Optional[pulumi.Input['GuestOSNICCustomizationArgs']]):
        pulumi.set(self, "customization", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        NIC ip address
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[pulumi.Input[str]]:
        """
        NIC MAC address
        """
        return pulumi.get(self, "mac_address")

    @mac_address.setter
    def mac_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac_address", value)

    @property
    @pulumi.getter(name="powerOnBoot")
    def power_on_boot(self) -> Optional[pulumi.Input[bool]]:
        """
        Is NIC powered on/off on boot
        """
        return pulumi.get(self, "power_on_boot")

    @power_on_boot.setter
    def power_on_boot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "power_on_boot", value)

    @property
    @pulumi.getter(name="virtualNicId")
    def virtual_nic_id(self) -> Optional[pulumi.Input[str]]:
        """
        NIC id
        """
        return pulumi.get(self, "virtual_nic_id")

    @virtual_nic_id.setter
    def virtual_nic_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_nic_id", value)


