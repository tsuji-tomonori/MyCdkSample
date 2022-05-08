import uuid

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
    Duration,
)
from constructs import Construct


PROJECK_NAME = "CdkSampleApp"
DESCRIPTION = "CDK Sample"


def build_resource_name(resource_name: str, service_name: str) -> str:
    return f"{resource_name}_{service_name}_cdk"


class MyCdkSampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self, build_resource_name("rol", "cdk_sample_role"),
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole")
            ],
            role_name=build_resource_name(
                "rol", "cdk_sample_role"),
            description=DESCRIPTION
        )

        layer = lambda_.LayerVersion(
            self, build_resource_name("lyr", "cdk_sample"),
            code=lambda_.Code.from_asset("layer"),
            layer_version_name=build_resource_name("lyr", "cdk_sample"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
            description="Python lib: cdk_sample",
        )

        fn = lambda_.Function(
            self, build_resource_name("lmd", "cdk_sample_service"),
            code=lambda_.Code.from_asset("lambda"),
            handler="lambda_function.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            function_name=build_resource_name(
                "lmd", "cdk_sample_service"),
            environment={
                "LOG_LEVEL": "ERROR",
                "HOGE": "hoge",
                "HUGA": "huga",
            },
            description=DESCRIPTION,
            timeout=Duration.seconds(300),
            memory_size=256,
            role=role,
            layers=[layer]
        )

        lambda_.Alias(
            self, f"{str(uuid.uuid4()).replace('-', '')[:5]}1",
            alias_name="live",
            version=lambda_.Version(
                self, "version",
                lambda_=fn,
                removal_policy=cdk.RemovalPolicy.RETAIN,
            ),
        )

        loggroup_name = f"/aws/lambda/{fn.function_name}"
        logs.LogGroup(
            self, build_resource_name("log", "cdk_sample_service"),
            log_group_name=loggroup_name,
            retention=logs.RetentionDays.THREE_MONTHS,
        )
