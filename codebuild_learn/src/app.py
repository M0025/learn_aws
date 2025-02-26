#!/usr/bin/env python3
import aws_cdk as cdk
from codebuild_learn.codebuild_learn_stack import CodebuildLearnStack
import boto3
import os
# 指定 AWS Profile
profile = os.getenv("AWS_PROFILE", "sandbox")  # 默认为 'sandbox'，可通过环境变量覆盖
session = boto3.Session(profile_name=profile)

# 获取当前调用者身份以获取 AWS 账户 ID 和区域
account_id = session.client('sts').get_caller_identity()['Account']
region = session.region_name or 'ap-northeast-1'  # 默认东京区域

app = cdk.App()

# 创建 Stack 并指定环境
CodebuildLearnStack(app, "CodebuildLearnStack",
    env=cdk.Environment(account=account_id, region=region)
)

app.synth()