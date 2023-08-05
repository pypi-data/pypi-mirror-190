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
from ._inputs import *

__all__ = ['TemplateArtifactArgs', 'TemplateArtifact']

@pulumi.input_type
class TemplateArtifactArgs:
    def __init__(__self__, *,
                 blueprint_name: pulumi.Input[str],
                 kind: pulumi.Input[str],
                 management_group_name: pulumi.Input[str],
                 parameters: pulumi.Input[Mapping[str, pulumi.Input['ParameterValueBaseArgs']]],
                 template: Any,
                 artifact_name: Optional[pulumi.Input[str]] = None,
                 depends_on: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TemplateArtifact resource.
        :param pulumi.Input[str] blueprint_name: name of the blueprint.
        :param pulumi.Input[str] kind: Specifies the kind of Blueprint artifact.
               Expected value is 'template'.
        :param pulumi.Input[str] management_group_name: ManagementGroup where blueprint stores.
        :param pulumi.Input[Mapping[str, pulumi.Input['ParameterValueBaseArgs']]] parameters: Template parameter values.
        :param Any template: The Azure Resource Manager template body.
        :param pulumi.Input[str] artifact_name: name of the artifact.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] depends_on: Artifacts which need to be deployed before the specified artifact.
        :param pulumi.Input[str] description: Multi-line explain this resource.
        :param pulumi.Input[str] display_name: One-liner string explain this resource.
        :param pulumi.Input[str] resource_group: If applicable, the name of the resource group placeholder to which the template will be deployed.
        """
        pulumi.set(__self__, "blueprint_name", blueprint_name)
        pulumi.set(__self__, "kind", 'template')
        pulumi.set(__self__, "management_group_name", management_group_name)
        pulumi.set(__self__, "parameters", parameters)
        pulumi.set(__self__, "template", template)
        if artifact_name is not None:
            pulumi.set(__self__, "artifact_name", artifact_name)
        if depends_on is not None:
            pulumi.set(__self__, "depends_on", depends_on)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if resource_group is not None:
            pulumi.set(__self__, "resource_group", resource_group)

    @property
    @pulumi.getter(name="blueprintName")
    def blueprint_name(self) -> pulumi.Input[str]:
        """
        name of the blueprint.
        """
        return pulumi.get(self, "blueprint_name")

    @blueprint_name.setter
    def blueprint_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "blueprint_name", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Specifies the kind of Blueprint artifact.
        Expected value is 'template'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="managementGroupName")
    def management_group_name(self) -> pulumi.Input[str]:
        """
        ManagementGroup where blueprint stores.
        """
        return pulumi.get(self, "management_group_name")

    @management_group_name.setter
    def management_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "management_group_name", value)

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Input[Mapping[str, pulumi.Input['ParameterValueBaseArgs']]]:
        """
        Template parameter values.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: pulumi.Input[Mapping[str, pulumi.Input['ParameterValueBaseArgs']]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter
    def template(self) -> Any:
        """
        The Azure Resource Manager template body.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Any):
        pulumi.set(self, "template", value)

    @property
    @pulumi.getter(name="artifactName")
    def artifact_name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the artifact.
        """
        return pulumi.get(self, "artifact_name")

    @artifact_name.setter
    def artifact_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_name", value)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Artifacts which need to be deployed before the specified artifact.
        """
        return pulumi.get(self, "depends_on")

    @depends_on.setter
    def depends_on(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "depends_on", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        If applicable, the name of the resource group placeholder to which the template will be deployed.
        """
        return pulumi.get(self, "resource_group")

    @resource_group.setter
    def resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group", value)


class TemplateArtifact(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_name: Optional[pulumi.Input[str]] = None,
                 blueprint_name: Optional[pulumi.Input[str]] = None,
                 depends_on: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 management_group_name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterValueBaseArgs']]]]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 template: Optional[Any] = None,
                 __props__=None):
        """
        Blueprint artifact deploys Azure resource manager template.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] artifact_name: name of the artifact.
        :param pulumi.Input[str] blueprint_name: name of the blueprint.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] depends_on: Artifacts which need to be deployed before the specified artifact.
        :param pulumi.Input[str] description: Multi-line explain this resource.
        :param pulumi.Input[str] display_name: One-liner string explain this resource.
        :param pulumi.Input[str] kind: Specifies the kind of Blueprint artifact.
               Expected value is 'template'.
        :param pulumi.Input[str] management_group_name: ManagementGroup where blueprint stores.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterValueBaseArgs']]]] parameters: Template parameter values.
        :param pulumi.Input[str] resource_group: If applicable, the name of the resource group placeholder to which the template will be deployed.
        :param Any template: The Azure Resource Manager template body.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TemplateArtifactArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Blueprint artifact deploys Azure resource manager template.

        :param str resource_name: The name of the resource.
        :param TemplateArtifactArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TemplateArtifactArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_name: Optional[pulumi.Input[str]] = None,
                 blueprint_name: Optional[pulumi.Input[str]] = None,
                 depends_on: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 management_group_name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterValueBaseArgs']]]]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 template: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TemplateArtifactArgs.__new__(TemplateArtifactArgs)

            __props__.__dict__["artifact_name"] = artifact_name
            if blueprint_name is None and not opts.urn:
                raise TypeError("Missing required property 'blueprint_name'")
            __props__.__dict__["blueprint_name"] = blueprint_name
            __props__.__dict__["depends_on"] = depends_on
            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'template'
            if management_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'management_group_name'")
            __props__.__dict__["management_group_name"] = management_group_name
            if parameters is None and not opts.urn:
                raise TypeError("Missing required property 'parameters'")
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["resource_group"] = resource_group
            if template is None and not opts.urn:
                raise TypeError("Missing required property 'template'")
            __props__.__dict__["template"] = template
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        super(TemplateArtifact, __self__).__init__(
            'azure-native:blueprint/v20171111preview:TemplateArtifact',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TemplateArtifact':
        """
        Get an existing TemplateArtifact resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TemplateArtifactArgs.__new__(TemplateArtifactArgs)

        __props__.__dict__["depends_on"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["parameters"] = None
        __props__.__dict__["resource_group"] = None
        __props__.__dict__["template"] = None
        __props__.__dict__["type"] = None
        return TemplateArtifact(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Artifacts which need to be deployed before the specified artifact.
        """
        return pulumi.get(self, "depends_on")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Specifies the kind of Blueprint artifact.
        Expected value is 'template'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Mapping[str, 'outputs.ParameterValueBaseResponse']]:
        """
        Template parameter values.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Output[Optional[str]]:
        """
        If applicable, the name of the resource group placeholder to which the template will be deployed.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter
    def template(self) -> pulumi.Output[Any]:
        """
        The Azure Resource Manager template body.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")

