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

__all__ = ['EndpointArgs', 'Endpoint']

@pulumi.input_type
class EndpointArgs:
    def __init__(__self__, *,
                 origins: pulumi.Input[Sequence[pulumi.Input['DeepCreatedOriginArgs']]],
                 profile_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 content_types_to_compress: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 geo_filters: Optional[pulumi.Input[Sequence[pulumi.Input['GeoFilterArgs']]]] = None,
                 is_compression_enabled: Optional[pulumi.Input[bool]] = None,
                 is_http_allowed: Optional[pulumi.Input[bool]] = None,
                 is_https_allowed: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 optimization_type: Optional[pulumi.Input[Union[str, 'OptimizationType']]] = None,
                 origin_host_header: Optional[pulumi.Input[str]] = None,
                 origin_path: Optional[pulumi.Input[str]] = None,
                 query_string_caching_behavior: Optional[pulumi.Input['QueryStringCachingBehavior']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Endpoint resource.
        :param pulumi.Input[Sequence[pulumi.Input['DeepCreatedOriginArgs']]] origins: The source of the content being delivered via CDN.
        :param pulumi.Input[str] profile_name: Name of the CDN profile which is unique within the resource group.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] content_types_to_compress: List of content types on which compression applies. The value should be a valid MIME type.
        :param pulumi.Input[str] endpoint_name: Name of the endpoint under the profile which is unique globally.
        :param pulumi.Input[Sequence[pulumi.Input['GeoFilterArgs']]] geo_filters: List of rules defining user geo access within a CDN endpoint. Each geo filter defines an access rule to a specified path or content, e.g. block APAC for path /pictures/
        :param pulumi.Input[bool] is_compression_enabled: Indicates whether content compression is enabled on CDN. Default value is false. If compression is enabled, content will be served as compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1 byte or larger than 1 MB.
        :param pulumi.Input[bool] is_http_allowed: Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        :param pulumi.Input[bool] is_https_allowed: Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Union[str, 'OptimizationType']] optimization_type: Customer can specify what scenario they want this CDN endpoint to optimize, e.g. Download, Media services. With this information we can apply scenario driven optimization.
        :param pulumi.Input[str] origin_host_header: The host header CDN sends along with content requests to origin. The default value is the host name of the origin.
        :param pulumi.Input[str] origin_path: The path used when CDN sends request to origin.
        :param pulumi.Input['QueryStringCachingBehavior'] query_string_caching_behavior: Defines the query string caching behavior
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "origins", origins)
        pulumi.set(__self__, "profile_name", profile_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if content_types_to_compress is not None:
            pulumi.set(__self__, "content_types_to_compress", content_types_to_compress)
        if endpoint_name is not None:
            pulumi.set(__self__, "endpoint_name", endpoint_name)
        if geo_filters is not None:
            pulumi.set(__self__, "geo_filters", geo_filters)
        if is_compression_enabled is not None:
            pulumi.set(__self__, "is_compression_enabled", is_compression_enabled)
        if is_http_allowed is not None:
            pulumi.set(__self__, "is_http_allowed", is_http_allowed)
        if is_https_allowed is not None:
            pulumi.set(__self__, "is_https_allowed", is_https_allowed)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if optimization_type is not None:
            pulumi.set(__self__, "optimization_type", optimization_type)
        if origin_host_header is not None:
            pulumi.set(__self__, "origin_host_header", origin_host_header)
        if origin_path is not None:
            pulumi.set(__self__, "origin_path", origin_path)
        if query_string_caching_behavior is not None:
            pulumi.set(__self__, "query_string_caching_behavior", query_string_caching_behavior)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def origins(self) -> pulumi.Input[Sequence[pulumi.Input['DeepCreatedOriginArgs']]]:
        """
        The source of the content being delivered via CDN.
        """
        return pulumi.get(self, "origins")

    @origins.setter
    def origins(self, value: pulumi.Input[Sequence[pulumi.Input['DeepCreatedOriginArgs']]]):
        pulumi.set(self, "origins", value)

    @property
    @pulumi.getter(name="profileName")
    def profile_name(self) -> pulumi.Input[str]:
        """
        Name of the CDN profile which is unique within the resource group.
        """
        return pulumi.get(self, "profile_name")

    @profile_name.setter
    def profile_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "profile_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="contentTypesToCompress")
    def content_types_to_compress(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of content types on which compression applies. The value should be a valid MIME type.
        """
        return pulumi.get(self, "content_types_to_compress")

    @content_types_to_compress.setter
    def content_types_to_compress(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "content_types_to_compress", value)

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the endpoint under the profile which is unique globally.
        """
        return pulumi.get(self, "endpoint_name")

    @endpoint_name.setter
    def endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_name", value)

    @property
    @pulumi.getter(name="geoFilters")
    def geo_filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GeoFilterArgs']]]]:
        """
        List of rules defining user geo access within a CDN endpoint. Each geo filter defines an access rule to a specified path or content, e.g. block APAC for path /pictures/
        """
        return pulumi.get(self, "geo_filters")

    @geo_filters.setter
    def geo_filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GeoFilterArgs']]]]):
        pulumi.set(self, "geo_filters", value)

    @property
    @pulumi.getter(name="isCompressionEnabled")
    def is_compression_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether content compression is enabled on CDN. Default value is false. If compression is enabled, content will be served as compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1 byte or larger than 1 MB.
        """
        return pulumi.get(self, "is_compression_enabled")

    @is_compression_enabled.setter
    def is_compression_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_compression_enabled", value)

    @property
    @pulumi.getter(name="isHttpAllowed")
    def is_http_allowed(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        """
        return pulumi.get(self, "is_http_allowed")

    @is_http_allowed.setter
    def is_http_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_http_allowed", value)

    @property
    @pulumi.getter(name="isHttpsAllowed")
    def is_https_allowed(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        """
        return pulumi.get(self, "is_https_allowed")

    @is_https_allowed.setter
    def is_https_allowed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_https_allowed", value)

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
    @pulumi.getter(name="optimizationType")
    def optimization_type(self) -> Optional[pulumi.Input[Union[str, 'OptimizationType']]]:
        """
        Customer can specify what scenario they want this CDN endpoint to optimize, e.g. Download, Media services. With this information we can apply scenario driven optimization.
        """
        return pulumi.get(self, "optimization_type")

    @optimization_type.setter
    def optimization_type(self, value: Optional[pulumi.Input[Union[str, 'OptimizationType']]]):
        pulumi.set(self, "optimization_type", value)

    @property
    @pulumi.getter(name="originHostHeader")
    def origin_host_header(self) -> Optional[pulumi.Input[str]]:
        """
        The host header CDN sends along with content requests to origin. The default value is the host name of the origin.
        """
        return pulumi.get(self, "origin_host_header")

    @origin_host_header.setter
    def origin_host_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "origin_host_header", value)

    @property
    @pulumi.getter(name="originPath")
    def origin_path(self) -> Optional[pulumi.Input[str]]:
        """
        The path used when CDN sends request to origin.
        """
        return pulumi.get(self, "origin_path")

    @origin_path.setter
    def origin_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "origin_path", value)

    @property
    @pulumi.getter(name="queryStringCachingBehavior")
    def query_string_caching_behavior(self) -> Optional[pulumi.Input['QueryStringCachingBehavior']]:
        """
        Defines the query string caching behavior
        """
        return pulumi.get(self, "query_string_caching_behavior")

    @query_string_caching_behavior.setter
    def query_string_caching_behavior(self, value: Optional[pulumi.Input['QueryStringCachingBehavior']]):
        pulumi.set(self, "query_string_caching_behavior", value)

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


warnings.warn("""Version 2016-10-02 will be removed in v2 of the provider.""", DeprecationWarning)


class Endpoint(pulumi.CustomResource):
    warnings.warn("""Version 2016-10-02 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_types_to_compress: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 geo_filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GeoFilterArgs']]]]] = None,
                 is_compression_enabled: Optional[pulumi.Input[bool]] = None,
                 is_http_allowed: Optional[pulumi.Input[bool]] = None,
                 is_https_allowed: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 optimization_type: Optional[pulumi.Input[Union[str, 'OptimizationType']]] = None,
                 origin_host_header: Optional[pulumi.Input[str]] = None,
                 origin_path: Optional[pulumi.Input[str]] = None,
                 origins: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeepCreatedOriginArgs']]]]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 query_string_caching_behavior: Optional[pulumi.Input['QueryStringCachingBehavior']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        CDN endpoint is the entity within a CDN profile containing configuration information such as origin, protocol, content caching and delivery behavior. The CDN endpoint uses the URL format <endpointname>.azureedge.net.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] content_types_to_compress: List of content types on which compression applies. The value should be a valid MIME type.
        :param pulumi.Input[str] endpoint_name: Name of the endpoint under the profile which is unique globally.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GeoFilterArgs']]]] geo_filters: List of rules defining user geo access within a CDN endpoint. Each geo filter defines an access rule to a specified path or content, e.g. block APAC for path /pictures/
        :param pulumi.Input[bool] is_compression_enabled: Indicates whether content compression is enabled on CDN. Default value is false. If compression is enabled, content will be served as compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1 byte or larger than 1 MB.
        :param pulumi.Input[bool] is_http_allowed: Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        :param pulumi.Input[bool] is_https_allowed: Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Union[str, 'OptimizationType']] optimization_type: Customer can specify what scenario they want this CDN endpoint to optimize, e.g. Download, Media services. With this information we can apply scenario driven optimization.
        :param pulumi.Input[str] origin_host_header: The host header CDN sends along with content requests to origin. The default value is the host name of the origin.
        :param pulumi.Input[str] origin_path: The path used when CDN sends request to origin.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeepCreatedOriginArgs']]]] origins: The source of the content being delivered via CDN.
        :param pulumi.Input[str] profile_name: Name of the CDN profile which is unique within the resource group.
        :param pulumi.Input['QueryStringCachingBehavior'] query_string_caching_behavior: Defines the query string caching behavior
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        CDN endpoint is the entity within a CDN profile containing configuration information such as origin, protocol, content caching and delivery behavior. The CDN endpoint uses the URL format <endpointname>.azureedge.net.

        :param str resource_name: The name of the resource.
        :param EndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_types_to_compress: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 geo_filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GeoFilterArgs']]]]] = None,
                 is_compression_enabled: Optional[pulumi.Input[bool]] = None,
                 is_http_allowed: Optional[pulumi.Input[bool]] = None,
                 is_https_allowed: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 optimization_type: Optional[pulumi.Input[Union[str, 'OptimizationType']]] = None,
                 origin_host_header: Optional[pulumi.Input[str]] = None,
                 origin_path: Optional[pulumi.Input[str]] = None,
                 origins: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeepCreatedOriginArgs']]]]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 query_string_caching_behavior: Optional[pulumi.Input['QueryStringCachingBehavior']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Endpoint is deprecated: Version 2016-10-02 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EndpointArgs.__new__(EndpointArgs)

            __props__.__dict__["content_types_to_compress"] = content_types_to_compress
            __props__.__dict__["endpoint_name"] = endpoint_name
            __props__.__dict__["geo_filters"] = geo_filters
            __props__.__dict__["is_compression_enabled"] = is_compression_enabled
            __props__.__dict__["is_http_allowed"] = is_http_allowed
            __props__.__dict__["is_https_allowed"] = is_https_allowed
            __props__.__dict__["location"] = location
            __props__.__dict__["optimization_type"] = optimization_type
            __props__.__dict__["origin_host_header"] = origin_host_header
            __props__.__dict__["origin_path"] = origin_path
            if origins is None and not opts.urn:
                raise TypeError("Missing required property 'origins'")
            __props__.__dict__["origins"] = origins
            if profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'profile_name'")
            __props__.__dict__["profile_name"] = profile_name
            __props__.__dict__["query_string_caching_behavior"] = query_string_caching_behavior
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["host_name"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:cdn:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20150601:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20160402:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20170402:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20171012:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20190415:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20190615:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20190615preview:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20191231:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20200331:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20200415:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20200901:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20210601:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20220501preview:Endpoint"), pulumi.Alias(type_="azure-native:cdn/v20221101preview:Endpoint")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Endpoint, __self__).__init__(
            'azure-native:cdn/v20161002:Endpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Endpoint':
        """
        Get an existing Endpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EndpointArgs.__new__(EndpointArgs)

        __props__.__dict__["content_types_to_compress"] = None
        __props__.__dict__["geo_filters"] = None
        __props__.__dict__["host_name"] = None
        __props__.__dict__["is_compression_enabled"] = None
        __props__.__dict__["is_http_allowed"] = None
        __props__.__dict__["is_https_allowed"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["optimization_type"] = None
        __props__.__dict__["origin_host_header"] = None
        __props__.__dict__["origin_path"] = None
        __props__.__dict__["origins"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["query_string_caching_behavior"] = None
        __props__.__dict__["resource_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Endpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="contentTypesToCompress")
    def content_types_to_compress(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of content types on which compression applies. The value should be a valid MIME type.
        """
        return pulumi.get(self, "content_types_to_compress")

    @property
    @pulumi.getter(name="geoFilters")
    def geo_filters(self) -> pulumi.Output[Optional[Sequence['outputs.GeoFilterResponse']]]:
        """
        List of rules defining user geo access within a CDN endpoint. Each geo filter defines an access rule to a specified path or content, e.g. block APAC for path /pictures/
        """
        return pulumi.get(self, "geo_filters")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The host name of the endpoint structured as {endpointName}.{DNSZone}, e.g. contoso.azureedge.net
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="isCompressionEnabled")
    def is_compression_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether content compression is enabled on CDN. Default value is false. If compression is enabled, content will be served as compressed if user requests for a compressed version. Content won't be compressed on CDN when requested content is smaller than 1 byte or larger than 1 MB.
        """
        return pulumi.get(self, "is_compression_enabled")

    @property
    @pulumi.getter(name="isHttpAllowed")
    def is_http_allowed(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether HTTP traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        """
        return pulumi.get(self, "is_http_allowed")

    @property
    @pulumi.getter(name="isHttpsAllowed")
    def is_https_allowed(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether HTTPS traffic is allowed on the endpoint. Default value is true. At least one protocol (HTTP or HTTPS) must be allowed.
        """
        return pulumi.get(self, "is_https_allowed")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
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
    @pulumi.getter(name="optimizationType")
    def optimization_type(self) -> pulumi.Output[Optional[str]]:
        """
        Customer can specify what scenario they want this CDN endpoint to optimize, e.g. Download, Media services. With this information we can apply scenario driven optimization.
        """
        return pulumi.get(self, "optimization_type")

    @property
    @pulumi.getter(name="originHostHeader")
    def origin_host_header(self) -> pulumi.Output[Optional[str]]:
        """
        The host header CDN sends along with content requests to origin. The default value is the host name of the origin.
        """
        return pulumi.get(self, "origin_host_header")

    @property
    @pulumi.getter(name="originPath")
    def origin_path(self) -> pulumi.Output[Optional[str]]:
        """
        The path used when CDN sends request to origin.
        """
        return pulumi.get(self, "origin_path")

    @property
    @pulumi.getter
    def origins(self) -> pulumi.Output[Sequence['outputs.DeepCreatedOriginResponse']]:
        """
        The source of the content being delivered via CDN.
        """
        return pulumi.get(self, "origins")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning status of the endpoint.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="queryStringCachingBehavior")
    def query_string_caching_behavior(self) -> pulumi.Output[Optional[str]]:
        """
        Defines the query string caching behavior
        """
        return pulumi.get(self, "query_string_caching_behavior")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        Resource status of the endpoint.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

