# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetDataCollectionRuleAssociationResult',
    'AwaitableGetDataCollectionRuleAssociationResult',
    'get_data_collection_rule_association',
    'get_data_collection_rule_association_output',
]

@pulumi.output_type
class GetDataCollectionRuleAssociationResult:
    """
    Definition of generic ARM proxy resource.
    """
    def __init__(__self__, data_collection_rule_id=None, description=None, etag=None, id=None, name=None, provisioning_state=None, type=None):
        if data_collection_rule_id and not isinstance(data_collection_rule_id, str):
            raise TypeError("Expected argument 'data_collection_rule_id' to be a str")
        pulumi.set(__self__, "data_collection_rule_id", data_collection_rule_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dataCollectionRuleId")
    def data_collection_rule_id(self) -> Optional[str]:
        """
        The resource ID of the data collection rule that is to be associated.
        """
        return pulumi.get(self, "data_collection_rule_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the association.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        Resource entity tag (ETag).
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified ID of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The resource provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetDataCollectionRuleAssociationResult(GetDataCollectionRuleAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataCollectionRuleAssociationResult(
            data_collection_rule_id=self.data_collection_rule_id,
            description=self.description,
            etag=self.etag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_data_collection_rule_association(association_name: Optional[str] = None,
                                         resource_uri: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataCollectionRuleAssociationResult:
    """
    Definition of generic ARM proxy resource.
    API Version: 2019-11-01-preview.


    :param str association_name: The name of the association. The name is case insensitive.
    :param str resource_uri: The identifier of the resource.
    """
    __args__ = dict()
    __args__['associationName'] = association_name
    __args__['resourceUri'] = resource_uri
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:insights:getDataCollectionRuleAssociation', __args__, opts=opts, typ=GetDataCollectionRuleAssociationResult).value

    return AwaitableGetDataCollectionRuleAssociationResult(
        data_collection_rule_id=__ret__.data_collection_rule_id,
        description=__ret__.description,
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_data_collection_rule_association)
def get_data_collection_rule_association_output(association_name: Optional[pulumi.Input[str]] = None,
                                                resource_uri: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDataCollectionRuleAssociationResult]:
    """
    Definition of generic ARM proxy resource.
    API Version: 2019-11-01-preview.


    :param str association_name: The name of the association. The name is case insensitive.
    :param str resource_uri: The identifier of the resource.
    """
    ...
