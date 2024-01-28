from constructs import Construct
from aws_cdk import (
        aws_ec2 as ec2,
        aws_iam as iam,
)

class ClusterSecurity(Construct):

    def __init__(self, scope: Construct, id: str,vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.security_group = ec2.SecurityGroup(self, "SecurityEcsCDKGroup",
            vpc=vpc,
            description="cdk ECS Task Security Group"
        )

        self.security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow incoming HTTP traffic"
        )

        self.instance_iam_role = iam.Role.from_role_arn(
            self, "ExistingInstanceIAMRole",
            role_arn="existing instance role"
        )

        task_role_arn = "existing task role"
        self.task_role = iam.Role.from_role_arn(self, "TaskExecutionRole", task_role_arn)