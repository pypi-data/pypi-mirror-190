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
    'GetRegistryResult',
    'AwaitableGetRegistryResult',
    'get_registry',
    'get_registry_output',
]

@pulumi.output_type
class GetRegistryResult:
    """
    An object that represents a container registry.
    """
    def __init__(__self__, admin_user_enabled=None, anonymous_pull_enabled=None, creation_date=None, data_endpoint_enabled=None, data_endpoint_host_names=None, encryption=None, id=None, identity=None, location=None, login_server=None, name=None, network_rule_bypass_options=None, network_rule_set=None, policies=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, sku=None, status=None, system_data=None, tags=None, type=None, zone_redundancy=None):
        if admin_user_enabled and not isinstance(admin_user_enabled, bool):
            raise TypeError("Expected argument 'admin_user_enabled' to be a bool")
        pulumi.set(__self__, "admin_user_enabled", admin_user_enabled)
        if anonymous_pull_enabled and not isinstance(anonymous_pull_enabled, bool):
            raise TypeError("Expected argument 'anonymous_pull_enabled' to be a bool")
        pulumi.set(__self__, "anonymous_pull_enabled", anonymous_pull_enabled)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if data_endpoint_enabled and not isinstance(data_endpoint_enabled, bool):
            raise TypeError("Expected argument 'data_endpoint_enabled' to be a bool")
        pulumi.set(__self__, "data_endpoint_enabled", data_endpoint_enabled)
        if data_endpoint_host_names and not isinstance(data_endpoint_host_names, list):
            raise TypeError("Expected argument 'data_endpoint_host_names' to be a list")
        pulumi.set(__self__, "data_endpoint_host_names", data_endpoint_host_names)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if login_server and not isinstance(login_server, str):
            raise TypeError("Expected argument 'login_server' to be a str")
        pulumi.set(__self__, "login_server", login_server)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_rule_bypass_options and not isinstance(network_rule_bypass_options, str):
            raise TypeError("Expected argument 'network_rule_bypass_options' to be a str")
        pulumi.set(__self__, "network_rule_bypass_options", network_rule_bypass_options)
        if network_rule_set and not isinstance(network_rule_set, dict):
            raise TypeError("Expected argument 'network_rule_set' to be a dict")
        pulumi.set(__self__, "network_rule_set", network_rule_set)
        if policies and not isinstance(policies, dict):
            raise TypeError("Expected argument 'policies' to be a dict")
        pulumi.set(__self__, "policies", policies)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if zone_redundancy and not isinstance(zone_redundancy, str):
            raise TypeError("Expected argument 'zone_redundancy' to be a str")
        pulumi.set(__self__, "zone_redundancy", zone_redundancy)

    @property
    @pulumi.getter(name="adminUserEnabled")
    def admin_user_enabled(self) -> Optional[bool]:
        """
        The value that indicates whether the admin user is enabled.
        """
        return pulumi.get(self, "admin_user_enabled")

    @property
    @pulumi.getter(name="anonymousPullEnabled")
    def anonymous_pull_enabled(self) -> Optional[bool]:
        """
        Enables registry-wide pull from unauthenticated clients. It's in preview and available in the Standard and Premium service tiers.
        """
        return pulumi.get(self, "anonymous_pull_enabled")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of the container registry in ISO8601 format.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="dataEndpointEnabled")
    def data_endpoint_enabled(self) -> Optional[bool]:
        """
        Enable a single data endpoint per region for serving data.
        """
        return pulumi.get(self, "data_endpoint_enabled")

    @property
    @pulumi.getter(name="dataEndpointHostNames")
    def data_endpoint_host_names(self) -> Sequence[str]:
        """
        List of host names that will serve data when dataEndpointEnabled is true.
        """
        return pulumi.get(self, "data_endpoint_host_names")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionPropertyResponse']:
        """
        The encryption settings of container registry.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityPropertiesResponse']:
        """
        The identity of the container registry.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="loginServer")
    def login_server(self) -> str:
        """
        The URL that can be used to log into the container registry.
        """
        return pulumi.get(self, "login_server")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkRuleBypassOptions")
    def network_rule_bypass_options(self) -> Optional[str]:
        """
        Whether to allow trusted Azure services to access a network restricted registry.
        """
        return pulumi.get(self, "network_rule_bypass_options")

    @property
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> Optional['outputs.NetworkRuleSetResponse']:
        """
        The network rule set for a container registry.
        """
        return pulumi.get(self, "network_rule_set")

    @property
    @pulumi.getter
    def policies(self) -> Optional['outputs.PoliciesResponse']:
        """
        The policies for a container registry.
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        List of private endpoint connections for a container registry.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        Whether or not public network access is allowed for the container registry.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The SKU of the container registry.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> 'outputs.StatusResponse':
        """
        The status of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "status")

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
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneRedundancy")
    def zone_redundancy(self) -> Optional[str]:
        """
        Whether or not zone redundancy is enabled for this container registry
        """
        return pulumi.get(self, "zone_redundancy")


class AwaitableGetRegistryResult(GetRegistryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistryResult(
            admin_user_enabled=self.admin_user_enabled,
            anonymous_pull_enabled=self.anonymous_pull_enabled,
            creation_date=self.creation_date,
            data_endpoint_enabled=self.data_endpoint_enabled,
            data_endpoint_host_names=self.data_endpoint_host_names,
            encryption=self.encryption,
            id=self.id,
            identity=self.identity,
            location=self.location,
            login_server=self.login_server,
            name=self.name,
            network_rule_bypass_options=self.network_rule_bypass_options,
            network_rule_set=self.network_rule_set,
            policies=self.policies,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_network_access=self.public_network_access,
            sku=self.sku,
            status=self.status,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            zone_redundancy=self.zone_redundancy)


def get_registry(registry_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistryResult:
    """
    An object that represents a container registry.


    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    __args__ = dict()
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:containerregistry/v20220201preview:getRegistry', __args__, opts=opts, typ=GetRegistryResult).value

    return AwaitableGetRegistryResult(
        admin_user_enabled=__ret__.admin_user_enabled,
        anonymous_pull_enabled=__ret__.anonymous_pull_enabled,
        creation_date=__ret__.creation_date,
        data_endpoint_enabled=__ret__.data_endpoint_enabled,
        data_endpoint_host_names=__ret__.data_endpoint_host_names,
        encryption=__ret__.encryption,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        login_server=__ret__.login_server,
        name=__ret__.name,
        network_rule_bypass_options=__ret__.network_rule_bypass_options,
        network_rule_set=__ret__.network_rule_set,
        policies=__ret__.policies,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_network_access=__ret__.public_network_access,
        sku=__ret__.sku,
        status=__ret__.status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        zone_redundancy=__ret__.zone_redundancy)


@_utilities.lift_output_func(get_registry)
def get_registry_output(registry_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegistryResult]:
    """
    An object that represents a container registry.


    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    ...
