from aws_cdk import Stack, aws_secretsmanager as secretsmanager, aws_codebuild as codebuild
from constructs import Construct

class CodebuildLearnStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 引用 Secrets Manager 中的 GitHub OAuth Token
        github_token = secretsmanager.Secret.from_secret_name_v2(
            self, "GithubToken", "github-oauth-token"  # 替换为你的 Secret 名称
        )

        # 创建 GitHub 凭证
        github_credentials = codebuild.GitHubSourceCredentials(
            self, "GitHubCredentials",  # 这里需要一个唯一的ID
            access_token=github_token.secret_value
        )

        # 创建 CodeBuild 项目
        codebuild.Project(
            self, "MiskoCodeBuildProject",
            project_name="misko-codebuild-project",
            source=codebuild.Source.git_hub(
                owner="M0025",             # 替换为你的 GitHub 用户名
                repo="learn_aws",         # 替换为你的 GitHub 仓库名
                webhook=True,             # 启用 webhook 自动触发构建
                webhook_filters=[
                    codebuild.FilterGroup.in_event_of(
                        codebuild.EventAction.PUSH,
                        codebuild.EventAction.PULL_REQUEST_MERGED
                    ).and_branch_is("main")  # 监听 main 分支
                ],
                report_build_status=True,  # 将构建状态回传到 GitHub
                webhook_triggers_batch_build=False,
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,  # 使用指定 CodeBuild 镜像
                compute_type=codebuild.ComputeType.SMALL,               # 设置计算资源大小
            ),
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"), 
        )