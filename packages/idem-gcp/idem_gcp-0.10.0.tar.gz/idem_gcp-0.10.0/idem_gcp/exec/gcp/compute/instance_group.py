"""Exec module for managing Instance Groups."""

__func_alias__ = {"list_": "list"}

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope
from idem_gcp.tool.gcp.utils import get_project_from_account


async def list_(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    filter: str = None,
    order_by: str = None,
):
    r"""Retrieves the list of zonal instance group resources contained within the specified zone. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone where the instance group is located.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.list
              - kwargs:
                  project: project-name
                  zone: zone-name
    """
    project = get_project_from_account(ctx, project)

    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="list",
        method_params={
            "ctx": ctx,
            "project": project,
            "zone": zone,
            "filter": filter,
            "order_by": order_by,
        },
        exec_params={
            ExecParam.SCOPED_FUNCTIONS: {
                Scope.ZONAL: "list",
                Scope.GLOBAL: "aggregatedList",
            }
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    instance_group: str = None,
):
    r"""Returns the specified zonal instance group. acceleratorTypes.get a list of available zonal instance groups by making a list() request. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance_group(str, Optional): The name of the instance group. Authorization requires the following IAM
        permission on the specified resource instanceGroup: compute.instance_group.get.

    Examples:
        .. code-block: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.get
              - kwargs:
                  project: project-name
                  zone: zone-name
                  instance: instance-name
    """
    project = get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instanceGroup": instance_group,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


# genericExecExecution
# return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
