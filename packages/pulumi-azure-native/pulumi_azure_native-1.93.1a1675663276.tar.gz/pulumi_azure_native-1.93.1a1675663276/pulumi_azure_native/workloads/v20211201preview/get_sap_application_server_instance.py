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
    'GetSAPApplicationServerInstanceResult',
    'AwaitableGetSAPApplicationServerInstanceResult',
    'get_sap_application_server_instance',
    'get_sap_application_server_instance_output',
]

@pulumi.output_type
class GetSAPApplicationServerInstanceResult:
    """
    Define the SAP Application Server Instance resource.
    """
    def __init__(__self__, errors=None, gateway_port=None, health=None, hostname=None, icm_http_port=None, icm_https_port=None, id=None, instance_no=None, ip_address=None, kernel_patch=None, kernel_version=None, location=None, name=None, provisioning_state=None, status=None, storage_details=None, subnet=None, system_data=None, tags=None, type=None, virtual_machine_id=None):
        if errors and not isinstance(errors, dict):
            raise TypeError("Expected argument 'errors' to be a dict")
        pulumi.set(__self__, "errors", errors)
        if gateway_port and not isinstance(gateway_port, float):
            raise TypeError("Expected argument 'gateway_port' to be a float")
        pulumi.set(__self__, "gateway_port", gateway_port)
        if health and not isinstance(health, str):
            raise TypeError("Expected argument 'health' to be a str")
        pulumi.set(__self__, "health", health)
        if hostname and not isinstance(hostname, str):
            raise TypeError("Expected argument 'hostname' to be a str")
        pulumi.set(__self__, "hostname", hostname)
        if icm_http_port and not isinstance(icm_http_port, float):
            raise TypeError("Expected argument 'icm_http_port' to be a float")
        pulumi.set(__self__, "icm_http_port", icm_http_port)
        if icm_https_port and not isinstance(icm_https_port, float):
            raise TypeError("Expected argument 'icm_https_port' to be a float")
        pulumi.set(__self__, "icm_https_port", icm_https_port)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_no and not isinstance(instance_no, str):
            raise TypeError("Expected argument 'instance_no' to be a str")
        pulumi.set(__self__, "instance_no", instance_no)
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, "ip_address", ip_address)
        if kernel_patch and not isinstance(kernel_patch, str):
            raise TypeError("Expected argument 'kernel_patch' to be a str")
        pulumi.set(__self__, "kernel_patch", kernel_patch)
        if kernel_version and not isinstance(kernel_version, str):
            raise TypeError("Expected argument 'kernel_version' to be a str")
        pulumi.set(__self__, "kernel_version", kernel_version)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if storage_details and not isinstance(storage_details, list):
            raise TypeError("Expected argument 'storage_details' to be a list")
        pulumi.set(__self__, "storage_details", storage_details)
        if subnet and not isinstance(subnet, str):
            raise TypeError("Expected argument 'subnet' to be a str")
        pulumi.set(__self__, "subnet", subnet)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if virtual_machine_id and not isinstance(virtual_machine_id, str):
            raise TypeError("Expected argument 'virtual_machine_id' to be a str")
        pulumi.set(__self__, "virtual_machine_id", virtual_machine_id)

    @property
    @pulumi.getter
    def errors(self) -> 'outputs.SAPVirtualInstanceErrorResponse':
        """
        Defines the Application Instance errors.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter(name="gatewayPort")
    def gateway_port(self) -> float:
        """
        Application server instance gateway Port.
        """
        return pulumi.get(self, "gateway_port")

    @property
    @pulumi.getter
    def health(self) -> str:
        """
        Defines the health of SAP Instances.
        """
        return pulumi.get(self, "health")

    @property
    @pulumi.getter
    def hostname(self) -> str:
        """
        Application server instance SAP hostname.
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter(name="icmHttpPort")
    def icm_http_port(self) -> float:
        """
        Application server instance ICM HTTP Port.
        """
        return pulumi.get(self, "icm_http_port")

    @property
    @pulumi.getter(name="icmHttpsPort")
    def icm_https_port(self) -> float:
        """
        Application server instance ICM HTTPS Port.
        """
        return pulumi.get(self, "icm_https_port")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceNo")
    def instance_no(self) -> str:
        """
        Application server Instance Number.
        """
        return pulumi.get(self, "instance_no")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
         Application server instance SAP IP Address.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="kernelPatch")
    def kernel_patch(self) -> str:
        """
        Application server instance SAP Kernel Patch level.
        """
        return pulumi.get(self, "kernel_patch")

    @property
    @pulumi.getter(name="kernelVersion")
    def kernel_version(self) -> str:
        """
         Application server instance SAP Kernel Version.
        """
        return pulumi.get(self, "kernel_version")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

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
        Defines the provisioning states.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Defines the SAP Instance status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageDetails")
    def storage_details(self) -> Sequence['outputs.StorageInformationResponse']:
        """
        Storage details of all the Storage Accounts attached to the App Virtual Machine. For e.g. NFS on AFS Shared Storage.
        """
        return pulumi.get(self, "storage_details")

    @property
    @pulumi.getter
    def subnet(self) -> str:
        """
        Application server Subnet.
        """
        return pulumi.get(self, "subnet")

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
    @pulumi.getter(name="virtualMachineId")
    def virtual_machine_id(self) -> str:
        """
        The virtual machine.
        """
        return pulumi.get(self, "virtual_machine_id")


class AwaitableGetSAPApplicationServerInstanceResult(GetSAPApplicationServerInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSAPApplicationServerInstanceResult(
            errors=self.errors,
            gateway_port=self.gateway_port,
            health=self.health,
            hostname=self.hostname,
            icm_http_port=self.icm_http_port,
            icm_https_port=self.icm_https_port,
            id=self.id,
            instance_no=self.instance_no,
            ip_address=self.ip_address,
            kernel_patch=self.kernel_patch,
            kernel_version=self.kernel_version,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            status=self.status,
            storage_details=self.storage_details,
            subnet=self.subnet,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            virtual_machine_id=self.virtual_machine_id)


def get_sap_application_server_instance(application_instance_name: Optional[str] = None,
                                        resource_group_name: Optional[str] = None,
                                        sap_virtual_instance_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSAPApplicationServerInstanceResult:
    """
    Define the SAP Application Server Instance resource.


    :param str application_instance_name: The name of SAP Application Server instance resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sap_virtual_instance_name: The name of the Virtual Instances for SAP solutions resource
    """
    __args__ = dict()
    __args__['applicationInstanceName'] = application_instance_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['sapVirtualInstanceName'] = sap_virtual_instance_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:workloads/v20211201preview:getSAPApplicationServerInstance', __args__, opts=opts, typ=GetSAPApplicationServerInstanceResult).value

    return AwaitableGetSAPApplicationServerInstanceResult(
        errors=__ret__.errors,
        gateway_port=__ret__.gateway_port,
        health=__ret__.health,
        hostname=__ret__.hostname,
        icm_http_port=__ret__.icm_http_port,
        icm_https_port=__ret__.icm_https_port,
        id=__ret__.id,
        instance_no=__ret__.instance_no,
        ip_address=__ret__.ip_address,
        kernel_patch=__ret__.kernel_patch,
        kernel_version=__ret__.kernel_version,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        status=__ret__.status,
        storage_details=__ret__.storage_details,
        subnet=__ret__.subnet,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        virtual_machine_id=__ret__.virtual_machine_id)


@_utilities.lift_output_func(get_sap_application_server_instance)
def get_sap_application_server_instance_output(application_instance_name: Optional[pulumi.Input[str]] = None,
                                               resource_group_name: Optional[pulumi.Input[str]] = None,
                                               sap_virtual_instance_name: Optional[pulumi.Input[str]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSAPApplicationServerInstanceResult]:
    """
    Define the SAP Application Server Instance resource.


    :param str application_instance_name: The name of SAP Application Server instance resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sap_virtual_instance_name: The name of the Virtual Instances for SAP solutions resource
    """
    ...
