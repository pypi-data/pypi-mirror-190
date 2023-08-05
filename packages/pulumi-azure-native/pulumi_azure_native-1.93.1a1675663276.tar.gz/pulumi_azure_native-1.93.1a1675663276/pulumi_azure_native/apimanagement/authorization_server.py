# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['AuthorizationServerArgs', 'AuthorizationServer']

@pulumi.input_type
class AuthorizationServerArgs:
    def __init__(__self__, *,
                 authorization_endpoint: pulumi.Input[str],
                 client_id: pulumi.Input[str],
                 client_registration_endpoint: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 grant_types: pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]],
                 resource_group_name: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 authorization_methods: Optional[pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]]] = None,
                 authsid: Optional[pulumi.Input[str]] = None,
                 bearer_token_sending_methods: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]]] = None,
                 client_authentication_method: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 default_scope: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 resource_owner_password: Optional[pulumi.Input[str]] = None,
                 resource_owner_username: Optional[pulumi.Input[str]] = None,
                 support_state: Optional[pulumi.Input[bool]] = None,
                 token_body_parameters: Optional[pulumi.Input[Sequence[pulumi.Input['TokenBodyParameterContractArgs']]]] = None,
                 token_endpoint: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AuthorizationServer resource.
        :param pulumi.Input[str] authorization_endpoint: OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2.
        :param pulumi.Input[str] client_id: Client or app id registered with this authorization server.
        :param pulumi.Input[str] client_registration_endpoint: Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity being referenced.
        :param pulumi.Input[str] display_name: User-friendly authorization server name.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]] grant_types: Form of an authorization grant, which the client uses to request the access token.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]] authorization_methods: HTTP verbs supported by the authorization endpoint. GET must be always present. POST is optional.
        :param pulumi.Input[str] authsid: Identifier of the authorization server.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]] bearer_token_sending_methods: Specifies the mechanism by which access token is passed to the API. 
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]] client_authentication_method: Method of authentication supported by the token endpoint of this authorization server. Possible values are Basic and/or Body. When Body is specified, client credentials and other parameters are passed within the request body in the application/x-www-form-urlencoded format.
        :param pulumi.Input[str] client_secret: Client or app secret registered with this authorization server. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        :param pulumi.Input[str] default_scope: Access token scope that is going to be requested by default. Can be overridden at the API level. Should be provided in the form of a string containing space-delimited values.
        :param pulumi.Input[str] description: Description of the authorization server. Can contain HTML formatting tags.
        :param pulumi.Input[str] resource_owner_password: Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner password.
        :param pulumi.Input[str] resource_owner_username: Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner username.
        :param pulumi.Input[bool] support_state: If true, authorization server will include state parameter from the authorization request to its response. Client may use state parameter to raise protocol security.
        :param pulumi.Input[Sequence[pulumi.Input['TokenBodyParameterContractArgs']]] token_body_parameters: Additional parameters required by the token endpoint of this authorization server represented as an array of JSON objects with name and value string properties, i.e. {"name" : "name value", "value": "a value"}.
        :param pulumi.Input[str] token_endpoint: OAuth token endpoint. Contains absolute URI to entity being referenced.
        """
        pulumi.set(__self__, "authorization_endpoint", authorization_endpoint)
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "client_registration_endpoint", client_registration_endpoint)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "grant_types", grant_types)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "service_name", service_name)
        if authorization_methods is not None:
            pulumi.set(__self__, "authorization_methods", authorization_methods)
        if authsid is not None:
            pulumi.set(__self__, "authsid", authsid)
        if bearer_token_sending_methods is not None:
            pulumi.set(__self__, "bearer_token_sending_methods", bearer_token_sending_methods)
        if client_authentication_method is not None:
            pulumi.set(__self__, "client_authentication_method", client_authentication_method)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if default_scope is not None:
            pulumi.set(__self__, "default_scope", default_scope)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if resource_owner_password is not None:
            pulumi.set(__self__, "resource_owner_password", resource_owner_password)
        if resource_owner_username is not None:
            pulumi.set(__self__, "resource_owner_username", resource_owner_username)
        if support_state is not None:
            pulumi.set(__self__, "support_state", support_state)
        if token_body_parameters is not None:
            pulumi.set(__self__, "token_body_parameters", token_body_parameters)
        if token_endpoint is not None:
            pulumi.set(__self__, "token_endpoint", token_endpoint)

    @property
    @pulumi.getter(name="authorizationEndpoint")
    def authorization_endpoint(self) -> pulumi.Input[str]:
        """
        OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2.
        """
        return pulumi.get(self, "authorization_endpoint")

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: pulumi.Input[str]):
        pulumi.set(self, "authorization_endpoint", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        """
        Client or app id registered with this authorization server.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientRegistrationEndpoint")
    def client_registration_endpoint(self) -> pulumi.Input[str]:
        """
        Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity being referenced.
        """
        return pulumi.get(self, "client_registration_endpoint")

    @client_registration_endpoint.setter
    def client_registration_endpoint(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_registration_endpoint", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        User-friendly authorization server name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="grantTypes")
    def grant_types(self) -> pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]]:
        """
        Form of an authorization grant, which the client uses to request the access token.
        """
        return pulumi.get(self, "grant_types")

    @grant_types.setter
    def grant_types(self, value: pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]]):
        pulumi.set(self, "grant_types", value)

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
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="authorizationMethods")
    def authorization_methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]]]:
        """
        HTTP verbs supported by the authorization endpoint. GET must be always present. POST is optional.
        """
        return pulumi.get(self, "authorization_methods")

    @authorization_methods.setter
    def authorization_methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]]]):
        pulumi.set(self, "authorization_methods", value)

    @property
    @pulumi.getter
    def authsid(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the authorization server.
        """
        return pulumi.get(self, "authsid")

    @authsid.setter
    def authsid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authsid", value)

    @property
    @pulumi.getter(name="bearerTokenSendingMethods")
    def bearer_token_sending_methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]]]:
        """
        Specifies the mechanism by which access token is passed to the API. 
        """
        return pulumi.get(self, "bearer_token_sending_methods")

    @bearer_token_sending_methods.setter
    def bearer_token_sending_methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]]]):
        pulumi.set(self, "bearer_token_sending_methods", value)

    @property
    @pulumi.getter(name="clientAuthenticationMethod")
    def client_authentication_method(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]]]:
        """
        Method of authentication supported by the token endpoint of this authorization server. Possible values are Basic and/or Body. When Body is specified, client credentials and other parameters are passed within the request body in the application/x-www-form-urlencoded format.
        """
        return pulumi.get(self, "client_authentication_method")

    @client_authentication_method.setter
    def client_authentication_method(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]]]):
        pulumi.set(self, "client_authentication_method", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Client or app secret registered with this authorization server. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="defaultScope")
    def default_scope(self) -> Optional[pulumi.Input[str]]:
        """
        Access token scope that is going to be requested by default. Can be overridden at the API level. Should be provided in the form of a string containing space-delimited values.
        """
        return pulumi.get(self, "default_scope")

    @default_scope.setter
    def default_scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_scope", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the authorization server. Can contain HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="resourceOwnerPassword")
    def resource_owner_password(self) -> Optional[pulumi.Input[str]]:
        """
        Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner password.
        """
        return pulumi.get(self, "resource_owner_password")

    @resource_owner_password.setter
    def resource_owner_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_owner_password", value)

    @property
    @pulumi.getter(name="resourceOwnerUsername")
    def resource_owner_username(self) -> Optional[pulumi.Input[str]]:
        """
        Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner username.
        """
        return pulumi.get(self, "resource_owner_username")

    @resource_owner_username.setter
    def resource_owner_username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_owner_username", value)

    @property
    @pulumi.getter(name="supportState")
    def support_state(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, authorization server will include state parameter from the authorization request to its response. Client may use state parameter to raise protocol security.
        """
        return pulumi.get(self, "support_state")

    @support_state.setter
    def support_state(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "support_state", value)

    @property
    @pulumi.getter(name="tokenBodyParameters")
    def token_body_parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TokenBodyParameterContractArgs']]]]:
        """
        Additional parameters required by the token endpoint of this authorization server represented as an array of JSON objects with name and value string properties, i.e. {"name" : "name value", "value": "a value"}.
        """
        return pulumi.get(self, "token_body_parameters")

    @token_body_parameters.setter
    def token_body_parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TokenBodyParameterContractArgs']]]]):
        pulumi.set(self, "token_body_parameters", value)

    @property
    @pulumi.getter(name="tokenEndpoint")
    def token_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        OAuth token endpoint. Contains absolute URI to entity being referenced.
        """
        return pulumi.get(self, "token_endpoint")

    @token_endpoint.setter
    def token_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_endpoint", value)


class AuthorizationServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_endpoint: Optional[pulumi.Input[str]] = None,
                 authorization_methods: Optional[pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]]] = None,
                 authsid: Optional[pulumi.Input[str]] = None,
                 bearer_token_sending_methods: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]]] = None,
                 client_authentication_method: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_registration_endpoint: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 default_scope: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 grant_types: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_owner_password: Optional[pulumi.Input[str]] = None,
                 resource_owner_username: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 support_state: Optional[pulumi.Input[bool]] = None,
                 token_body_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TokenBodyParameterContractArgs']]]]] = None,
                 token_endpoint: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        External OAuth authorization server settings.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_endpoint: OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2.
        :param pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]] authorization_methods: HTTP verbs supported by the authorization endpoint. GET must be always present. POST is optional.
        :param pulumi.Input[str] authsid: Identifier of the authorization server.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]] bearer_token_sending_methods: Specifies the mechanism by which access token is passed to the API. 
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]] client_authentication_method: Method of authentication supported by the token endpoint of this authorization server. Possible values are Basic and/or Body. When Body is specified, client credentials and other parameters are passed within the request body in the application/x-www-form-urlencoded format.
        :param pulumi.Input[str] client_id: Client or app id registered with this authorization server.
        :param pulumi.Input[str] client_registration_endpoint: Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity being referenced.
        :param pulumi.Input[str] client_secret: Client or app secret registered with this authorization server. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        :param pulumi.Input[str] default_scope: Access token scope that is going to be requested by default. Can be overridden at the API level. Should be provided in the form of a string containing space-delimited values.
        :param pulumi.Input[str] description: Description of the authorization server. Can contain HTML formatting tags.
        :param pulumi.Input[str] display_name: User-friendly authorization server name.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]] grant_types: Form of an authorization grant, which the client uses to request the access token.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_owner_password: Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner password.
        :param pulumi.Input[str] resource_owner_username: Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner username.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[bool] support_state: If true, authorization server will include state parameter from the authorization request to its response. Client may use state parameter to raise protocol security.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TokenBodyParameterContractArgs']]]] token_body_parameters: Additional parameters required by the token endpoint of this authorization server represented as an array of JSON objects with name and value string properties, i.e. {"name" : "name value", "value": "a value"}.
        :param pulumi.Input[str] token_endpoint: OAuth token endpoint. Contains absolute URI to entity being referenced.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AuthorizationServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        External OAuth authorization server settings.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param AuthorizationServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AuthorizationServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_endpoint: Optional[pulumi.Input[str]] = None,
                 authorization_methods: Optional[pulumi.Input[Sequence[pulumi.Input['AuthorizationMethod']]]] = None,
                 authsid: Optional[pulumi.Input[str]] = None,
                 bearer_token_sending_methods: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'BearerTokenSendingMethod']]]]] = None,
                 client_authentication_method: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ClientAuthenticationMethod']]]]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_registration_endpoint: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 default_scope: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 grant_types: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'GrantType']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_owner_password: Optional[pulumi.Input[str]] = None,
                 resource_owner_username: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 support_state: Optional[pulumi.Input[bool]] = None,
                 token_body_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TokenBodyParameterContractArgs']]]]] = None,
                 token_endpoint: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AuthorizationServerArgs.__new__(AuthorizationServerArgs)

            if authorization_endpoint is None and not opts.urn:
                raise TypeError("Missing required property 'authorization_endpoint'")
            __props__.__dict__["authorization_endpoint"] = authorization_endpoint
            __props__.__dict__["authorization_methods"] = authorization_methods
            __props__.__dict__["authsid"] = authsid
            __props__.__dict__["bearer_token_sending_methods"] = bearer_token_sending_methods
            __props__.__dict__["client_authentication_method"] = client_authentication_method
            if client_id is None and not opts.urn:
                raise TypeError("Missing required property 'client_id'")
            __props__.__dict__["client_id"] = client_id
            if client_registration_endpoint is None and not opts.urn:
                raise TypeError("Missing required property 'client_registration_endpoint'")
            __props__.__dict__["client_registration_endpoint"] = client_registration_endpoint
            __props__.__dict__["client_secret"] = client_secret
            __props__.__dict__["default_scope"] = default_scope
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if grant_types is None and not opts.urn:
                raise TypeError("Missing required property 'grant_types'")
            __props__.__dict__["grant_types"] = grant_types
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_owner_password"] = resource_owner_password
            __props__.__dict__["resource_owner_username"] = resource_owner_username
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["support_state"] = support_state
            __props__.__dict__["token_body_parameters"] = token_body_parameters
            __props__.__dict__["token_endpoint"] = token_endpoint
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:apimanagement/v20160707:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20161010:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20170301:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20180101:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20180601preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20190101:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20191201:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20191201preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20200601preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20201201:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20210101preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20210401preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20210801:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20211201preview:AuthorizationServer"), pulumi.Alias(type_="azure-native:apimanagement/v20220401preview:AuthorizationServer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AuthorizationServer, __self__).__init__(
            'azure-native:apimanagement:AuthorizationServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AuthorizationServer':
        """
        Get an existing AuthorizationServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AuthorizationServerArgs.__new__(AuthorizationServerArgs)

        __props__.__dict__["authorization_endpoint"] = None
        __props__.__dict__["authorization_methods"] = None
        __props__.__dict__["bearer_token_sending_methods"] = None
        __props__.__dict__["client_authentication_method"] = None
        __props__.__dict__["client_id"] = None
        __props__.__dict__["client_registration_endpoint"] = None
        __props__.__dict__["client_secret"] = None
        __props__.__dict__["default_scope"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["grant_types"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["resource_owner_password"] = None
        __props__.__dict__["resource_owner_username"] = None
        __props__.__dict__["support_state"] = None
        __props__.__dict__["token_body_parameters"] = None
        __props__.__dict__["token_endpoint"] = None
        __props__.__dict__["type"] = None
        return AuthorizationServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authorizationEndpoint")
    def authorization_endpoint(self) -> pulumi.Output[str]:
        """
        OAuth authorization endpoint. See http://tools.ietf.org/html/rfc6749#section-3.2.
        """
        return pulumi.get(self, "authorization_endpoint")

    @property
    @pulumi.getter(name="authorizationMethods")
    def authorization_methods(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        HTTP verbs supported by the authorization endpoint. GET must be always present. POST is optional.
        """
        return pulumi.get(self, "authorization_methods")

    @property
    @pulumi.getter(name="bearerTokenSendingMethods")
    def bearer_token_sending_methods(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies the mechanism by which access token is passed to the API. 
        """
        return pulumi.get(self, "bearer_token_sending_methods")

    @property
    @pulumi.getter(name="clientAuthenticationMethod")
    def client_authentication_method(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Method of authentication supported by the token endpoint of this authorization server. Possible values are Basic and/or Body. When Body is specified, client credentials and other parameters are passed within the request body in the application/x-www-form-urlencoded format.
        """
        return pulumi.get(self, "client_authentication_method")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        Client or app id registered with this authorization server.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientRegistrationEndpoint")
    def client_registration_endpoint(self) -> pulumi.Output[str]:
        """
        Optional reference to a page where client or app registration for this authorization server is performed. Contains absolute URL to entity being referenced.
        """
        return pulumi.get(self, "client_registration_endpoint")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> pulumi.Output[Optional[str]]:
        """
        Client or app secret registered with this authorization server. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="defaultScope")
    def default_scope(self) -> pulumi.Output[Optional[str]]:
        """
        Access token scope that is going to be requested by default. Can be overridden at the API level. Should be provided in the form of a string containing space-delimited values.
        """
        return pulumi.get(self, "default_scope")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the authorization server. Can contain HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        User-friendly authorization server name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="grantTypes")
    def grant_types(self) -> pulumi.Output[Sequence[str]]:
        """
        Form of an authorization grant, which the client uses to request the access token.
        """
        return pulumi.get(self, "grant_types")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceOwnerPassword")
    def resource_owner_password(self) -> pulumi.Output[Optional[str]]:
        """
        Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner password.
        """
        return pulumi.get(self, "resource_owner_password")

    @property
    @pulumi.getter(name="resourceOwnerUsername")
    def resource_owner_username(self) -> pulumi.Output[Optional[str]]:
        """
        Can be optionally specified when resource owner password grant type is supported by this authorization server. Default resource owner username.
        """
        return pulumi.get(self, "resource_owner_username")

    @property
    @pulumi.getter(name="supportState")
    def support_state(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, authorization server will include state parameter from the authorization request to its response. Client may use state parameter to raise protocol security.
        """
        return pulumi.get(self, "support_state")

    @property
    @pulumi.getter(name="tokenBodyParameters")
    def token_body_parameters(self) -> pulumi.Output[Optional[Sequence['outputs.TokenBodyParameterContractResponse']]]:
        """
        Additional parameters required by the token endpoint of this authorization server represented as an array of JSON objects with name and value string properties, i.e. {"name" : "name value", "value": "a value"}.
        """
        return pulumi.get(self, "token_body_parameters")

    @property
    @pulumi.getter(name="tokenEndpoint")
    def token_endpoint(self) -> pulumi.Output[Optional[str]]:
        """
        OAuth token endpoint. Contains absolute URI to entity being referenced.
        """
        return pulumi.get(self, "token_endpoint")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

