from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_autoscaling as autoscaling,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_servicediscovery as sd,
)
import aws_cdk as cdk
from ecs_cdk.cluster_module.cluster_network_module import ClusterNetwork
from ecs_cdk.cluster_module.cluster_security_module import ClusterSecurity

class ClusterEcs(Construct):
    
    def __init__(self, scope: Construct, id: str,vpc: ec2.Vpc, instance_iam_role: iam.Role,sg: ec2.SecurityGroup,task_role, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(
            self, "EcsCluster",
            vpc=vpc
        )
        
        auto_scaling_group = autoscaling.AutoScalingGroup(
            self, "ASG",
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            vpc=vpc,
            desired_capacity=1,
            role=instance_iam_role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )
        auto_scaling_group.add_security_group(sg)

        capacity_provider = ecs.AsgCapacityProvider(self, "EcsAsgCapacityProvider",
            auto_scaling_group=auto_scaling_group
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        ecs_namespace_first = sd.PrivateDnsNamespace(self, "FirstApp-Namespace",
            name="practice-1.local",
            vpc=vpc,
        )

        ecs_namespace_second = sd.PrivateDnsNamespace(self, "SecondApp-Namespace",
            name="practice-2.local",
            vpc=vpc,
        )
        
        first_app_task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDefFirstApp",
            network_mode=ecs.NetworkMode.AWS_VPC,
            task_role= task_role,
            execution_role=task_role,  
        )

        second_app_task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDefSecondApp",
            network_mode=ecs.NetworkMode.AWS_VPC,
            task_role= task_role,
            execution_role=task_role,
        )

        first_app_container = first_app_task_definition.add_container(
            "Nginx-app",
            image=ecs.ContainerImage.from_registry("Put here ecr image URI"),
            memory_limit_mib=500,
            cpu=256,
        )

        second_app_container = second_app_task_definition.add_container(
            "Nginx-app2",
            image=ecs.ContainerImage.from_registry("Put here ecr image URI"),
            memory_limit_mib=500,
            cpu=256,
        )

        port_mapping = ecs.PortMapping(
            container_port=80,
            # host_port=80,
            protocol=ecs.Protocol.TCP,
        )
        

        first_app_container.add_port_mappings(port_mapping)
        second_app_container.add_port_mappings(port_mapping)

        first_app_service = ecs.Ec2Service(
            self, "Service",
            cluster=cluster,
            task_definition=first_app_container,
            security_groups=[sg],
            cloud_map_options=ecs.CloudMapOptions(
                name= 'my-service',
                dns_record_type= sd.DnsRecordType.A,
                cloud_map_namespace= ecs_namespace_first,
                dns_ttl=cdk.Duration.minutes(1),
            )
        )

        second_app_service = ecs.Ec2Service(
            self, "Service2",
            cluster=cluster,
            task_definition=second_app_task_definition,
            security_groups=[sg],
            cloud_map_options=ecs.CloudMapOptions(
                name= 'my-service2', 
                dns_record_type= sd.DnsRecordType.A,
                cloud_map_namespace= ecs_namespace_second,
                dns_ttl=cdk.Duration.minutes(1),
            )
        )