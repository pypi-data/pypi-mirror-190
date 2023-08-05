# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'RunbookTypeEnum',
]


class RunbookTypeEnum(str, Enum):
    """
    Gets or sets the type of the runbook.
    """
    SCRIPT = "Script"
    GRAPH = "Graph"
    POWER_SHELL_WORKFLOW = "PowerShellWorkflow"
    POWER_SHELL = "PowerShell"
    GRAPH_POWER_SHELL_WORKFLOW = "GraphPowerShellWorkflow"
    GRAPH_POWER_SHELL = "GraphPowerShell"
    PYTHON2 = "Python2"
    PYTHON3 = "Python3"
