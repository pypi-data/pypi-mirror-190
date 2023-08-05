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
    'GetWebAppSlotResult',
    'AwaitableGetWebAppSlotResult',
    'get_web_app_slot',
    'get_web_app_slot_output',
]

@pulumi.output_type
class GetWebAppSlotResult:
    """
    A web app, a mobile app backend, or an API app.
    """
    def __init__(__self__, availability_state=None, client_affinity_enabled=None, client_cert_enabled=None, client_cert_exclusion_paths=None, client_cert_mode=None, container_size=None, custom_domain_verification_id=None, daily_memory_time_quota=None, default_host_name=None, enabled=None, enabled_host_names=None, host_name_ssl_states=None, host_names=None, host_names_disabled=None, hosting_environment_profile=None, https_only=None, hyper_v=None, id=None, identity=None, in_progress_operation_id=None, is_default_container=None, is_xenon=None, kind=None, last_modified_time_utc=None, location=None, max_number_of_workers=None, name=None, outbound_ip_addresses=None, possible_outbound_ip_addresses=None, redundancy_mode=None, repository_site_name=None, reserved=None, resource_group=None, scm_site_also_stopped=None, server_farm_id=None, site_config=None, slot_swap_status=None, state=None, suspended_till=None, system_data=None, tags=None, target_swap_slot=None, traffic_manager_host_names=None, type=None, usage_state=None):
        if availability_state and not isinstance(availability_state, str):
            raise TypeError("Expected argument 'availability_state' to be a str")
        pulumi.set(__self__, "availability_state", availability_state)
        if client_affinity_enabled and not isinstance(client_affinity_enabled, bool):
            raise TypeError("Expected argument 'client_affinity_enabled' to be a bool")
        pulumi.set(__self__, "client_affinity_enabled", client_affinity_enabled)
        if client_cert_enabled and not isinstance(client_cert_enabled, bool):
            raise TypeError("Expected argument 'client_cert_enabled' to be a bool")
        pulumi.set(__self__, "client_cert_enabled", client_cert_enabled)
        if client_cert_exclusion_paths and not isinstance(client_cert_exclusion_paths, str):
            raise TypeError("Expected argument 'client_cert_exclusion_paths' to be a str")
        pulumi.set(__self__, "client_cert_exclusion_paths", client_cert_exclusion_paths)
        if client_cert_mode and not isinstance(client_cert_mode, str):
            raise TypeError("Expected argument 'client_cert_mode' to be a str")
        pulumi.set(__self__, "client_cert_mode", client_cert_mode)
        if container_size and not isinstance(container_size, int):
            raise TypeError("Expected argument 'container_size' to be a int")
        pulumi.set(__self__, "container_size", container_size)
        if custom_domain_verification_id and not isinstance(custom_domain_verification_id, str):
            raise TypeError("Expected argument 'custom_domain_verification_id' to be a str")
        pulumi.set(__self__, "custom_domain_verification_id", custom_domain_verification_id)
        if daily_memory_time_quota and not isinstance(daily_memory_time_quota, int):
            raise TypeError("Expected argument 'daily_memory_time_quota' to be a int")
        pulumi.set(__self__, "daily_memory_time_quota", daily_memory_time_quota)
        if default_host_name and not isinstance(default_host_name, str):
            raise TypeError("Expected argument 'default_host_name' to be a str")
        pulumi.set(__self__, "default_host_name", default_host_name)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if enabled_host_names and not isinstance(enabled_host_names, list):
            raise TypeError("Expected argument 'enabled_host_names' to be a list")
        pulumi.set(__self__, "enabled_host_names", enabled_host_names)
        if host_name_ssl_states and not isinstance(host_name_ssl_states, list):
            raise TypeError("Expected argument 'host_name_ssl_states' to be a list")
        pulumi.set(__self__, "host_name_ssl_states", host_name_ssl_states)
        if host_names and not isinstance(host_names, list):
            raise TypeError("Expected argument 'host_names' to be a list")
        pulumi.set(__self__, "host_names", host_names)
        if host_names_disabled and not isinstance(host_names_disabled, bool):
            raise TypeError("Expected argument 'host_names_disabled' to be a bool")
        pulumi.set(__self__, "host_names_disabled", host_names_disabled)
        if hosting_environment_profile and not isinstance(hosting_environment_profile, dict):
            raise TypeError("Expected argument 'hosting_environment_profile' to be a dict")
        pulumi.set(__self__, "hosting_environment_profile", hosting_environment_profile)
        if https_only and not isinstance(https_only, bool):
            raise TypeError("Expected argument 'https_only' to be a bool")
        pulumi.set(__self__, "https_only", https_only)
        if hyper_v and not isinstance(hyper_v, bool):
            raise TypeError("Expected argument 'hyper_v' to be a bool")
        pulumi.set(__self__, "hyper_v", hyper_v)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if in_progress_operation_id and not isinstance(in_progress_operation_id, str):
            raise TypeError("Expected argument 'in_progress_operation_id' to be a str")
        pulumi.set(__self__, "in_progress_operation_id", in_progress_operation_id)
        if is_default_container and not isinstance(is_default_container, bool):
            raise TypeError("Expected argument 'is_default_container' to be a bool")
        pulumi.set(__self__, "is_default_container", is_default_container)
        if is_xenon and not isinstance(is_xenon, bool):
            raise TypeError("Expected argument 'is_xenon' to be a bool")
        pulumi.set(__self__, "is_xenon", is_xenon)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_modified_time_utc and not isinstance(last_modified_time_utc, str):
            raise TypeError("Expected argument 'last_modified_time_utc' to be a str")
        pulumi.set(__self__, "last_modified_time_utc", last_modified_time_utc)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if max_number_of_workers and not isinstance(max_number_of_workers, int):
            raise TypeError("Expected argument 'max_number_of_workers' to be a int")
        pulumi.set(__self__, "max_number_of_workers", max_number_of_workers)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if outbound_ip_addresses and not isinstance(outbound_ip_addresses, str):
            raise TypeError("Expected argument 'outbound_ip_addresses' to be a str")
        pulumi.set(__self__, "outbound_ip_addresses", outbound_ip_addresses)
        if possible_outbound_ip_addresses and not isinstance(possible_outbound_ip_addresses, str):
            raise TypeError("Expected argument 'possible_outbound_ip_addresses' to be a str")
        pulumi.set(__self__, "possible_outbound_ip_addresses", possible_outbound_ip_addresses)
        if redundancy_mode and not isinstance(redundancy_mode, str):
            raise TypeError("Expected argument 'redundancy_mode' to be a str")
        pulumi.set(__self__, "redundancy_mode", redundancy_mode)
        if repository_site_name and not isinstance(repository_site_name, str):
            raise TypeError("Expected argument 'repository_site_name' to be a str")
        pulumi.set(__self__, "repository_site_name", repository_site_name)
        if reserved and not isinstance(reserved, bool):
            raise TypeError("Expected argument 'reserved' to be a bool")
        pulumi.set(__self__, "reserved", reserved)
        if resource_group and not isinstance(resource_group, str):
            raise TypeError("Expected argument 'resource_group' to be a str")
        pulumi.set(__self__, "resource_group", resource_group)
        if scm_site_also_stopped and not isinstance(scm_site_also_stopped, bool):
            raise TypeError("Expected argument 'scm_site_also_stopped' to be a bool")
        pulumi.set(__self__, "scm_site_also_stopped", scm_site_also_stopped)
        if server_farm_id and not isinstance(server_farm_id, str):
            raise TypeError("Expected argument 'server_farm_id' to be a str")
        pulumi.set(__self__, "server_farm_id", server_farm_id)
        if site_config and not isinstance(site_config, dict):
            raise TypeError("Expected argument 'site_config' to be a dict")
        pulumi.set(__self__, "site_config", site_config)
        if slot_swap_status and not isinstance(slot_swap_status, dict):
            raise TypeError("Expected argument 'slot_swap_status' to be a dict")
        pulumi.set(__self__, "slot_swap_status", slot_swap_status)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if suspended_till and not isinstance(suspended_till, str):
            raise TypeError("Expected argument 'suspended_till' to be a str")
        pulumi.set(__self__, "suspended_till", suspended_till)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_swap_slot and not isinstance(target_swap_slot, str):
            raise TypeError("Expected argument 'target_swap_slot' to be a str")
        pulumi.set(__self__, "target_swap_slot", target_swap_slot)
        if traffic_manager_host_names and not isinstance(traffic_manager_host_names, list):
            raise TypeError("Expected argument 'traffic_manager_host_names' to be a list")
        pulumi.set(__self__, "traffic_manager_host_names", traffic_manager_host_names)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if usage_state and not isinstance(usage_state, str):
            raise TypeError("Expected argument 'usage_state' to be a str")
        pulumi.set(__self__, "usage_state", usage_state)

    @property
    @pulumi.getter(name="availabilityState")
    def availability_state(self) -> str:
        """
        Management information availability state for the app.
        """
        return pulumi.get(self, "availability_state")

    @property
    @pulumi.getter(name="clientAffinityEnabled")
    def client_affinity_enabled(self) -> Optional[bool]:
        """
        <code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests in the same session to the same instance. Default is <code>true</code>.
        """
        return pulumi.get(self, "client_affinity_enabled")

    @property
    @pulumi.getter(name="clientCertEnabled")
    def client_cert_enabled(self) -> Optional[bool]:
        """
        <code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is <code>false</code>.
        """
        return pulumi.get(self, "client_cert_enabled")

    @property
    @pulumi.getter(name="clientCertExclusionPaths")
    def client_cert_exclusion_paths(self) -> Optional[str]:
        """
        client certificate authentication comma-separated exclusion paths
        """
        return pulumi.get(self, "client_cert_exclusion_paths")

    @property
    @pulumi.getter(name="clientCertMode")
    def client_cert_mode(self) -> Optional[str]:
        """
        This composes with ClientCertEnabled setting.
        - ClientCertEnabled: false means ClientCert is ignored.
        - ClientCertEnabled: true and ClientCertMode: Required means ClientCert is required.
        - ClientCertEnabled: true and ClientCertMode: Optional means ClientCert is optional or accepted.
        """
        return pulumi.get(self, "client_cert_mode")

    @property
    @pulumi.getter(name="containerSize")
    def container_size(self) -> Optional[int]:
        """
        Size of the function container.
        """
        return pulumi.get(self, "container_size")

    @property
    @pulumi.getter(name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> Optional[str]:
        """
        Unique identifier that verifies the custom domains assigned to the app. Customer will add this id to a txt record for verification.
        """
        return pulumi.get(self, "custom_domain_verification_id")

    @property
    @pulumi.getter(name="dailyMemoryTimeQuota")
    def daily_memory_time_quota(self) -> Optional[int]:
        """
        Maximum allowed daily memory-time quota (applicable on dynamic apps only).
        """
        return pulumi.get(self, "daily_memory_time_quota")

    @property
    @pulumi.getter(name="defaultHostName")
    def default_host_name(self) -> str:
        """
        Default hostname of the app. Read-only.
        """
        return pulumi.get(self, "default_host_name")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        <code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app offline).
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="enabledHostNames")
    def enabled_host_names(self) -> Sequence[str]:
        """
        Enabled hostnames for the app.Hostnames need to be assigned (see HostNames) AND enabled. Otherwise,
        the app is not served on those hostnames.
        """
        return pulumi.get(self, "enabled_host_names")

    @property
    @pulumi.getter(name="hostNameSslStates")
    def host_name_ssl_states(self) -> Optional[Sequence['outputs.HostNameSslStateResponse']]:
        """
        Hostname SSL states are used to manage the SSL bindings for app's hostnames.
        """
        return pulumi.get(self, "host_name_ssl_states")

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> Sequence[str]:
        """
        Hostnames associated with the app.
        """
        return pulumi.get(self, "host_names")

    @property
    @pulumi.getter(name="hostNamesDisabled")
    def host_names_disabled(self) -> Optional[bool]:
        """
        <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
         If <code>true</code>, the app is only accessible via API management process.
        """
        return pulumi.get(self, "host_names_disabled")

    @property
    @pulumi.getter(name="hostingEnvironmentProfile")
    def hosting_environment_profile(self) -> Optional['outputs.HostingEnvironmentProfileResponse']:
        """
        App Service Environment to use for the app.
        """
        return pulumi.get(self, "hosting_environment_profile")

    @property
    @pulumi.getter(name="httpsOnly")
    def https_only(self) -> Optional[bool]:
        """
        HttpsOnly: configures a web site to accept only https requests. Issues redirect for
        http requests
        """
        return pulumi.get(self, "https_only")

    @property
    @pulumi.getter(name="hyperV")
    def hyper_v(self) -> Optional[bool]:
        """
        Hyper-V sandbox.
        """
        return pulumi.get(self, "hyper_v")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ManagedServiceIdentityResponse']:
        """
        Managed service identity.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="inProgressOperationId")
    def in_progress_operation_id(self) -> str:
        """
        Specifies an operation id if this site has a pending operation.
        """
        return pulumi.get(self, "in_progress_operation_id")

    @property
    @pulumi.getter(name="isDefaultContainer")
    def is_default_container(self) -> bool:
        """
        <code>true</code> if the app is a default container; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "is_default_container")

    @property
    @pulumi.getter(name="isXenon")
    def is_xenon(self) -> Optional[bool]:
        """
        Obsolete: Hyper-V sandbox.
        """
        return pulumi.get(self, "is_xenon")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedTimeUtc")
    def last_modified_time_utc(self) -> str:
        """
        Last time the app was modified, in UTC. Read-only.
        """
        return pulumi.get(self, "last_modified_time_utc")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxNumberOfWorkers")
    def max_number_of_workers(self) -> int:
        """
        Maximum number of workers.
        This only applies to Functions container.
        """
        return pulumi.get(self, "max_number_of_workers")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> str:
        """
        List of IP addresses that the app uses for outbound connections (e.g. database access). Includes VIPs from tenants that site can be hosted with current settings. Read-only.
        """
        return pulumi.get(self, "outbound_ip_addresses")

    @property
    @pulumi.getter(name="possibleOutboundIpAddresses")
    def possible_outbound_ip_addresses(self) -> str:
        """
        List of IP addresses that the app uses for outbound connections (e.g. database access). Includes VIPs from all tenants except dataComponent. Read-only.
        """
        return pulumi.get(self, "possible_outbound_ip_addresses")

    @property
    @pulumi.getter(name="redundancyMode")
    def redundancy_mode(self) -> Optional[str]:
        """
        Site redundancy mode
        """
        return pulumi.get(self, "redundancy_mode")

    @property
    @pulumi.getter(name="repositorySiteName")
    def repository_site_name(self) -> str:
        """
        Name of the repository site.
        """
        return pulumi.get(self, "repository_site_name")

    @property
    @pulumi.getter
    def reserved(self) -> Optional[bool]:
        """
        <code>true</code> if reserved; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "reserved")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> str:
        """
        Name of the resource group the app belongs to. Read-only.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter(name="scmSiteAlsoStopped")
    def scm_site_also_stopped(self) -> Optional[bool]:
        """
        <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
        """
        return pulumi.get(self, "scm_site_also_stopped")

    @property
    @pulumi.getter(name="serverFarmId")
    def server_farm_id(self) -> Optional[str]:
        """
        Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        """
        return pulumi.get(self, "server_farm_id")

    @property
    @pulumi.getter(name="siteConfig")
    def site_config(self) -> Optional['outputs.SiteConfigResponse']:
        """
        Configuration of the app.
        """
        return pulumi.get(self, "site_config")

    @property
    @pulumi.getter(name="slotSwapStatus")
    def slot_swap_status(self) -> 'outputs.SlotSwapStatusResponse':
        """
        Status of the last deployment slot swap operation.
        """
        return pulumi.get(self, "slot_swap_status")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the app.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="suspendedTill")
    def suspended_till(self) -> str:
        """
        App suspended till in case memory-time quota is exceeded.
        """
        return pulumi.get(self, "suspended_till")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
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
    @pulumi.getter(name="targetSwapSlot")
    def target_swap_slot(self) -> str:
        """
        Specifies which deployment slot this app will swap into. Read-only.
        """
        return pulumi.get(self, "target_swap_slot")

    @property
    @pulumi.getter(name="trafficManagerHostNames")
    def traffic_manager_host_names(self) -> Sequence[str]:
        """
        Azure Traffic Manager hostnames associated with the app. Read-only.
        """
        return pulumi.get(self, "traffic_manager_host_names")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usageState")
    def usage_state(self) -> str:
        """
        State indicating whether the app has exceeded its quota usage. Read-only.
        """
        return pulumi.get(self, "usage_state")


class AwaitableGetWebAppSlotResult(GetWebAppSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppSlotResult(
            availability_state=self.availability_state,
            client_affinity_enabled=self.client_affinity_enabled,
            client_cert_enabled=self.client_cert_enabled,
            client_cert_exclusion_paths=self.client_cert_exclusion_paths,
            client_cert_mode=self.client_cert_mode,
            container_size=self.container_size,
            custom_domain_verification_id=self.custom_domain_verification_id,
            daily_memory_time_quota=self.daily_memory_time_quota,
            default_host_name=self.default_host_name,
            enabled=self.enabled,
            enabled_host_names=self.enabled_host_names,
            host_name_ssl_states=self.host_name_ssl_states,
            host_names=self.host_names,
            host_names_disabled=self.host_names_disabled,
            hosting_environment_profile=self.hosting_environment_profile,
            https_only=self.https_only,
            hyper_v=self.hyper_v,
            id=self.id,
            identity=self.identity,
            in_progress_operation_id=self.in_progress_operation_id,
            is_default_container=self.is_default_container,
            is_xenon=self.is_xenon,
            kind=self.kind,
            last_modified_time_utc=self.last_modified_time_utc,
            location=self.location,
            max_number_of_workers=self.max_number_of_workers,
            name=self.name,
            outbound_ip_addresses=self.outbound_ip_addresses,
            possible_outbound_ip_addresses=self.possible_outbound_ip_addresses,
            redundancy_mode=self.redundancy_mode,
            repository_site_name=self.repository_site_name,
            reserved=self.reserved,
            resource_group=self.resource_group,
            scm_site_also_stopped=self.scm_site_also_stopped,
            server_farm_id=self.server_farm_id,
            site_config=self.site_config,
            slot_swap_status=self.slot_swap_status,
            state=self.state,
            suspended_till=self.suspended_till,
            system_data=self.system_data,
            tags=self.tags,
            target_swap_slot=self.target_swap_slot,
            traffic_manager_host_names=self.traffic_manager_host_names,
            type=self.type,
            usage_state=self.usage_state)


def get_web_app_slot(name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     slot: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppSlotResult:
    """
    A web app, a mobile app backend, or an API app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. By default, this API returns the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20200901:getWebAppSlot', __args__, opts=opts, typ=GetWebAppSlotResult).value

    return AwaitableGetWebAppSlotResult(
        availability_state=__ret__.availability_state,
        client_affinity_enabled=__ret__.client_affinity_enabled,
        client_cert_enabled=__ret__.client_cert_enabled,
        client_cert_exclusion_paths=__ret__.client_cert_exclusion_paths,
        client_cert_mode=__ret__.client_cert_mode,
        container_size=__ret__.container_size,
        custom_domain_verification_id=__ret__.custom_domain_verification_id,
        daily_memory_time_quota=__ret__.daily_memory_time_quota,
        default_host_name=__ret__.default_host_name,
        enabled=__ret__.enabled,
        enabled_host_names=__ret__.enabled_host_names,
        host_name_ssl_states=__ret__.host_name_ssl_states,
        host_names=__ret__.host_names,
        host_names_disabled=__ret__.host_names_disabled,
        hosting_environment_profile=__ret__.hosting_environment_profile,
        https_only=__ret__.https_only,
        hyper_v=__ret__.hyper_v,
        id=__ret__.id,
        identity=__ret__.identity,
        in_progress_operation_id=__ret__.in_progress_operation_id,
        is_default_container=__ret__.is_default_container,
        is_xenon=__ret__.is_xenon,
        kind=__ret__.kind,
        last_modified_time_utc=__ret__.last_modified_time_utc,
        location=__ret__.location,
        max_number_of_workers=__ret__.max_number_of_workers,
        name=__ret__.name,
        outbound_ip_addresses=__ret__.outbound_ip_addresses,
        possible_outbound_ip_addresses=__ret__.possible_outbound_ip_addresses,
        redundancy_mode=__ret__.redundancy_mode,
        repository_site_name=__ret__.repository_site_name,
        reserved=__ret__.reserved,
        resource_group=__ret__.resource_group,
        scm_site_also_stopped=__ret__.scm_site_also_stopped,
        server_farm_id=__ret__.server_farm_id,
        site_config=__ret__.site_config,
        slot_swap_status=__ret__.slot_swap_status,
        state=__ret__.state,
        suspended_till=__ret__.suspended_till,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        target_swap_slot=__ret__.target_swap_slot,
        traffic_manager_host_names=__ret__.traffic_manager_host_names,
        type=__ret__.type,
        usage_state=__ret__.usage_state)


@_utilities.lift_output_func(get_web_app_slot)
def get_web_app_slot_output(name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            slot: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppSlotResult]:
    """
    A web app, a mobile app backend, or an API app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. By default, this API returns the production slot.
    """
    ...
