'''
# Attini CDK

The Attini CDK is currently an experimental feature.

## How to use

The Attini CDK Constructs are used to generate a CloudFormation template for
(attini deplyment plans)[https://attini.io/attini-concepts/].
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import aws_cdk.aws_stepfunctions_tasks as _aws_cdk_aws_stepfunctions_tasks_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniCfnProps",
    jsii_struct_bases=[],
    name_mapping={
        "stack_name": "stackName",
        "template": "template",
        "action": "action",
        "config_file": "configFile",
        "enable_termination_protection": "enableTerminationProtection",
        "execution_role_arn": "executionRoleArn",
        "output_path": "outputPath",
        "parameters": "parameters",
        "region": "region",
        "stack_role_arn": "stackRoleArn",
        "tags": "tags",
        "variables": "variables",
    },
)
class AttiniCfnProps:
    def __init__(
        self,
        *,
        stack_name: builtins.str,
        template: builtins.str,
        action: typing.Optional[builtins.str] = None,
        config_file: typing.Optional[builtins.str] = None,
        enable_termination_protection: typing.Optional[builtins.bool] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param stack_name: 
        :param template: 
        :param action: 
        :param config_file: 
        :param enable_termination_protection: 
        :param execution_role_arn: 
        :param output_path: 
        :param parameters: 
        :param region: 
        :param stack_role_arn: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efee3739a3d8d157597580f32a2f019cc45f6723b85476b2f3e94a6be3e77dec)
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument enable_termination_protection", value=enable_termination_protection, expected_type=type_hints["enable_termination_protection"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument output_path", value=output_path, expected_type=type_hints["output_path"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stack_role_arn", value=stack_role_arn, expected_type=type_hints["stack_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack_name": stack_name,
            "template": template,
        }
        if action is not None:
            self._values["action"] = action
        if config_file is not None:
            self._values["config_file"] = config_file
        if enable_termination_protection is not None:
            self._values["enable_termination_protection"] = enable_termination_protection
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if region is not None:
            self._values["region"] = region
        if stack_role_arn is not None:
            self._values["stack_role_arn"] = stack_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def stack_name(self) -> builtins.str:
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> builtins.str:
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_file(self) -> typing.Optional[builtins.str]:
        result = self._values.get("config_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_termination_protection(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stack_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniCfnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniImportProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_type": "sourceType",
        "distribution_source": "distributionSource",
        "execution_role_arn": "executionRoleArn",
        "mapping": "mapping",
        "s3_source": "s3Source",
    },
)
class AttiniImportProps:
    def __init__(
        self,
        *,
        source_type: "SourceType",
        distribution_source: typing.Optional[typing.Union["DistributionSource", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        s3_source: typing.Optional[typing.Union["S3Source", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_type: 
        :param distribution_source: 
        :param execution_role_arn: 
        :param mapping: 
        :param s3_source: 
        '''
        if isinstance(distribution_source, dict):
            distribution_source = DistributionSource(**distribution_source)
        if isinstance(s3_source, dict):
            s3_source = S3Source(**s3_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4272a047f0c54f5f4793626d07ed10c5985251edbd6d8440e6d12c44ee5d6bf)
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument distribution_source", value=distribution_source, expected_type=type_hints["distribution_source"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
            check_type(argname="argument s3_source", value=s3_source, expected_type=type_hints["s3_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_type": source_type,
        }
        if distribution_source is not None:
            self._values["distribution_source"] = distribution_source
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if mapping is not None:
            self._values["mapping"] = mapping
        if s3_source is not None:
            self._values["s3_source"] = s3_source

    @builtins.property
    def source_type(self) -> "SourceType":
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast("SourceType", result)

    @builtins.property
    def distribution_source(self) -> typing.Optional["DistributionSource"]:
        result = self._values.get("distribution_source")
        return typing.cast(typing.Optional["DistributionSource"], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapping(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def s3_source(self) -> typing.Optional["S3Source"]:
        result = self._values.get("s3_source")
        return typing.cast(typing.Optional["S3Source"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniImportProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniLambdaInvokeProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "client_context": "clientContext",
        "invocation_type": "invocationType",
        "payload": "payload",
        "qualifier": "qualifier",
    },
)
class AttiniLambdaInvokeProps:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        client_context: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType] = None,
        payload: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param function_name: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function.
        :param invocation_type: Invocation type of the Lambda function.
        :param payload: The JSON that will be supplied as input to the Lambda function.
        :param qualifier: Version or alias to invoke a published version of the function.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9319b97be1b91b9451a0489e5f3f56a999c0bdb85c333bfbd50eaee32e78260)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument client_context", value=client_context, expected_type=type_hints["client_context"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
        }
        if client_context is not None:
            self._values["client_context"] = client_context
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if payload is not None:
            self._values["payload"] = payload
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def function_name(self) -> builtins.str:
        '''Lambda function to invoke.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_context(self) -> typing.Optional[builtins.str]:
        '''Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function.'''
        result = self._values.get("client_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType]:
        '''Invocation type of the Lambda function.'''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType], result)

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[typing.Any, typing.Any]]:
        '''The JSON that will be supplied as input to the Lambda function.'''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[typing.Mapping[typing.Any, typing.Any]], result)

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        '''Version or alias to invoke a published version of the function.'''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniLambdaInvokeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AttiniRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniRunner",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union["AwsVpcConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_name: typing.Optional[builtins.str] = None,
        ecs_cluster: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        runner_configuration: typing.Optional[typing.Union["RunnerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        startup: typing.Optional[typing.Union["Startup", typing.Dict[builtins.str, typing.Any]]] = None,
        task_definition_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_vpc_configuration: 
        :param container_name: 
        :param ecs_cluster: 
        :param image: 
        :param role_arn: 
        :param runner_configuration: 
        :param startup: 
        :param task_definition_arn: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660ed4052feaa95482efe568ab8ebc4f76163ce6d31bba60f75428748043a640)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniRunnerProps(
            aws_vpc_configuration=aws_vpc_configuration,
            container_name=container_name,
            ecs_cluster=ecs_cluster,
            image=image,
            role_arn=role_arn,
            runner_configuration=runner_configuration,
            startup=startup,
            task_definition_arn=task_definition_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="runnerName")
    def runner_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnerName"))


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniRunnerJobProps",
    jsii_struct_bases=[],
    name_mapping={"commands": "commands", "runner": "runner"},
)
class AttiniRunnerJobProps:
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        runner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param commands: 
        :param runner: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae193c66e80029f3db0b0c6578f97c4c712826e72eb55f45f880c14f2aaf3c46)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
        }
        if runner is not None:
            self._values["runner"] = runner

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def runner(self) -> typing.Optional[builtins.str]:
        result = self._values.get("runner")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniRunnerJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_vpc_configuration": "awsVpcConfiguration",
        "container_name": "containerName",
        "ecs_cluster": "ecsCluster",
        "image": "image",
        "role_arn": "roleArn",
        "runner_configuration": "runnerConfiguration",
        "startup": "startup",
        "task_definition_arn": "taskDefinitionArn",
    },
)
class AttiniRunnerProps:
    def __init__(
        self,
        *,
        aws_vpc_configuration: typing.Optional[typing.Union["AwsVpcConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        container_name: typing.Optional[builtins.str] = None,
        ecs_cluster: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        runner_configuration: typing.Optional[typing.Union["RunnerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        startup: typing.Optional[typing.Union["Startup", typing.Dict[builtins.str, typing.Any]]] = None,
        task_definition_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_vpc_configuration: 
        :param container_name: 
        :param ecs_cluster: 
        :param image: 
        :param role_arn: 
        :param runner_configuration: 
        :param startup: 
        :param task_definition_arn: 
        '''
        if isinstance(aws_vpc_configuration, dict):
            aws_vpc_configuration = AwsVpcConfiguration(**aws_vpc_configuration)
        if isinstance(runner_configuration, dict):
            runner_configuration = RunnerConfiguration(**runner_configuration)
        if isinstance(startup, dict):
            startup = Startup(**startup)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fca31ef6f03939f00deed50f6175576696144f7d8eb08c3c6dab2f5143f2ff6)
            check_type(argname="argument aws_vpc_configuration", value=aws_vpc_configuration, expected_type=type_hints["aws_vpc_configuration"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument ecs_cluster", value=ecs_cluster, expected_type=type_hints["ecs_cluster"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument runner_configuration", value=runner_configuration, expected_type=type_hints["runner_configuration"])
            check_type(argname="argument startup", value=startup, expected_type=type_hints["startup"])
            check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_vpc_configuration is not None:
            self._values["aws_vpc_configuration"] = aws_vpc_configuration
        if container_name is not None:
            self._values["container_name"] = container_name
        if ecs_cluster is not None:
            self._values["ecs_cluster"] = ecs_cluster
        if image is not None:
            self._values["image"] = image
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if runner_configuration is not None:
            self._values["runner_configuration"] = runner_configuration
        if startup is not None:
            self._values["startup"] = startup
        if task_definition_arn is not None:
            self._values["task_definition_arn"] = task_definition_arn

    @builtins.property
    def aws_vpc_configuration(self) -> typing.Optional["AwsVpcConfiguration"]:
        result = self._values.get("aws_vpc_configuration")
        return typing.cast(typing.Optional["AwsVpcConfiguration"], result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs_cluster(self) -> typing.Optional[builtins.str]:
        result = self._values.get("ecs_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runner_configuration(self) -> typing.Optional["RunnerConfiguration"]:
        result = self._values.get("runner_configuration")
        return typing.cast(typing.Optional["RunnerConfiguration"], result)

    @builtins.property
    def startup(self) -> typing.Optional["Startup"]:
        result = self._values.get("startup")
        return typing.cast(typing.Optional["Startup"], result)

    @builtins.property
    def task_definition_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("task_definition_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.AttiniSamProps",
    jsii_struct_bases=[],
    name_mapping={
        "project": "project",
        "stack_name": "stackName",
        "action": "action",
        "config_file": "configFile",
        "enable_termination_protection": "enableTerminationProtection",
        "execution_role_arn": "executionRoleArn",
        "parameters": "parameters",
        "stack_role_arn": "stackRoleArn",
        "tags": "tags",
        "variables": "variables",
    },
)
class AttiniSamProps:
    def __init__(
        self,
        *,
        project: typing.Union["Project", typing.Dict[builtins.str, typing.Any]],
        stack_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        config_file: typing.Optional[builtins.str] = None,
        enable_termination_protection: typing.Optional[builtins.bool] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stack_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param project: 
        :param stack_name: 
        :param action: 
        :param config_file: 
        :param enable_termination_protection: 
        :param execution_role_arn: 
        :param parameters: 
        :param stack_role_arn: 
        :param tags: 
        :param variables: 
        '''
        if isinstance(project, dict):
            project = Project(**project)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935e347576123adb888e488d474420b0c9baa9be31ae99190bcc69e96b58d1d5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument enable_termination_protection", value=enable_termination_protection, expected_type=type_hints["enable_termination_protection"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument stack_role_arn", value=stack_role_arn, expected_type=type_hints["stack_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
            "stack_name": stack_name,
        }
        if action is not None:
            self._values["action"] = action
        if config_file is not None:
            self._values["config_file"] = config_file
        if enable_termination_protection is not None:
            self._values["enable_termination_protection"] = enable_termination_protection
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if parameters is not None:
            self._values["parameters"] = parameters
        if stack_role_arn is not None:
            self._values["stack_role_arn"] = stack_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def project(self) -> "Project":
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast("Project", result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_file(self) -> typing.Optional[builtins.str]:
        result = self._values.get("config_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_termination_protection(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stack_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stack_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttiniSamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, _aws_cdk_aws_stepfunctions_ceddda9d.INextable)
class AttiniState(
    _aws_cdk_aws_stepfunctions_ceddda9d.State,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@attini/cdk.AttiniState",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61484c7fed517c4a84c18c237681abe348106fa95fe19f286910d6f5824bba1a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="next")
    def next(
        self,
        next: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        '''Go to the indicated state after this state.

        :param next: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3d93cc289d6cadd1689ab5dfb1a692b6400219b43133ea453ce59a074f2130)
            check_type(argname="argument next", value=next, expected_type=type_hints["next"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="renderProps")
    @abc.abstractmethod
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        ...

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''Render the state as JSON.'''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable]:
        '''Continuable states of this Chainable.'''
        return typing.cast(typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable], jsii.get(self, "endStates"))

    @builtins.property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> builtins.str:
        ...

    @type.setter
    @abc.abstractmethod
    def type(self, value: builtins.str) -> None:
        ...


class _AttiniStateProxy(
    AttiniState,
    jsii.proxy_for(_aws_cdk_aws_stepfunctions_ceddda9d.State), # type: ignore[misc]
):
    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da77a215a76820be36b301c6f44b5c1b86ed6561e685b603143ad8361ecb0dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AttiniState).__jsii_proxy_class__ = lambda : _AttiniStateProxy


class AttiniTask(
    AttiniState,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@attini/cdk.AttiniTask",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0280f6d5e2bb29f5c6e3e338e4df2b5cd4fe610260577f4f2fe773779c83fa06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="getOutputPath")
    def get_output_path(
        self,
        path: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Get the json path to this steps output.

        Convenience
        method that will return a string with the following format
        $.output...

        :param path: - The path to the value from the outputs root.

        :: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca4cee19a72afc9be870d0bab9f61fc828058e6f8897c6753f1f5d2737d3c58)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(builtins.str, jsii.invoke(self, "getOutputPath", [path]))


class _AttiniTaskProxy(
    AttiniTask,
    jsii.proxy_for(AttiniState), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AttiniTask).__jsii_proxy_class__ = lambda : _AttiniTaskProxy


@jsii.data_type(
    jsii_type="@attini/cdk.AwsVpcConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class AwsVpcConfiguration:
    def __init__(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assign_public_ip: 
        :param security_groups: 
        :param subnets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017915461dbc8dcfdff54e43f11b8aa0851931a8cb448ee5a13bd6b1dc1691a1)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsVpcConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeploymentPlan(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.DeploymentPlan",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        definition: _aws_cdk_aws_stepfunctions_ceddda9d.Chain,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param definition: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2885b2d345e6ab77c7d63f1ce19c13ad634ffd1ab4652e4723dd2228ec8757f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DeploymentPlanProps(definition=definition)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@attini/cdk.DeploymentPlanProps",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition"},
)
class DeploymentPlanProps:
    def __init__(
        self,
        *,
        definition: _aws_cdk_aws_stepfunctions_ceddda9d.Chain,
    ) -> None:
        '''
        :param definition: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c8b8e079c57e087176c5737b3648eb0acf7aea26e121bf2f42dba6bba40b9e)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }

    @builtins.property
    def definition(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentPlanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeploymentPlanStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.DeploymentPlanStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6a51d1475caa2a9af656abae5bcf0f588e6df3d2ea248ed5cc9f81dd8bd2cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.StackProps(
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@attini/cdk.DistributionSource",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class DistributionSource:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c396e701f6efcb92c096d07741726f7f6fc70b675aee75bbcc6a7683d7cf0396)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.Project",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "build_dir": "buildDir", "template": "template"},
)
class Project:
    def __init__(
        self,
        *,
        path: builtins.str,
        build_dir: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: 
        :param build_dir: 
        :param template: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b5541fa7622b1155017a66dc54ea8b3d313290b55062564f73ff9a3a70e192)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument build_dir", value=build_dir, expected_type=type_hints["build_dir"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if build_dir is not None:
            self._values["build_dir"] = build_dir
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_dir(self) -> typing.Optional[builtins.str]:
        result = self._values.get("build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Project(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PropsUtil(metaclass=jsii.JSIIMeta, jsii_type="@attini/cdk.PropsUtil"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fixCase")
    @builtins.classmethod
    def fix_case(cls, props: typing.Any) -> typing.Mapping[typing.Any, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd230e32fafd39d2b52ca73d0926bb8990dfe883bc95e6cff13a985ec638971)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.sinvoke(cls, "fixCase", [props]))


@jsii.data_type(
    jsii_type="@attini/cdk.RunnerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "idle_time_to_live": "idleTimeToLive",
        "job_timeout": "jobTimeout",
        "log_level": "logLevel",
        "max_concurrent_jobs": "maxConcurrentJobs",
    },
)
class RunnerConfiguration:
    def __init__(
        self,
        *,
        idle_time_to_live: typing.Optional[jsii.Number] = None,
        job_timeout: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_concurrent_jobs: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param idle_time_to_live: 
        :param job_timeout: 
        :param log_level: 
        :param max_concurrent_jobs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ae26cb00abc467b50f2dc4e1eb5424c750c987c736744283d07fa06afd9399)
            check_type(argname="argument idle_time_to_live", value=idle_time_to_live, expected_type=type_hints["idle_time_to_live"])
            check_type(argname="argument job_timeout", value=job_timeout, expected_type=type_hints["job_timeout"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument max_concurrent_jobs", value=max_concurrent_jobs, expected_type=type_hints["max_concurrent_jobs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_time_to_live is not None:
            self._values["idle_time_to_live"] = idle_time_to_live
        if job_timeout is not None:
            self._values["job_timeout"] = job_timeout
        if log_level is not None:
            self._values["log_level"] = log_level
        if max_concurrent_jobs is not None:
            self._values["max_concurrent_jobs"] = max_concurrent_jobs

    @builtins.property
    def idle_time_to_live(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("idle_time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def job_timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("job_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrent_jobs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_concurrent_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@attini/cdk.S3Source",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class S3Source:
    def __init__(self, *, bucket: builtins.str, key: builtins.str) -> None:
        '''
        :param bucket: 
        :param key: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdae58e2f57d92f4a7ad74ea5af81c7b2d0e28d2f5ea75ee6b393f57337e41d2)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@attini/cdk.SourceType")
class SourceType(enum.Enum):
    S3_SOURCE = "S3_SOURCE"
    DISTRIBUTION_SOURCE = "DISTRIBUTION_SOURCE"


@jsii.data_type(
    jsii_type="@attini/cdk.Startup",
    jsii_struct_bases=[],
    name_mapping={"commands": "commands", "commands_timeout": "commandsTimeout"},
)
class Startup:
    def __init__(
        self,
        *,
        commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        commands_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param commands: 
        :param commands_timeout: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cc1948a8e614a2a963dff1af42e2cc454066bda9674044c8d0398b3e1db6ee)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument commands_timeout", value=commands_timeout, expected_type=type_hints["commands_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if commands is not None:
            self._values["commands"] = commands
        if commands_timeout is not None:
            self._values["commands_timeout"] = commands_timeout

    @builtins.property
    def commands(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def commands_timeout(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("commands_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Startup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AttiniCfn(AttiniTask, metaclass=jsii.JSIIMeta, jsii_type="@attini/cdk.AttiniCfn"):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stack_name: builtins.str,
        template: builtins.str,
        action: typing.Optional[builtins.str] = None,
        config_file: typing.Optional[builtins.str] = None,
        enable_termination_protection: typing.Optional[builtins.bool] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stack_name: 
        :param template: 
        :param action: 
        :param config_file: 
        :param enable_termination_protection: 
        :param execution_role_arn: 
        :param output_path: 
        :param parameters: 
        :param region: 
        :param stack_role_arn: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54478923aeac4042c35c75785f865162694731c0c225aebea693c341fc5ae7a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniCfnProps(
            stack_name=stack_name,
            template=template,
            action=action,
            config_file=config_file,
            enable_termination_protection=enable_termination_protection,
            execution_role_arn=execution_role_arn,
            output_path=output_path,
            parameters=parameters,
            region=region,
            stack_role_arn=stack_role_arn,
            tags=tags,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fbf431173dc996ee863c8a3e4d036da6ee93330f61666bd8ce0e0f41439757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniImport(
    AttiniTask,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniImport",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_type: SourceType,
        distribution_source: typing.Optional[typing.Union[DistributionSource, typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        s3_source: typing.Optional[typing.Union[S3Source, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_type: 
        :param distribution_source: 
        :param execution_role_arn: 
        :param mapping: 
        :param s3_source: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2a675fc157b4a2d0181c771cc0fd92a88d36e9d7df5e02c45ba50684817b2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniImportProps(
            source_type=source_type,
            distribution_source=distribution_source,
            execution_role_arn=execution_role_arn,
            mapping=mapping,
            s3_source=s3_source,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ceb1437fb7ec5255d44261203a95bf4e16f550118e5176d56325c5bedc84dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniLambdaInvoke(
    AttiniState,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniLambdaInvoke",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        function_name: builtins.str,
        client_context: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType] = None,
        payload: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param function_name: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function.
        :param invocation_type: Invocation type of the Lambda function.
        :param payload: The JSON that will be supplied as input to the Lambda function.
        :param qualifier: Version or alias to invoke a published version of the function.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4649f44ba2240df9b9c2d484418c479bdf74e09403c20b15c7a4fef49292d379)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniLambdaInvokeProps(
            function_name=function_name,
            client_context=client_context,
            invocation_type=invocation_type,
            payload=payload,
            qualifier=qualifier,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320686430ecf0920e9292b5f1f7284cbb0e671248f9eb026c2870cac0e651ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniManualApproval(
    AttiniTask,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniManualApproval",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f122fb80effa349f97fede301ec431126abe9d9a1432a2653d6b81460744a9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff510d1e2041e8283374b3a6450f774c85ba5f2f733294337e44f28c89b2cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniMerge(
    AttiniState,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniMerge",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e2e3acbff353ccd76b8d125391d657b91af7dc9525a9f2ed6c87db2295b776)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049fcdff8f8a6da495e421047638ac0e956da20360f17bf60d8c6e1465f74ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniRunnerJob(
    AttiniTask,
    metaclass=jsii.JSIIMeta,
    jsii_type="@attini/cdk.AttiniRunnerJob",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        commands: typing.Sequence[builtins.str],
        runner: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param commands: 
        :param runner: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f87e8d114e474018f355f4a9d07dfd1fa04529858c88fa98dcdabae47d9166)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniRunnerJobProps(commands=commands, runner=runner)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dac10205258bc21c390ea1f0cd1a1735e5d7b07b40362d9bed7ff26d2439081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


class AttiniSam(AttiniTask, metaclass=jsii.JSIIMeta, jsii_type="@attini/cdk.AttiniSam"):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        project: typing.Union[Project, typing.Dict[builtins.str, typing.Any]],
        stack_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        config_file: typing.Optional[builtins.str] = None,
        enable_termination_protection: typing.Optional[builtins.bool] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stack_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param project: 
        :param stack_name: 
        :param action: 
        :param config_file: 
        :param enable_termination_protection: 
        :param execution_role_arn: 
        :param parameters: 
        :param stack_role_arn: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ddb904e07478beb1701637d8302e9bc1f8f9f5e367519b6b8d8179d0bda1ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AttiniSamProps(
            project=project,
            stack_name=stack_name,
            action=action,
            config_file=config_file,
            enable_termination_protection=enable_termination_protection,
            execution_role_arn=execution_role_arn,
            parameters=parameters,
            stack_role_arn=stack_role_arn,
            tags=tags,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="renderProps")
    def _render_props(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "renderProps", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c7f5ee2937aa55f3b81817dd4fd94a0677c01883333e11abac2727faac72ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


__all__ = [
    "AttiniCfn",
    "AttiniCfnProps",
    "AttiniImport",
    "AttiniImportProps",
    "AttiniLambdaInvoke",
    "AttiniLambdaInvokeProps",
    "AttiniManualApproval",
    "AttiniMerge",
    "AttiniRunner",
    "AttiniRunnerJob",
    "AttiniRunnerJobProps",
    "AttiniRunnerProps",
    "AttiniSam",
    "AttiniSamProps",
    "AttiniState",
    "AttiniTask",
    "AwsVpcConfiguration",
    "DeploymentPlan",
    "DeploymentPlanProps",
    "DeploymentPlanStack",
    "DistributionSource",
    "Project",
    "PropsUtil",
    "RunnerConfiguration",
    "S3Source",
    "SourceType",
    "Startup",
]

publication.publish()

def _typecheckingstub__efee3739a3d8d157597580f32a2f019cc45f6723b85476b2f3e94a6be3e77dec(
    *,
    stack_name: builtins.str,
    template: builtins.str,
    action: typing.Optional[builtins.str] = None,
    config_file: typing.Optional[builtins.str] = None,
    enable_termination_protection: typing.Optional[builtins.bool] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    output_path: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    stack_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4272a047f0c54f5f4793626d07ed10c5985251edbd6d8440e6d12c44ee5d6bf(
    *,
    source_type: SourceType,
    distribution_source: typing.Optional[typing.Union[DistributionSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    s3_source: typing.Optional[typing.Union[S3Source, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9319b97be1b91b9451a0489e5f3f56a999c0bdb85c333bfbd50eaee32e78260(
    *,
    function_name: builtins.str,
    client_context: typing.Optional[builtins.str] = None,
    invocation_type: typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType] = None,
    payload: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
    qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660ed4052feaa95482efe568ab8ebc4f76163ce6d31bba60f75428748043a640(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_vpc_configuration: typing.Optional[typing.Union[AwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    container_name: typing.Optional[builtins.str] = None,
    ecs_cluster: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    runner_configuration: typing.Optional[typing.Union[RunnerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    startup: typing.Optional[typing.Union[Startup, typing.Dict[builtins.str, typing.Any]]] = None,
    task_definition_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae193c66e80029f3db0b0c6578f97c4c712826e72eb55f45f880c14f2aaf3c46(
    *,
    commands: typing.Sequence[builtins.str],
    runner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fca31ef6f03939f00deed50f6175576696144f7d8eb08c3c6dab2f5143f2ff6(
    *,
    aws_vpc_configuration: typing.Optional[typing.Union[AwsVpcConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    container_name: typing.Optional[builtins.str] = None,
    ecs_cluster: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    runner_configuration: typing.Optional[typing.Union[RunnerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    startup: typing.Optional[typing.Union[Startup, typing.Dict[builtins.str, typing.Any]]] = None,
    task_definition_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935e347576123adb888e488d474420b0c9baa9be31ae99190bcc69e96b58d1d5(
    *,
    project: typing.Union[Project, typing.Dict[builtins.str, typing.Any]],
    stack_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    config_file: typing.Optional[builtins.str] = None,
    enable_termination_protection: typing.Optional[builtins.bool] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stack_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61484c7fed517c4a84c18c237681abe348106fa95fe19f286910d6f5824bba1a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3d93cc289d6cadd1689ab5dfb1a692b6400219b43133ea453ce59a074f2130(
    next: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da77a215a76820be36b301c6f44b5c1b86ed6561e685b603143ad8361ecb0dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0280f6d5e2bb29f5c6e3e338e4df2b5cd4fe610260577f4f2fe773779c83fa06(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca4cee19a72afc9be870d0bab9f61fc828058e6f8897c6753f1f5d2737d3c58(
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017915461dbc8dcfdff54e43f11b8aa0851931a8cb448ee5a13bd6b1dc1691a1(
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2885b2d345e6ab77c7d63f1ce19c13ad634ffd1ab4652e4723dd2228ec8757f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    definition: _aws_cdk_aws_stepfunctions_ceddda9d.Chain,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c8b8e079c57e087176c5737b3648eb0acf7aea26e121bf2f42dba6bba40b9e(
    *,
    definition: _aws_cdk_aws_stepfunctions_ceddda9d.Chain,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6a51d1475caa2a9af656abae5bcf0f588e6df3d2ea248ed5cc9f81dd8bd2cb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c396e701f6efcb92c096d07741726f7f6fc70b675aee75bbcc6a7683d7cf0396(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b5541fa7622b1155017a66dc54ea8b3d313290b55062564f73ff9a3a70e192(
    *,
    path: builtins.str,
    build_dir: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd230e32fafd39d2b52ca73d0926bb8990dfe883bc95e6cff13a985ec638971(
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ae26cb00abc467b50f2dc4e1eb5424c750c987c736744283d07fa06afd9399(
    *,
    idle_time_to_live: typing.Optional[jsii.Number] = None,
    job_timeout: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_concurrent_jobs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdae58e2f57d92f4a7ad74ea5af81c7b2d0e28d2f5ea75ee6b393f57337e41d2(
    *,
    bucket: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cc1948a8e614a2a963dff1af42e2cc454066bda9674044c8d0398b3e1db6ee(
    *,
    commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    commands_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54478923aeac4042c35c75785f865162694731c0c225aebea693c341fc5ae7a6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stack_name: builtins.str,
    template: builtins.str,
    action: typing.Optional[builtins.str] = None,
    config_file: typing.Optional[builtins.str] = None,
    enable_termination_protection: typing.Optional[builtins.bool] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    output_path: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    stack_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fbf431173dc996ee863c8a3e4d036da6ee93330f61666bd8ce0e0f41439757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2a675fc157b4a2d0181c771cc0fd92a88d36e9d7df5e02c45ba50684817b2b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_type: SourceType,
    distribution_source: typing.Optional[typing.Union[DistributionSource, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    s3_source: typing.Optional[typing.Union[S3Source, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ceb1437fb7ec5255d44261203a95bf4e16f550118e5176d56325c5bedc84dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4649f44ba2240df9b9c2d484418c479bdf74e09403c20b15c7a4fef49292d379(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    function_name: builtins.str,
    client_context: typing.Optional[builtins.str] = None,
    invocation_type: typing.Optional[_aws_cdk_aws_stepfunctions_tasks_ceddda9d.LambdaInvocationType] = None,
    payload: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
    qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320686430ecf0920e9292b5f1f7284cbb0e671248f9eb026c2870cac0e651ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f122fb80effa349f97fede301ec431126abe9d9a1432a2653d6b81460744a9c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff510d1e2041e8283374b3a6450f774c85ba5f2f733294337e44f28c89b2cbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e2e3acbff353ccd76b8d125391d657b91af7dc9525a9f2ed6c87db2295b776(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049fcdff8f8a6da495e421047638ac0e956da20360f17bf60d8c6e1465f74ffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f87e8d114e474018f355f4a9d07dfd1fa04529858c88fa98dcdabae47d9166(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    commands: typing.Sequence[builtins.str],
    runner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dac10205258bc21c390ea1f0cd1a1735e5d7b07b40362d9bed7ff26d2439081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ddb904e07478beb1701637d8302e9bc1f8f9f5e367519b6b8d8179d0bda1ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    project: typing.Union[Project, typing.Dict[builtins.str, typing.Any]],
    stack_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    config_file: typing.Optional[builtins.str] = None,
    enable_termination_protection: typing.Optional[builtins.bool] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stack_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c7f5ee2937aa55f3b81817dd4fd94a0677c01883333e11abac2727faac72ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
