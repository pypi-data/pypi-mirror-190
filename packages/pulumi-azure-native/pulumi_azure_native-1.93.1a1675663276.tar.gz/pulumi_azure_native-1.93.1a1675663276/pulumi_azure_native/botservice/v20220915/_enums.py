# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'Kind',
    'MsaAppType',
    'PrivateEndpointServiceConnectionStatus',
    'PublicNetworkAccess',
    'SkuName',
]


class Kind(str, Enum):
    """
    Required. Gets or sets the Kind of the resource.
    """
    SDK = "sdk"
    DESIGNER = "designer"
    BOT = "bot"
    FUNCTION = "function"
    AZUREBOT = "azurebot"


class MsaAppType(str, Enum):
    """
    Microsoft App Type for the bot
    """
    USER_ASSIGNED_MSI = "UserAssignedMSI"
    SINGLE_TENANT = "SingleTenant"
    MULTI_TENANT = "MultiTenant"


class PrivateEndpointServiceConnectionStatus(str, Enum):
    """
    Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
    """
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class PublicNetworkAccess(str, Enum):
    """
    Whether the bot is in an isolated network
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class SkuName(str, Enum):
    """
    The sku name
    """
    F0 = "F0"
    S1 = "S1"
