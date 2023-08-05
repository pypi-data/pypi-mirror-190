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
    'DataPoolEncryptionResponse',
    'DataPoolLocationResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class DataPoolEncryptionResponse(dict):
    """
    Encryption properties of a Data Pool
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyName":
            suggest = "key_name"
        elif key == "keyVaultUri":
            suggest = "key_vault_uri"
        elif key == "userAssignedIdentity":
            suggest = "user_assigned_identity"
        elif key == "keyVersion":
            suggest = "key_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DataPoolEncryptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DataPoolEncryptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DataPoolEncryptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_name: str,
                 key_vault_uri: str,
                 user_assigned_identity: str,
                 key_version: Optional[str] = None):
        """
        Encryption properties of a Data Pool
        :param str key_name: The name of Key Vault key
        :param str key_vault_uri: The URI of a soft delete-enabled Key Vault that is in the same location as the Data Pool location
        :param str user_assigned_identity: The resource ID of a user-assigned Managed Identity used to access the encryption key in the Key Vault. Requires access to the key operations get, wrap, unwrap, and recover
        :param str key_version: The version of Key Vault key
        """
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        pulumi.set(__self__, "user_assigned_identity", user_assigned_identity)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        """
        The name of Key Vault key
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> str:
        """
        The URI of a soft delete-enabled Key Vault that is in the same location as the Data Pool location
        """
        return pulumi.get(self, "key_vault_uri")

    @property
    @pulumi.getter(name="userAssignedIdentity")
    def user_assigned_identity(self) -> str:
        """
        The resource ID of a user-assigned Managed Identity used to access the encryption key in the Key Vault. Requires access to the key operations get, wrap, unwrap, and recover
        """
        return pulumi.get(self, "user_assigned_identity")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The version of Key Vault key
        """
        return pulumi.get(self, "key_version")


@pulumi.output_type
class DataPoolLocationResponse(dict):
    """
    Location of a Data Pool
    """
    def __init__(__self__, *,
                 name: str,
                 encryption: Optional['outputs.DataPoolEncryptionResponse'] = None):
        """
        Location of a Data Pool
        :param str name: The location name
        :param 'DataPoolEncryptionResponse' encryption: Encryption properties of a Data Pool location
        """
        pulumi.set(__self__, "name", name)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The location name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.DataPoolEncryptionResponse']:
        """
        Encryption properties of a Data Pool location
        """
        return pulumi.get(self, "encryption")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


