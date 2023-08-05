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
    'GetmonitorResult',
    'AwaitableGetmonitorResult',
    'getmonitor',
    'getmonitor_output',
]

@pulumi.output_type
class GetmonitorResult:
    """
    SAP monitor info on Azure (ARM properties and SAP monitor properties)
    """
    def __init__(__self__, app_location=None, errors=None, id=None, identity=None, location=None, log_analytics_workspace_arm_id=None, managed_resource_group_configuration=None, monitor_subnet=None, msi_arm_id=None, name=None, provisioning_state=None, routing_preference=None, storage_account_arm_id=None, system_data=None, tags=None, type=None, zone_redundancy_preference=None):
        if app_location and not isinstance(app_location, str):
            raise TypeError("Expected argument 'app_location' to be a str")
        pulumi.set(__self__, "app_location", app_location)
        if errors and not isinstance(errors, dict):
            raise TypeError("Expected argument 'errors' to be a dict")
        pulumi.set(__self__, "errors", errors)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if log_analytics_workspace_arm_id and not isinstance(log_analytics_workspace_arm_id, str):
            raise TypeError("Expected argument 'log_analytics_workspace_arm_id' to be a str")
        pulumi.set(__self__, "log_analytics_workspace_arm_id", log_analytics_workspace_arm_id)
        if managed_resource_group_configuration and not isinstance(managed_resource_group_configuration, dict):
            raise TypeError("Expected argument 'managed_resource_group_configuration' to be a dict")
        pulumi.set(__self__, "managed_resource_group_configuration", managed_resource_group_configuration)
        if monitor_subnet and not isinstance(monitor_subnet, str):
            raise TypeError("Expected argument 'monitor_subnet' to be a str")
        pulumi.set(__self__, "monitor_subnet", monitor_subnet)
        if msi_arm_id and not isinstance(msi_arm_id, str):
            raise TypeError("Expected argument 'msi_arm_id' to be a str")
        pulumi.set(__self__, "msi_arm_id", msi_arm_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if routing_preference and not isinstance(routing_preference, str):
            raise TypeError("Expected argument 'routing_preference' to be a str")
        pulumi.set(__self__, "routing_preference", routing_preference)
        if storage_account_arm_id and not isinstance(storage_account_arm_id, str):
            raise TypeError("Expected argument 'storage_account_arm_id' to be a str")
        pulumi.set(__self__, "storage_account_arm_id", storage_account_arm_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if zone_redundancy_preference and not isinstance(zone_redundancy_preference, str):
            raise TypeError("Expected argument 'zone_redundancy_preference' to be a str")
        pulumi.set(__self__, "zone_redundancy_preference", zone_redundancy_preference)

    @property
    @pulumi.getter(name="appLocation")
    def app_location(self) -> Optional[str]:
        """
        The SAP monitor resources will be deployed in the SAP monitoring region. The subnet region should be same as the SAP monitoring region.
        """
        return pulumi.get(self, "app_location")

    @property
    @pulumi.getter
    def errors(self) -> 'outputs.MonitorPropertiesResponseErrors':
        """
        Defines the SAP monitor errors.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.UserAssignedServiceIdentityResponse']:
        """
        Managed service identity (user assigned identities)
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceArmId")
    def log_analytics_workspace_arm_id(self) -> Optional[str]:
        """
        The ARM ID of the Log Analytics Workspace that is used for SAP monitoring.
        """
        return pulumi.get(self, "log_analytics_workspace_arm_id")

    @property
    @pulumi.getter(name="managedResourceGroupConfiguration")
    def managed_resource_group_configuration(self) -> Optional['outputs.ManagedRGConfigurationResponse']:
        """
        Managed resource group configuration
        """
        return pulumi.get(self, "managed_resource_group_configuration")

    @property
    @pulumi.getter(name="monitorSubnet")
    def monitor_subnet(self) -> Optional[str]:
        """
        The subnet which the SAP monitor will be deployed in
        """
        return pulumi.get(self, "monitor_subnet")

    @property
    @pulumi.getter(name="msiArmId")
    def msi_arm_id(self) -> str:
        """
        The ARM ID of the MSI used for SAP monitoring.
        """
        return pulumi.get(self, "msi_arm_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of provisioning of the SAP monitor.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="routingPreference")
    def routing_preference(self) -> Optional[str]:
        """
        Sets the routing preference of the SAP monitor. By default only RFC1918 traffic is routed to the customer VNET.
        """
        return pulumi.get(self, "routing_preference")

    @property
    @pulumi.getter(name="storageAccountArmId")
    def storage_account_arm_id(self) -> str:
        """
        The ARM ID of the Storage account used for SAP monitoring.
        """
        return pulumi.get(self, "storage_account_arm_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneRedundancyPreference")
    def zone_redundancy_preference(self) -> Optional[str]:
        """
        Sets the preference for zone redundancy on resources created for the SAP monitor. By default resources will be created which do not support zone redundancy.
        """
        return pulumi.get(self, "zone_redundancy_preference")


class AwaitableGetmonitorResult(GetmonitorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetmonitorResult(
            app_location=self.app_location,
            errors=self.errors,
            id=self.id,
            identity=self.identity,
            location=self.location,
            log_analytics_workspace_arm_id=self.log_analytics_workspace_arm_id,
            managed_resource_group_configuration=self.managed_resource_group_configuration,
            monitor_subnet=self.monitor_subnet,
            msi_arm_id=self.msi_arm_id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            routing_preference=self.routing_preference,
            storage_account_arm_id=self.storage_account_arm_id,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            zone_redundancy_preference=self.zone_redundancy_preference)


def getmonitor(monitor_name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetmonitorResult:
    """
    SAP monitor info on Azure (ARM properties and SAP monitor properties)


    :param str monitor_name: Name of the SAP monitor resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:workloads/v20221101preview:getmonitor', __args__, opts=opts, typ=GetmonitorResult).value

    return AwaitableGetmonitorResult(
        app_location=__ret__.app_location,
        errors=__ret__.errors,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        log_analytics_workspace_arm_id=__ret__.log_analytics_workspace_arm_id,
        managed_resource_group_configuration=__ret__.managed_resource_group_configuration,
        monitor_subnet=__ret__.monitor_subnet,
        msi_arm_id=__ret__.msi_arm_id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        routing_preference=__ret__.routing_preference,
        storage_account_arm_id=__ret__.storage_account_arm_id,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        zone_redundancy_preference=__ret__.zone_redundancy_preference)


@_utilities.lift_output_func(getmonitor)
def getmonitor_output(monitor_name: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetmonitorResult]:
    """
    SAP monitor info on Azure (ARM properties and SAP monitor properties)


    :param str monitor_name: Name of the SAP monitor resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
