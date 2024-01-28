from constructs import Construct
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_autoscaling as autoscaling,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
)

from ecs_cdk.cluster_module.cluster_ecs_module import ClusterEcs
from ecs_cdk.cluster_module.cluster_network_module import ClusterNetwork
from ecs_cdk.cluster_module.cluster_security_module import ClusterSecurity

class CdkEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecs_cluster_network = ClusterNetwork(self, "ClusterNetwork")
        ecs_security = ClusterSecurity(self,"ClusterSecurity",vpc=ecs_cluster_network.vpc )
        ecs_cluster_construct = ClusterEcs(self, "ClusterEcs", vpc=ecs_cluster_network.vpc, sg=ecs_security.security_group, ei_iam_role=ecs_security.existing_instance_iam_role, task_role=ecs_security.task_role)