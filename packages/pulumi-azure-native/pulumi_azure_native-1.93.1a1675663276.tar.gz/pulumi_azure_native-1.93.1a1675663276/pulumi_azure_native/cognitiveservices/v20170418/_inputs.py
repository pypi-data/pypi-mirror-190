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
    'CognitiveServicesAccountApiPropertiesArgs',
    'CognitiveServicesAccountPropertiesArgs',
    'EncryptionArgs',
    'IdentityArgs',
    'IpRuleArgs',
    'KeyVaultPropertiesArgs',
    'NetworkRuleSetArgs',
    'PrivateEndpointConnectionPropertiesArgs',
    'PrivateEndpointConnectionArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'SkuArgs',
    'UserAssignedIdentityArgs',
    'UserOwnedStorageArgs',
    'VirtualNetworkRuleArgs',
]

@pulumi.input_type
class CognitiveServicesAccountApiPropertiesArgs:
    def __init__(__self__, *,
                 aad_client_id: Optional[pulumi.Input[str]] = None,
                 aad_tenant_id: Optional[pulumi.Input[str]] = None,
                 event_hub_connection_string: Optional[pulumi.Input[str]] = None,
                 qna_azure_search_endpoint_id: Optional[pulumi.Input[str]] = None,
                 qna_azure_search_endpoint_key: Optional[pulumi.Input[str]] = None,
                 qna_runtime_endpoint: Optional[pulumi.Input[str]] = None,
                 statistics_enabled: Optional[pulumi.Input[bool]] = None,
                 storage_account_connection_string: Optional[pulumi.Input[str]] = None,
                 super_user: Optional[pulumi.Input[str]] = None,
                 website_name: Optional[pulumi.Input[str]] = None):
        """
        The api properties for special APIs.
        :param pulumi.Input[str] aad_client_id: (Metrics Advisor Only) The Azure AD Client Id (Application Id).
        :param pulumi.Input[str] aad_tenant_id: (Metrics Advisor Only) The Azure AD Tenant Id.
        :param pulumi.Input[str] event_hub_connection_string: (Personalization Only) The flag to enable statistics of Bing Search.
        :param pulumi.Input[str] qna_azure_search_endpoint_id: (QnAMaker Only) The Azure Search endpoint id of QnAMaker.
        :param pulumi.Input[str] qna_azure_search_endpoint_key: (QnAMaker Only) The Azure Search endpoint key of QnAMaker.
        :param pulumi.Input[str] qna_runtime_endpoint: (QnAMaker Only) The runtime endpoint of QnAMaker.
        :param pulumi.Input[bool] statistics_enabled: (Bing Search Only) The flag to enable statistics of Bing Search.
        :param pulumi.Input[str] storage_account_connection_string: (Personalization Only) The storage account connection string.
        :param pulumi.Input[str] super_user: (Metrics Advisor Only) The super user of Metrics Advisor.
        :param pulumi.Input[str] website_name: (Metrics Advisor Only) The website name of Metrics Advisor.
        """
        if aad_client_id is not None:
            pulumi.set(__self__, "aad_client_id", aad_client_id)
        if aad_tenant_id is not None:
            pulumi.set(__self__, "aad_tenant_id", aad_tenant_id)
        if event_hub_connection_string is not None:
            pulumi.set(__self__, "event_hub_connection_string", event_hub_connection_string)
        if qna_azure_search_endpoint_id is not None:
            pulumi.set(__self__, "qna_azure_search_endpoint_id", qna_azure_search_endpoint_id)
        if qna_azure_search_endpoint_key is not None:
            pulumi.set(__self__, "qna_azure_search_endpoint_key", qna_azure_search_endpoint_key)
        if qna_runtime_endpoint is not None:
            pulumi.set(__self__, "qna_runtime_endpoint", qna_runtime_endpoint)
        if statistics_enabled is not None:
            pulumi.set(__self__, "statistics_enabled", statistics_enabled)
        if storage_account_connection_string is not None:
            pulumi.set(__self__, "storage_account_connection_string", storage_account_connection_string)
        if super_user is not None:
            pulumi.set(__self__, "super_user", super_user)
        if website_name is not None:
            pulumi.set(__self__, "website_name", website_name)

    @property
    @pulumi.getter(name="aadClientId")
    def aad_client_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Metrics Advisor Only) The Azure AD Client Id (Application Id).
        """
        return pulumi.get(self, "aad_client_id")

    @aad_client_id.setter
    def aad_client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aad_client_id", value)

    @property
    @pulumi.getter(name="aadTenantId")
    def aad_tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Metrics Advisor Only) The Azure AD Tenant Id.
        """
        return pulumi.get(self, "aad_tenant_id")

    @aad_tenant_id.setter
    def aad_tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aad_tenant_id", value)

    @property
    @pulumi.getter(name="eventHubConnectionString")
    def event_hub_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        (Personalization Only) The flag to enable statistics of Bing Search.
        """
        return pulumi.get(self, "event_hub_connection_string")

    @event_hub_connection_string.setter
    def event_hub_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_hub_connection_string", value)

    @property
    @pulumi.getter(name="qnaAzureSearchEndpointId")
    def qna_azure_search_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        (QnAMaker Only) The Azure Search endpoint id of QnAMaker.
        """
        return pulumi.get(self, "qna_azure_search_endpoint_id")

    @qna_azure_search_endpoint_id.setter
    def qna_azure_search_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qna_azure_search_endpoint_id", value)

    @property
    @pulumi.getter(name="qnaAzureSearchEndpointKey")
    def qna_azure_search_endpoint_key(self) -> Optional[pulumi.Input[str]]:
        """
        (QnAMaker Only) The Azure Search endpoint key of QnAMaker.
        """
        return pulumi.get(self, "qna_azure_search_endpoint_key")

    @qna_azure_search_endpoint_key.setter
    def qna_azure_search_endpoint_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qna_azure_search_endpoint_key", value)

    @property
    @pulumi.getter(name="qnaRuntimeEndpoint")
    def qna_runtime_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        (QnAMaker Only) The runtime endpoint of QnAMaker.
        """
        return pulumi.get(self, "qna_runtime_endpoint")

    @qna_runtime_endpoint.setter
    def qna_runtime_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qna_runtime_endpoint", value)

    @property
    @pulumi.getter(name="statisticsEnabled")
    def statistics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        (Bing Search Only) The flag to enable statistics of Bing Search.
        """
        return pulumi.get(self, "statistics_enabled")

    @statistics_enabled.setter
    def statistics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "statistics_enabled", value)

    @property
    @pulumi.getter(name="storageAccountConnectionString")
    def storage_account_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        (Personalization Only) The storage account connection string.
        """
        return pulumi.get(self, "storage_account_connection_string")

    @storage_account_connection_string.setter
    def storage_account_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_connection_string", value)

    @property
    @pulumi.getter(name="superUser")
    def super_user(self) -> Optional[pulumi.Input[str]]:
        """
        (Metrics Advisor Only) The super user of Metrics Advisor.
        """
        return pulumi.get(self, "super_user")

    @super_user.setter
    def super_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "super_user", value)

    @property
    @pulumi.getter(name="websiteName")
    def website_name(self) -> Optional[pulumi.Input[str]]:
        """
        (Metrics Advisor Only) The website name of Metrics Advisor.
        """
        return pulumi.get(self, "website_name")

    @website_name.setter
    def website_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "website_name", value)


@pulumi.input_type
class CognitiveServicesAccountPropertiesArgs:
    def __init__(__self__, *,
                 api_properties: Optional[pulumi.Input['CognitiveServicesAccountApiPropertiesArgs']] = None,
                 custom_sub_domain_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input['EncryptionArgs']] = None,
                 network_acls: Optional[pulumi.Input['NetworkRuleSetArgs']] = None,
                 private_endpoint_connections: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 user_owned_storage: Optional[pulumi.Input[Sequence[pulumi.Input['UserOwnedStorageArgs']]]] = None):
        """
        Properties of Cognitive Services account.
        :param pulumi.Input['CognitiveServicesAccountApiPropertiesArgs'] api_properties: The api properties for special APIs.
        :param pulumi.Input[str] custom_sub_domain_name: Optional subdomain name used for token-based authentication.
        :param pulumi.Input['EncryptionArgs'] encryption: The encryption properties for this resource.
        :param pulumi.Input['NetworkRuleSetArgs'] network_acls: A collection of rules governing the accessibility from specific network locations.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]] private_endpoint_connections: The private endpoint connection associated with the Cognitive Services account.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public endpoint access is allowed for this account. Value is optional but if passed in, must be 'Enabled' or 'Disabled'
        :param pulumi.Input[Sequence[pulumi.Input['UserOwnedStorageArgs']]] user_owned_storage: The storage accounts for this resource.
        """
        if api_properties is not None:
            pulumi.set(__self__, "api_properties", api_properties)
        if custom_sub_domain_name is not None:
            pulumi.set(__self__, "custom_sub_domain_name", custom_sub_domain_name)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)
        if network_acls is not None:
            pulumi.set(__self__, "network_acls", network_acls)
        if private_endpoint_connections is not None:
            pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if user_owned_storage is not None:
            pulumi.set(__self__, "user_owned_storage", user_owned_storage)

    @property
    @pulumi.getter(name="apiProperties")
    def api_properties(self) -> Optional[pulumi.Input['CognitiveServicesAccountApiPropertiesArgs']]:
        """
        The api properties for special APIs.
        """
        return pulumi.get(self, "api_properties")

    @api_properties.setter
    def api_properties(self, value: Optional[pulumi.Input['CognitiveServicesAccountApiPropertiesArgs']]):
        pulumi.set(self, "api_properties", value)

    @property
    @pulumi.getter(name="customSubDomainName")
    def custom_sub_domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional subdomain name used for token-based authentication.
        """
        return pulumi.get(self, "custom_sub_domain_name")

    @custom_sub_domain_name.setter
    def custom_sub_domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_sub_domain_name", value)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[pulumi.Input['EncryptionArgs']]:
        """
        The encryption properties for this resource.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: Optional[pulumi.Input['EncryptionArgs']]):
        pulumi.set(self, "encryption", value)

    @property
    @pulumi.getter(name="networkAcls")
    def network_acls(self) -> Optional[pulumi.Input['NetworkRuleSetArgs']]:
        """
        A collection of rules governing the accessibility from specific network locations.
        """
        return pulumi.get(self, "network_acls")

    @network_acls.setter
    def network_acls(self, value: Optional[pulumi.Input['NetworkRuleSetArgs']]):
        pulumi.set(self, "network_acls", value)

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]]:
        """
        The private endpoint connection associated with the Cognitive Services account.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @private_endpoint_connections.setter
    def private_endpoint_connections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]]):
        pulumi.set(self, "private_endpoint_connections", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]:
        """
        Whether or not public endpoint access is allowed for this account. Value is optional but if passed in, must be 'Enabled' or 'Disabled'
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="userOwnedStorage")
    def user_owned_storage(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserOwnedStorageArgs']]]]:
        """
        The storage accounts for this resource.
        """
        return pulumi.get(self, "user_owned_storage")

    @user_owned_storage.setter
    def user_owned_storage(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserOwnedStorageArgs']]]]):
        pulumi.set(self, "user_owned_storage", value)


@pulumi.input_type
class EncryptionArgs:
    def __init__(__self__, *,
                 key_source: Optional[pulumi.Input[Union[str, 'KeySource']]] = None,
                 key_vault_properties: Optional[pulumi.Input['KeyVaultPropertiesArgs']] = None):
        """
        Properties to configure Encryption
        :param pulumi.Input[Union[str, 'KeySource']] key_source: Enumerates the possible value of keySource for Encryption
        :param pulumi.Input['KeyVaultPropertiesArgs'] key_vault_properties: Properties of KeyVault
        """
        if key_source is None:
            key_source = 'Microsoft.KeyVault'
        if key_source is not None:
            pulumi.set(__self__, "key_source", key_source)
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter(name="keySource")
    def key_source(self) -> Optional[pulumi.Input[Union[str, 'KeySource']]]:
        """
        Enumerates the possible value of keySource for Encryption
        """
        return pulumi.get(self, "key_source")

    @key_source.setter
    def key_source(self, value: Optional[pulumi.Input[Union[str, 'KeySource']]]):
        pulumi.set(self, "key_source", value)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional[pulumi.Input['KeyVaultPropertiesArgs']]:
        """
        Properties of KeyVault
        """
        return pulumi.get(self, "key_vault_properties")

    @key_vault_properties.setter
    def key_vault_properties(self, value: Optional[pulumi.Input['KeyVaultPropertiesArgs']]):
        pulumi.set(self, "key_vault_properties", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['IdentityType']] = None,
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserAssignedIdentityArgs']]]] = None):
        """
        Managed service identity.
        :param pulumi.Input['IdentityType'] type: Type of managed service identity.
        :param pulumi.Input[Mapping[str, pulumi.Input['UserAssignedIdentityArgs']]] user_assigned_identities: The list of user assigned identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}
        """
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['IdentityType']]:
        """
        Type of managed service identity.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['IdentityType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['UserAssignedIdentityArgs']]]]:
        """
        The list of user assigned identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserAssignedIdentityArgs']]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class IpRuleArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[str]):
        """
        A rule governing the accessibility from a specific ip address or ip range.
        :param pulumi.Input[str] value: An IPv4 address range in CIDR notation, such as '124.56.78.91' (simple IP address) or '124.56.78.0/24' (all addresses that start with 124.56.78).
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        An IPv4 address range in CIDR notation, such as '124.56.78.91' (simple IP address) or '124.56.78.0/24' (all addresses that start with 124.56.78).
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 key_name: Optional[pulumi.Input[str]] = None,
                 key_vault_uri: Optional[pulumi.Input[str]] = None,
                 key_version: Optional[pulumi.Input[str]] = None):
        """
        Properties to configure keyVault Properties
        :param pulumi.Input[str] key_name: Name of the Key from KeyVault
        :param pulumi.Input[str] key_vault_uri: Uri of KeyVault
        :param pulumi.Input[str] key_version: Version of the Key from KeyVault
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Key from KeyVault
        """
        return pulumi.get(self, "key_name")

    @key_name.setter
    def key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_name", value)

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Uri of KeyVault
        """
        return pulumi.get(self, "key_vault_uri")

    @key_vault_uri.setter
    def key_vault_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_uri", value)

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the Key from KeyVault
        """
        return pulumi.get(self, "key_version")

    @key_version.setter
    def key_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_version", value)


@pulumi.input_type
class NetworkRuleSetArgs:
    def __init__(__self__, *,
                 default_action: Optional[pulumi.Input[Union[str, 'NetworkRuleAction']]] = None,
                 ip_rules: Optional[pulumi.Input[Sequence[pulumi.Input['IpRuleArgs']]]] = None,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]] = None):
        """
        A set of rules governing the network accessibility.
        :param pulumi.Input[Union[str, 'NetworkRuleAction']] default_action: The default action when no rule from ipRules and from virtualNetworkRules match. This is only used after the bypass property has been evaluated.
        :param pulumi.Input[Sequence[pulumi.Input['IpRuleArgs']]] ip_rules: The list of IP address rules.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]] virtual_network_rules: The list of virtual network rules.
        """
        if default_action is not None:
            pulumi.set(__self__, "default_action", default_action)
        if ip_rules is not None:
            pulumi.set(__self__, "ip_rules", ip_rules)
        if virtual_network_rules is not None:
            pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> Optional[pulumi.Input[Union[str, 'NetworkRuleAction']]]:
        """
        The default action when no rule from ipRules and from virtualNetworkRules match. This is only used after the bypass property has been evaluated.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: Optional[pulumi.Input[Union[str, 'NetworkRuleAction']]]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="ipRules")
    def ip_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpRuleArgs']]]]:
        """
        The list of IP address rules.
        """
        return pulumi.get(self, "ip_rules")

    @ip_rules.setter
    def ip_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpRuleArgs']]]]):
        pulumi.set(self, "ip_rules", value)

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]:
        """
        The list of virtual network rules.
        """
        return pulumi.get(self, "virtual_network_rules")

    @virtual_network_rules.setter
    def virtual_network_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]):
        pulumi.set(self, "virtual_network_rules", value)


@pulumi.input_type
class PrivateEndpointConnectionPropertiesArgs:
    def __init__(__self__, *,
                 private_link_service_connection_state: pulumi.Input['PrivateLinkServiceConnectionStateArgs'],
                 group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Properties of the PrivateEndpointConnectProperties.
        :param pulumi.Input['PrivateLinkServiceConnectionStateArgs'] private_link_service_connection_state: A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: The private link resource group ids.
        """
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        if group_ids is not None:
            pulumi.set(__self__, "group_ids", group_ids)

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> pulumi.Input['PrivateLinkServiceConnectionStateArgs']:
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: pulumi.Input['PrivateLinkServiceConnectionStateArgs']):
        pulumi.set(self, "private_link_service_connection_state", value)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The private link resource group ids.
        """
        return pulumi.get(self, "group_ids")

    @group_ids.setter
    def group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_ids", value)


@pulumi.input_type
class PrivateEndpointConnectionArgs:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']] = None):
        """
        The Private Endpoint Connection resource.
        :param pulumi.Input[str] location: The location of the private endpoint connection
        :param pulumi.Input['PrivateEndpointConnectionPropertiesArgs'] properties: Resource properties.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the private endpoint connection
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']]:
        """
        Resource properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']]):
        pulumi.set(self, "properties", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str]):
        """
        The SKU of the cognitive services account.
        :param pulumi.Input[str] name: Gets or sets the sku name. Required for account creation, optional for update.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Gets or sets the sku name. Required for account creation, optional for update.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class UserAssignedIdentityArgs:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None):
        """
        User-assigned managed identity.
        :param pulumi.Input[str] client_id: Client App Id associated with this identity.
        :param pulumi.Input[str] principal_id: Azure Active Directory principal ID associated with this Identity.
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        Client App Id associated with this identity.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        Azure Active Directory principal ID associated with this Identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)


@pulumi.input_type
class UserOwnedStorageArgs:
    def __init__(__self__, *,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        The user owned storage for Cognitive Services account.
        :param pulumi.Input[str] resource_id: Full resource id of a Microsoft.Storage resource.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Full resource id of a Microsoft.Storage resource.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class VirtualNetworkRuleArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 ignore_missing_vnet_service_endpoint: Optional[pulumi.Input[bool]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        A rule governing the accessibility from a specific virtual network.
        :param pulumi.Input[str] id: Full resource id of a vnet subnet, such as '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/test-vnet/subnets/subnet1'.
        :param pulumi.Input[bool] ignore_missing_vnet_service_endpoint: Ignore missing vnet service endpoint or not.
        :param pulumi.Input[str] state: Gets the state of virtual network rule.
        """
        pulumi.set(__self__, "id", id)
        if ignore_missing_vnet_service_endpoint is not None:
            pulumi.set(__self__, "ignore_missing_vnet_service_endpoint", ignore_missing_vnet_service_endpoint)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        Full resource id of a vnet subnet, such as '/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/test-vnet/subnets/subnet1'.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="ignoreMissingVnetServiceEndpoint")
    def ignore_missing_vnet_service_endpoint(self) -> Optional[pulumi.Input[bool]]:
        """
        Ignore missing vnet service endpoint or not.
        """
        return pulumi.get(self, "ignore_missing_vnet_service_endpoint")

    @ignore_missing_vnet_service_endpoint.setter
    def ignore_missing_vnet_service_endpoint(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_missing_vnet_service_endpoint", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        Gets the state of virtual network rule.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


