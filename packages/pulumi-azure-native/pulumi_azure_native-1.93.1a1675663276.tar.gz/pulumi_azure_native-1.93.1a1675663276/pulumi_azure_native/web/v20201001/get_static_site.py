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
    'GetStaticSiteResult',
    'AwaitableGetStaticSiteResult',
    'get_static_site',
    'get_static_site_output',
]

@pulumi.output_type
class GetStaticSiteResult:
    """
    Static Site ARM resource.
    """
    def __init__(__self__, branch=None, build_properties=None, custom_domains=None, default_hostname=None, id=None, kind=None, location=None, name=None, repository_token=None, repository_url=None, sku=None, system_data=None, tags=None, type=None):
        if branch and not isinstance(branch, str):
            raise TypeError("Expected argument 'branch' to be a str")
        pulumi.set(__self__, "branch", branch)
        if build_properties and not isinstance(build_properties, dict):
            raise TypeError("Expected argument 'build_properties' to be a dict")
        pulumi.set(__self__, "build_properties", build_properties)
        if custom_domains and not isinstance(custom_domains, list):
            raise TypeError("Expected argument 'custom_domains' to be a list")
        pulumi.set(__self__, "custom_domains", custom_domains)
        if default_hostname and not isinstance(default_hostname, str):
            raise TypeError("Expected argument 'default_hostname' to be a str")
        pulumi.set(__self__, "default_hostname", default_hostname)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if repository_token and not isinstance(repository_token, str):
            raise TypeError("Expected argument 'repository_token' to be a str")
        pulumi.set(__self__, "repository_token", repository_token)
        if repository_url and not isinstance(repository_url, str):
            raise TypeError("Expected argument 'repository_url' to be a str")
        pulumi.set(__self__, "repository_url", repository_url)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def branch(self) -> Optional[str]:
        """
        The target branch in the repository.
        """
        return pulumi.get(self, "branch")

    @property
    @pulumi.getter(name="buildProperties")
    def build_properties(self) -> Optional['outputs.StaticSiteBuildPropertiesResponse']:
        """
        Build properties to configure on the repository.
        """
        return pulumi.get(self, "build_properties")

    @property
    @pulumi.getter(name="customDomains")
    def custom_domains(self) -> Sequence[str]:
        """
        The custom domains associated with this static site.
        """
        return pulumi.get(self, "custom_domains")

    @property
    @pulumi.getter(name="defaultHostname")
    def default_hostname(self) -> str:
        """
        The default autogenerated hostname for the static site.
        """
        return pulumi.get(self, "default_hostname")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="repositoryToken")
    def repository_token(self) -> Optional[str]:
        """
        A user's github repository token. This is used to setup the Github Actions workflow file and API secrets.
        """
        return pulumi.get(self, "repository_token")

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> Optional[str]:
        """
        URL for the repository of the static site.
        """
        return pulumi.get(self, "repository_url")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuDescriptionResponse']:
        """
        Description of a SKU for a scalable resource.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetStaticSiteResult(GetStaticSiteResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStaticSiteResult(
            branch=self.branch,
            build_properties=self.build_properties,
            custom_domains=self.custom_domains,
            default_hostname=self.default_hostname,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            repository_token=self.repository_token,
            repository_url=self.repository_url,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_static_site(name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStaticSiteResult:
    """
    Static Site ARM resource.


    :param str name: Name of the static site.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20201001:getStaticSite', __args__, opts=opts, typ=GetStaticSiteResult).value

    return AwaitableGetStaticSiteResult(
        branch=__ret__.branch,
        build_properties=__ret__.build_properties,
        custom_domains=__ret__.custom_domains,
        default_hostname=__ret__.default_hostname,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        repository_token=__ret__.repository_token,
        repository_url=__ret__.repository_url,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_static_site)
def get_static_site_output(name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStaticSiteResult]:
    """
    Static Site ARM resource.


    :param str name: Name of the static site.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
