# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'BranchResponse',
    'CapabilityPropertiesResponse',
    'ContinuousActionResponse',
    'DelayActionResponse',
    'DiscreteActionResponse',
    'ExperimentPropertiesResponse',
    'KeyValuePairResponse',
    'ResourceIdentityResponse',
    'SelectorResponse',
    'StepResponse',
    'SystemDataResponse',
    'TargetReferenceResponse',
]

@pulumi.output_type
class BranchResponse(dict):
    """
    Model that represents a branch in the step.
    """
    def __init__(__self__, *,
                 actions: Sequence[Any],
                 name: str):
        """
        Model that represents a branch in the step.
        :param Sequence[Union['ContinuousActionResponse', 'DelayActionResponse', 'DiscreteActionResponse']] actions: List of actions.
        :param str name: String of the branch name.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def actions(self) -> Sequence[Any]:
        """
        List of actions.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        String of the branch name.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class CapabilityPropertiesResponse(dict):
    """
    Model that represents the Capability properties model.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "parametersSchema":
            suggest = "parameters_schema"
        elif key == "targetType":
            suggest = "target_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CapabilityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CapabilityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CapabilityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 description: str,
                 parameters_schema: str,
                 publisher: str,
                 target_type: str,
                 urn: str):
        """
        Model that represents the Capability properties model.
        :param str description: Localized string of the description.
        :param str parameters_schema: URL to retrieve JSON schema of the Capability parameters.
        :param str publisher: String of the Publisher that this Capability extends.
        :param str target_type: String of the Target Type that this Capability extends.
        :param str urn: String of the URN for this Capability Type.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "parameters_schema", parameters_schema)
        pulumi.set(__self__, "publisher", publisher)
        pulumi.set(__self__, "target_type", target_type)
        pulumi.set(__self__, "urn", urn)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Localized string of the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="parametersSchema")
    def parameters_schema(self) -> str:
        """
        URL to retrieve JSON schema of the Capability parameters.
        """
        return pulumi.get(self, "parameters_schema")

    @property
    @pulumi.getter
    def publisher(self) -> str:
        """
        String of the Publisher that this Capability extends.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> str:
        """
        String of the Target Type that this Capability extends.
        """
        return pulumi.get(self, "target_type")

    @property
    @pulumi.getter
    def urn(self) -> str:
        """
        String of the URN for this Capability Type.
        """
        return pulumi.get(self, "urn")


@pulumi.output_type
class ContinuousActionResponse(dict):
    """
    Model that represents a continuous action.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "selectorId":
            suggest = "selector_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContinuousActionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContinuousActionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContinuousActionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 duration: str,
                 name: str,
                 parameters: Sequence['outputs.KeyValuePairResponse'],
                 selector_id: str,
                 type: str):
        """
        Model that represents a continuous action.
        :param str duration: ISO8601 formatted string that represents a duration.
        :param str name: String that represents a Capability URN.
        :param Sequence['KeyValuePairResponse'] parameters: List of key value pairs.
        :param str selector_id: String that represents a selector.
        :param str type: Enum that discriminates between action models.
               Expected value is 'continuous'.
        """
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "parameters", parameters)
        pulumi.set(__self__, "selector_id", selector_id)
        pulumi.set(__self__, "type", 'continuous')

    @property
    @pulumi.getter
    def duration(self) -> str:
        """
        ISO8601 formatted string that represents a duration.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        String that represents a Capability URN.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Sequence['outputs.KeyValuePairResponse']:
        """
        List of key value pairs.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="selectorId")
    def selector_id(self) -> str:
        """
        String that represents a selector.
        """
        return pulumi.get(self, "selector_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Enum that discriminates between action models.
        Expected value is 'continuous'.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class DelayActionResponse(dict):
    """
    Model that represents a delay action.
    """
    def __init__(__self__, *,
                 duration: str,
                 name: str,
                 type: str):
        """
        Model that represents a delay action.
        :param str duration: ISO8601 formatted string that represents a duration.
        :param str name: String that represents a Capability URN.
        :param str type: Enum that discriminates between action models.
               Expected value is 'delay'.
        """
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", 'delay')

    @property
    @pulumi.getter
    def duration(self) -> str:
        """
        ISO8601 formatted string that represents a duration.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        String that represents a Capability URN.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Enum that discriminates between action models.
        Expected value is 'delay'.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class DiscreteActionResponse(dict):
    """
    Model that represents a discrete action.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "selectorId":
            suggest = "selector_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DiscreteActionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DiscreteActionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DiscreteActionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 parameters: Sequence['outputs.KeyValuePairResponse'],
                 selector_id: str,
                 type: str):
        """
        Model that represents a discrete action.
        :param str name: String that represents a Capability URN.
        :param Sequence['KeyValuePairResponse'] parameters: List of key value pairs.
        :param str selector_id: String that represents a selector.
        :param str type: Enum that discriminates between action models.
               Expected value is 'discrete'.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "parameters", parameters)
        pulumi.set(__self__, "selector_id", selector_id)
        pulumi.set(__self__, "type", 'discrete')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        String that represents a Capability URN.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Sequence['outputs.KeyValuePairResponse']:
        """
        List of key value pairs.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="selectorId")
    def selector_id(self) -> str:
        """
        String that represents a selector.
        """
        return pulumi.get(self, "selector_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Enum that discriminates between action models.
        Expected value is 'discrete'.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class ExperimentPropertiesResponse(dict):
    """
    Model that represents the Experiment properties model.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "startOnCreation":
            suggest = "start_on_creation"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 selectors: Sequence['outputs.SelectorResponse'],
                 steps: Sequence['outputs.StepResponse'],
                 start_on_creation: Optional[bool] = None):
        """
        Model that represents the Experiment properties model.
        :param Sequence['SelectorResponse'] selectors: List of selectors.
        :param Sequence['StepResponse'] steps: List of steps.
        :param bool start_on_creation: A boolean value that indicates if experiment should be started on creation or not.
        """
        pulumi.set(__self__, "selectors", selectors)
        pulumi.set(__self__, "steps", steps)
        if start_on_creation is not None:
            pulumi.set(__self__, "start_on_creation", start_on_creation)

    @property
    @pulumi.getter
    def selectors(self) -> Sequence['outputs.SelectorResponse']:
        """
        List of selectors.
        """
        return pulumi.get(self, "selectors")

    @property
    @pulumi.getter
    def steps(self) -> Sequence['outputs.StepResponse']:
        """
        List of steps.
        """
        return pulumi.get(self, "steps")

    @property
    @pulumi.getter(name="startOnCreation")
    def start_on_creation(self) -> Optional[bool]:
        """
        A boolean value that indicates if experiment should be started on creation or not.
        """
        return pulumi.get(self, "start_on_creation")


@pulumi.output_type
class KeyValuePairResponse(dict):
    """
    A map to describe the settings of an action.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A map to describe the settings of an action.
        :param str key: The name of the setting for the action.
        :param str value: The value of the setting for the action.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name of the setting for the action.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the setting for the action.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ResourceIdentityResponse(dict):
    """
    The managed identity of a resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        The managed identity of a resource.
        :param str principal_id: GUID that represents the principal ID of this resource identity.
        :param str tenant_id: GUID that represents the tenant ID of this resource identity.
        :param str type: String of the resource identity type.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        GUID that represents the principal ID of this resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        GUID that represents the tenant ID of this resource identity.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        String of the resource identity type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class SelectorResponse(dict):
    """
    Model that represents a selector in the Experiment resource.
    """
    def __init__(__self__, *,
                 id: str,
                 targets: Sequence['outputs.TargetReferenceResponse'],
                 type: str):
        """
        Model that represents a selector in the Experiment resource.
        :param str id: String of the selector ID.
        :param Sequence['TargetReferenceResponse'] targets: List of Target references.
        :param str type: Enum of the selector type.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "targets", targets)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String of the selector ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def targets(self) -> Sequence['outputs.TargetReferenceResponse']:
        """
        List of Target references.
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Enum of the selector type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class StepResponse(dict):
    """
    Model that represents a step in the Experiment resource.
    """
    def __init__(__self__, *,
                 branches: Sequence['outputs.BranchResponse'],
                 name: str):
        """
        Model that represents a step in the Experiment resource.
        :param Sequence['BranchResponse'] branches: List of branches.
        :param str name: String of the step name.
        """
        pulumi.set(__self__, "branches", branches)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def branches(self) -> Sequence['outputs.BranchResponse']:
        """
        List of branches.
        """
        return pulumi.get(self, "branches")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        String of the step name.
        """
        return pulumi.get(self, "name")


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
class TargetReferenceResponse(dict):
    """
    Model that represents a reference to a Target in the selector.
    """
    def __init__(__self__, *,
                 id: str,
                 type: str):
        """
        Model that represents a reference to a Target in the selector.
        :param str id: String of the resource ID of a Target resource.
        :param str type: Enum of the Target reference type.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String of the resource ID of a Target resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Enum of the Target reference type.
        """
        return pulumi.get(self, "type")


