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
    'GetGalleryApplicationVersionResult',
    'AwaitableGetGalleryApplicationVersionResult',
    'get_gallery_application_version',
    'get_gallery_application_version_output',
]

@pulumi.output_type
class GetGalleryApplicationVersionResult:
    """
    Specifies information about the gallery Application Version that you want to create or update.
    """
    def __init__(__self__, id=None, location=None, name=None, provisioning_state=None, publishing_profile=None, replication_status=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if publishing_profile and not isinstance(publishing_profile, dict):
            raise TypeError("Expected argument 'publishing_profile' to be a dict")
        pulumi.set(__self__, "publishing_profile", publishing_profile)
        if replication_status and not isinstance(replication_status, dict):
            raise TypeError("Expected argument 'replication_status' to be a dict")
        pulumi.set(__self__, "replication_status", replication_status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publishingProfile")
    def publishing_profile(self) -> 'outputs.GalleryApplicationVersionPublishingProfileResponse':
        """
        The publishing profile of a gallery image version.
        """
        return pulumi.get(self, "publishing_profile")

    @property
    @pulumi.getter(name="replicationStatus")
    def replication_status(self) -> 'outputs.ReplicationStatusResponse':
        """
        This is the replication status of the gallery image version.
        """
        return pulumi.get(self, "replication_status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetGalleryApplicationVersionResult(GetGalleryApplicationVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGalleryApplicationVersionResult(
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            publishing_profile=self.publishing_profile,
            replication_status=self.replication_status,
            tags=self.tags,
            type=self.type)


def get_gallery_application_version(expand: Optional[str] = None,
                                    gallery_application_name: Optional[str] = None,
                                    gallery_application_version_name: Optional[str] = None,
                                    gallery_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGalleryApplicationVersionResult:
    """
    Specifies information about the gallery Application Version that you want to create or update.


    :param str expand: The expand expression to apply on the operation.
    :param str gallery_application_name: The name of the gallery Application Definition in which the Application Version resides.
    :param str gallery_application_version_name: The name of the gallery Application Version to be retrieved.
    :param str gallery_name: The name of the Shared Application Gallery in which the Application Definition resides.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['galleryApplicationName'] = gallery_application_name
    __args__['galleryApplicationVersionName'] = gallery_application_version_name
    __args__['galleryName'] = gallery_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20200930:getGalleryApplicationVersion', __args__, opts=opts, typ=GetGalleryApplicationVersionResult).value

    return AwaitableGetGalleryApplicationVersionResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        publishing_profile=__ret__.publishing_profile,
        replication_status=__ret__.replication_status,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_gallery_application_version)
def get_gallery_application_version_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                           gallery_application_name: Optional[pulumi.Input[str]] = None,
                                           gallery_application_version_name: Optional[pulumi.Input[str]] = None,
                                           gallery_name: Optional[pulumi.Input[str]] = None,
                                           resource_group_name: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGalleryApplicationVersionResult]:
    """
    Specifies information about the gallery Application Version that you want to create or update.


    :param str expand: The expand expression to apply on the operation.
    :param str gallery_application_name: The name of the gallery Application Definition in which the Application Version resides.
    :param str gallery_application_version_name: The name of the gallery Application Version to be retrieved.
    :param str gallery_name: The name of the Shared Application Gallery in which the Application Definition resides.
    :param str resource_group_name: The name of the resource group.
    """
    ...
