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

__all__ = [
    'DigitalTwinsSkuInfoResponse',
    'EventGridResponse',
    'EventHubResponse',
    'ServiceBusResponse',
]

@pulumi.output_type
class DigitalTwinsSkuInfoResponse(dict):
    """
    Information about the SKU of the DigitalTwinsInstance.
    """
    def __init__(__self__, *,
                 name: str):
        """
        Information about the SKU of the DigitalTwinsInstance.
        :param str name: The name of the SKU.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class EventGridResponse(dict):
    """
    properties related to eventgrid.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessKey1":
            suggest = "access_key1"
        elif key == "accessKey2":
            suggest = "access_key2"
        elif key == "createdTime":
            suggest = "created_time"
        elif key == "endpointType":
            suggest = "endpoint_type"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "topicEndpoint":
            suggest = "topic_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventGridResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventGridResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventGridResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_key1: str,
                 access_key2: str,
                 created_time: str,
                 endpoint_type: str,
                 provisioning_state: str,
                 tags: Optional[Mapping[str, str]] = None,
                 topic_endpoint: Optional[str] = None):
        """
        properties related to eventgrid.
        :param str access_key1: EventGrid secondary accesskey. Will be obfuscated during read
        :param str access_key2: EventGrid secondary accesskey. Will be obfuscated during read
        :param str created_time: Time when the Endpoint was added to DigitalTwinsInstance.
        :param str endpoint_type: The type of Digital Twins endpoint
               Expected value is 'EventGrid'.
        :param str provisioning_state: The provisioning state.
        :param Mapping[str, str] tags: The resource tags.
        :param str topic_endpoint: EventGrid Topic Endpoint
        """
        pulumi.set(__self__, "access_key1", access_key1)
        pulumi.set(__self__, "access_key2", access_key2)
        pulumi.set(__self__, "created_time", created_time)
        pulumi.set(__self__, "endpoint_type", 'EventGrid')
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if topic_endpoint is not None:
            pulumi.set(__self__, "topic_endpoint", topic_endpoint)

    @property
    @pulumi.getter(name="accessKey1")
    def access_key1(self) -> str:
        """
        EventGrid secondary accesskey. Will be obfuscated during read
        """
        return pulumi.get(self, "access_key1")

    @property
    @pulumi.getter(name="accessKey2")
    def access_key2(self) -> str:
        """
        EventGrid secondary accesskey. Will be obfuscated during read
        """
        return pulumi.get(self, "access_key2")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        """
        Time when the Endpoint was added to DigitalTwinsInstance.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        The type of Digital Twins endpoint
        Expected value is 'EventGrid'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="topicEndpoint")
    def topic_endpoint(self) -> Optional[str]:
        """
        EventGrid Topic Endpoint
        """
        return pulumi.get(self, "topic_endpoint")


@pulumi.output_type
class EventHubResponse(dict):
    """
    properties related to eventhub.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "connectionStringPrimaryKey":
            suggest = "connection_string_primary_key"
        elif key == "connectionStringSecondaryKey":
            suggest = "connection_string_secondary_key"
        elif key == "createdTime":
            suggest = "created_time"
        elif key == "endpointType":
            suggest = "endpoint_type"
        elif key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventHubResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventHubResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventHubResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 connection_string_primary_key: str,
                 connection_string_secondary_key: str,
                 created_time: str,
                 endpoint_type: str,
                 provisioning_state: str,
                 tags: Optional[Mapping[str, str]] = None):
        """
        properties related to eventhub.
        :param str connection_string_primary_key: PrimaryConnectionString of the endpoint. Will be obfuscated during read
        :param str connection_string_secondary_key: SecondaryConnectionString of the endpoint. Will be obfuscated during read
        :param str created_time: Time when the Endpoint was added to DigitalTwinsInstance.
        :param str endpoint_type: The type of Digital Twins endpoint
               Expected value is 'EventHub'.
        :param str provisioning_state: The provisioning state.
        :param Mapping[str, str] tags: The resource tags.
        """
        pulumi.set(__self__, "connection_string_primary_key", connection_string_primary_key)
        pulumi.set(__self__, "connection_string_secondary_key", connection_string_secondary_key)
        pulumi.set(__self__, "created_time", created_time)
        pulumi.set(__self__, "endpoint_type", 'EventHub')
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="connectionStringPrimaryKey")
    def connection_string_primary_key(self) -> str:
        """
        PrimaryConnectionString of the endpoint. Will be obfuscated during read
        """
        return pulumi.get(self, "connection_string_primary_key")

    @property
    @pulumi.getter(name="connectionStringSecondaryKey")
    def connection_string_secondary_key(self) -> str:
        """
        SecondaryConnectionString of the endpoint. Will be obfuscated during read
        """
        return pulumi.get(self, "connection_string_secondary_key")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        """
        Time when the Endpoint was added to DigitalTwinsInstance.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        The type of Digital Twins endpoint
        Expected value is 'EventHub'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")


@pulumi.output_type
class ServiceBusResponse(dict):
    """
    properties related to servicebus.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdTime":
            suggest = "created_time"
        elif key == "endpointType":
            suggest = "endpoint_type"
        elif key == "primaryConnectionString":
            suggest = "primary_connection_string"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "secondaryConnectionString":
            suggest = "secondary_connection_string"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceBusResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceBusResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceBusResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_time: str,
                 endpoint_type: str,
                 primary_connection_string: str,
                 provisioning_state: str,
                 secondary_connection_string: str,
                 tags: Optional[Mapping[str, str]] = None):
        """
        properties related to servicebus.
        :param str created_time: Time when the Endpoint was added to DigitalTwinsInstance.
        :param str endpoint_type: The type of Digital Twins endpoint
               Expected value is 'ServiceBus'.
        :param str primary_connection_string: PrimaryConnectionString of the endpoint. Will be obfuscated during read
        :param str provisioning_state: The provisioning state.
        :param str secondary_connection_string: SecondaryConnectionString of the endpoint. Will be obfuscated during read
        :param Mapping[str, str] tags: The resource tags.
        """
        pulumi.set(__self__, "created_time", created_time)
        pulumi.set(__self__, "endpoint_type", 'ServiceBus')
        pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        """
        Time when the Endpoint was added to DigitalTwinsInstance.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        The type of Digital Twins endpoint
        Expected value is 'ServiceBus'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> str:
        """
        PrimaryConnectionString of the endpoint. Will be obfuscated during read
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> str:
        """
        SecondaryConnectionString of the endpoint. Will be obfuscated during read
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")


