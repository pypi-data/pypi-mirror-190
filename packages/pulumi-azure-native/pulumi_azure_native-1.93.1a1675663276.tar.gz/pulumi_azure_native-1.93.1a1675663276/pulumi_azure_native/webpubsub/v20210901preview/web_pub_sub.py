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

__all__ = ['WebPubSubArgs', 'WebPubSub']

@pulumi.input_type
class WebPubSubArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 event_handler: Optional[pulumi.Input['EventHandlerSettingsArgs']] = None,
                 identity: Optional[pulumi.Input['ManagedIdentityArgs']] = None,
                 live_trace_configuration: Optional[pulumi.Input['LiveTraceConfigurationArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input['WebPubSubNetworkACLsArgs']] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['ResourceSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input['WebPubSubTlsSettingsArgs']] = None):
        """
        The set of arguments for constructing a WebPubSub resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[bool] disable_aad_auth: DisableLocalAuth
               Enable or disable aad auth
               When set as true, connection with AuthType=aad won't work.
        :param pulumi.Input[bool] disable_local_auth: DisableLocalAuth
               Enable or disable local auth with AccessKey
               When set as true, connection with AccessKey=xxx won't work.
        :param pulumi.Input['EventHandlerSettingsArgs'] event_handler: The settings for event handler in webpubsub service.
        :param pulumi.Input['ManagedIdentityArgs'] identity: The managed identity response
        :param pulumi.Input['LiveTraceConfigurationArgs'] live_trace_configuration: Live trace configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[str] location: The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        :param pulumi.Input['WebPubSubNetworkACLsArgs'] network_acls: Network ACLs
        :param pulumi.Input[str] public_network_access: Enable or disable public network access. Default to "Enabled".
               When it's Enabled, network ACLs still apply.
               When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        :param pulumi.Input[str] resource_name: The name of the resource.
        :param pulumi.Input['ResourceSkuArgs'] sku: The billing information of the resource.(e.g. Free, Standard)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the service which is a list of key value pairs that describe the resource.
        :param pulumi.Input['WebPubSubTlsSettingsArgs'] tls: TLS settings.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if disable_aad_auth is None:
            disable_aad_auth = False
        if disable_aad_auth is not None:
            pulumi.set(__self__, "disable_aad_auth", disable_aad_auth)
        if disable_local_auth is None:
            disable_local_auth = False
        if disable_local_auth is not None:
            pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if event_handler is not None:
            pulumi.set(__self__, "event_handler", event_handler)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if live_trace_configuration is not None:
            pulumi.set(__self__, "live_trace_configuration", live_trace_configuration)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_acls is not None:
            pulumi.set(__self__, "network_acls", network_acls)
        if public_network_access is None:
            public_network_access = 'Enabled'
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tls is not None:
            pulumi.set(__self__, "tls", tls)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="disableAadAuth")
    def disable_aad_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        DisableLocalAuth
        Enable or disable aad auth
        When set as true, connection with AuthType=aad won't work.
        """
        return pulumi.get(self, "disable_aad_auth")

    @disable_aad_auth.setter
    def disable_aad_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_aad_auth", value)

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        DisableLocalAuth
        Enable or disable local auth with AccessKey
        When set as true, connection with AccessKey=xxx won't work.
        """
        return pulumi.get(self, "disable_local_auth")

    @disable_local_auth.setter
    def disable_local_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_local_auth", value)

    @property
    @pulumi.getter(name="eventHandler")
    def event_handler(self) -> Optional[pulumi.Input['EventHandlerSettingsArgs']]:
        """
        The settings for event handler in webpubsub service.
        """
        return pulumi.get(self, "event_handler")

    @event_handler.setter
    def event_handler(self, value: Optional[pulumi.Input['EventHandlerSettingsArgs']]):
        pulumi.set(self, "event_handler", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedIdentityArgs']]:
        """
        The managed identity response
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="liveTraceConfiguration")
    def live_trace_configuration(self) -> Optional[pulumi.Input['LiveTraceConfigurationArgs']]:
        """
        Live trace configuration of a Microsoft.SignalRService resource.
        """
        return pulumi.get(self, "live_trace_configuration")

    @live_trace_configuration.setter
    def live_trace_configuration(self, value: Optional[pulumi.Input['LiveTraceConfigurationArgs']]):
        pulumi.set(self, "live_trace_configuration", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkACLs")
    def network_acls(self) -> Optional[pulumi.Input['WebPubSubNetworkACLsArgs']]:
        """
        Network ACLs
        """
        return pulumi.get(self, "network_acls")

    @network_acls.setter
    def network_acls(self, value: Optional[pulumi.Input['WebPubSubNetworkACLsArgs']]):
        pulumi.set(self, "network_acls", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[str]]:
        """
        Enable or disable public network access. Default to "Enabled".
        When it's Enabled, network ACLs still apply.
        When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ResourceSkuArgs']]:
        """
        The billing information of the resource.(e.g. Free, Standard)
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ResourceSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def tls(self) -> Optional[pulumi.Input['WebPubSubTlsSettingsArgs']]:
        """
        TLS settings.
        """
        return pulumi.get(self, "tls")

    @tls.setter
    def tls(self, value: Optional[pulumi.Input['WebPubSubTlsSettingsArgs']]):
        pulumi.set(self, "tls", value)


class WebPubSub(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 event_handler: Optional[pulumi.Input[pulumi.InputType['EventHandlerSettingsArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedIdentityArgs']]] = None,
                 live_trace_configuration: Optional[pulumi.Input[pulumi.InputType['LiveTraceConfigurationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input[pulumi.InputType['WebPubSubNetworkACLsArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ResourceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input[pulumi.InputType['WebPubSubTlsSettingsArgs']]] = None,
                 __props__=None):
        """
        A class represent a resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] disable_aad_auth: DisableLocalAuth
               Enable or disable aad auth
               When set as true, connection with AuthType=aad won't work.
        :param pulumi.Input[bool] disable_local_auth: DisableLocalAuth
               Enable or disable local auth with AccessKey
               When set as true, connection with AccessKey=xxx won't work.
        :param pulumi.Input[pulumi.InputType['EventHandlerSettingsArgs']] event_handler: The settings for event handler in webpubsub service.
        :param pulumi.Input[pulumi.InputType['ManagedIdentityArgs']] identity: The managed identity response
        :param pulumi.Input[pulumi.InputType['LiveTraceConfigurationArgs']] live_trace_configuration: Live trace configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[str] location: The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        :param pulumi.Input[pulumi.InputType['WebPubSubNetworkACLsArgs']] network_acls: Network ACLs
        :param pulumi.Input[str] public_network_access: Enable or disable public network access. Default to "Enabled".
               When it's Enabled, network ACLs still apply.
               When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] resource_name_: The name of the resource.
        :param pulumi.Input[pulumi.InputType['ResourceSkuArgs']] sku: The billing information of the resource.(e.g. Free, Standard)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the service which is a list of key value pairs that describe the resource.
        :param pulumi.Input[pulumi.InputType['WebPubSubTlsSettingsArgs']] tls: TLS settings.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebPubSubArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A class represent a resource.

        :param str resource_name: The name of the resource.
        :param WebPubSubArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebPubSubArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 event_handler: Optional[pulumi.Input[pulumi.InputType['EventHandlerSettingsArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedIdentityArgs']]] = None,
                 live_trace_configuration: Optional[pulumi.Input[pulumi.InputType['LiveTraceConfigurationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input[pulumi.InputType['WebPubSubNetworkACLsArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ResourceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input[pulumi.InputType['WebPubSubTlsSettingsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebPubSubArgs.__new__(WebPubSubArgs)

            if disable_aad_auth is None:
                disable_aad_auth = False
            __props__.__dict__["disable_aad_auth"] = disable_aad_auth
            if disable_local_auth is None:
                disable_local_auth = False
            __props__.__dict__["disable_local_auth"] = disable_local_auth
            __props__.__dict__["event_handler"] = event_handler
            __props__.__dict__["identity"] = identity
            __props__.__dict__["live_trace_configuration"] = live_trace_configuration
            __props__.__dict__["location"] = location
            __props__.__dict__["network_acls"] = network_acls
            if public_network_access is None:
                public_network_access = 'Enabled'
            __props__.__dict__["public_network_access"] = public_network_access
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tls"] = tls
            __props__.__dict__["external_ip"] = None
            __props__.__dict__["host_name"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["public_port"] = None
            __props__.__dict__["server_port"] = None
            __props__.__dict__["shared_private_link_resources"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["version"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:webpubsub:WebPubSub"), pulumi.Alias(type_="azure-native:webpubsub/v20210401preview:WebPubSub"), pulumi.Alias(type_="azure-native:webpubsub/v20210601preview:WebPubSub"), pulumi.Alias(type_="azure-native:webpubsub/v20211001:WebPubSub"), pulumi.Alias(type_="azure-native:webpubsub/v20220801preview:WebPubSub")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebPubSub, __self__).__init__(
            'azure-native:webpubsub/v20210901preview:WebPubSub',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebPubSub':
        """
        Get an existing WebPubSub resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebPubSubArgs.__new__(WebPubSubArgs)

        __props__.__dict__["disable_aad_auth"] = None
        __props__.__dict__["disable_local_auth"] = None
        __props__.__dict__["event_handler"] = None
        __props__.__dict__["external_ip"] = None
        __props__.__dict__["host_name"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["live_trace_configuration"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_acls"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_network_access"] = None
        __props__.__dict__["public_port"] = None
        __props__.__dict__["server_port"] = None
        __props__.__dict__["shared_private_link_resources"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tls"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["version"] = None
        return WebPubSub(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="disableAadAuth")
    def disable_aad_auth(self) -> pulumi.Output[Optional[bool]]:
        """
        DisableLocalAuth
        Enable or disable aad auth
        When set as true, connection with AuthType=aad won't work.
        """
        return pulumi.get(self, "disable_aad_auth")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> pulumi.Output[Optional[bool]]:
        """
        DisableLocalAuth
        Enable or disable local auth with AccessKey
        When set as true, connection with AccessKey=xxx won't work.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="eventHandler")
    def event_handler(self) -> pulumi.Output[Optional['outputs.EventHandlerSettingsResponse']]:
        """
        The settings for event handler in webpubsub service.
        """
        return pulumi.get(self, "event_handler")

    @property
    @pulumi.getter(name="externalIP")
    def external_ip(self) -> pulumi.Output[str]:
        """
        The publicly accessible IP of the resource.
        """
        return pulumi.get(self, "external_ip")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        FQDN of the service instance.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedIdentityResponse']]:
        """
        The managed identity response
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="liveTraceConfiguration")
    def live_trace_configuration(self) -> pulumi.Output[Optional['outputs.LiveTraceConfigurationResponse']]:
        """
        Live trace configuration of a Microsoft.SignalRService resource.
        """
        return pulumi.get(self, "live_trace_configuration")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkACLs")
    def network_acls(self) -> pulumi.Output[Optional['outputs.WebPubSubNetworkACLsResponse']]:
        """
        Network ACLs
        """
        return pulumi.get(self, "network_acls")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        Private endpoint connections to the resource.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Enable or disable public network access. Default to "Enabled".
        When it's Enabled, network ACLs still apply.
        When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="publicPort")
    def public_port(self) -> pulumi.Output[int]:
        """
        The publicly accessible port of the resource which is designed for browser/client side usage.
        """
        return pulumi.get(self, "public_port")

    @property
    @pulumi.getter(name="serverPort")
    def server_port(self) -> pulumi.Output[int]:
        """
        The publicly accessible port of the resource which is designed for customer server side usage.
        """
        return pulumi.get(self, "server_port")

    @property
    @pulumi.getter(name="sharedPrivateLinkResources")
    def shared_private_link_resources(self) -> pulumi.Output[Sequence['outputs.SharedPrivateLinkResourceResponse']]:
        """
        The list of shared private link resources.
        """
        return pulumi.get(self, "shared_private_link_resources")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ResourceSkuResponse']]:
        """
        The billing information of the resource.(e.g. Free, Standard)
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def tls(self) -> pulumi.Output[Optional['outputs.WebPubSubTlsSettingsResponse']]:
        """
        TLS settings.
        """
        return pulumi.get(self, "tls")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        Version of the resource. Probably you need the same or higher version of client SDKs.
        """
        return pulumi.get(self, "version")

