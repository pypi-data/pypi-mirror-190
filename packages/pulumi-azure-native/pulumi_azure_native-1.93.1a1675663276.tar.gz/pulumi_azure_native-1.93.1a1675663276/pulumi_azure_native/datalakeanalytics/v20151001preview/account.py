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
from ._inputs import *

__all__ = ['AccountArgs', 'Account']

@pulumi.input_type
class AccountArgs:
    def __init__(__self__, *,
                 data_lake_store_accounts: pulumi.Input[Sequence[pulumi.Input['AddDataLakeStoreWithAccountParametersArgs']]],
                 default_data_lake_store_account: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 account_name: Optional[pulumi.Input[str]] = None,
                 compute_policies: Optional[pulumi.Input[Sequence[pulumi.Input['CreateComputePolicyWithAccountParametersArgs']]]] = None,
                 firewall_allow_azure_ips: Optional[pulumi.Input['FirewallAllowAzureIpsState']] = None,
                 firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input['CreateFirewallRuleWithAccountParametersArgs']]]] = None,
                 firewall_state: Optional[pulumi.Input['FirewallState']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_degree_of_parallelism: Optional[pulumi.Input[int]] = None,
                 max_degree_of_parallelism_per_job: Optional[pulumi.Input[int]] = None,
                 max_job_count: Optional[pulumi.Input[int]] = None,
                 min_priority_per_job: Optional[pulumi.Input[int]] = None,
                 new_tier: Optional[pulumi.Input['TierType']] = None,
                 query_store_retention: Optional[pulumi.Input[int]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['AddStorageAccountWithAccountParametersArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Account resource.
        :param pulumi.Input[Sequence[pulumi.Input['AddDataLakeStoreWithAccountParametersArgs']]] data_lake_store_accounts: The list of Data Lake Store accounts associated with this account.
        :param pulumi.Input[str] default_data_lake_store_account: The default Data Lake Store account associated with this account.
        :param pulumi.Input[str] resource_group_name: The name of the Azure resource group.
        :param pulumi.Input[str] account_name: The name of the Data Lake Analytics account to retrieve.
        :param pulumi.Input[Sequence[pulumi.Input['CreateComputePolicyWithAccountParametersArgs']]] compute_policies: The list of compute policies associated with this account.
        :param pulumi.Input['FirewallAllowAzureIpsState'] firewall_allow_azure_ips: The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is disabled, this is not enforced.
        :param pulumi.Input[Sequence[pulumi.Input['CreateFirewallRuleWithAccountParametersArgs']]] firewall_rules: The list of firewall rules associated with this account.
        :param pulumi.Input['FirewallState'] firewall_state: The current state of the IP address firewall for this account.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[int] max_degree_of_parallelism: The maximum supported degree of parallelism for this account.
        :param pulumi.Input[int] max_degree_of_parallelism_per_job: The maximum supported degree of parallelism per job for this account.
        :param pulumi.Input[int] max_job_count: The maximum supported jobs running under the account at the same time.
        :param pulumi.Input[int] min_priority_per_job: The minimum supported priority per job for this account.
        :param pulumi.Input['TierType'] new_tier: The commitment tier for the next month.
        :param pulumi.Input[int] query_store_retention: The number of days that job metadata is retained.
        :param pulumi.Input[Sequence[pulumi.Input['AddStorageAccountWithAccountParametersArgs']]] storage_accounts: The list of Azure Blob Storage accounts associated with this account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        pulumi.set(__self__, "data_lake_store_accounts", data_lake_store_accounts)
        pulumi.set(__self__, "default_data_lake_store_account", default_data_lake_store_account)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if compute_policies is not None:
            pulumi.set(__self__, "compute_policies", compute_policies)
        if firewall_allow_azure_ips is None:
            firewall_allow_azure_ips = 'Disabled'
        if firewall_allow_azure_ips is not None:
            pulumi.set(__self__, "firewall_allow_azure_ips", firewall_allow_azure_ips)
        if firewall_rules is not None:
            pulumi.set(__self__, "firewall_rules", firewall_rules)
        if firewall_state is None:
            firewall_state = 'Disabled'
        if firewall_state is not None:
            pulumi.set(__self__, "firewall_state", firewall_state)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if max_degree_of_parallelism is not None:
            pulumi.set(__self__, "max_degree_of_parallelism", max_degree_of_parallelism)
        if max_degree_of_parallelism_per_job is None:
            max_degree_of_parallelism_per_job = 32
        if max_degree_of_parallelism_per_job is not None:
            pulumi.set(__self__, "max_degree_of_parallelism_per_job", max_degree_of_parallelism_per_job)
        if max_job_count is None:
            max_job_count = 20
        if max_job_count is not None:
            pulumi.set(__self__, "max_job_count", max_job_count)
        if min_priority_per_job is not None:
            pulumi.set(__self__, "min_priority_per_job", min_priority_per_job)
        if new_tier is None:
            new_tier = 'Consumption'
        if new_tier is not None:
            pulumi.set(__self__, "new_tier", new_tier)
        if query_store_retention is None:
            query_store_retention = 30
        if query_store_retention is not None:
            pulumi.set(__self__, "query_store_retention", query_store_retention)
        if storage_accounts is not None:
            pulumi.set(__self__, "storage_accounts", storage_accounts)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dataLakeStoreAccounts")
    def data_lake_store_accounts(self) -> pulumi.Input[Sequence[pulumi.Input['AddDataLakeStoreWithAccountParametersArgs']]]:
        """
        The list of Data Lake Store accounts associated with this account.
        """
        return pulumi.get(self, "data_lake_store_accounts")

    @data_lake_store_accounts.setter
    def data_lake_store_accounts(self, value: pulumi.Input[Sequence[pulumi.Input['AddDataLakeStoreWithAccountParametersArgs']]]):
        pulumi.set(self, "data_lake_store_accounts", value)

    @property
    @pulumi.getter(name="defaultDataLakeStoreAccount")
    def default_data_lake_store_account(self) -> pulumi.Input[str]:
        """
        The default Data Lake Store account associated with this account.
        """
        return pulumi.get(self, "default_data_lake_store_account")

    @default_data_lake_store_account.setter
    def default_data_lake_store_account(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_data_lake_store_account", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Azure resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Data Lake Analytics account to retrieve.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="computePolicies")
    def compute_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CreateComputePolicyWithAccountParametersArgs']]]]:
        """
        The list of compute policies associated with this account.
        """
        return pulumi.get(self, "compute_policies")

    @compute_policies.setter
    def compute_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CreateComputePolicyWithAccountParametersArgs']]]]):
        pulumi.set(self, "compute_policies", value)

    @property
    @pulumi.getter(name="firewallAllowAzureIps")
    def firewall_allow_azure_ips(self) -> Optional[pulumi.Input['FirewallAllowAzureIpsState']]:
        """
        The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is disabled, this is not enforced.
        """
        return pulumi.get(self, "firewall_allow_azure_ips")

    @firewall_allow_azure_ips.setter
    def firewall_allow_azure_ips(self, value: Optional[pulumi.Input['FirewallAllowAzureIpsState']]):
        pulumi.set(self, "firewall_allow_azure_ips", value)

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CreateFirewallRuleWithAccountParametersArgs']]]]:
        """
        The list of firewall rules associated with this account.
        """
        return pulumi.get(self, "firewall_rules")

    @firewall_rules.setter
    def firewall_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CreateFirewallRuleWithAccountParametersArgs']]]]):
        pulumi.set(self, "firewall_rules", value)

    @property
    @pulumi.getter(name="firewallState")
    def firewall_state(self) -> Optional[pulumi.Input['FirewallState']]:
        """
        The current state of the IP address firewall for this account.
        """
        return pulumi.get(self, "firewall_state")

    @firewall_state.setter
    def firewall_state(self, value: Optional[pulumi.Input['FirewallState']]):
        pulumi.set(self, "firewall_state", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maxDegreeOfParallelism")
    def max_degree_of_parallelism(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum supported degree of parallelism for this account.
        """
        return pulumi.get(self, "max_degree_of_parallelism")

    @max_degree_of_parallelism.setter
    def max_degree_of_parallelism(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_degree_of_parallelism", value)

    @property
    @pulumi.getter(name="maxDegreeOfParallelismPerJob")
    def max_degree_of_parallelism_per_job(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum supported degree of parallelism per job for this account.
        """
        return pulumi.get(self, "max_degree_of_parallelism_per_job")

    @max_degree_of_parallelism_per_job.setter
    def max_degree_of_parallelism_per_job(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_degree_of_parallelism_per_job", value)

    @property
    @pulumi.getter(name="maxJobCount")
    def max_job_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum supported jobs running under the account at the same time.
        """
        return pulumi.get(self, "max_job_count")

    @max_job_count.setter
    def max_job_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_job_count", value)

    @property
    @pulumi.getter(name="minPriorityPerJob")
    def min_priority_per_job(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum supported priority per job for this account.
        """
        return pulumi.get(self, "min_priority_per_job")

    @min_priority_per_job.setter
    def min_priority_per_job(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_priority_per_job", value)

    @property
    @pulumi.getter(name="newTier")
    def new_tier(self) -> Optional[pulumi.Input['TierType']]:
        """
        The commitment tier for the next month.
        """
        return pulumi.get(self, "new_tier")

    @new_tier.setter
    def new_tier(self, value: Optional[pulumi.Input['TierType']]):
        pulumi.set(self, "new_tier", value)

    @property
    @pulumi.getter(name="queryStoreRetention")
    def query_store_retention(self) -> Optional[pulumi.Input[int]]:
        """
        The number of days that job metadata is retained.
        """
        return pulumi.get(self, "query_store_retention")

    @query_store_retention.setter
    def query_store_retention(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "query_store_retention", value)

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AddStorageAccountWithAccountParametersArgs']]]]:
        """
        The list of Azure Blob Storage accounts associated with this account.
        """
        return pulumi.get(self, "storage_accounts")

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AddStorageAccountWithAccountParametersArgs']]]]):
        pulumi.set(self, "storage_accounts", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2015-10-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class Account(pulumi.CustomResource):
    warnings.warn("""Version 2015-10-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 compute_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateComputePolicyWithAccountParametersArgs']]]]] = None,
                 data_lake_store_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddDataLakeStoreWithAccountParametersArgs']]]]] = None,
                 default_data_lake_store_account: Optional[pulumi.Input[str]] = None,
                 firewall_allow_azure_ips: Optional[pulumi.Input['FirewallAllowAzureIpsState']] = None,
                 firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateFirewallRuleWithAccountParametersArgs']]]]] = None,
                 firewall_state: Optional[pulumi.Input['FirewallState']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_degree_of_parallelism: Optional[pulumi.Input[int]] = None,
                 max_degree_of_parallelism_per_job: Optional[pulumi.Input[int]] = None,
                 max_job_count: Optional[pulumi.Input[int]] = None,
                 min_priority_per_job: Optional[pulumi.Input[int]] = None,
                 new_tier: Optional[pulumi.Input['TierType']] = None,
                 query_store_retention: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddStorageAccountWithAccountParametersArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A Data Lake Analytics account object, containing all information associated with the named Data Lake Analytics account.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Data Lake Analytics account to retrieve.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateComputePolicyWithAccountParametersArgs']]]] compute_policies: The list of compute policies associated with this account.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddDataLakeStoreWithAccountParametersArgs']]]] data_lake_store_accounts: The list of Data Lake Store accounts associated with this account.
        :param pulumi.Input[str] default_data_lake_store_account: The default Data Lake Store account associated with this account.
        :param pulumi.Input['FirewallAllowAzureIpsState'] firewall_allow_azure_ips: The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is disabled, this is not enforced.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateFirewallRuleWithAccountParametersArgs']]]] firewall_rules: The list of firewall rules associated with this account.
        :param pulumi.Input['FirewallState'] firewall_state: The current state of the IP address firewall for this account.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[int] max_degree_of_parallelism: The maximum supported degree of parallelism for this account.
        :param pulumi.Input[int] max_degree_of_parallelism_per_job: The maximum supported degree of parallelism per job for this account.
        :param pulumi.Input[int] max_job_count: The maximum supported jobs running under the account at the same time.
        :param pulumi.Input[int] min_priority_per_job: The minimum supported priority per job for this account.
        :param pulumi.Input['TierType'] new_tier: The commitment tier for the next month.
        :param pulumi.Input[int] query_store_retention: The number of days that job metadata is retained.
        :param pulumi.Input[str] resource_group_name: The name of the Azure resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddStorageAccountWithAccountParametersArgs']]]] storage_accounts: The list of Azure Blob Storage accounts associated with this account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A Data Lake Analytics account object, containing all information associated with the named Data Lake Analytics account.

        :param str resource_name: The name of the resource.
        :param AccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 compute_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateComputePolicyWithAccountParametersArgs']]]]] = None,
                 data_lake_store_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddDataLakeStoreWithAccountParametersArgs']]]]] = None,
                 default_data_lake_store_account: Optional[pulumi.Input[str]] = None,
                 firewall_allow_azure_ips: Optional[pulumi.Input['FirewallAllowAzureIpsState']] = None,
                 firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CreateFirewallRuleWithAccountParametersArgs']]]]] = None,
                 firewall_state: Optional[pulumi.Input['FirewallState']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_degree_of_parallelism: Optional[pulumi.Input[int]] = None,
                 max_degree_of_parallelism_per_job: Optional[pulumi.Input[int]] = None,
                 max_job_count: Optional[pulumi.Input[int]] = None,
                 min_priority_per_job: Optional[pulumi.Input[int]] = None,
                 new_tier: Optional[pulumi.Input['TierType']] = None,
                 query_store_retention: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AddStorageAccountWithAccountParametersArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Account is deprecated: Version 2015-10-01-preview will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountArgs.__new__(AccountArgs)

            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["compute_policies"] = compute_policies
            if data_lake_store_accounts is None and not opts.urn:
                raise TypeError("Missing required property 'data_lake_store_accounts'")
            __props__.__dict__["data_lake_store_accounts"] = data_lake_store_accounts
            if default_data_lake_store_account is None and not opts.urn:
                raise TypeError("Missing required property 'default_data_lake_store_account'")
            __props__.__dict__["default_data_lake_store_account"] = default_data_lake_store_account
            if firewall_allow_azure_ips is None:
                firewall_allow_azure_ips = 'Disabled'
            __props__.__dict__["firewall_allow_azure_ips"] = firewall_allow_azure_ips
            __props__.__dict__["firewall_rules"] = firewall_rules
            if firewall_state is None:
                firewall_state = 'Disabled'
            __props__.__dict__["firewall_state"] = firewall_state
            __props__.__dict__["location"] = location
            __props__.__dict__["max_degree_of_parallelism"] = max_degree_of_parallelism
            if max_degree_of_parallelism_per_job is None:
                max_degree_of_parallelism_per_job = 32
            __props__.__dict__["max_degree_of_parallelism_per_job"] = max_degree_of_parallelism_per_job
            if max_job_count is None:
                max_job_count = 20
            __props__.__dict__["max_job_count"] = max_job_count
            __props__.__dict__["min_priority_per_job"] = min_priority_per_job
            if new_tier is None:
                new_tier = 'Consumption'
            __props__.__dict__["new_tier"] = new_tier
            if query_store_retention is None:
                query_store_retention = 30
            __props__.__dict__["query_store_retention"] = query_store_retention
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["storage_accounts"] = storage_accounts
            __props__.__dict__["tags"] = tags
            __props__.__dict__["account_id"] = None
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["current_tier"] = None
            __props__.__dict__["debug_data_access_level"] = None
            __props__.__dict__["endpoint"] = None
            __props__.__dict__["hierarchical_queue_state"] = None
            __props__.__dict__["hive_metastores"] = None
            __props__.__dict__["last_modified_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["public_data_lake_store_accounts"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["system_max_degree_of_parallelism"] = None
            __props__.__dict__["system_max_job_count"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["virtual_network_rules"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:datalakeanalytics:Account"), pulumi.Alias(type_="azure-native:datalakeanalytics/v20161101:Account"), pulumi.Alias(type_="azure-native:datalakeanalytics/v20191101preview:Account")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Account, __self__).__init__(
            'azure-native:datalakeanalytics/v20151001preview:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Account':
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AccountArgs.__new__(AccountArgs)

        __props__.__dict__["account_id"] = None
        __props__.__dict__["compute_policies"] = None
        __props__.__dict__["creation_time"] = None
        __props__.__dict__["current_tier"] = None
        __props__.__dict__["data_lake_store_accounts"] = None
        __props__.__dict__["debug_data_access_level"] = None
        __props__.__dict__["default_data_lake_store_account"] = None
        __props__.__dict__["endpoint"] = None
        __props__.__dict__["firewall_allow_azure_ips"] = None
        __props__.__dict__["firewall_rules"] = None
        __props__.__dict__["firewall_state"] = None
        __props__.__dict__["hierarchical_queue_state"] = None
        __props__.__dict__["hive_metastores"] = None
        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["max_degree_of_parallelism"] = None
        __props__.__dict__["max_degree_of_parallelism_per_job"] = None
        __props__.__dict__["max_job_count"] = None
        __props__.__dict__["min_priority_per_job"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["new_tier"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_data_lake_store_accounts"] = None
        __props__.__dict__["query_store_retention"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["storage_accounts"] = None
        __props__.__dict__["system_max_degree_of_parallelism"] = None
        __props__.__dict__["system_max_job_count"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_network_rules"] = None
        return Account(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The unique identifier associated with this Data Lake Analytics account.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="computePolicies")
    def compute_policies(self) -> pulumi.Output[Sequence['outputs.ComputePolicyResponse']]:
        """
        The list of compute policies associated with this account.
        """
        return pulumi.get(self, "compute_policies")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The account creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="currentTier")
    def current_tier(self) -> pulumi.Output[str]:
        """
        The commitment tier in use for the current month.
        """
        return pulumi.get(self, "current_tier")

    @property
    @pulumi.getter(name="dataLakeStoreAccounts")
    def data_lake_store_accounts(self) -> pulumi.Output[Optional[Sequence['outputs.DataLakeStoreAccountInformationResponse']]]:
        """
        The list of Data Lake Store accounts associated with this account.
        """
        return pulumi.get(self, "data_lake_store_accounts")

    @property
    @pulumi.getter(name="debugDataAccessLevel")
    def debug_data_access_level(self) -> pulumi.Output[str]:
        """
        The current state of the DebugDataAccessLevel for this account.
        """
        return pulumi.get(self, "debug_data_access_level")

    @property
    @pulumi.getter(name="defaultDataLakeStoreAccount")
    def default_data_lake_store_account(self) -> pulumi.Output[str]:
        """
        The default Data Lake Store account associated with this account.
        """
        return pulumi.get(self, "default_data_lake_store_account")

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[str]:
        """
        The full CName endpoint for this account.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="firewallAllowAzureIps")
    def firewall_allow_azure_ips(self) -> pulumi.Output[Optional[str]]:
        """
        The current state of allowing or disallowing IPs originating within Azure through the firewall. If the firewall is disabled, this is not enforced.
        """
        return pulumi.get(self, "firewall_allow_azure_ips")

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> pulumi.Output[Sequence['outputs.FirewallRuleResponse']]:
        """
        The list of firewall rules associated with this account.
        """
        return pulumi.get(self, "firewall_rules")

    @property
    @pulumi.getter(name="firewallState")
    def firewall_state(self) -> pulumi.Output[Optional[str]]:
        """
        The current state of the IP address firewall for this account.
        """
        return pulumi.get(self, "firewall_state")

    @property
    @pulumi.getter(name="hierarchicalQueueState")
    def hierarchical_queue_state(self) -> pulumi.Output[str]:
        """
        The hierarchical queue state associated with this account.
        """
        return pulumi.get(self, "hierarchical_queue_state")

    @property
    @pulumi.getter(name="hiveMetastores")
    def hive_metastores(self) -> pulumi.Output[Sequence['outputs.HiveMetastoreResponse']]:
        """
        The list of hiveMetastores associated with this account.
        """
        return pulumi.get(self, "hive_metastores")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        The account last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxDegreeOfParallelism")
    def max_degree_of_parallelism(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum supported degree of parallelism for this account.
        """
        return pulumi.get(self, "max_degree_of_parallelism")

    @property
    @pulumi.getter(name="maxDegreeOfParallelismPerJob")
    def max_degree_of_parallelism_per_job(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum supported degree of parallelism per job for this account.
        """
        return pulumi.get(self, "max_degree_of_parallelism_per_job")

    @property
    @pulumi.getter(name="maxJobCount")
    def max_job_count(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum supported jobs running under the account at the same time.
        """
        return pulumi.get(self, "max_job_count")

    @property
    @pulumi.getter(name="minPriorityPerJob")
    def min_priority_per_job(self) -> pulumi.Output[int]:
        """
        The minimum supported priority per job for this account.
        """
        return pulumi.get(self, "min_priority_per_job")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="newTier")
    def new_tier(self) -> pulumi.Output[Optional[str]]:
        """
        The commitment tier for the next month.
        """
        return pulumi.get(self, "new_tier")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning status of the Data Lake Analytics account.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicDataLakeStoreAccounts")
    def public_data_lake_store_accounts(self) -> pulumi.Output[Optional[Sequence['outputs.DataLakeStoreAccountInformationResponse']]]:
        """
        The list of Data Lake Store accounts associated with this account.
        """
        return pulumi.get(self, "public_data_lake_store_accounts")

    @property
    @pulumi.getter(name="queryStoreRetention")
    def query_store_retention(self) -> pulumi.Output[Optional[int]]:
        """
        The number of days that job metadata is retained.
        """
        return pulumi.get(self, "query_store_retention")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the Data Lake Analytics account.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> pulumi.Output[Sequence['outputs.StorageAccountInformationResponse']]:
        """
        The list of Azure Blob Storage accounts associated with this account.
        """
        return pulumi.get(self, "storage_accounts")

    @property
    @pulumi.getter(name="systemMaxDegreeOfParallelism")
    def system_max_degree_of_parallelism(self) -> pulumi.Output[int]:
        """
        The system defined maximum supported degree of parallelism for this account, which restricts the maximum value of parallelism the user can set for the account.
        """
        return pulumi.get(self, "system_max_degree_of_parallelism")

    @property
    @pulumi.getter(name="systemMaxJobCount")
    def system_max_job_count(self) -> pulumi.Output[int]:
        """
        The system defined maximum supported jobs running under the account at the same time, which restricts the maximum number of running jobs the user can set for the account.
        """
        return pulumi.get(self, "system_max_job_count")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> pulumi.Output[Sequence['outputs.VirtualNetworkRuleResponse']]:
        """
        The list of virtualNetwork rules associated with this account.
        """
        return pulumi.get(self, "virtual_network_rules")

