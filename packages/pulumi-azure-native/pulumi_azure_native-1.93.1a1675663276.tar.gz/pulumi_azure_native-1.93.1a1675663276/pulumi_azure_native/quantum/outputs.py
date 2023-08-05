# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ProviderResponse',
    'QuantumWorkspaceResponseIdentity',
    'SystemDataResponse',
]

@pulumi.output_type
class ProviderResponse(dict):
    """
    Information about a Provider. A Provider is an entity that offers Targets to run Azure Quantum Jobs.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationName":
            suggest = "application_name"
        elif key == "instanceUri":
            suggest = "instance_uri"
        elif key == "providerId":
            suggest = "provider_id"
        elif key == "providerSku":
            suggest = "provider_sku"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "resourceUsageId":
            suggest = "resource_usage_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ProviderResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ProviderResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ProviderResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_name: Optional[str] = None,
                 instance_uri: Optional[str] = None,
                 provider_id: Optional[str] = None,
                 provider_sku: Optional[str] = None,
                 provisioning_state: Optional[str] = None,
                 resource_usage_id: Optional[str] = None):
        """
        Information about a Provider. A Provider is an entity that offers Targets to run Azure Quantum Jobs.
        :param str application_name: The provider's marketplace application display name.
        :param str instance_uri: A Uri identifying the specific instance of this provider.
        :param str provider_id: Unique id of this provider.
        :param str provider_sku: The sku associated with pricing information for this provider.
        :param str provisioning_state: Provisioning status field
        :param str resource_usage_id: Id to track resource usage for the provider.
        """
        if application_name is not None:
            pulumi.set(__self__, "application_name", application_name)
        if instance_uri is not None:
            pulumi.set(__self__, "instance_uri", instance_uri)
        if provider_id is not None:
            pulumi.set(__self__, "provider_id", provider_id)
        if provider_sku is not None:
            pulumi.set(__self__, "provider_sku", provider_sku)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_usage_id is not None:
            pulumi.set(__self__, "resource_usage_id", resource_usage_id)

    @property
    @pulumi.getter(name="applicationName")
    def application_name(self) -> Optional[str]:
        """
        The provider's marketplace application display name.
        """
        return pulumi.get(self, "application_name")

    @property
    @pulumi.getter(name="instanceUri")
    def instance_uri(self) -> Optional[str]:
        """
        A Uri identifying the specific instance of this provider.
        """
        return pulumi.get(self, "instance_uri")

    @property
    @pulumi.getter(name="providerId")
    def provider_id(self) -> Optional[str]:
        """
        Unique id of this provider.
        """
        return pulumi.get(self, "provider_id")

    @property
    @pulumi.getter(name="providerSku")
    def provider_sku(self) -> Optional[str]:
        """
        The sku associated with pricing information for this provider.
        """
        return pulumi.get(self, "provider_sku")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning status field
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceUsageId")
    def resource_usage_id(self) -> Optional[str]:
        """
        Id to track resource usage for the provider.
        """
        return pulumi.get(self, "resource_usage_id")


@pulumi.output_type
class QuantumWorkspaceResponseIdentity(dict):
    """
    Managed Identity information.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in QuantumWorkspaceResponseIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        QuantumWorkspaceResponseIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        QuantumWorkspaceResponseIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        Managed Identity information.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: The identity type.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")


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


