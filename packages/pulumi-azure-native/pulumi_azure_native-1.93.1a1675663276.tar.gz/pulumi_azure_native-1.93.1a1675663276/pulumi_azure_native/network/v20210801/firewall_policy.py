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
from ._enums import *
from ._inputs import *

__all__ = ['FirewallPolicyArgs', 'FirewallPolicy']

@pulumi.input_type
class FirewallPolicyArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 base_policy: Optional[pulumi.Input['SubResourceArgs']] = None,
                 dns_settings: Optional[pulumi.Input['DnsSettingsArgs']] = None,
                 explicit_proxy_settings: Optional[pulumi.Input['ExplicitProxySettingsArgs']] = None,
                 firewall_policy_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']] = None,
                 insights: Optional[pulumi.Input['FirewallPolicyInsightsArgs']] = None,
                 intrusion_detection: Optional[pulumi.Input['FirewallPolicyIntrusionDetectionArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['FirewallPolicySkuArgs']] = None,
                 snat: Optional[pulumi.Input['FirewallPolicySNATArgs']] = None,
                 sql: Optional[pulumi.Input['FirewallPolicySQLArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 threat_intel_mode: Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]] = None,
                 threat_intel_whitelist: Optional[pulumi.Input['FirewallPolicyThreatIntelWhitelistArgs']] = None,
                 transport_security: Optional[pulumi.Input['FirewallPolicyTransportSecurityArgs']] = None):
        """
        The set of arguments for constructing a FirewallPolicy resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['SubResourceArgs'] base_policy: The parent firewall policy from which rules are inherited.
        :param pulumi.Input['DnsSettingsArgs'] dns_settings: DNS Proxy Settings definition.
        :param pulumi.Input['ExplicitProxySettingsArgs'] explicit_proxy_settings: Explicit Proxy Settings definition.
        :param pulumi.Input[str] firewall_policy_name: The name of the Firewall Policy.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: The identity of the firewall policy.
        :param pulumi.Input['FirewallPolicyInsightsArgs'] insights: Insights on Firewall Policy.
        :param pulumi.Input['FirewallPolicyIntrusionDetectionArgs'] intrusion_detection: The configuration for Intrusion detection.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input['FirewallPolicySkuArgs'] sku: The Firewall Policy SKU.
        :param pulumi.Input['FirewallPolicySNATArgs'] snat: The private IP addresses/IP ranges to which traffic will not be SNAT.
        :param pulumi.Input['FirewallPolicySQLArgs'] sql: SQL Settings definition.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']] threat_intel_mode: The operation mode for Threat Intelligence.
        :param pulumi.Input['FirewallPolicyThreatIntelWhitelistArgs'] threat_intel_whitelist: ThreatIntel Whitelist for Firewall Policy.
        :param pulumi.Input['FirewallPolicyTransportSecurityArgs'] transport_security: TLS Configuration definition.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if base_policy is not None:
            pulumi.set(__self__, "base_policy", base_policy)
        if dns_settings is not None:
            pulumi.set(__self__, "dns_settings", dns_settings)
        if explicit_proxy_settings is not None:
            pulumi.set(__self__, "explicit_proxy_settings", explicit_proxy_settings)
        if firewall_policy_name is not None:
            pulumi.set(__self__, "firewall_policy_name", firewall_policy_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if insights is not None:
            pulumi.set(__self__, "insights", insights)
        if intrusion_detection is not None:
            pulumi.set(__self__, "intrusion_detection", intrusion_detection)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if snat is not None:
            pulumi.set(__self__, "snat", snat)
        if sql is not None:
            pulumi.set(__self__, "sql", sql)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if threat_intel_mode is not None:
            pulumi.set(__self__, "threat_intel_mode", threat_intel_mode)
        if threat_intel_whitelist is not None:
            pulumi.set(__self__, "threat_intel_whitelist", threat_intel_whitelist)
        if transport_security is not None:
            pulumi.set(__self__, "transport_security", transport_security)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="basePolicy")
    def base_policy(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The parent firewall policy from which rules are inherited.
        """
        return pulumi.get(self, "base_policy")

    @base_policy.setter
    def base_policy(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "base_policy", value)

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> Optional[pulumi.Input['DnsSettingsArgs']]:
        """
        DNS Proxy Settings definition.
        """
        return pulumi.get(self, "dns_settings")

    @dns_settings.setter
    def dns_settings(self, value: Optional[pulumi.Input['DnsSettingsArgs']]):
        pulumi.set(self, "dns_settings", value)

    @property
    @pulumi.getter(name="explicitProxySettings")
    def explicit_proxy_settings(self) -> Optional[pulumi.Input['ExplicitProxySettingsArgs']]:
        """
        Explicit Proxy Settings definition.
        """
        return pulumi.get(self, "explicit_proxy_settings")

    @explicit_proxy_settings.setter
    def explicit_proxy_settings(self, value: Optional[pulumi.Input['ExplicitProxySettingsArgs']]):
        pulumi.set(self, "explicit_proxy_settings", value)

    @property
    @pulumi.getter(name="firewallPolicyName")
    def firewall_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Firewall Policy.
        """
        return pulumi.get(self, "firewall_policy_name")

    @firewall_policy_name.setter
    def firewall_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "firewall_policy_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        The identity of the firewall policy.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def insights(self) -> Optional[pulumi.Input['FirewallPolicyInsightsArgs']]:
        """
        Insights on Firewall Policy.
        """
        return pulumi.get(self, "insights")

    @insights.setter
    def insights(self, value: Optional[pulumi.Input['FirewallPolicyInsightsArgs']]):
        pulumi.set(self, "insights", value)

    @property
    @pulumi.getter(name="intrusionDetection")
    def intrusion_detection(self) -> Optional[pulumi.Input['FirewallPolicyIntrusionDetectionArgs']]:
        """
        The configuration for Intrusion detection.
        """
        return pulumi.get(self, "intrusion_detection")

    @intrusion_detection.setter
    def intrusion_detection(self, value: Optional[pulumi.Input['FirewallPolicyIntrusionDetectionArgs']]):
        pulumi.set(self, "intrusion_detection", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['FirewallPolicySkuArgs']]:
        """
        The Firewall Policy SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['FirewallPolicySkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def snat(self) -> Optional[pulumi.Input['FirewallPolicySNATArgs']]:
        """
        The private IP addresses/IP ranges to which traffic will not be SNAT.
        """
        return pulumi.get(self, "snat")

    @snat.setter
    def snat(self, value: Optional[pulumi.Input['FirewallPolicySNATArgs']]):
        pulumi.set(self, "snat", value)

    @property
    @pulumi.getter
    def sql(self) -> Optional[pulumi.Input['FirewallPolicySQLArgs']]:
        """
        SQL Settings definition.
        """
        return pulumi.get(self, "sql")

    @sql.setter
    def sql(self, value: Optional[pulumi.Input['FirewallPolicySQLArgs']]):
        pulumi.set(self, "sql", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="threatIntelMode")
    def threat_intel_mode(self) -> Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]]:
        """
        The operation mode for Threat Intelligence.
        """
        return pulumi.get(self, "threat_intel_mode")

    @threat_intel_mode.setter
    def threat_intel_mode(self, value: Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]]):
        pulumi.set(self, "threat_intel_mode", value)

    @property
    @pulumi.getter(name="threatIntelWhitelist")
    def threat_intel_whitelist(self) -> Optional[pulumi.Input['FirewallPolicyThreatIntelWhitelistArgs']]:
        """
        ThreatIntel Whitelist for Firewall Policy.
        """
        return pulumi.get(self, "threat_intel_whitelist")

    @threat_intel_whitelist.setter
    def threat_intel_whitelist(self, value: Optional[pulumi.Input['FirewallPolicyThreatIntelWhitelistArgs']]):
        pulumi.set(self, "threat_intel_whitelist", value)

    @property
    @pulumi.getter(name="transportSecurity")
    def transport_security(self) -> Optional[pulumi.Input['FirewallPolicyTransportSecurityArgs']]:
        """
        TLS Configuration definition.
        """
        return pulumi.get(self, "transport_security")

    @transport_security.setter
    def transport_security(self, value: Optional[pulumi.Input['FirewallPolicyTransportSecurityArgs']]):
        pulumi.set(self, "transport_security", value)


class FirewallPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_policy: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 dns_settings: Optional[pulumi.Input[pulumi.InputType['DnsSettingsArgs']]] = None,
                 explicit_proxy_settings: Optional[pulumi.Input[pulumi.InputType['ExplicitProxySettingsArgs']]] = None,
                 firewall_policy_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 insights: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyInsightsArgs']]] = None,
                 intrusion_detection: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyIntrusionDetectionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySkuArgs']]] = None,
                 snat: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySNATArgs']]] = None,
                 sql: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySQLArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 threat_intel_mode: Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]] = None,
                 threat_intel_whitelist: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyThreatIntelWhitelistArgs']]] = None,
                 transport_security: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyTransportSecurityArgs']]] = None,
                 __props__=None):
        """
        FirewallPolicy Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] base_policy: The parent firewall policy from which rules are inherited.
        :param pulumi.Input[pulumi.InputType['DnsSettingsArgs']] dns_settings: DNS Proxy Settings definition.
        :param pulumi.Input[pulumi.InputType['ExplicitProxySettingsArgs']] explicit_proxy_settings: Explicit Proxy Settings definition.
        :param pulumi.Input[str] firewall_policy_name: The name of the Firewall Policy.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: The identity of the firewall policy.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyInsightsArgs']] insights: Insights on Firewall Policy.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyIntrusionDetectionArgs']] intrusion_detection: The configuration for Intrusion detection.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['FirewallPolicySkuArgs']] sku: The Firewall Policy SKU.
        :param pulumi.Input[pulumi.InputType['FirewallPolicySNATArgs']] snat: The private IP addresses/IP ranges to which traffic will not be SNAT.
        :param pulumi.Input[pulumi.InputType['FirewallPolicySQLArgs']] sql: SQL Settings definition.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']] threat_intel_mode: The operation mode for Threat Intelligence.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyThreatIntelWhitelistArgs']] threat_intel_whitelist: ThreatIntel Whitelist for Firewall Policy.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyTransportSecurityArgs']] transport_security: TLS Configuration definition.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FirewallPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        FirewallPolicy Resource.

        :param str resource_name: The name of the resource.
        :param FirewallPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FirewallPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_policy: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 dns_settings: Optional[pulumi.Input[pulumi.InputType['DnsSettingsArgs']]] = None,
                 explicit_proxy_settings: Optional[pulumi.Input[pulumi.InputType['ExplicitProxySettingsArgs']]] = None,
                 firewall_policy_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 insights: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyInsightsArgs']]] = None,
                 intrusion_detection: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyIntrusionDetectionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySkuArgs']]] = None,
                 snat: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySNATArgs']]] = None,
                 sql: Optional[pulumi.Input[pulumi.InputType['FirewallPolicySQLArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 threat_intel_mode: Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]] = None,
                 threat_intel_whitelist: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyThreatIntelWhitelistArgs']]] = None,
                 transport_security: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyTransportSecurityArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FirewallPolicyArgs.__new__(FirewallPolicyArgs)

            __props__.__dict__["base_policy"] = base_policy
            __props__.__dict__["dns_settings"] = dns_settings
            __props__.__dict__["explicit_proxy_settings"] = explicit_proxy_settings
            __props__.__dict__["firewall_policy_name"] = firewall_policy_name
            __props__.__dict__["id"] = id
            __props__.__dict__["identity"] = identity
            __props__.__dict__["insights"] = insights
            __props__.__dict__["intrusion_detection"] = intrusion_detection
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["snat"] = snat
            __props__.__dict__["sql"] = sql
            __props__.__dict__["tags"] = tags
            __props__.__dict__["threat_intel_mode"] = threat_intel_mode
            __props__.__dict__["threat_intel_whitelist"] = threat_intel_whitelist
            __props__.__dict__["transport_security"] = transport_security
            __props__.__dict__["child_policies"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["firewalls"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["rule_collection_groups"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20190601:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20190701:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20190801:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20190901:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20191101:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20191201:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200301:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200401:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200501:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200601:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200701:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20200801:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20201101:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20210201:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20210301:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20210501:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20220101:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20220501:FirewallPolicy"), pulumi.Alias(type_="azure-native:network/v20220701:FirewallPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FirewallPolicy, __self__).__init__(
            'azure-native:network/v20210801:FirewallPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FirewallPolicy':
        """
        Get an existing FirewallPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FirewallPolicyArgs.__new__(FirewallPolicyArgs)

        __props__.__dict__["base_policy"] = None
        __props__.__dict__["child_policies"] = None
        __props__.__dict__["dns_settings"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["explicit_proxy_settings"] = None
        __props__.__dict__["firewalls"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["insights"] = None
        __props__.__dict__["intrusion_detection"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["rule_collection_groups"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["snat"] = None
        __props__.__dict__["sql"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["threat_intel_mode"] = None
        __props__.__dict__["threat_intel_whitelist"] = None
        __props__.__dict__["transport_security"] = None
        __props__.__dict__["type"] = None
        return FirewallPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="basePolicy")
    def base_policy(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The parent firewall policy from which rules are inherited.
        """
        return pulumi.get(self, "base_policy")

    @property
    @pulumi.getter(name="childPolicies")
    def child_policies(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Child Firewall Policies.
        """
        return pulumi.get(self, "child_policies")

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> pulumi.Output[Optional['outputs.DnsSettingsResponse']]:
        """
        DNS Proxy Settings definition.
        """
        return pulumi.get(self, "dns_settings")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="explicitProxySettings")
    def explicit_proxy_settings(self) -> pulumi.Output[Optional['outputs.ExplicitProxySettingsResponse']]:
        """
        Explicit Proxy Settings definition.
        """
        return pulumi.get(self, "explicit_proxy_settings")

    @property
    @pulumi.getter
    def firewalls(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Azure Firewalls that this Firewall Policy is associated with.
        """
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        The identity of the firewall policy.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def insights(self) -> pulumi.Output[Optional['outputs.FirewallPolicyInsightsResponse']]:
        """
        Insights on Firewall Policy.
        """
        return pulumi.get(self, "insights")

    @property
    @pulumi.getter(name="intrusionDetection")
    def intrusion_detection(self) -> pulumi.Output[Optional['outputs.FirewallPolicyIntrusionDetectionResponse']]:
        """
        The configuration for Intrusion detection.
        """
        return pulumi.get(self, "intrusion_detection")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the firewall policy resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="ruleCollectionGroups")
    def rule_collection_groups(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to FirewallPolicyRuleCollectionGroups.
        """
        return pulumi.get(self, "rule_collection_groups")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.FirewallPolicySkuResponse']]:
        """
        The Firewall Policy SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def snat(self) -> pulumi.Output[Optional['outputs.FirewallPolicySNATResponse']]:
        """
        The private IP addresses/IP ranges to which traffic will not be SNAT.
        """
        return pulumi.get(self, "snat")

    @property
    @pulumi.getter
    def sql(self) -> pulumi.Output[Optional['outputs.FirewallPolicySQLResponse']]:
        """
        SQL Settings definition.
        """
        return pulumi.get(self, "sql")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threatIntelMode")
    def threat_intel_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The operation mode for Threat Intelligence.
        """
        return pulumi.get(self, "threat_intel_mode")

    @property
    @pulumi.getter(name="threatIntelWhitelist")
    def threat_intel_whitelist(self) -> pulumi.Output[Optional['outputs.FirewallPolicyThreatIntelWhitelistResponse']]:
        """
        ThreatIntel Whitelist for Firewall Policy.
        """
        return pulumi.get(self, "threat_intel_whitelist")

    @property
    @pulumi.getter(name="transportSecurity")
    def transport_security(self) -> pulumi.Output[Optional['outputs.FirewallPolicyTransportSecurityResponse']]:
        """
        TLS Configuration definition.
        """
        return pulumi.get(self, "transport_security")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

