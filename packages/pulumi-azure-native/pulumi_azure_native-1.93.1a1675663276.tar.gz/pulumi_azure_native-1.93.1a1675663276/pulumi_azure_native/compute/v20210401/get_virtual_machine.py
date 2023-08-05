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

__all__ = [
    'GetVirtualMachineResult',
    'AwaitableGetVirtualMachineResult',
    'get_virtual_machine',
    'get_virtual_machine_output',
]

@pulumi.output_type
class GetVirtualMachineResult:
    """
    Describes a Virtual Machine.
    """
    def __init__(__self__, additional_capabilities=None, availability_set=None, billing_profile=None, capacity_reservation=None, diagnostics_profile=None, eviction_policy=None, extended_location=None, extensions_time_budget=None, hardware_profile=None, host=None, host_group=None, id=None, identity=None, instance_view=None, license_type=None, location=None, name=None, network_profile=None, os_profile=None, plan=None, platform_fault_domain=None, priority=None, provisioning_state=None, proximity_placement_group=None, resources=None, scheduled_events_profile=None, security_profile=None, storage_profile=None, tags=None, type=None, user_data=None, virtual_machine_scale_set=None, vm_id=None, zones=None):
        if additional_capabilities and not isinstance(additional_capabilities, dict):
            raise TypeError("Expected argument 'additional_capabilities' to be a dict")
        pulumi.set(__self__, "additional_capabilities", additional_capabilities)
        if availability_set and not isinstance(availability_set, dict):
            raise TypeError("Expected argument 'availability_set' to be a dict")
        pulumi.set(__self__, "availability_set", availability_set)
        if billing_profile and not isinstance(billing_profile, dict):
            raise TypeError("Expected argument 'billing_profile' to be a dict")
        pulumi.set(__self__, "billing_profile", billing_profile)
        if capacity_reservation and not isinstance(capacity_reservation, dict):
            raise TypeError("Expected argument 'capacity_reservation' to be a dict")
        pulumi.set(__self__, "capacity_reservation", capacity_reservation)
        if diagnostics_profile and not isinstance(diagnostics_profile, dict):
            raise TypeError("Expected argument 'diagnostics_profile' to be a dict")
        pulumi.set(__self__, "diagnostics_profile", diagnostics_profile)
        if eviction_policy and not isinstance(eviction_policy, str):
            raise TypeError("Expected argument 'eviction_policy' to be a str")
        pulumi.set(__self__, "eviction_policy", eviction_policy)
        if extended_location and not isinstance(extended_location, dict):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, "extended_location", extended_location)
        if extensions_time_budget and not isinstance(extensions_time_budget, str):
            raise TypeError("Expected argument 'extensions_time_budget' to be a str")
        pulumi.set(__self__, "extensions_time_budget", extensions_time_budget)
        if hardware_profile and not isinstance(hardware_profile, dict):
            raise TypeError("Expected argument 'hardware_profile' to be a dict")
        pulumi.set(__self__, "hardware_profile", hardware_profile)
        if host and not isinstance(host, dict):
            raise TypeError("Expected argument 'host' to be a dict")
        pulumi.set(__self__, "host", host)
        if host_group and not isinstance(host_group, dict):
            raise TypeError("Expected argument 'host_group' to be a dict")
        pulumi.set(__self__, "host_group", host_group)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if instance_view and not isinstance(instance_view, dict):
            raise TypeError("Expected argument 'instance_view' to be a dict")
        pulumi.set(__self__, "instance_view", instance_view)
        if license_type and not isinstance(license_type, str):
            raise TypeError("Expected argument 'license_type' to be a str")
        pulumi.set(__self__, "license_type", license_type)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_profile and not isinstance(network_profile, dict):
            raise TypeError("Expected argument 'network_profile' to be a dict")
        pulumi.set(__self__, "network_profile", network_profile)
        if os_profile and not isinstance(os_profile, dict):
            raise TypeError("Expected argument 'os_profile' to be a dict")
        pulumi.set(__self__, "os_profile", os_profile)
        if plan and not isinstance(plan, dict):
            raise TypeError("Expected argument 'plan' to be a dict")
        pulumi.set(__self__, "plan", plan)
        if platform_fault_domain and not isinstance(platform_fault_domain, int):
            raise TypeError("Expected argument 'platform_fault_domain' to be a int")
        pulumi.set(__self__, "platform_fault_domain", platform_fault_domain)
        if priority and not isinstance(priority, str):
            raise TypeError("Expected argument 'priority' to be a str")
        pulumi.set(__self__, "priority", priority)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if proximity_placement_group and not isinstance(proximity_placement_group, dict):
            raise TypeError("Expected argument 'proximity_placement_group' to be a dict")
        pulumi.set(__self__, "proximity_placement_group", proximity_placement_group)
        if resources and not isinstance(resources, list):
            raise TypeError("Expected argument 'resources' to be a list")
        pulumi.set(__self__, "resources", resources)
        if scheduled_events_profile and not isinstance(scheduled_events_profile, dict):
            raise TypeError("Expected argument 'scheduled_events_profile' to be a dict")
        pulumi.set(__self__, "scheduled_events_profile", scheduled_events_profile)
        if security_profile and not isinstance(security_profile, dict):
            raise TypeError("Expected argument 'security_profile' to be a dict")
        pulumi.set(__self__, "security_profile", security_profile)
        if storage_profile and not isinstance(storage_profile, dict):
            raise TypeError("Expected argument 'storage_profile' to be a dict")
        pulumi.set(__self__, "storage_profile", storage_profile)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_data and not isinstance(user_data, str):
            raise TypeError("Expected argument 'user_data' to be a str")
        pulumi.set(__self__, "user_data", user_data)
        if virtual_machine_scale_set and not isinstance(virtual_machine_scale_set, dict):
            raise TypeError("Expected argument 'virtual_machine_scale_set' to be a dict")
        pulumi.set(__self__, "virtual_machine_scale_set", virtual_machine_scale_set)
        if vm_id and not isinstance(vm_id, str):
            raise TypeError("Expected argument 'vm_id' to be a str")
        pulumi.set(__self__, "vm_id", vm_id)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="additionalCapabilities")
    def additional_capabilities(self) -> Optional['outputs.AdditionalCapabilitiesResponse']:
        """
        Specifies additional capabilities enabled or disabled on the virtual machine.
        """
        return pulumi.get(self, "additional_capabilities")

    @property
    @pulumi.getter(name="availabilitySet")
    def availability_set(self) -> Optional['outputs.SubResourceResponse']:
        """
        Specifies information about the availability set that the virtual machine should be assigned to. Virtual machines specified in the same availability set are allocated to different nodes to maximize availability. For more information about availability sets, see [Availability sets overview](https://docs.microsoft.com/azure/virtual-machines/availability-set-overview). <br><br> For more information on Azure planned maintenance, see [Maintenance and updates for Virtual Machines in Azure](https://docs.microsoft.com/azure/virtual-machines/maintenance-and-updates) <br><br> Currently, a VM can only be added to availability set at creation time. The availability set to which the VM is being added should be under the same resource group as the availability set resource. An existing VM cannot be added to an availability set. <br><br>This property cannot exist along with a non-null properties.virtualMachineScaleSet reference.
        """
        return pulumi.get(self, "availability_set")

    @property
    @pulumi.getter(name="billingProfile")
    def billing_profile(self) -> Optional['outputs.BillingProfileResponse']:
        """
        Specifies the billing related details of a Azure Spot virtual machine. <br><br>Minimum api-version: 2019-03-01.
        """
        return pulumi.get(self, "billing_profile")

    @property
    @pulumi.getter(name="capacityReservation")
    def capacity_reservation(self) -> Optional['outputs.CapacityReservationProfileResponse']:
        """
        Specifies information about the capacity reservation that is used to allocate virtual machine. <br><br>Minimum api-version: 2021-04-01.
        """
        return pulumi.get(self, "capacity_reservation")

    @property
    @pulumi.getter(name="diagnosticsProfile")
    def diagnostics_profile(self) -> Optional['outputs.DiagnosticsProfileResponse']:
        """
        Specifies the boot diagnostic settings state. <br><br>Minimum api-version: 2015-06-15.
        """
        return pulumi.get(self, "diagnostics_profile")

    @property
    @pulumi.getter(name="evictionPolicy")
    def eviction_policy(self) -> Optional[str]:
        """
        Specifies the eviction policy for the Azure Spot virtual machine and Azure Spot scale set. <br><br>For Azure Spot virtual machines, both 'Deallocate' and 'Delete' are supported and the minimum api-version is 2019-03-01. <br><br>For Azure Spot scale sets, both 'Deallocate' and 'Delete' are supported and the minimum api-version is 2017-10-30-preview.
        """
        return pulumi.get(self, "eviction_policy")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> Optional['outputs.ExtendedLocationResponse']:
        """
        The extended location of the Virtual Machine.
        """
        return pulumi.get(self, "extended_location")

    @property
    @pulumi.getter(name="extensionsTimeBudget")
    def extensions_time_budget(self) -> Optional[str]:
        """
        Specifies the time alloted for all extensions to start. The time duration should be between 15 minutes and 120 minutes (inclusive) and should be specified in ISO 8601 format. The default value is 90 minutes (PT1H30M). <br><br> Minimum api-version: 2020-06-01
        """
        return pulumi.get(self, "extensions_time_budget")

    @property
    @pulumi.getter(name="hardwareProfile")
    def hardware_profile(self) -> Optional['outputs.HardwareProfileResponse']:
        """
        Specifies the hardware settings for the virtual machine.
        """
        return pulumi.get(self, "hardware_profile")

    @property
    @pulumi.getter
    def host(self) -> Optional['outputs.SubResourceResponse']:
        """
        Specifies information about the dedicated host that the virtual machine resides in. <br><br>Minimum api-version: 2018-10-01.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter(name="hostGroup")
    def host_group(self) -> Optional['outputs.SubResourceResponse']:
        """
        Specifies information about the dedicated host group that the virtual machine resides in. <br><br>Minimum api-version: 2020-06-01. <br><br>NOTE: User cannot specify both host and hostGroup properties.
        """
        return pulumi.get(self, "host_group")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.VirtualMachineIdentityResponse']:
        """
        The identity of the virtual machine, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> 'outputs.VirtualMachineInstanceViewResponse':
        """
        The virtual machine instance view.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> Optional[str]:
        """
        Specifies that the image or disk that is being used was licensed on-premises. <br><br> Possible values for Windows Server operating system are: <br><br> Windows_Client <br><br> Windows_Server <br><br> Possible values for Linux Server operating system are: <br><br> RHEL_BYOS (for RHEL) <br><br> SLES_BYOS (for SUSE) <br><br> For more information, see [Azure Hybrid Use Benefit for Windows Server](https://docs.microsoft.com/azure/virtual-machines/windows/hybrid-use-benefit-licensing) <br><br> [Azure Hybrid Use Benefit for Linux Server](https://docs.microsoft.com/azure/virtual-machines/linux/azure-hybrid-benefit-linux) <br><br> Minimum api-version: 2015-06-15
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional['outputs.NetworkProfileResponse']:
        """
        Specifies the network interfaces of the virtual machine.
        """
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="osProfile")
    def os_profile(self) -> Optional['outputs.OSProfileResponse']:
        """
        Specifies the operating system settings used while creating the virtual machine. Some of the settings cannot be changed once VM is provisioned.
        """
        return pulumi.get(self, "os_profile")

    @property
    @pulumi.getter
    def plan(self) -> Optional['outputs.PlanResponse']:
        """
        Specifies information about the marketplace image used to create the virtual machine. This element is only used for marketplace images. Before you can use a marketplace image from an API, you must enable the image for programmatic use.  In the Azure portal, find the marketplace image that you want to use and then click **Want to deploy programmatically, Get Started ->**. Enter any required information and then click **Save**.
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter(name="platformFaultDomain")
    def platform_fault_domain(self) -> Optional[int]:
        """
        Specifies the scale set logical fault domain into which the Virtual Machine will be created. By default, the Virtual Machine will by automatically assigned to a fault domain that best maintains balance across available fault domains.<br><li>This is applicable only if the 'virtualMachineScaleSet' property of this Virtual Machine is set.<li>The Virtual Machine Scale Set that is referenced, must have 'platformFaultDomainCount' &gt; 1.<li>This property cannot be updated once the Virtual Machine is created.<li>Fault domain assignment can be viewed in the Virtual Machine Instance View.<br><br>Minimum api‐version: 2020‐12‐01
        """
        return pulumi.get(self, "platform_fault_domain")

    @property
    @pulumi.getter
    def priority(self) -> Optional[str]:
        """
        Specifies the priority for the virtual machine. <br><br>Minimum api-version: 2019-03-01
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="proximityPlacementGroup")
    def proximity_placement_group(self) -> Optional['outputs.SubResourceResponse']:
        """
        Specifies information about the proximity placement group that the virtual machine should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        """
        return pulumi.get(self, "proximity_placement_group")

    @property
    @pulumi.getter
    def resources(self) -> Sequence['outputs.VirtualMachineExtensionResponse']:
        """
        The virtual machine child extension resources.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter(name="scheduledEventsProfile")
    def scheduled_events_profile(self) -> Optional['outputs.ScheduledEventsProfileResponse']:
        """
        Specifies Scheduled Event related configurations.
        """
        return pulumi.get(self, "scheduled_events_profile")

    @property
    @pulumi.getter(name="securityProfile")
    def security_profile(self) -> Optional['outputs.SecurityProfileResponse']:
        """
        Specifies the Security related profile settings for the virtual machine.
        """
        return pulumi.get(self, "security_profile")

    @property
    @pulumi.getter(name="storageProfile")
    def storage_profile(self) -> Optional['outputs.StorageProfileResponse']:
        """
        Specifies the storage settings for the virtual machine disks.
        """
        return pulumi.get(self, "storage_profile")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userData")
    def user_data(self) -> Optional[str]:
        """
        UserData for the VM, which must be base-64 encoded. Customer should not pass any secrets in here. <br><br>Minimum api-version: 2021-03-01
        """
        return pulumi.get(self, "user_data")

    @property
    @pulumi.getter(name="virtualMachineScaleSet")
    def virtual_machine_scale_set(self) -> Optional['outputs.SubResourceResponse']:
        """
        Specifies information about the virtual machine scale set that the virtual machine should be assigned to. Virtual machines specified in the same virtual machine scale set are allocated to different nodes to maximize availability. Currently, a VM can only be added to virtual machine scale set at creation time. An existing VM cannot be added to a virtual machine scale set. <br><br>This property cannot exist along with a non-null properties.availabilitySet reference. <br><br>Minimum api‐version: 2019‐03‐01
        """
        return pulumi.get(self, "virtual_machine_scale_set")

    @property
    @pulumi.getter(name="vmId")
    def vm_id(self) -> str:
        """
        Specifies the VM unique ID which is a 128-bits identifier that is encoded and stored in all Azure IaaS VMs SMBIOS and can be read using platform BIOS commands.
        """
        return pulumi.get(self, "vm_id")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        The virtual machine zones.
        """
        return pulumi.get(self, "zones")


class AwaitableGetVirtualMachineResult(GetVirtualMachineResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineResult(
            additional_capabilities=self.additional_capabilities,
            availability_set=self.availability_set,
            billing_profile=self.billing_profile,
            capacity_reservation=self.capacity_reservation,
            diagnostics_profile=self.diagnostics_profile,
            eviction_policy=self.eviction_policy,
            extended_location=self.extended_location,
            extensions_time_budget=self.extensions_time_budget,
            hardware_profile=self.hardware_profile,
            host=self.host,
            host_group=self.host_group,
            id=self.id,
            identity=self.identity,
            instance_view=self.instance_view,
            license_type=self.license_type,
            location=self.location,
            name=self.name,
            network_profile=self.network_profile,
            os_profile=self.os_profile,
            plan=self.plan,
            platform_fault_domain=self.platform_fault_domain,
            priority=self.priority,
            provisioning_state=self.provisioning_state,
            proximity_placement_group=self.proximity_placement_group,
            resources=self.resources,
            scheduled_events_profile=self.scheduled_events_profile,
            security_profile=self.security_profile,
            storage_profile=self.storage_profile,
            tags=self.tags,
            type=self.type,
            user_data=self.user_data,
            virtual_machine_scale_set=self.virtual_machine_scale_set,
            vm_id=self.vm_id,
            zones=self.zones)


def get_virtual_machine(expand: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        vm_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMachineResult:
    """
    Describes a Virtual Machine.


    :param str expand: The expand expression to apply on the operation. 'InstanceView' retrieves a snapshot of the runtime properties of the virtual machine that is managed by the platform and can change outside of control plane operations. 'UserData' retrieves the UserData property as part of the VM model view that was provided by the user during the VM Create/Update operation.
    :param str resource_group_name: The name of the resource group.
    :param str vm_name: The name of the virtual machine.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['vmName'] = vm_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20210401:getVirtualMachine', __args__, opts=opts, typ=GetVirtualMachineResult).value

    return AwaitableGetVirtualMachineResult(
        additional_capabilities=__ret__.additional_capabilities,
        availability_set=__ret__.availability_set,
        billing_profile=__ret__.billing_profile,
        capacity_reservation=__ret__.capacity_reservation,
        diagnostics_profile=__ret__.diagnostics_profile,
        eviction_policy=__ret__.eviction_policy,
        extended_location=__ret__.extended_location,
        extensions_time_budget=__ret__.extensions_time_budget,
        hardware_profile=__ret__.hardware_profile,
        host=__ret__.host,
        host_group=__ret__.host_group,
        id=__ret__.id,
        identity=__ret__.identity,
        instance_view=__ret__.instance_view,
        license_type=__ret__.license_type,
        location=__ret__.location,
        name=__ret__.name,
        network_profile=__ret__.network_profile,
        os_profile=__ret__.os_profile,
        plan=__ret__.plan,
        platform_fault_domain=__ret__.platform_fault_domain,
        priority=__ret__.priority,
        provisioning_state=__ret__.provisioning_state,
        proximity_placement_group=__ret__.proximity_placement_group,
        resources=__ret__.resources,
        scheduled_events_profile=__ret__.scheduled_events_profile,
        security_profile=__ret__.security_profile,
        storage_profile=__ret__.storage_profile,
        tags=__ret__.tags,
        type=__ret__.type,
        user_data=__ret__.user_data,
        virtual_machine_scale_set=__ret__.virtual_machine_scale_set,
        vm_id=__ret__.vm_id,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_virtual_machine)
def get_virtual_machine_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               vm_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualMachineResult]:
    """
    Describes a Virtual Machine.


    :param str expand: The expand expression to apply on the operation. 'InstanceView' retrieves a snapshot of the runtime properties of the virtual machine that is managed by the platform and can change outside of control plane operations. 'UserData' retrieves the UserData property as part of the VM model view that was provided by the user during the VM Create/Update operation.
    :param str resource_group_name: The name of the resource group.
    :param str vm_name: The name of the virtual machine.
    """
    ...
