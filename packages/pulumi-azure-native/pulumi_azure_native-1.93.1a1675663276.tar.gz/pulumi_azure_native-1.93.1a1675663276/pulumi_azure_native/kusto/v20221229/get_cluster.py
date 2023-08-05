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
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    """
    Class representing a Kusto cluster.
    """
    def __init__(__self__, accepted_audiences=None, allowed_fqdn_list=None, allowed_ip_range_list=None, data_ingestion_uri=None, enable_auto_stop=None, enable_disk_encryption=None, enable_double_encryption=None, enable_purge=None, enable_streaming_ingest=None, engine_type=None, etag=None, id=None, identity=None, key_vault_properties=None, language_extensions=None, location=None, name=None, optimized_autoscale=None, private_endpoint_connections=None, provisioning_state=None, public_ip_type=None, public_network_access=None, restrict_outbound_network_access=None, sku=None, state=None, state_reason=None, system_data=None, tags=None, trusted_external_tenants=None, type=None, uri=None, virtual_network_configuration=None, zones=None):
        if accepted_audiences and not isinstance(accepted_audiences, list):
            raise TypeError("Expected argument 'accepted_audiences' to be a list")
        pulumi.set(__self__, "accepted_audiences", accepted_audiences)
        if allowed_fqdn_list and not isinstance(allowed_fqdn_list, list):
            raise TypeError("Expected argument 'allowed_fqdn_list' to be a list")
        pulumi.set(__self__, "allowed_fqdn_list", allowed_fqdn_list)
        if allowed_ip_range_list and not isinstance(allowed_ip_range_list, list):
            raise TypeError("Expected argument 'allowed_ip_range_list' to be a list")
        pulumi.set(__self__, "allowed_ip_range_list", allowed_ip_range_list)
        if data_ingestion_uri and not isinstance(data_ingestion_uri, str):
            raise TypeError("Expected argument 'data_ingestion_uri' to be a str")
        pulumi.set(__self__, "data_ingestion_uri", data_ingestion_uri)
        if enable_auto_stop and not isinstance(enable_auto_stop, bool):
            raise TypeError("Expected argument 'enable_auto_stop' to be a bool")
        pulumi.set(__self__, "enable_auto_stop", enable_auto_stop)
        if enable_disk_encryption and not isinstance(enable_disk_encryption, bool):
            raise TypeError("Expected argument 'enable_disk_encryption' to be a bool")
        pulumi.set(__self__, "enable_disk_encryption", enable_disk_encryption)
        if enable_double_encryption and not isinstance(enable_double_encryption, bool):
            raise TypeError("Expected argument 'enable_double_encryption' to be a bool")
        pulumi.set(__self__, "enable_double_encryption", enable_double_encryption)
        if enable_purge and not isinstance(enable_purge, bool):
            raise TypeError("Expected argument 'enable_purge' to be a bool")
        pulumi.set(__self__, "enable_purge", enable_purge)
        if enable_streaming_ingest and not isinstance(enable_streaming_ingest, bool):
            raise TypeError("Expected argument 'enable_streaming_ingest' to be a bool")
        pulumi.set(__self__, "enable_streaming_ingest", enable_streaming_ingest)
        if engine_type and not isinstance(engine_type, str):
            raise TypeError("Expected argument 'engine_type' to be a str")
        pulumi.set(__self__, "engine_type", engine_type)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if key_vault_properties and not isinstance(key_vault_properties, dict):
            raise TypeError("Expected argument 'key_vault_properties' to be a dict")
        pulumi.set(__self__, "key_vault_properties", key_vault_properties)
        if language_extensions and not isinstance(language_extensions, dict):
            raise TypeError("Expected argument 'language_extensions' to be a dict")
        pulumi.set(__self__, "language_extensions", language_extensions)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if optimized_autoscale and not isinstance(optimized_autoscale, dict):
            raise TypeError("Expected argument 'optimized_autoscale' to be a dict")
        pulumi.set(__self__, "optimized_autoscale", optimized_autoscale)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_ip_type and not isinstance(public_ip_type, str):
            raise TypeError("Expected argument 'public_ip_type' to be a str")
        pulumi.set(__self__, "public_ip_type", public_ip_type)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if restrict_outbound_network_access and not isinstance(restrict_outbound_network_access, str):
            raise TypeError("Expected argument 'restrict_outbound_network_access' to be a str")
        pulumi.set(__self__, "restrict_outbound_network_access", restrict_outbound_network_access)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if state_reason and not isinstance(state_reason, str):
            raise TypeError("Expected argument 'state_reason' to be a str")
        pulumi.set(__self__, "state_reason", state_reason)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if trusted_external_tenants and not isinstance(trusted_external_tenants, list):
            raise TypeError("Expected argument 'trusted_external_tenants' to be a list")
        pulumi.set(__self__, "trusted_external_tenants", trusted_external_tenants)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if uri and not isinstance(uri, str):
            raise TypeError("Expected argument 'uri' to be a str")
        pulumi.set(__self__, "uri", uri)
        if virtual_network_configuration and not isinstance(virtual_network_configuration, dict):
            raise TypeError("Expected argument 'virtual_network_configuration' to be a dict")
        pulumi.set(__self__, "virtual_network_configuration", virtual_network_configuration)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="acceptedAudiences")
    def accepted_audiences(self) -> Optional[Sequence['outputs.AcceptedAudiencesResponse']]:
        """
        The cluster's accepted audiences.
        """
        return pulumi.get(self, "accepted_audiences")

    @property
    @pulumi.getter(name="allowedFqdnList")
    def allowed_fqdn_list(self) -> Optional[Sequence[str]]:
        """
        List of allowed FQDNs(Fully Qualified Domain Name) for egress from Cluster.
        """
        return pulumi.get(self, "allowed_fqdn_list")

    @property
    @pulumi.getter(name="allowedIpRangeList")
    def allowed_ip_range_list(self) -> Optional[Sequence[str]]:
        """
        The list of ips in the format of CIDR allowed to connect to the cluster.
        """
        return pulumi.get(self, "allowed_ip_range_list")

    @property
    @pulumi.getter(name="dataIngestionUri")
    def data_ingestion_uri(self) -> str:
        """
        The cluster data ingestion URI.
        """
        return pulumi.get(self, "data_ingestion_uri")

    @property
    @pulumi.getter(name="enableAutoStop")
    def enable_auto_stop(self) -> Optional[bool]:
        """
        A boolean value that indicates if the cluster could be automatically stopped (due to lack of data or no activity for many days).
        """
        return pulumi.get(self, "enable_auto_stop")

    @property
    @pulumi.getter(name="enableDiskEncryption")
    def enable_disk_encryption(self) -> Optional[bool]:
        """
        A boolean value that indicates if the cluster's disks are encrypted.
        """
        return pulumi.get(self, "enable_disk_encryption")

    @property
    @pulumi.getter(name="enableDoubleEncryption")
    def enable_double_encryption(self) -> Optional[bool]:
        """
        A boolean value that indicates if double encryption is enabled.
        """
        return pulumi.get(self, "enable_double_encryption")

    @property
    @pulumi.getter(name="enablePurge")
    def enable_purge(self) -> Optional[bool]:
        """
        A boolean value that indicates if the purge operations are enabled.
        """
        return pulumi.get(self, "enable_purge")

    @property
    @pulumi.getter(name="enableStreamingIngest")
    def enable_streaming_ingest(self) -> Optional[bool]:
        """
        A boolean value that indicates if the streaming ingest is enabled.
        """
        return pulumi.get(self, "enable_streaming_ingest")

    @property
    @pulumi.getter(name="engineType")
    def engine_type(self) -> Optional[str]:
        """
        The engine type
        """
        return pulumi.get(self, "engine_type")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity of the cluster, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional['outputs.KeyVaultPropertiesResponse']:
        """
        KeyVault properties for the cluster encryption.
        """
        return pulumi.get(self, "key_vault_properties")

    @property
    @pulumi.getter(name="languageExtensions")
    def language_extensions(self) -> Optional['outputs.LanguageExtensionsListResponse']:
        """
        List of the cluster's language extensions.
        """
        return pulumi.get(self, "language_extensions")

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
    @pulumi.getter(name="optimizedAutoscale")
    def optimized_autoscale(self) -> Optional['outputs.OptimizedAutoscaleResponse']:
        """
        Optimized auto scale definition.
        """
        return pulumi.get(self, "optimized_autoscale")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        A list of private endpoint connections.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioned state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPType")
    def public_ip_type(self) -> Optional[str]:
        """
        Indicates what public IP type to create - IPv4 (default), or DualStack (both IPv4 and IPv6)
        """
        return pulumi.get(self, "public_ip_type")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        Public network access to the cluster is enabled by default. When disabled, only private endpoint connection to the cluster is allowed
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="restrictOutboundNetworkAccess")
    def restrict_outbound_network_access(self) -> Optional[str]:
        """
        Whether or not to restrict outbound network access.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'
        """
        return pulumi.get(self, "restrict_outbound_network_access")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.AzureSkuResponse':
        """
        The SKU of the cluster.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the resource.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateReason")
    def state_reason(self) -> str:
        """
        The reason for the cluster's current state.
        """
        return pulumi.get(self, "state_reason")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
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
    @pulumi.getter(name="trustedExternalTenants")
    def trusted_external_tenants(self) -> Optional[Sequence['outputs.TrustedExternalTenantResponse']]:
        """
        The cluster's external tenants.
        """
        return pulumi.get(self, "trusted_external_tenants")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The cluster URI.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="virtualNetworkConfiguration")
    def virtual_network_configuration(self) -> Optional['outputs.VirtualNetworkConfigurationResponse']:
        """
        Virtual network definition.
        """
        return pulumi.get(self, "virtual_network_configuration")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        The availability zones of the cluster.
        """
        return pulumi.get(self, "zones")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            accepted_audiences=self.accepted_audiences,
            allowed_fqdn_list=self.allowed_fqdn_list,
            allowed_ip_range_list=self.allowed_ip_range_list,
            data_ingestion_uri=self.data_ingestion_uri,
            enable_auto_stop=self.enable_auto_stop,
            enable_disk_encryption=self.enable_disk_encryption,
            enable_double_encryption=self.enable_double_encryption,
            enable_purge=self.enable_purge,
            enable_streaming_ingest=self.enable_streaming_ingest,
            engine_type=self.engine_type,
            etag=self.etag,
            id=self.id,
            identity=self.identity,
            key_vault_properties=self.key_vault_properties,
            language_extensions=self.language_extensions,
            location=self.location,
            name=self.name,
            optimized_autoscale=self.optimized_autoscale,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_ip_type=self.public_ip_type,
            public_network_access=self.public_network_access,
            restrict_outbound_network_access=self.restrict_outbound_network_access,
            sku=self.sku,
            state=self.state,
            state_reason=self.state_reason,
            system_data=self.system_data,
            tags=self.tags,
            trusted_external_tenants=self.trusted_external_tenants,
            type=self.type,
            uri=self.uri,
            virtual_network_configuration=self.virtual_network_configuration,
            zones=self.zones)


def get_cluster(cluster_name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Class representing a Kusto cluster.


    :param str cluster_name: The name of the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:kusto/v20221229:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        accepted_audiences=__ret__.accepted_audiences,
        allowed_fqdn_list=__ret__.allowed_fqdn_list,
        allowed_ip_range_list=__ret__.allowed_ip_range_list,
        data_ingestion_uri=__ret__.data_ingestion_uri,
        enable_auto_stop=__ret__.enable_auto_stop,
        enable_disk_encryption=__ret__.enable_disk_encryption,
        enable_double_encryption=__ret__.enable_double_encryption,
        enable_purge=__ret__.enable_purge,
        enable_streaming_ingest=__ret__.enable_streaming_ingest,
        engine_type=__ret__.engine_type,
        etag=__ret__.etag,
        id=__ret__.id,
        identity=__ret__.identity,
        key_vault_properties=__ret__.key_vault_properties,
        language_extensions=__ret__.language_extensions,
        location=__ret__.location,
        name=__ret__.name,
        optimized_autoscale=__ret__.optimized_autoscale,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_ip_type=__ret__.public_ip_type,
        public_network_access=__ret__.public_network_access,
        restrict_outbound_network_access=__ret__.restrict_outbound_network_access,
        sku=__ret__.sku,
        state=__ret__.state,
        state_reason=__ret__.state_reason,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        trusted_external_tenants=__ret__.trusted_external_tenants,
        type=__ret__.type,
        uri=__ret__.uri,
        virtual_network_configuration=__ret__.virtual_network_configuration,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_cluster)
def get_cluster_output(cluster_name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Class representing a Kusto cluster.


    :param str cluster_name: The name of the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    ...
