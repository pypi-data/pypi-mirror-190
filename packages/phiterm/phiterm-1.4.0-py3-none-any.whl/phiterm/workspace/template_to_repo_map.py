from typing import Dict

from phiterm.workspace.ws_enums import WorkspaceStarterTemplate

template_to_repo_map: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.aws_dp: "https://github.com/phidatahq/aws-dp-template.git",
    WorkspaceStarterTemplate.aws_snowflake_dp: "https://github.com/phidatahq/aws-snowflake-dp-template.git",
    WorkspaceStarterTemplate.aws_api_server: "https://github.com/phidatahq/aws-api-server-template.git",
    WorkspaceStarterTemplate.aws_ml_server: "https://github.com/phidatahq/aws-ml-server-template.git",
}
