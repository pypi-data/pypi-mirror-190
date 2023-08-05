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

__all__ = [
    'InboundEndpointIPConfigurationResponse',
    'SubResourceResponse',
    'SystemDataResponse',
    'TargetDnsServerResponse',
    'VirtualNetworkDnsForwardingRulesetResponse',
]

@pulumi.output_type
class InboundEndpointIPConfigurationResponse(dict):
    """
    IP configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "privateIpAllocationMethod":
            suggest = "private_ip_allocation_method"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InboundEndpointIPConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InboundEndpointIPConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InboundEndpointIPConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 private_ip_address: Optional[str] = None,
                 private_ip_allocation_method: Optional[str] = None,
                 subnet: Optional['outputs.SubResourceResponse'] = None):
        """
        IP configuration.
        :param str private_ip_address: Private IP address of the IP configuration.
        :param str private_ip_allocation_method: Private IP address allocation method.
        :param 'SubResourceResponse' subnet: The reference to the subnet bound to the IP configuration.
        """
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if private_ip_allocation_method is None:
            private_ip_allocation_method = 'Dynamic'
        if private_ip_allocation_method is not None:
            pulumi.set(__self__, "private_ip_allocation_method", private_ip_allocation_method)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        Private IP address of the IP configuration.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIpAllocationMethod")
    def private_ip_allocation_method(self) -> Optional[str]:
        """
        Private IP address allocation method.
        """
        return pulumi.get(self, "private_ip_allocation_method")

    @property
    @pulumi.getter
    def subnet(self) -> Optional['outputs.SubResourceResponse']:
        """
        The reference to the subnet bound to the IP configuration.
        """
        return pulumi.get(self, "subnet")


@pulumi.output_type
class SubResourceResponse(dict):
    """
    Reference to another ARM resource.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Reference to another ARM resource.
        :param str id: Resource ID.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")


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


@pulumi.output_type
class TargetDnsServerResponse(dict):
    """
    Describes a server to forward the DNS queries to.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddress":
            suggest = "ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TargetDnsServerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TargetDnsServerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TargetDnsServerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address: Optional[str] = None,
                 port: Optional[int] = None):
        """
        Describes a server to forward the DNS queries to.
        :param str ip_address: DNS server IP address.
        :param int port: DNS server port.
        """
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if port is None:
            port = 53
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[str]:
        """
        DNS server IP address.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        DNS server port.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class VirtualNetworkDnsForwardingRulesetResponse(dict):
    """
    Reference to DNS forwarding ruleset and associated virtual network link.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 virtual_network_link: Optional['outputs.SubResourceResponse'] = None):
        """
        Reference to DNS forwarding ruleset and associated virtual network link.
        :param str id: DNS Forwarding Ruleset Resource ID.
        :param 'SubResourceResponse' virtual_network_link: The reference to the virtual network link.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if virtual_network_link is not None:
            pulumi.set(__self__, "virtual_network_link", virtual_network_link)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        DNS Forwarding Ruleset Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="virtualNetworkLink")
    def virtual_network_link(self) -> Optional['outputs.SubResourceResponse']:
        """
        The reference to the virtual network link.
        """
        return pulumi.get(self, "virtual_network_link")


