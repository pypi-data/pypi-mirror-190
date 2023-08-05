# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'CheckpointArgs',
    'ExtendedLocationArgs',
    'HardwareProfileArgs',
    'NetworkInterfacesArgs',
    'NetworkProfileArgs',
    'OsProfileArgs',
    'StorageProfileArgs',
    'StorageQoSPolicyDetailsArgs',
    'VMMServerPropertiesCredentialsArgs',
    'VirtualDiskArgs',
    'VirtualMachinePropertiesAvailabilitySetsArgs',
]

@pulumi.input_type
class CheckpointArgs:
    def __init__(__self__, *,
                 checkpoint_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_checkpoint_id: Optional[pulumi.Input[str]] = None):
        """
        Defines the resource properties.
        :param pulumi.Input[str] checkpoint_id: Gets ID of the checkpoint.
        :param pulumi.Input[str] description: Gets description of the checkpoint.
        :param pulumi.Input[str] name: Gets name of the checkpoint.
        :param pulumi.Input[str] parent_checkpoint_id: Gets ID of parent of the checkpoint.
        """
        if checkpoint_id is not None:
            pulumi.set(__self__, "checkpoint_id", checkpoint_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_checkpoint_id is not None:
            pulumi.set(__self__, "parent_checkpoint_id", parent_checkpoint_id)

    @property
    @pulumi.getter(name="checkpointID")
    def checkpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets ID of the checkpoint.
        """
        return pulumi.get(self, "checkpoint_id")

    @checkpoint_id.setter
    def checkpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "checkpoint_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Gets description of the checkpoint.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets name of the checkpoint.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parentCheckpointID")
    def parent_checkpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets ID of parent of the checkpoint.
        """
        return pulumi.get(self, "parent_checkpoint_id")

    @parent_checkpoint_id.setter
    def parent_checkpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_checkpoint_id", value)


@pulumi.input_type
class ExtendedLocationArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The extended location.
        :param pulumi.Input[str] name: The extended location name.
        :param pulumi.Input[str] type: The extended location type.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The extended location name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The extended location type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class HardwareProfileArgs:
    def __init__(__self__, *,
                 cpu_count: Optional[pulumi.Input[int]] = None,
                 dynamic_memory_enabled: Optional[pulumi.Input[Union[str, 'DynamicMemoryEnabled']]] = None,
                 dynamic_memory_max_mb: Optional[pulumi.Input[int]] = None,
                 dynamic_memory_min_mb: Optional[pulumi.Input[int]] = None,
                 is_highly_available: Optional[pulumi.Input[str]] = None,
                 limit_cpu_for_migration: Optional[pulumi.Input[Union[str, 'LimitCpuForMigration']]] = None,
                 memory_mb: Optional[pulumi.Input[int]] = None):
        """
        Defines the resource properties.
        :param pulumi.Input[int] cpu_count: Gets or sets the number of vCPUs for the vm.
        :param pulumi.Input[Union[str, 'DynamicMemoryEnabled']] dynamic_memory_enabled: Gets or sets a value indicating whether to enable dynamic memory or not.
        :param pulumi.Input[int] dynamic_memory_max_mb: Gets or sets the max dynamic memory for the vm.
        :param pulumi.Input[int] dynamic_memory_min_mb: Gets or sets the min dynamic memory for the vm.
        :param pulumi.Input[str] is_highly_available: Gets highly available property.
        :param pulumi.Input[Union[str, 'LimitCpuForMigration']] limit_cpu_for_migration: Gets or sets a value indicating whether to enable processor compatibility mode for live migration of VMs.
        :param pulumi.Input[int] memory_mb: MemoryMB is the size of a virtual machine's memory, in MB.
        """
        if cpu_count is not None:
            pulumi.set(__self__, "cpu_count", cpu_count)
        if dynamic_memory_enabled is not None:
            pulumi.set(__self__, "dynamic_memory_enabled", dynamic_memory_enabled)
        if dynamic_memory_max_mb is not None:
            pulumi.set(__self__, "dynamic_memory_max_mb", dynamic_memory_max_mb)
        if dynamic_memory_min_mb is not None:
            pulumi.set(__self__, "dynamic_memory_min_mb", dynamic_memory_min_mb)
        if is_highly_available is not None:
            pulumi.set(__self__, "is_highly_available", is_highly_available)
        if limit_cpu_for_migration is not None:
            pulumi.set(__self__, "limit_cpu_for_migration", limit_cpu_for_migration)
        if memory_mb is not None:
            pulumi.set(__self__, "memory_mb", memory_mb)

    @property
    @pulumi.getter(name="cpuCount")
    def cpu_count(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the number of vCPUs for the vm.
        """
        return pulumi.get(self, "cpu_count")

    @cpu_count.setter
    def cpu_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cpu_count", value)

    @property
    @pulumi.getter(name="dynamicMemoryEnabled")
    def dynamic_memory_enabled(self) -> Optional[pulumi.Input[Union[str, 'DynamicMemoryEnabled']]]:
        """
        Gets or sets a value indicating whether to enable dynamic memory or not.
        """
        return pulumi.get(self, "dynamic_memory_enabled")

    @dynamic_memory_enabled.setter
    def dynamic_memory_enabled(self, value: Optional[pulumi.Input[Union[str, 'DynamicMemoryEnabled']]]):
        pulumi.set(self, "dynamic_memory_enabled", value)

    @property
    @pulumi.getter(name="dynamicMemoryMaxMB")
    def dynamic_memory_max_mb(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the max dynamic memory for the vm.
        """
        return pulumi.get(self, "dynamic_memory_max_mb")

    @dynamic_memory_max_mb.setter
    def dynamic_memory_max_mb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dynamic_memory_max_mb", value)

    @property
    @pulumi.getter(name="dynamicMemoryMinMB")
    def dynamic_memory_min_mb(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the min dynamic memory for the vm.
        """
        return pulumi.get(self, "dynamic_memory_min_mb")

    @dynamic_memory_min_mb.setter
    def dynamic_memory_min_mb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dynamic_memory_min_mb", value)

    @property
    @pulumi.getter(name="isHighlyAvailable")
    def is_highly_available(self) -> Optional[pulumi.Input[str]]:
        """
        Gets highly available property.
        """
        return pulumi.get(self, "is_highly_available")

    @is_highly_available.setter
    def is_highly_available(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "is_highly_available", value)

    @property
    @pulumi.getter(name="limitCpuForMigration")
    def limit_cpu_for_migration(self) -> Optional[pulumi.Input[Union[str, 'LimitCpuForMigration']]]:
        """
        Gets or sets a value indicating whether to enable processor compatibility mode for live migration of VMs.
        """
        return pulumi.get(self, "limit_cpu_for_migration")

    @limit_cpu_for_migration.setter
    def limit_cpu_for_migration(self, value: Optional[pulumi.Input[Union[str, 'LimitCpuForMigration']]]):
        pulumi.set(self, "limit_cpu_for_migration", value)

    @property
    @pulumi.getter(name="memoryMB")
    def memory_mb(self) -> Optional[pulumi.Input[int]]:
        """
        MemoryMB is the size of a virtual machine's memory, in MB.
        """
        return pulumi.get(self, "memory_mb")

    @memory_mb.setter
    def memory_mb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "memory_mb", value)


@pulumi.input_type
class NetworkInterfacesArgs:
    def __init__(__self__, *,
                 ipv4_address_type: Optional[pulumi.Input[Union[str, 'AllocationMethod']]] = None,
                 ipv6_address_type: Optional[pulumi.Input[Union[str, 'AllocationMethod']]] = None,
                 mac_address: Optional[pulumi.Input[str]] = None,
                 mac_address_type: Optional[pulumi.Input[Union[str, 'AllocationMethod']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 nic_id: Optional[pulumi.Input[str]] = None,
                 virtual_network_id: Optional[pulumi.Input[str]] = None):
        """
        Network Interface model
        :param pulumi.Input[Union[str, 'AllocationMethod']] ipv4_address_type: Gets or sets the ipv4 address type.
        :param pulumi.Input[Union[str, 'AllocationMethod']] ipv6_address_type: Gets or sets the ipv6 address type.
        :param pulumi.Input[str] mac_address: Gets or sets the nic MAC address.
        :param pulumi.Input[Union[str, 'AllocationMethod']] mac_address_type: Gets or sets the mac address type.
        :param pulumi.Input[str] name: Gets or sets the name of the network interface.
        :param pulumi.Input[str] nic_id: Gets or sets the nic id.
        :param pulumi.Input[str] virtual_network_id: Gets or sets the ARM Id of the Microsoft.ScVmm/virtualNetwork resource to connect the nic.
        """
        if ipv4_address_type is not None:
            pulumi.set(__self__, "ipv4_address_type", ipv4_address_type)
        if ipv6_address_type is not None:
            pulumi.set(__self__, "ipv6_address_type", ipv6_address_type)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if mac_address_type is not None:
            pulumi.set(__self__, "mac_address_type", mac_address_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if nic_id is not None:
            pulumi.set(__self__, "nic_id", nic_id)
        if virtual_network_id is not None:
            pulumi.set(__self__, "virtual_network_id", virtual_network_id)

    @property
    @pulumi.getter(name="ipv4AddressType")
    def ipv4_address_type(self) -> Optional[pulumi.Input[Union[str, 'AllocationMethod']]]:
        """
        Gets or sets the ipv4 address type.
        """
        return pulumi.get(self, "ipv4_address_type")

    @ipv4_address_type.setter
    def ipv4_address_type(self, value: Optional[pulumi.Input[Union[str, 'AllocationMethod']]]):
        pulumi.set(self, "ipv4_address_type", value)

    @property
    @pulumi.getter(name="ipv6AddressType")
    def ipv6_address_type(self) -> Optional[pulumi.Input[Union[str, 'AllocationMethod']]]:
        """
        Gets or sets the ipv6 address type.
        """
        return pulumi.get(self, "ipv6_address_type")

    @ipv6_address_type.setter
    def ipv6_address_type(self, value: Optional[pulumi.Input[Union[str, 'AllocationMethod']]]):
        pulumi.set(self, "ipv6_address_type", value)

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the nic MAC address.
        """
        return pulumi.get(self, "mac_address")

    @mac_address.setter
    def mac_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mac_address", value)

    @property
    @pulumi.getter(name="macAddressType")
    def mac_address_type(self) -> Optional[pulumi.Input[Union[str, 'AllocationMethod']]]:
        """
        Gets or sets the mac address type.
        """
        return pulumi.get(self, "mac_address_type")

    @mac_address_type.setter
    def mac_address_type(self, value: Optional[pulumi.Input[Union[str, 'AllocationMethod']]]):
        pulumi.set(self, "mac_address_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the name of the network interface.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nicId")
    def nic_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the nic id.
        """
        return pulumi.get(self, "nic_id")

    @nic_id.setter
    def nic_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nic_id", value)

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the ARM Id of the Microsoft.ScVmm/virtualNetwork resource to connect the nic.
        """
        return pulumi.get(self, "virtual_network_id")

    @virtual_network_id.setter
    def virtual_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_network_id", value)


@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 network_interfaces: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfacesArgs']]]] = None):
        """
        Defines the resource properties.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkInterfacesArgs']]] network_interfaces: Gets or sets the list of network interfaces associated with the virtual machine.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfacesArgs']]]]:
        """
        Gets or sets the list of network interfaces associated with the virtual machine.
        """
        return pulumi.get(self, "network_interfaces")

    @network_interfaces.setter
    def network_interfaces(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfacesArgs']]]]):
        pulumi.set(self, "network_interfaces", value)


@pulumi.input_type
class OsProfileArgs:
    def __init__(__self__, *,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 computer_name: Optional[pulumi.Input[str]] = None):
        """
        Defines the resource properties.
        :param pulumi.Input[str] admin_password: Admin password of the virtual machine.
        :param pulumi.Input[str] computer_name: Gets or sets computer name.
        """
        if admin_password is not None:
            pulumi.set(__self__, "admin_password", admin_password)
        if computer_name is not None:
            pulumi.set(__self__, "computer_name", computer_name)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> Optional[pulumi.Input[str]]:
        """
        Admin password of the virtual machine.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter(name="computerName")
    def computer_name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets computer name.
        """
        return pulumi.get(self, "computer_name")

    @computer_name.setter
    def computer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "computer_name", value)


@pulumi.input_type
class StorageProfileArgs:
    def __init__(__self__, *,
                 disks: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualDiskArgs']]]] = None):
        """
        Defines the resource properties.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualDiskArgs']]] disks: Gets or sets the list of virtual disks associated with the virtual machine.
        """
        if disks is not None:
            pulumi.set(__self__, "disks", disks)

    @property
    @pulumi.getter
    def disks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualDiskArgs']]]]:
        """
        Gets or sets the list of virtual disks associated with the virtual machine.
        """
        return pulumi.get(self, "disks")

    @disks.setter
    def disks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualDiskArgs']]]]):
        pulumi.set(self, "disks", value)


@pulumi.input_type
class StorageQoSPolicyDetailsArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The StorageQoSPolicyDetails definition.
        :param pulumi.Input[str] id: The ID of the QoS policy.
        :param pulumi.Input[str] name: The name of the policy.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the QoS policy.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class VMMServerPropertiesCredentialsArgs:
    def __init__(__self__, *,
                 password: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Credentials to connect to VMMServer.
        :param pulumi.Input[str] password: Credentials to use to connect to VMMServer.
        :param pulumi.Input[str] username: Username to use to connect to VMMServer.
        """
        if password is not None:
            pulumi.set(__self__, "password", password)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Credentials to use to connect to VMMServer.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Username to use to connect to VMMServer.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class VirtualDiskArgs:
    def __init__(__self__, *,
                 bus: Optional[pulumi.Input[int]] = None,
                 bus_type: Optional[pulumi.Input[str]] = None,
                 create_diff_disk: Optional[pulumi.Input[Union[str, 'CreateDiffDisk']]] = None,
                 disk_id: Optional[pulumi.Input[str]] = None,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 lun: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 storage_qo_s_policy: Optional[pulumi.Input['StorageQoSPolicyDetailsArgs']] = None,
                 template_disk_id: Optional[pulumi.Input[str]] = None,
                 vhd_type: Optional[pulumi.Input[str]] = None):
        """
        Virtual disk model
        :param pulumi.Input[int] bus: Gets or sets the disk bus.
        :param pulumi.Input[str] bus_type: Gets or sets the disk bus type.
        :param pulumi.Input[Union[str, 'CreateDiffDisk']] create_diff_disk: Gets or sets a value indicating diff disk.
        :param pulumi.Input[str] disk_id: Gets or sets the disk id.
        :param pulumi.Input[int] disk_size_gb: Gets or sets the disk total size.
        :param pulumi.Input[int] lun: Gets or sets the disk lun.
        :param pulumi.Input[str] name: Gets or sets the name of the disk.
        :param pulumi.Input['StorageQoSPolicyDetailsArgs'] storage_qo_s_policy: The QoS policy for the disk.
        :param pulumi.Input[str] template_disk_id: Gets or sets the disk id in the template.
        :param pulumi.Input[str] vhd_type: Gets or sets the disk vhd type.
        """
        if bus is not None:
            pulumi.set(__self__, "bus", bus)
        if bus_type is not None:
            pulumi.set(__self__, "bus_type", bus_type)
        if create_diff_disk is not None:
            pulumi.set(__self__, "create_diff_disk", create_diff_disk)
        if disk_id is not None:
            pulumi.set(__self__, "disk_id", disk_id)
        if disk_size_gb is not None:
            pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if lun is not None:
            pulumi.set(__self__, "lun", lun)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if storage_qo_s_policy is not None:
            pulumi.set(__self__, "storage_qo_s_policy", storage_qo_s_policy)
        if template_disk_id is not None:
            pulumi.set(__self__, "template_disk_id", template_disk_id)
        if vhd_type is not None:
            pulumi.set(__self__, "vhd_type", vhd_type)

    @property
    @pulumi.getter
    def bus(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the disk bus.
        """
        return pulumi.get(self, "bus")

    @bus.setter
    def bus(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bus", value)

    @property
    @pulumi.getter(name="busType")
    def bus_type(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the disk bus type.
        """
        return pulumi.get(self, "bus_type")

    @bus_type.setter
    def bus_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bus_type", value)

    @property
    @pulumi.getter(name="createDiffDisk")
    def create_diff_disk(self) -> Optional[pulumi.Input[Union[str, 'CreateDiffDisk']]]:
        """
        Gets or sets a value indicating diff disk.
        """
        return pulumi.get(self, "create_diff_disk")

    @create_diff_disk.setter
    def create_diff_disk(self, value: Optional[pulumi.Input[Union[str, 'CreateDiffDisk']]]):
        pulumi.set(self, "create_diff_disk", value)

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the disk id.
        """
        return pulumi.get(self, "disk_id")

    @disk_id.setter
    def disk_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disk_id", value)

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the disk total size.
        """
        return pulumi.get(self, "disk_size_gb")

    @disk_size_gb.setter
    def disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "disk_size_gb", value)

    @property
    @pulumi.getter
    def lun(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the disk lun.
        """
        return pulumi.get(self, "lun")

    @lun.setter
    def lun(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lun", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the name of the disk.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="storageQoSPolicy")
    def storage_qo_s_policy(self) -> Optional[pulumi.Input['StorageQoSPolicyDetailsArgs']]:
        """
        The QoS policy for the disk.
        """
        return pulumi.get(self, "storage_qo_s_policy")

    @storage_qo_s_policy.setter
    def storage_qo_s_policy(self, value: Optional[pulumi.Input['StorageQoSPolicyDetailsArgs']]):
        pulumi.set(self, "storage_qo_s_policy", value)

    @property
    @pulumi.getter(name="templateDiskId")
    def template_disk_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the disk id in the template.
        """
        return pulumi.get(self, "template_disk_id")

    @template_disk_id.setter
    def template_disk_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_disk_id", value)

    @property
    @pulumi.getter(name="vhdType")
    def vhd_type(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the disk vhd type.
        """
        return pulumi.get(self, "vhd_type")

    @vhd_type.setter
    def vhd_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vhd_type", value)


@pulumi.input_type
class VirtualMachinePropertiesAvailabilitySetsArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Availability Set model
        :param pulumi.Input[str] id: Gets the ARM Id of the microsoft.scvmm/availabilitySets resource.
        :param pulumi.Input[str] name: Gets or sets the name of the availability set.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets the ARM Id of the microsoft.scvmm/availabilitySets resource.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the name of the availability set.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


