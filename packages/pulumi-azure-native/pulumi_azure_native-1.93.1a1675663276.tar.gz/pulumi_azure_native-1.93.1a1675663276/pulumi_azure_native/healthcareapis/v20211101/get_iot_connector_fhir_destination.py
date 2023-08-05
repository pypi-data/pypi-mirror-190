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
    'GetIotConnectorFhirDestinationResult',
    'AwaitableGetIotConnectorFhirDestinationResult',
    'get_iot_connector_fhir_destination',
    'get_iot_connector_fhir_destination_output',
]

@pulumi.output_type
class GetIotConnectorFhirDestinationResult:
    """
    IoT Connector FHIR destination definition.
    """
    def __init__(__self__, etag=None, fhir_mapping=None, fhir_service_resource_id=None, id=None, location=None, name=None, resource_identity_resolution_type=None, system_data=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if fhir_mapping and not isinstance(fhir_mapping, dict):
            raise TypeError("Expected argument 'fhir_mapping' to be a dict")
        pulumi.set(__self__, "fhir_mapping", fhir_mapping)
        if fhir_service_resource_id and not isinstance(fhir_service_resource_id, str):
            raise TypeError("Expected argument 'fhir_service_resource_id' to be a str")
        pulumi.set(__self__, "fhir_service_resource_id", fhir_service_resource_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_identity_resolution_type and not isinstance(resource_identity_resolution_type, str):
            raise TypeError("Expected argument 'resource_identity_resolution_type' to be a str")
        pulumi.set(__self__, "resource_identity_resolution_type", resource_identity_resolution_type)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        An etag associated with the resource, used for optimistic concurrency when editing it.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="fhirMapping")
    def fhir_mapping(self) -> 'outputs.IotMappingPropertiesResponse':
        """
        FHIR Mappings
        """
        return pulumi.get(self, "fhir_mapping")

    @property
    @pulumi.getter(name="fhirServiceResourceId")
    def fhir_service_resource_id(self) -> str:
        """
        Fully qualified resource id of the FHIR service to connect to.
        """
        return pulumi.get(self, "fhir_service_resource_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceIdentityResolutionType")
    def resource_identity_resolution_type(self) -> str:
        """
        Determines how resource identity is resolved on the destination.
        """
        return pulumi.get(self, "resource_identity_resolution_type")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetIotConnectorFhirDestinationResult(GetIotConnectorFhirDestinationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIotConnectorFhirDestinationResult(
            etag=self.etag,
            fhir_mapping=self.fhir_mapping,
            fhir_service_resource_id=self.fhir_service_resource_id,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_identity_resolution_type=self.resource_identity_resolution_type,
            system_data=self.system_data,
            type=self.type)


def get_iot_connector_fhir_destination(fhir_destination_name: Optional[str] = None,
                                       iot_connector_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       workspace_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIotConnectorFhirDestinationResult:
    """
    IoT Connector FHIR destination definition.


    :param str fhir_destination_name: The name of IoT Connector FHIR destination resource.
    :param str iot_connector_name: The name of IoT Connector resource.
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str workspace_name: The name of workspace resource.
    """
    __args__ = dict()
    __args__['fhirDestinationName'] = fhir_destination_name
    __args__['iotConnectorName'] = iot_connector_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:healthcareapis/v20211101:getIotConnectorFhirDestination', __args__, opts=opts, typ=GetIotConnectorFhirDestinationResult).value

    return AwaitableGetIotConnectorFhirDestinationResult(
        etag=__ret__.etag,
        fhir_mapping=__ret__.fhir_mapping,
        fhir_service_resource_id=__ret__.fhir_service_resource_id,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource_identity_resolution_type=__ret__.resource_identity_resolution_type,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_iot_connector_fhir_destination)
def get_iot_connector_fhir_destination_output(fhir_destination_name: Optional[pulumi.Input[str]] = None,
                                              iot_connector_name: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              workspace_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIotConnectorFhirDestinationResult]:
    """
    IoT Connector FHIR destination definition.


    :param str fhir_destination_name: The name of IoT Connector FHIR destination resource.
    :param str iot_connector_name: The name of IoT Connector resource.
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str workspace_name: The name of workspace resource.
    """
    ...
