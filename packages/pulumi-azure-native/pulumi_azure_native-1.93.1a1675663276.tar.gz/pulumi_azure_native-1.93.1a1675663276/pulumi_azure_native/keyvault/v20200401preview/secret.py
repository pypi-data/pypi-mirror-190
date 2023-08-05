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
from ._inputs import *

__all__ = ['SecretArgs', 'Secret']

@pulumi.input_type
class SecretArgs:
    def __init__(__self__, *,
                 properties: pulumi.Input['SecretPropertiesArgs'],
                 resource_group_name: pulumi.Input[str],
                 vault_name: pulumi.Input[str],
                 secret_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Secret resource.
        :param pulumi.Input['SecretPropertiesArgs'] properties: Properties of the secret
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group to which the vault belongs.
        :param pulumi.Input[str] vault_name: Name of the vault
        :param pulumi.Input[str] secret_name: Name of the secret
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the secret. 
        """
        pulumi.set(__self__, "properties", properties)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "vault_name", vault_name)
        if secret_name is not None:
            pulumi.set(__self__, "secret_name", secret_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['SecretPropertiesArgs']:
        """
        Properties of the secret
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: pulumi.Input['SecretPropertiesArgs']):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group to which the vault belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        Name of the vault
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the secret
        """
        return pulumi.get(self, "secret_name")

    @secret_name.setter
    def secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags that will be assigned to the secret. 
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Secret(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['SecretPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 secret_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource information with extended details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SecretPropertiesArgs']] properties: Properties of the secret
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group to which the vault belongs.
        :param pulumi.Input[str] secret_name: Name of the secret
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the secret. 
        :param pulumi.Input[str] vault_name: Name of the vault
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecretArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource information with extended details.

        :param str resource_name: The name of the resource.
        :param SecretArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecretArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['SecretPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 secret_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecretArgs.__new__(SecretArgs)

            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["secret_name"] = secret_name
            __props__.__dict__["tags"] = tags
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:keyvault:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20161001:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20180214:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20180214preview:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20190901:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20210401preview:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20210601preview:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20211001:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20211101preview:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20220201preview:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20220701:Secret"), pulumi.Alias(type_="azure-native:keyvault/v20221101:Secret")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Secret, __self__).__init__(
            'azure-native:keyvault/v20200401preview:Secret',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Secret':
        """
        Get an existing Secret resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SecretArgs.__new__(SecretArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Secret(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Azure location of the key vault resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the key vault resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.SecretPropertiesResponse']:
        """
        Properties of the secret
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Tags assigned to the key vault resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type of the key vault resource.
        """
        return pulumi.get(self, "type")

