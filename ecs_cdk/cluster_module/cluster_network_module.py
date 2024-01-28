from constructs import Construct
import aws_cdk.aws_ec2 as ec2

class ClusterNetwork(Construct):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # availability_zones = ['ap-south-1a', 'ap-south-1b','ap-south-1c']

        self.vpc = ec2.Vpc(
            self, "EcsClusterVpc",
            max_azs=None,  #len(availability_zones),
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                {
                    'cidrMask': 24,
                    'name': 'Public',
                    'subnetType': ec2.SubnetType.PUBLIC,
                },
                {
                    'cidrMask': 24,
                    'name': 'Private',
                    'subnetType': ec2.SubnetType.PRIVATE_WITH_EGRESS,
                }
            ],
        )
