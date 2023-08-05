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

__all__ = ['RoleAssignmentArgs', 'RoleAssignment']

@pulumi.input_type
class RoleAssignmentArgs:
    def __init__(__self__, *,
                 principal_id: pulumi.Input[str],
                 role_definition_id: pulumi.Input[str],
                 scope: pulumi.Input[str],
                 can_delegate: Optional[pulumi.Input[bool]] = None,
                 condition: Optional[pulumi.Input[str]] = None,
                 condition_version: Optional[pulumi.Input[str]] = None,
                 delegated_managed_identity_resource_id: Optional[pulumi.Input[str]] = None,
                 principal_type: Optional[pulumi.Input[Union[str, 'PrincipalType']]] = None,
                 role_assignment_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RoleAssignment resource.
        :param pulumi.Input[str] principal_id: The principal ID.
        :param pulumi.Input[str] role_definition_id: The role definition ID.
        :param pulumi.Input[str] scope: The role assignment scope.
        :param pulumi.Input[bool] can_delegate: The delegation flag used for creating a role assignment
        :param pulumi.Input[str] condition: The conditions on the role assignment. This limits the resources it can be assigned to. e.g.: @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:ContainerName] StringEqualsIgnoreCase 'foo_storage_container'
        :param pulumi.Input[str] condition_version: Version of the condition. Currently accepted value is '2.0'
        :param pulumi.Input[str] delegated_managed_identity_resource_id: Id of the delegated managed identity resource
        :param pulumi.Input[Union[str, 'PrincipalType']] principal_type: The principal type of the assigned principal ID.
        :param pulumi.Input[str] role_assignment_name: The name of the role assignment. It can be any valid GUID.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)
        pulumi.set(__self__, "scope", scope)
        if can_delegate is not None:
            pulumi.set(__self__, "can_delegate", can_delegate)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if condition_version is not None:
            pulumi.set(__self__, "condition_version", condition_version)
        if delegated_managed_identity_resource_id is not None:
            pulumi.set(__self__, "delegated_managed_identity_resource_id", delegated_managed_identity_resource_id)
        if principal_type is None:
            principal_type = 'User'
        if principal_type is not None:
            pulumi.set(__self__, "principal_type", principal_type)
        if role_assignment_name is not None:
            pulumi.set(__self__, "role_assignment_name", role_assignment_name)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Input[str]:
        """
        The principal ID.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> pulumi.Input[str]:
        """
        The role definition ID.
        """
        return pulumi.get(self, "role_definition_id")

    @role_definition_id.setter
    def role_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_definition_id", value)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The role assignment scope.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="canDelegate")
    def can_delegate(self) -> Optional[pulumi.Input[bool]]:
        """
        The delegation flag used for creating a role assignment
        """
        return pulumi.get(self, "can_delegate")

    @can_delegate.setter
    def can_delegate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "can_delegate", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input[str]]:
        """
        The conditions on the role assignment. This limits the resources it can be assigned to. e.g.: @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:ContainerName] StringEqualsIgnoreCase 'foo_storage_container'
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter(name="conditionVersion")
    def condition_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the condition. Currently accepted value is '2.0'
        """
        return pulumi.get(self, "condition_version")

    @condition_version.setter
    def condition_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "condition_version", value)

    @property
    @pulumi.getter(name="delegatedManagedIdentityResourceId")
    def delegated_managed_identity_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the delegated managed identity resource
        """
        return pulumi.get(self, "delegated_managed_identity_resource_id")

    @delegated_managed_identity_resource_id.setter
    def delegated_managed_identity_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delegated_managed_identity_resource_id", value)

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> Optional[pulumi.Input[Union[str, 'PrincipalType']]]:
        """
        The principal type of the assigned principal ID.
        """
        return pulumi.get(self, "principal_type")

    @principal_type.setter
    def principal_type(self, value: Optional[pulumi.Input[Union[str, 'PrincipalType']]]):
        pulumi.set(self, "principal_type", value)

    @property
    @pulumi.getter(name="roleAssignmentName")
    def role_assignment_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the role assignment. It can be any valid GUID.
        """
        return pulumi.get(self, "role_assignment_name")

    @role_assignment_name.setter
    def role_assignment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_assignment_name", value)


class RoleAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 can_delegate: Optional[pulumi.Input[bool]] = None,
                 condition: Optional[pulumi.Input[str]] = None,
                 condition_version: Optional[pulumi.Input[str]] = None,
                 delegated_managed_identity_resource_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 principal_type: Optional[pulumi.Input[Union[str, 'PrincipalType']]] = None,
                 role_assignment_name: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Role Assignments

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] can_delegate: The delegation flag used for creating a role assignment
        :param pulumi.Input[str] condition: The conditions on the role assignment. This limits the resources it can be assigned to. e.g.: @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:ContainerName] StringEqualsIgnoreCase 'foo_storage_container'
        :param pulumi.Input[str] condition_version: Version of the condition. Currently accepted value is '2.0'
        :param pulumi.Input[str] delegated_managed_identity_resource_id: Id of the delegated managed identity resource
        :param pulumi.Input[str] principal_id: The principal ID.
        :param pulumi.Input[Union[str, 'PrincipalType']] principal_type: The principal type of the assigned principal ID.
        :param pulumi.Input[str] role_assignment_name: The name of the role assignment. It can be any valid GUID.
        :param pulumi.Input[str] role_definition_id: The role definition ID.
        :param pulumi.Input[str] scope: The role assignment scope.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RoleAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Role Assignments

        :param str resource_name: The name of the resource.
        :param RoleAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 can_delegate: Optional[pulumi.Input[bool]] = None,
                 condition: Optional[pulumi.Input[str]] = None,
                 condition_version: Optional[pulumi.Input[str]] = None,
                 delegated_managed_identity_resource_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 principal_type: Optional[pulumi.Input[Union[str, 'PrincipalType']]] = None,
                 role_assignment_name: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleAssignmentArgs.__new__(RoleAssignmentArgs)

            __props__.__dict__["can_delegate"] = can_delegate
            __props__.__dict__["condition"] = condition
            __props__.__dict__["condition_version"] = condition_version
            __props__.__dict__["delegated_managed_identity_resource_id"] = delegated_managed_identity_resource_id
            if principal_id is None and not opts.urn:
                raise TypeError("Missing required property 'principal_id'")
            __props__.__dict__["principal_id"] = principal_id
            if principal_type is None:
                principal_type = 'User'
            __props__.__dict__["principal_type"] = principal_type
            __props__.__dict__["role_assignment_name"] = role_assignment_name
            if role_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'role_definition_id'")
            __props__.__dict__["role_definition_id"] = role_definition_id
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["created_by"] = None
            __props__.__dict__["created_on"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["updated_by"] = None
            __props__.__dict__["updated_on"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:authorization:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20150701:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20171001preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20180101preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20180901preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20200401preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20200801preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20201001preview:RoleAssignment"), pulumi.Alias(type_="azure-native:authorization/v20220401:RoleAssignment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RoleAssignment, __self__).__init__(
            'azure-native:authorization/v20200301preview:RoleAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RoleAssignment':
        """
        Get an existing RoleAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RoleAssignmentArgs.__new__(RoleAssignmentArgs)

        __props__.__dict__["can_delegate"] = None
        __props__.__dict__["condition"] = None
        __props__.__dict__["condition_version"] = None
        __props__.__dict__["created_by"] = None
        __props__.__dict__["created_on"] = None
        __props__.__dict__["delegated_managed_identity_resource_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["principal_id"] = None
        __props__.__dict__["principal_type"] = None
        __props__.__dict__["role_definition_id"] = None
        __props__.__dict__["scope"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["updated_by"] = None
        __props__.__dict__["updated_on"] = None
        return RoleAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="canDelegate")
    def can_delegate(self) -> pulumi.Output[Optional[bool]]:
        """
        The delegation flag used for creating a role assignment
        """
        return pulumi.get(self, "can_delegate")

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional[str]]:
        """
        The conditions on the role assignment. This limits the resources it can be assigned to. e.g.: @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:ContainerName] StringEqualsIgnoreCase 'foo_storage_container'
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="conditionVersion")
    def condition_version(self) -> pulumi.Output[Optional[str]]:
        """
        Version of the condition. Currently accepted value is '2.0'
        """
        return pulumi.get(self, "condition_version")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[str]:
        """
        Id of the user who created the assignment
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> pulumi.Output[str]:
        """
        Time it was created
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="delegatedManagedIdentityResourceId")
    def delegated_managed_identity_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the delegated managed identity resource
        """
        return pulumi.get(self, "delegated_managed_identity_resource_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The role assignment name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Output[str]:
        """
        The principal ID.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> pulumi.Output[Optional[str]]:
        """
        The principal type of the assigned principal ID.
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> pulumi.Output[str]:
        """
        The role definition ID.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Optional[str]]:
        """
        The role assignment scope.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The role assignment type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> pulumi.Output[str]:
        """
        Id of the user who updated the assignment
        """
        return pulumi.get(self, "updated_by")

    @property
    @pulumi.getter(name="updatedOn")
    def updated_on(self) -> pulumi.Output[str]:
        """
        Time it was updated
        """
        return pulumi.get(self, "updated_on")

