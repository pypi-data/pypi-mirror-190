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
    'DescendantParentGroupInfoResponse',
    'EntityInfoResponse',
    'EntityParentGroupInfoResponse',
    'ManagementGroupChildInfoResponse',
    'ManagementGroupDetailsResponse',
    'ManagementGroupPathElementResponse',
    'ParentGroupInfoResponse',
]

@pulumi.output_type
class DescendantParentGroupInfoResponse(dict):
    """
    The ID of the parent management group.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        The ID of the parent management group.
        :param str id: The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class EntityInfoResponse(dict):
    """
    The entity.
    """
    def __init__(__self__, *,
                 id: str,
                 name: str,
                 type: str,
                 display_name: Optional[str] = None,
                 inherited_permissions: Optional[str] = None,
                 number_of_child_groups: Optional[int] = None,
                 number_of_children: Optional[int] = None,
                 number_of_descendants: Optional[int] = None,
                 parent: Optional['outputs.EntityParentGroupInfoResponse'] = None,
                 parent_display_name_chain: Optional[Sequence[str]] = None,
                 parent_name_chain: Optional[Sequence[str]] = None,
                 permissions: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        The entity.
        :param str id: The fully qualified ID for the entity.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        :param str name: The name of the entity. For example, 00000000-0000-0000-0000-000000000000
        :param str type: The type of the resource. For example, Microsoft.Management/managementGroups
        :param str display_name: The friendly name of the management group.
        :param str inherited_permissions: The users specific permissions to this item.
        :param int number_of_child_groups: Number of children is the number of Groups that are exactly one level underneath the current Group.
        :param int number_of_children: Number of children is the number of Groups and Subscriptions that are exactly one level underneath the current Group.
        :param 'EntityParentGroupInfoResponse' parent: (Optional) The ID of the parent management group.
        :param Sequence[str] parent_display_name_chain: The parent display name chain from the root group to the immediate parent
        :param Sequence[str] parent_name_chain: The parent name chain from the root group to the immediate parent
        :param str permissions: The users specific permissions to this item.
        :param str tenant_id: The AAD Tenant ID associated with the entity. For example, 00000000-0000-0000-0000-000000000000
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if inherited_permissions is not None:
            pulumi.set(__self__, "inherited_permissions", inherited_permissions)
        if number_of_child_groups is not None:
            pulumi.set(__self__, "number_of_child_groups", number_of_child_groups)
        if number_of_children is not None:
            pulumi.set(__self__, "number_of_children", number_of_children)
        if number_of_descendants is not None:
            pulumi.set(__self__, "number_of_descendants", number_of_descendants)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if parent_display_name_chain is not None:
            pulumi.set(__self__, "parent_display_name_chain", parent_display_name_chain)
        if parent_name_chain is not None:
            pulumi.set(__self__, "parent_name_chain", parent_name_chain)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The fully qualified ID for the entity.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the entity. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. For example, Microsoft.Management/managementGroups
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the management group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="inheritedPermissions")
    def inherited_permissions(self) -> Optional[str]:
        """
        The users specific permissions to this item.
        """
        return pulumi.get(self, "inherited_permissions")

    @property
    @pulumi.getter(name="numberOfChildGroups")
    def number_of_child_groups(self) -> Optional[int]:
        """
        Number of children is the number of Groups that are exactly one level underneath the current Group.
        """
        return pulumi.get(self, "number_of_child_groups")

    @property
    @pulumi.getter(name="numberOfChildren")
    def number_of_children(self) -> Optional[int]:
        """
        Number of children is the number of Groups and Subscriptions that are exactly one level underneath the current Group.
        """
        return pulumi.get(self, "number_of_children")

    @property
    @pulumi.getter(name="numberOfDescendants")
    def number_of_descendants(self) -> Optional[int]:
        return pulumi.get(self, "number_of_descendants")

    @property
    @pulumi.getter
    def parent(self) -> Optional['outputs.EntityParentGroupInfoResponse']:
        """
        (Optional) The ID of the parent management group.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="parentDisplayNameChain")
    def parent_display_name_chain(self) -> Optional[Sequence[str]]:
        """
        The parent display name chain from the root group to the immediate parent
        """
        return pulumi.get(self, "parent_display_name_chain")

    @property
    @pulumi.getter(name="parentNameChain")
    def parent_name_chain(self) -> Optional[Sequence[str]]:
        """
        The parent name chain from the root group to the immediate parent
        """
        return pulumi.get(self, "parent_name_chain")

    @property
    @pulumi.getter
    def permissions(self) -> Optional[str]:
        """
        The users specific permissions to this item.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The AAD Tenant ID associated with the entity. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class EntityParentGroupInfoResponse(dict):
    """
    (Optional) The ID of the parent management group.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        (Optional) The ID of the parent management group.
        :param str id: The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class ManagementGroupChildInfoResponse(dict):
    """
    The child information of a management group.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagementGroupChildInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagementGroupChildInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagementGroupChildInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 children: Optional[Sequence['outputs.ManagementGroupChildInfoResponse']] = None,
                 display_name: Optional[str] = None,
                 id: Optional[str] = None,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        The child information of a management group.
        :param Sequence['ManagementGroupChildInfoResponse'] children: The list of children.
        :param str display_name: The friendly name of the child resource.
        :param str id: The fully qualified ID for the child resource (management group or subscription).  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        :param str name: The name of the child entity.
        :param str type: The fully qualified resource type which includes provider namespace (e.g. Microsoft.Management/managementGroups)
        """
        if children is not None:
            pulumi.set(__self__, "children", children)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def children(self) -> Optional[Sequence['outputs.ManagementGroupChildInfoResponse']]:
        """
        The list of children.
        """
        return pulumi.get(self, "children")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the child resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The fully qualified ID for the child resource (management group or subscription).  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the child entity.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The fully qualified resource type which includes provider namespace (e.g. Microsoft.Management/managementGroups)
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class ManagementGroupDetailsResponse(dict):
    """
    The details of a management group.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "updatedBy":
            suggest = "updated_by"
        elif key == "updatedTime":
            suggest = "updated_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagementGroupDetailsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagementGroupDetailsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagementGroupDetailsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 parent: Optional['outputs.ParentGroupInfoResponse'] = None,
                 path: Optional[Sequence['outputs.ManagementGroupPathElementResponse']] = None,
                 updated_by: Optional[str] = None,
                 updated_time: Optional[str] = None,
                 version: Optional[float] = None):
        """
        The details of a management group.
        :param 'ParentGroupInfoResponse' parent: (Optional) The ID of the parent management group.
        :param Sequence['ManagementGroupPathElementResponse'] path: The path from the root to the current group.
        :param str updated_by: The identity of the principal or process that updated the object.
        :param str updated_time: The date and time when this object was last updated.
        :param float version: The version number of the object.
        """
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if updated_by is not None:
            pulumi.set(__self__, "updated_by", updated_by)
        if updated_time is not None:
            pulumi.set(__self__, "updated_time", updated_time)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def parent(self) -> Optional['outputs.ParentGroupInfoResponse']:
        """
        (Optional) The ID of the parent management group.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def path(self) -> Optional[Sequence['outputs.ManagementGroupPathElementResponse']]:
        """
        The path from the root to the current group.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> Optional[str]:
        """
        The identity of the principal or process that updated the object.
        """
        return pulumi.get(self, "updated_by")

    @property
    @pulumi.getter(name="updatedTime")
    def updated_time(self) -> Optional[str]:
        """
        The date and time when this object was last updated.
        """
        return pulumi.get(self, "updated_time")

    @property
    @pulumi.getter
    def version(self) -> Optional[float]:
        """
        The version number of the object.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class ManagementGroupPathElementResponse(dict):
    """
    A path element of a management group ancestors.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagementGroupPathElementResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagementGroupPathElementResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagementGroupPathElementResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 display_name: Optional[str] = None,
                 name: Optional[str] = None):
        """
        A path element of a management group ancestors.
        :param str display_name: The friendly name of the group.
        :param str name: The name of the group.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the group.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class ParentGroupInfoResponse(dict):
    """
    (Optional) The ID of the parent management group.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ParentGroupInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ParentGroupInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ParentGroupInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 display_name: Optional[str] = None,
                 id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        (Optional) The ID of the parent management group.
        :param str display_name: The friendly name of the parent management group.
        :param str id: The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        :param str name: The name of the parent management group
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The friendly name of the parent management group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The fully qualified ID for the parent management group.  For example, /providers/Microsoft.Management/managementGroups/0000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the parent management group
        """
        return pulumi.get(self, "name")


