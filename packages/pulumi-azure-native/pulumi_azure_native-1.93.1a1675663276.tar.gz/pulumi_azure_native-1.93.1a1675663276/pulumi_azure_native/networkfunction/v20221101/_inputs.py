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
    'EmissionPoliciesPropertiesFormatArgs',
    'EmissionPolicyDestinationArgs',
    'IngestionPolicyPropertiesFormatArgs',
    'IngestionSourcesPropertiesFormatArgs',
]

@pulumi.input_type
class EmissionPoliciesPropertiesFormatArgs:
    def __init__(__self__, *,
                 emission_destinations: Optional[pulumi.Input[Sequence[pulumi.Input['EmissionPolicyDestinationArgs']]]] = None,
                 emission_type: Optional[pulumi.Input[Union[str, 'EmissionType']]] = None):
        """
        Emission policy properties.
        :param pulumi.Input[Sequence[pulumi.Input['EmissionPolicyDestinationArgs']]] emission_destinations: Emission policy destinations.
        :param pulumi.Input[Union[str, 'EmissionType']] emission_type: Emission format type.
        """
        if emission_destinations is not None:
            pulumi.set(__self__, "emission_destinations", emission_destinations)
        if emission_type is not None:
            pulumi.set(__self__, "emission_type", emission_type)

    @property
    @pulumi.getter(name="emissionDestinations")
    def emission_destinations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EmissionPolicyDestinationArgs']]]]:
        """
        Emission policy destinations.
        """
        return pulumi.get(self, "emission_destinations")

    @emission_destinations.setter
    def emission_destinations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EmissionPolicyDestinationArgs']]]]):
        pulumi.set(self, "emission_destinations", value)

    @property
    @pulumi.getter(name="emissionType")
    def emission_type(self) -> Optional[pulumi.Input[Union[str, 'EmissionType']]]:
        """
        Emission format type.
        """
        return pulumi.get(self, "emission_type")

    @emission_type.setter
    def emission_type(self, value: Optional[pulumi.Input[Union[str, 'EmissionType']]]):
        pulumi.set(self, "emission_type", value)


@pulumi.input_type
class EmissionPolicyDestinationArgs:
    def __init__(__self__, *,
                 destination_type: Optional[pulumi.Input[Union[str, 'DestinationType']]] = None):
        """
        Emission policy destination properties.
        :param pulumi.Input[Union[str, 'DestinationType']] destination_type: Emission destination type.
        """
        if destination_type is not None:
            pulumi.set(__self__, "destination_type", destination_type)

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> Optional[pulumi.Input[Union[str, 'DestinationType']]]:
        """
        Emission destination type.
        """
        return pulumi.get(self, "destination_type")

    @destination_type.setter
    def destination_type(self, value: Optional[pulumi.Input[Union[str, 'DestinationType']]]):
        pulumi.set(self, "destination_type", value)


@pulumi.input_type
class IngestionPolicyPropertiesFormatArgs:
    def __init__(__self__, *,
                 ingestion_sources: Optional[pulumi.Input[Sequence[pulumi.Input['IngestionSourcesPropertiesFormatArgs']]]] = None,
                 ingestion_type: Optional[pulumi.Input[Union[str, 'IngestionType']]] = None):
        """
        Ingestion Policy properties.
        :param pulumi.Input[Sequence[pulumi.Input['IngestionSourcesPropertiesFormatArgs']]] ingestion_sources: Ingestion Sources.
        :param pulumi.Input[Union[str, 'IngestionType']] ingestion_type: The ingestion type.
        """
        if ingestion_sources is not None:
            pulumi.set(__self__, "ingestion_sources", ingestion_sources)
        if ingestion_type is not None:
            pulumi.set(__self__, "ingestion_type", ingestion_type)

    @property
    @pulumi.getter(name="ingestionSources")
    def ingestion_sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IngestionSourcesPropertiesFormatArgs']]]]:
        """
        Ingestion Sources.
        """
        return pulumi.get(self, "ingestion_sources")

    @ingestion_sources.setter
    def ingestion_sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IngestionSourcesPropertiesFormatArgs']]]]):
        pulumi.set(self, "ingestion_sources", value)

    @property
    @pulumi.getter(name="ingestionType")
    def ingestion_type(self) -> Optional[pulumi.Input[Union[str, 'IngestionType']]]:
        """
        The ingestion type.
        """
        return pulumi.get(self, "ingestion_type")

    @ingestion_type.setter
    def ingestion_type(self, value: Optional[pulumi.Input[Union[str, 'IngestionType']]]):
        pulumi.set(self, "ingestion_type", value)


@pulumi.input_type
class IngestionSourcesPropertiesFormatArgs:
    def __init__(__self__, *,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 source_type: Optional[pulumi.Input[Union[str, 'SourceType']]] = None):
        """
        Ingestion policy properties.
        :param pulumi.Input[str] resource_id: Resource ID.
        :param pulumi.Input[Union[str, 'SourceType']] source_type: Ingestion source type.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if source_type is not None:
            pulumi.set(__self__, "source_type", source_type)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> Optional[pulumi.Input[Union[str, 'SourceType']]]:
        """
        Ingestion source type.
        """
        return pulumi.get(self, "source_type")

    @source_type.setter
    def source_type(self, value: Optional[pulumi.Input[Union[str, 'SourceType']]]):
        pulumi.set(self, "source_type", value)


