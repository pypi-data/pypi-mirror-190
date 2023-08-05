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
    'CacheExpirationActionParametersArgs',
    'DeepCreatedOriginArgs',
    'DeliveryRuleCacheExpirationActionArgs',
    'DeliveryRuleUrlFileExtensionConditionArgs',
    'DeliveryRuleUrlPathConditionArgs',
    'DeliveryRuleArgs',
    'EndpointPropertiesUpdateParametersDeliveryPolicyArgs',
    'GeoFilterArgs',
    'SkuArgs',
    'UrlFileExtensionConditionParametersArgs',
    'UrlPathConditionParametersArgs',
]

@pulumi.input_type
class CacheExpirationActionParametersArgs:
    def __init__(__self__, *,
                 cache_behavior: pulumi.Input[str],
                 cache_type: pulumi.Input[str],
                 odata_type: pulumi.Input[str],
                 cache_duration: Optional[pulumi.Input[str]] = None):
        """
        Defines the parameters for the cache expiration action.
        :param pulumi.Input[str] cache_behavior: Caching behavior for the requests that include query strings.
        :param pulumi.Input[str] cache_type: The level at which the content needs to be cached.
        :param pulumi.Input[str] cache_duration: The duration for which the content needs to be cached. Allowed format is [d.]hh:mm:ss
        """
        pulumi.set(__self__, "cache_behavior", cache_behavior)
        pulumi.set(__self__, "cache_type", cache_type)
        pulumi.set(__self__, "odata_type", odata_type)
        if cache_duration is not None:
            pulumi.set(__self__, "cache_duration", cache_duration)

    @property
    @pulumi.getter(name="cacheBehavior")
    def cache_behavior(self) -> pulumi.Input[str]:
        """
        Caching behavior for the requests that include query strings.
        """
        return pulumi.get(self, "cache_behavior")

    @cache_behavior.setter
    def cache_behavior(self, value: pulumi.Input[str]):
        pulumi.set(self, "cache_behavior", value)

    @property
    @pulumi.getter(name="cacheType")
    def cache_type(self) -> pulumi.Input[str]:
        """
        The level at which the content needs to be cached.
        """
        return pulumi.get(self, "cache_type")

    @cache_type.setter
    def cache_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "cache_type", value)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "odata_type")

    @odata_type.setter
    def odata_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "odata_type", value)

    @property
    @pulumi.getter(name="cacheDuration")
    def cache_duration(self) -> Optional[pulumi.Input[str]]:
        """
        The duration for which the content needs to be cached. Allowed format is [d.]hh:mm:ss
        """
        return pulumi.get(self, "cache_duration")

    @cache_duration.setter
    def cache_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cache_duration", value)


@pulumi.input_type
class DeepCreatedOriginArgs:
    def __init__(__self__, *,
                 host_name: pulumi.Input[str],
                 name: pulumi.Input[str],
                 http_port: Optional[pulumi.Input[int]] = None,
                 https_port: Optional[pulumi.Input[int]] = None):
        """
        The main origin of CDN content which is added when creating a CDN endpoint.
        :param pulumi.Input[str] host_name: The address of the origin. It can be a domain name, IPv4 address, or IPv6 address.
        :param pulumi.Input[str] name: Origin name
        :param pulumi.Input[int] http_port: The value of the HTTP port. Must be between 1 and 65535
        :param pulumi.Input[int] https_port: The value of the HTTPS port. Must be between 1 and 65535
        """
        pulumi.set(__self__, "host_name", host_name)
        pulumi.set(__self__, "name", name)
        if http_port is not None:
            pulumi.set(__self__, "http_port", http_port)
        if https_port is not None:
            pulumi.set(__self__, "https_port", https_port)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Input[str]:
        """
        The address of the origin. It can be a domain name, IPv4 address, or IPv6 address.
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Origin name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="httpPort")
    def http_port(self) -> Optional[pulumi.Input[int]]:
        """
        The value of the HTTP port. Must be between 1 and 65535
        """
        return pulumi.get(self, "http_port")

    @http_port.setter
    def http_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_port", value)

    @property
    @pulumi.getter(name="httpsPort")
    def https_port(self) -> Optional[pulumi.Input[int]]:
        """
        The value of the HTTPS port. Must be between 1 and 65535
        """
        return pulumi.get(self, "https_port")

    @https_port.setter
    def https_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "https_port", value)


@pulumi.input_type
class DeliveryRuleCacheExpirationActionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 parameters: pulumi.Input['CacheExpirationActionParametersArgs']):
        """
        Defines the cache expiration action for the delivery rule.
        :param pulumi.Input[str] name: The name of the action for the delivery rule.
               Expected value is 'CacheExpiration'.
        :param pulumi.Input['CacheExpirationActionParametersArgs'] parameters: Defines the parameters for the action.
        """
        pulumi.set(__self__, "name", 'CacheExpiration')
        pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the action for the delivery rule.
        Expected value is 'CacheExpiration'.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Input['CacheExpirationActionParametersArgs']:
        """
        Defines the parameters for the action.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: pulumi.Input['CacheExpirationActionParametersArgs']):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class DeliveryRuleUrlFileExtensionConditionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 parameters: pulumi.Input['UrlFileExtensionConditionParametersArgs']):
        """
        Defines the URL file extension condition for the delivery rule.
        :param pulumi.Input[str] name: The name of the condition for the delivery rule.
               Expected value is 'UrlFileExtension'.
        :param pulumi.Input['UrlFileExtensionConditionParametersArgs'] parameters: Defines the parameters for the condition.
        """
        pulumi.set(__self__, "name", 'UrlFileExtension')
        pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the condition for the delivery rule.
        Expected value is 'UrlFileExtension'.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Input['UrlFileExtensionConditionParametersArgs']:
        """
        Defines the parameters for the condition.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: pulumi.Input['UrlFileExtensionConditionParametersArgs']):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class DeliveryRuleUrlPathConditionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 parameters: pulumi.Input['UrlPathConditionParametersArgs']):
        """
        Defines the URL path condition for the delivery rule.
        :param pulumi.Input[str] name: The name of the condition for the delivery rule.
               Expected value is 'UrlPath'.
        :param pulumi.Input['UrlPathConditionParametersArgs'] parameters: Defines the parameters for the condition.
        """
        pulumi.set(__self__, "name", 'UrlPath')
        pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the condition for the delivery rule.
        Expected value is 'UrlPath'.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Input['UrlPathConditionParametersArgs']:
        """
        Defines the parameters for the condition.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: pulumi.Input['UrlPathConditionParametersArgs']):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class DeliveryRuleArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input[Sequence[pulumi.Input['DeliveryRuleCacheExpirationActionArgs']]],
                 order: pulumi.Input[int],
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['DeliveryRuleUrlFileExtensionConditionArgs', 'DeliveryRuleUrlPathConditionArgs']]]]] = None):
        """
        A rule that specifies a set of actions and conditions
        :param pulumi.Input[Sequence[pulumi.Input['DeliveryRuleCacheExpirationActionArgs']]] actions: A list of actions that are executed when all the conditions of a rule are satisfied.
        :param pulumi.Input[int] order: The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order will be applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any condition and actions listed in it will always be applied.
        :param pulumi.Input[Sequence[pulumi.Input[Union['DeliveryRuleUrlFileExtensionConditionArgs', 'DeliveryRuleUrlPathConditionArgs']]]] conditions: A list of conditions that must be matched for the actions to be executed
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "order", order)
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input[Sequence[pulumi.Input['DeliveryRuleCacheExpirationActionArgs']]]:
        """
        A list of actions that are executed when all the conditions of a rule are satisfied.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input[Sequence[pulumi.Input['DeliveryRuleCacheExpirationActionArgs']]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def order(self) -> pulumi.Input[int]:
        """
        The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order will be applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any condition and actions listed in it will always be applied.
        """
        return pulumi.get(self, "order")

    @order.setter
    def order(self, value: pulumi.Input[int]):
        pulumi.set(self, "order", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union['DeliveryRuleUrlFileExtensionConditionArgs', 'DeliveryRuleUrlPathConditionArgs']]]]]:
        """
        A list of conditions that must be matched for the actions to be executed
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union['DeliveryRuleUrlFileExtensionConditionArgs', 'DeliveryRuleUrlPathConditionArgs']]]]]):
        pulumi.set(self, "conditions", value)


@pulumi.input_type
class EndpointPropertiesUpdateParametersDeliveryPolicyArgs:
    def __init__(__self__, *,
                 rules: pulumi.Input[Sequence[pulumi.Input['DeliveryRuleArgs']]],
                 description: Optional[pulumi.Input[str]] = None):
        """
        A policy that specifies the delivery rules to be used for an endpoint.
        :param pulumi.Input[Sequence[pulumi.Input['DeliveryRuleArgs']]] rules: A list of the delivery rules.
        :param pulumi.Input[str] description: User-friendly description of the policy.
        """
        pulumi.set(__self__, "rules", rules)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['DeliveryRuleArgs']]]:
        """
        A list of the delivery rules.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['DeliveryRuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-friendly description of the policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class GeoFilterArgs:
    def __init__(__self__, *,
                 action: pulumi.Input['GeoFilterActions'],
                 country_codes: pulumi.Input[Sequence[pulumi.Input[str]]],
                 relative_path: pulumi.Input[str]):
        """
        Rules defining user's geo access within a CDN endpoint.
        :param pulumi.Input['GeoFilterActions'] action: Action of the geo filter, i.e. allow or block access.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] country_codes: Two letter country codes defining user country access in a geo filter, e.g. AU, MX, US.
        :param pulumi.Input[str] relative_path: Relative path applicable to geo filter. (e.g. '/mypictures', '/mypicture/kitty.jpg', and etc.)
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "country_codes", country_codes)
        pulumi.set(__self__, "relative_path", relative_path)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input['GeoFilterActions']:
        """
        Action of the geo filter, i.e. allow or block access.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input['GeoFilterActions']):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="countryCodes")
    def country_codes(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Two letter country codes defining user country access in a geo filter, e.g. AU, MX, US.
        """
        return pulumi.get(self, "country_codes")

    @country_codes.setter
    def country_codes(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "country_codes", value)

    @property
    @pulumi.getter(name="relativePath")
    def relative_path(self) -> pulumi.Input[str]:
        """
        Relative path applicable to geo filter. (e.g. '/mypictures', '/mypicture/kitty.jpg', and etc.)
        """
        return pulumi.get(self, "relative_path")

    @relative_path.setter
    def relative_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "relative_path", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[Union[str, 'SkuName']]] = None):
        """
        The pricing tier (defines a CDN provider, feature list and rate) of the CDN profile.
        :param pulumi.Input[Union[str, 'SkuName']] name: Name of the pricing tier.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'SkuName']]]:
        """
        Name of the pricing tier.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'SkuName']]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class UrlFileExtensionConditionParametersArgs:
    def __init__(__self__, *,
                 extensions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 odata_type: pulumi.Input[str]):
        """
        Defines the parameters for the URL file extension condition.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] extensions: A list of extensions for the condition of the delivery rule.
        """
        pulumi.set(__self__, "extensions", extensions)
        pulumi.set(__self__, "odata_type", odata_type)

    @property
    @pulumi.getter
    def extensions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of extensions for the condition of the delivery rule.
        """
        return pulumi.get(self, "extensions")

    @extensions.setter
    def extensions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "extensions", value)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "odata_type")

    @odata_type.setter
    def odata_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "odata_type", value)


@pulumi.input_type
class UrlPathConditionParametersArgs:
    def __init__(__self__, *,
                 match_type: pulumi.Input[str],
                 odata_type: pulumi.Input[str],
                 path: pulumi.Input[str]):
        """
        Defines the parameters for the URL path condition.
        :param pulumi.Input[str] match_type: The match type for the condition of the delivery rule
        :param pulumi.Input[str] path: A URL path for the condition of the delivery rule
        """
        pulumi.set(__self__, "match_type", match_type)
        pulumi.set(__self__, "odata_type", odata_type)
        pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter(name="matchType")
    def match_type(self) -> pulumi.Input[str]:
        """
        The match type for the condition of the delivery rule
        """
        return pulumi.get(self, "match_type")

    @match_type.setter
    def match_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "match_type", value)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "odata_type")

    @odata_type.setter
    def odata_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "odata_type", value)

    @property
    @pulumi.getter
    def path(self) -> pulumi.Input[str]:
        """
        A URL path for the condition of the delivery rule
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: pulumi.Input[str]):
        pulumi.set(self, "path", value)


