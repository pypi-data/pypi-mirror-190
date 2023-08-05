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
    'GetManagedClusterResult',
    'AwaitableGetManagedClusterResult',
    'get_managed_cluster',
    'get_managed_cluster_output',
]

@pulumi.output_type
class GetManagedClusterResult:
    """
    Managed cluster.
    """
    def __init__(__self__, aad_profile=None, addon_profiles=None, agent_pool_profiles=None, api_server_access_profile=None, auto_scaler_profile=None, auto_upgrade_profile=None, disk_encryption_set_id=None, dns_prefix=None, enable_pod_security_policy=None, enable_rbac=None, fqdn=None, id=None, identity=None, identity_profile=None, kubernetes_version=None, linux_profile=None, location=None, max_agent_pools=None, name=None, network_profile=None, node_resource_group=None, pod_identity_profile=None, power_state=None, private_fqdn=None, provisioning_state=None, service_principal_profile=None, sku=None, tags=None, type=None, windows_profile=None):
        if aad_profile and not isinstance(aad_profile, dict):
            raise TypeError("Expected argument 'aad_profile' to be a dict")
        pulumi.set(__self__, "aad_profile", aad_profile)
        if addon_profiles and not isinstance(addon_profiles, dict):
            raise TypeError("Expected argument 'addon_profiles' to be a dict")
        pulumi.set(__self__, "addon_profiles", addon_profiles)
        if agent_pool_profiles and not isinstance(agent_pool_profiles, list):
            raise TypeError("Expected argument 'agent_pool_profiles' to be a list")
        pulumi.set(__self__, "agent_pool_profiles", agent_pool_profiles)
        if api_server_access_profile and not isinstance(api_server_access_profile, dict):
            raise TypeError("Expected argument 'api_server_access_profile' to be a dict")
        pulumi.set(__self__, "api_server_access_profile", api_server_access_profile)
        if auto_scaler_profile and not isinstance(auto_scaler_profile, dict):
            raise TypeError("Expected argument 'auto_scaler_profile' to be a dict")
        pulumi.set(__self__, "auto_scaler_profile", auto_scaler_profile)
        if auto_upgrade_profile and not isinstance(auto_upgrade_profile, dict):
            raise TypeError("Expected argument 'auto_upgrade_profile' to be a dict")
        pulumi.set(__self__, "auto_upgrade_profile", auto_upgrade_profile)
        if disk_encryption_set_id and not isinstance(disk_encryption_set_id, str):
            raise TypeError("Expected argument 'disk_encryption_set_id' to be a str")
        pulumi.set(__self__, "disk_encryption_set_id", disk_encryption_set_id)
        if dns_prefix and not isinstance(dns_prefix, str):
            raise TypeError("Expected argument 'dns_prefix' to be a str")
        pulumi.set(__self__, "dns_prefix", dns_prefix)
        if enable_pod_security_policy and not isinstance(enable_pod_security_policy, bool):
            raise TypeError("Expected argument 'enable_pod_security_policy' to be a bool")
        pulumi.set(__self__, "enable_pod_security_policy", enable_pod_security_policy)
        if enable_rbac and not isinstance(enable_rbac, bool):
            raise TypeError("Expected argument 'enable_rbac' to be a bool")
        pulumi.set(__self__, "enable_rbac", enable_rbac)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if identity_profile and not isinstance(identity_profile, dict):
            raise TypeError("Expected argument 'identity_profile' to be a dict")
        pulumi.set(__self__, "identity_profile", identity_profile)
        if kubernetes_version and not isinstance(kubernetes_version, str):
            raise TypeError("Expected argument 'kubernetes_version' to be a str")
        pulumi.set(__self__, "kubernetes_version", kubernetes_version)
        if linux_profile and not isinstance(linux_profile, dict):
            raise TypeError("Expected argument 'linux_profile' to be a dict")
        pulumi.set(__self__, "linux_profile", linux_profile)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if max_agent_pools and not isinstance(max_agent_pools, int):
            raise TypeError("Expected argument 'max_agent_pools' to be a int")
        pulumi.set(__self__, "max_agent_pools", max_agent_pools)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_profile and not isinstance(network_profile, dict):
            raise TypeError("Expected argument 'network_profile' to be a dict")
        pulumi.set(__self__, "network_profile", network_profile)
        if node_resource_group and not isinstance(node_resource_group, str):
            raise TypeError("Expected argument 'node_resource_group' to be a str")
        pulumi.set(__self__, "node_resource_group", node_resource_group)
        if pod_identity_profile and not isinstance(pod_identity_profile, dict):
            raise TypeError("Expected argument 'pod_identity_profile' to be a dict")
        pulumi.set(__self__, "pod_identity_profile", pod_identity_profile)
        if power_state and not isinstance(power_state, dict):
            raise TypeError("Expected argument 'power_state' to be a dict")
        pulumi.set(__self__, "power_state", power_state)
        if private_fqdn and not isinstance(private_fqdn, str):
            raise TypeError("Expected argument 'private_fqdn' to be a str")
        pulumi.set(__self__, "private_fqdn", private_fqdn)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_principal_profile and not isinstance(service_principal_profile, dict):
            raise TypeError("Expected argument 'service_principal_profile' to be a dict")
        pulumi.set(__self__, "service_principal_profile", service_principal_profile)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if windows_profile and not isinstance(windows_profile, dict):
            raise TypeError("Expected argument 'windows_profile' to be a dict")
        pulumi.set(__self__, "windows_profile", windows_profile)

    @property
    @pulumi.getter(name="aadProfile")
    def aad_profile(self) -> Optional['outputs.ManagedClusterAADProfileResponse']:
        """
        Profile of Azure Active Directory configuration.
        """
        return pulumi.get(self, "aad_profile")

    @property
    @pulumi.getter(name="addonProfiles")
    def addon_profiles(self) -> Optional[Mapping[str, 'outputs.ManagedClusterAddonProfileResponse']]:
        """
        Profile of managed cluster add-on.
        """
        return pulumi.get(self, "addon_profiles")

    @property
    @pulumi.getter(name="agentPoolProfiles")
    def agent_pool_profiles(self) -> Optional[Sequence['outputs.ManagedClusterAgentPoolProfileResponse']]:
        """
        Properties of the agent pool.
        """
        return pulumi.get(self, "agent_pool_profiles")

    @property
    @pulumi.getter(name="apiServerAccessProfile")
    def api_server_access_profile(self) -> Optional['outputs.ManagedClusterAPIServerAccessProfileResponse']:
        """
        Access profile for managed cluster API server.
        """
        return pulumi.get(self, "api_server_access_profile")

    @property
    @pulumi.getter(name="autoScalerProfile")
    def auto_scaler_profile(self) -> Optional['outputs.ManagedClusterPropertiesResponseAutoScalerProfile']:
        """
        Parameters to be applied to the cluster-autoscaler when enabled
        """
        return pulumi.get(self, "auto_scaler_profile")

    @property
    @pulumi.getter(name="autoUpgradeProfile")
    def auto_upgrade_profile(self) -> Optional['outputs.ManagedClusterAutoUpgradeProfileResponse']:
        """
        Profile of auto upgrade configuration.
        """
        return pulumi.get(self, "auto_upgrade_profile")

    @property
    @pulumi.getter(name="diskEncryptionSetID")
    def disk_encryption_set_id(self) -> Optional[str]:
        """
        ResourceId of the disk encryption set to use for enabling encryption at rest.
        """
        return pulumi.get(self, "disk_encryption_set_id")

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> Optional[str]:
        """
        DNS prefix specified when creating the managed cluster.
        """
        return pulumi.get(self, "dns_prefix")

    @property
    @pulumi.getter(name="enablePodSecurityPolicy")
    def enable_pod_security_policy(self) -> Optional[bool]:
        """
        (DEPRECATING) Whether to enable Kubernetes pod security policy (preview). This feature is set for removal on October 15th, 2020. Learn more at aka.ms/aks/azpodpolicy.
        """
        return pulumi.get(self, "enable_pod_security_policy")

    @property
    @pulumi.getter(name="enableRBAC")
    def enable_rbac(self) -> Optional[bool]:
        """
        Whether to enable Kubernetes Role-Based Access Control.
        """
        return pulumi.get(self, "enable_rbac")

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        FQDN for the master pool.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ManagedClusterIdentityResponse']:
        """
        The identity of the managed cluster, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="identityProfile")
    def identity_profile(self) -> Optional[Mapping[str, 'outputs.ManagedClusterPropertiesResponseIdentityProfile']]:
        """
        Identities associated with the cluster.
        """
        return pulumi.get(self, "identity_profile")

    @property
    @pulumi.getter(name="kubernetesVersion")
    def kubernetes_version(self) -> Optional[str]:
        """
        Version of Kubernetes specified when creating the managed cluster.
        """
        return pulumi.get(self, "kubernetes_version")

    @property
    @pulumi.getter(name="linuxProfile")
    def linux_profile(self) -> Optional['outputs.ContainerServiceLinuxProfileResponse']:
        """
        Profile for Linux VMs in the container service cluster.
        """
        return pulumi.get(self, "linux_profile")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxAgentPools")
    def max_agent_pools(self) -> int:
        """
        The max number of agent pools for the managed cluster.
        """
        return pulumi.get(self, "max_agent_pools")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional['outputs.ContainerServiceNetworkProfileResponse']:
        """
        Profile of network configuration.
        """
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="nodeResourceGroup")
    def node_resource_group(self) -> Optional[str]:
        """
        Name of the resource group containing agent pool nodes.
        """
        return pulumi.get(self, "node_resource_group")

    @property
    @pulumi.getter(name="podIdentityProfile")
    def pod_identity_profile(self) -> Optional['outputs.ManagedClusterPodIdentityProfileResponse']:
        """
        Profile of managed cluster pod identity.
        """
        return pulumi.get(self, "pod_identity_profile")

    @property
    @pulumi.getter(name="powerState")
    def power_state(self) -> 'outputs.PowerStateResponse':
        """
        Represents the Power State of the cluster
        """
        return pulumi.get(self, "power_state")

    @property
    @pulumi.getter(name="privateFQDN")
    def private_fqdn(self) -> str:
        """
        FQDN of private cluster.
        """
        return pulumi.get(self, "private_fqdn")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="servicePrincipalProfile")
    def service_principal_profile(self) -> Optional['outputs.ManagedClusterServicePrincipalProfileResponse']:
        """
        Information about a service principal identity for the cluster to use for manipulating Azure APIs.
        """
        return pulumi.get(self, "service_principal_profile")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ManagedClusterSKUResponse']:
        """
        The managed cluster SKU.
        """
        return pulumi.get(self, "sku")

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
    @pulumi.getter(name="windowsProfile")
    def windows_profile(self) -> Optional['outputs.ManagedClusterWindowsProfileResponse']:
        """
        Profile for Windows VMs in the container service cluster.
        """
        return pulumi.get(self, "windows_profile")


class AwaitableGetManagedClusterResult(GetManagedClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedClusterResult(
            aad_profile=self.aad_profile,
            addon_profiles=self.addon_profiles,
            agent_pool_profiles=self.agent_pool_profiles,
            api_server_access_profile=self.api_server_access_profile,
            auto_scaler_profile=self.auto_scaler_profile,
            auto_upgrade_profile=self.auto_upgrade_profile,
            disk_encryption_set_id=self.disk_encryption_set_id,
            dns_prefix=self.dns_prefix,
            enable_pod_security_policy=self.enable_pod_security_policy,
            enable_rbac=self.enable_rbac,
            fqdn=self.fqdn,
            id=self.id,
            identity=self.identity,
            identity_profile=self.identity_profile,
            kubernetes_version=self.kubernetes_version,
            linux_profile=self.linux_profile,
            location=self.location,
            max_agent_pools=self.max_agent_pools,
            name=self.name,
            network_profile=self.network_profile,
            node_resource_group=self.node_resource_group,
            pod_identity_profile=self.pod_identity_profile,
            power_state=self.power_state,
            private_fqdn=self.private_fqdn,
            provisioning_state=self.provisioning_state,
            service_principal_profile=self.service_principal_profile,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            windows_profile=self.windows_profile)


def get_managed_cluster(resource_group_name: Optional[str] = None,
                        resource_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedClusterResult:
    """
    Managed cluster.


    :param str resource_group_name: The name of the resource group.
    :param str resource_name: The name of the managed cluster resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:containerservice/v20201201:getManagedCluster', __args__, opts=opts, typ=GetManagedClusterResult).value

    return AwaitableGetManagedClusterResult(
        aad_profile=__ret__.aad_profile,
        addon_profiles=__ret__.addon_profiles,
        agent_pool_profiles=__ret__.agent_pool_profiles,
        api_server_access_profile=__ret__.api_server_access_profile,
        auto_scaler_profile=__ret__.auto_scaler_profile,
        auto_upgrade_profile=__ret__.auto_upgrade_profile,
        disk_encryption_set_id=__ret__.disk_encryption_set_id,
        dns_prefix=__ret__.dns_prefix,
        enable_pod_security_policy=__ret__.enable_pod_security_policy,
        enable_rbac=__ret__.enable_rbac,
        fqdn=__ret__.fqdn,
        id=__ret__.id,
        identity=__ret__.identity,
        identity_profile=__ret__.identity_profile,
        kubernetes_version=__ret__.kubernetes_version,
        linux_profile=__ret__.linux_profile,
        location=__ret__.location,
        max_agent_pools=__ret__.max_agent_pools,
        name=__ret__.name,
        network_profile=__ret__.network_profile,
        node_resource_group=__ret__.node_resource_group,
        pod_identity_profile=__ret__.pod_identity_profile,
        power_state=__ret__.power_state,
        private_fqdn=__ret__.private_fqdn,
        provisioning_state=__ret__.provisioning_state,
        service_principal_profile=__ret__.service_principal_profile,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        windows_profile=__ret__.windows_profile)


@_utilities.lift_output_func(get_managed_cluster)
def get_managed_cluster_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                               resource_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedClusterResult]:
    """
    Managed cluster.


    :param str resource_group_name: The name of the resource group.
    :param str resource_name: The name of the managed cluster resource.
    """
    ...
