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
    'GetStorageAccountCredentialResult',
    'AwaitableGetStorageAccountCredentialResult',
    'get_storage_account_credential',
    'get_storage_account_credential_output',
]

@pulumi.output_type
class GetStorageAccountCredentialResult:
    """
    The storage account credential.
    """
    def __init__(__self__, account_key=None, account_type=None, alias=None, blob_domain_name=None, connection_string=None, id=None, name=None, ssl_status=None, storage_account_id=None, system_data=None, type=None, user_name=None):
        if account_key and not isinstance(account_key, dict):
            raise TypeError("Expected argument 'account_key' to be a dict")
        pulumi.set(__self__, "account_key", account_key)
        if account_type and not isinstance(account_type, str):
            raise TypeError("Expected argument 'account_type' to be a str")
        pulumi.set(__self__, "account_type", account_type)
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        pulumi.set(__self__, "alias", alias)
        if blob_domain_name and not isinstance(blob_domain_name, str):
            raise TypeError("Expected argument 'blob_domain_name' to be a str")
        pulumi.set(__self__, "blob_domain_name", blob_domain_name)
        if connection_string and not isinstance(connection_string, str):
            raise TypeError("Expected argument 'connection_string' to be a str")
        pulumi.set(__self__, "connection_string", connection_string)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if ssl_status and not isinstance(ssl_status, str):
            raise TypeError("Expected argument 'ssl_status' to be a str")
        pulumi.set(__self__, "ssl_status", ssl_status)
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError("Expected argument 'storage_account_id' to be a str")
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> Optional['outputs.AsymmetricEncryptedSecretResponse']:
        """
        Encrypted storage key.
        """
        return pulumi.get(self, "account_key")

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> str:
        """
        Type of storage accessed on the storage account.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter
    def alias(self) -> str:
        """
        Alias for the storage account.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="blobDomainName")
    def blob_domain_name(self) -> Optional[str]:
        """
        Blob end point for private clouds.
        """
        return pulumi.get(self, "blob_domain_name")

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[str]:
        """
        Connection string for the storage account. Use this string if username and account key are not specified.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sslStatus")
    def ssl_status(self) -> str:
        """
        Signifies whether SSL needs to be enabled or not.
        """
        return pulumi.get(self, "ssl_status")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> Optional[str]:
        """
        Id of the storage account.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        StorageAccountCredential object
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[str]:
        """
        Username for the storage account.
        """
        return pulumi.get(self, "user_name")


class AwaitableGetStorageAccountCredentialResult(GetStorageAccountCredentialResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageAccountCredentialResult(
            account_key=self.account_key,
            account_type=self.account_type,
            alias=self.alias,
            blob_domain_name=self.blob_domain_name,
            connection_string=self.connection_string,
            id=self.id,
            name=self.name,
            ssl_status=self.ssl_status,
            storage_account_id=self.storage_account_id,
            system_data=self.system_data,
            type=self.type,
            user_name=self.user_name)


def get_storage_account_credential(device_name: Optional[str] = None,
                                   name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageAccountCredentialResult:
    """
    The storage account credential.


    :param str device_name: The device name.
    :param str name: The storage account credential name.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge/v20201201:getStorageAccountCredential', __args__, opts=opts, typ=GetStorageAccountCredentialResult).value

    return AwaitableGetStorageAccountCredentialResult(
        account_key=__ret__.account_key,
        account_type=__ret__.account_type,
        alias=__ret__.alias,
        blob_domain_name=__ret__.blob_domain_name,
        connection_string=__ret__.connection_string,
        id=__ret__.id,
        name=__ret__.name,
        ssl_status=__ret__.ssl_status,
        storage_account_id=__ret__.storage_account_id,
        system_data=__ret__.system_data,
        type=__ret__.type,
        user_name=__ret__.user_name)


@_utilities.lift_output_func(get_storage_account_credential)
def get_storage_account_credential_output(device_name: Optional[pulumi.Input[str]] = None,
                                          name: Optional[pulumi.Input[str]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStorageAccountCredentialResult]:
    """
    The storage account credential.


    :param str device_name: The device name.
    :param str name: The storage account credential name.
    :param str resource_group_name: The resource group name.
    """
    ...
