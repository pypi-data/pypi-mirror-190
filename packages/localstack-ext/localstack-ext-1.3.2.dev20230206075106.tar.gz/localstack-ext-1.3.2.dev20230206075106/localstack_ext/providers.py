_A='lambda'
import functools
from localstack.aws.forwarder import HttpFallbackDispatcher
from localstack.aws.proxy import AwsApiListener
from localstack.config import is_env_true
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.services.moto import MotoFallbackDispatcher
from localstack.services.plugins import Service,aws_provider
pro_aws_provider=functools.partial(aws_provider,name='pro',should_load=lambda:is_env_true(ENV_PRO_ACTIVATED))
@pro_aws_provider()
def acm():from localstack.services.acm.provider import AcmProvider as A;from localstack.services.moto import MotoFallbackDispatcher as B;C=A();return Service.for_provider(C,dispatch_table_factory=B)
@pro_aws_provider()
def amplify():from localstack_ext.services.amplify.provider import AmplifyProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def apigatewaymanagementapi():from localstack_ext.services.apigateway.provider_mgmtapi import ApigatewaymanagementapiProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def apigatewayv2():from localstack_ext.services.apigateway.provider_v2 import ApiGatewayV2Provider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def appconfig():from localstack_ext.services.appconfig.provider import AppconfigProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider(api='application-autoscaling')
def application_autoscaling():from localstack_ext.services.applicationautoscaling.provider import ApplicationAutoscalingProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def appsync():from localstack_ext.services.appsync.provider import AppSyncProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def athena():from localstack_ext.services.athena.provider import AthenaProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def autoscaling():from localstack_ext.services.autoscaling.provider import AutoscalingProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(should_load=lambda:is_env_true(ENV_PRO_ACTIVATED)and is_env_true('AZURE'))
def azure():from localstack_ext.services.azure import azure_starter as A;return Service('azure',start=A.start_azure)
@pro_aws_provider()
def backup():from localstack_ext.services.backup.provider import BackupProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def batch():from localstack_ext.services.batch.provider import BatchProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def ce():from localstack_ext.services.costexplorer.provider import CeProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def cloudfront():from localstack_ext.services.cloudfront.provider import CloudFrontProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def cloudtrail():from localstack_ext.services.cloudtrail.provider import CloudtrailProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def codecommit():from localstack_ext.services.codecommit.provider import CodecommitProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='cognito-identity')
def cognito_identity():from localstack_ext.services.cognito_identity.provider import CognitoIdentityProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='cognito-idp')
def cognito_idp():from localstack_ext.services.cognito_idp.provider import CognitoIdpProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def docdb():from localstack_ext.services.docdb import docdb_api as A;return Service('docdb',start=A.start_docdb)
@pro_aws_provider()
def ec2():from localstack_ext.services.ec2.provider import Ec2Provider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def ecr():from localstack_ext.services.ecr.provider import EcrProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def ecs():from localstack_ext.services.ecs.provider import ECSProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def efs():from localstack_ext.services.efs.provider import EfsProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def elasticache():from localstack_ext.services.elasticache.provider import ElasticacheProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def elasticbeanstalk():from localstack_ext.services.elasticbeanstalk.provider import ElasticBeanstalkProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def elb():from localstack_ext.services.elb.provider import ElbProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def elbv2():from localstack_ext.services.elbv2.provider import Elbv2Provider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def eks():from localstack_ext.services.eks.provider import EksProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def emr():from localstack_ext.services.emr.provider import EmrProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def fis():from localstack_ext.services.fis.provider import FisProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def glacier():from localstack_ext.services.glacier.provider import GlacierProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def glue():from localstack_ext.services.glue.provider import GlueProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def iot():from localstack_ext.services.iot.provider import IotProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='iot-data')
def iot_data():from localstack_ext.services.iot_data.provider import IotDataProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def iotanalytics():from localstack_ext.services.iotanalytics.provider import IotAnalyticsProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def iotwireless():from localstack_ext.services.iotwireless.provider import IotWirelessProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def kafka():from localstack_ext.services.kafka.provider import KafkaProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def kinesisanalytics():from localstack_ext.services.kinesisanalytics.provider import KinesisAnalyticsProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def kinesisanalyticsv2():from localstack_ext.services.kinesisanalyticsv2.provider import KinesisAnalyticsV2Provider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def kinesis():B='kinesis';from localstack.services.kinesis.provider import KinesisProvider as C;A=C();D=AwsApiListener(B,HttpFallbackDispatcher(A,A.get_forward_url));return Service(B,listener=D,lifecycle_hook=A)
@pro_aws_provider()
def lakeformation():from localstack_ext.services.lakeformation.provider import LakeFormationProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def logs():from localstack_ext.services.logs.provider import LogsProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def mediastore():from localstack_ext.services.mediastore.provider import MediastoreProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider(api='mediastore-data')
def mediastore_data():from localstack_ext.services.mediastore.provider import MediaStoreDataProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def mwaa():from localstack_ext.services.mwaa.provider import MwaaProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def neptune():from localstack_ext.services.neptune import neptune_api as A;return Service('neptune',start=A.start_neptune)
@pro_aws_provider()
def organizations():from localstack_ext.services.organizations.provider import OrganizationsProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def qldb():from localstack_ext.services.qldb.provider import QldbProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider(api='qldb-session')
def qldb_session():from localstack_ext.services.qldb.provider import QldbSessionProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def rds():from localstack_ext.services.rds.provider import RdsProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='rds-data')
def rds_data():from localstack_ext.services.rds_data.provider import RdsDataProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def redshift():from localstack_ext.services.redshift.provider import RedshiftProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='redshift-data')
def redshift_data():from localstack_ext.services.redshift.provider import RedshiftDataProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def sagemaker():from localstack_ext.services.sagemaker.provider import SagemakerProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='sagemaker-runtime')
def sagemaker_runtime():from localstack_ext.services.sagemaker.provider import SageMakerRuntimeProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def serverlessrepo():from localstack_ext.services.serverlessrepo.provider import ServerlessrepoProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def servicediscovery():from localstack_ext.services.servicediscovery.provider import ServicediscoveryProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def ssm():from localstack_ext.services.ssm.provider import SsmProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='timestream-write')
def timestream_write():from localstack_ext.services.timestream.provider import TimestreamWriteProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider(api='timestream-query')
def timestream_query():from localstack_ext.services.timestream.provider import TimestreamQueryProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def transfer():from localstack_ext.services.transfer.provider import TransferProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def xray():from localstack_ext.services.xray.provider import XrayProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def apigateway():from localstack_ext.services.apigateway.apigateway_extended import ApigatewayExtProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api=_A)
def awslambda():from localstack.services.awslambda import lambda_starter as A;from localstack_ext.services.awslambda.lambda_extended import patch_lambda as B;B();return Service(_A,start=A.start_lambda,stop=A.stop_lambda,check=A.check_lambda)
@pro_aws_provider(api='cloudwatch')
def cloudwatch():from localstack_ext.services.cloudwatch.provider import CloudwatchProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def cloudformation():from localstack.services.cloudformation.provider import CloudformationProvider as A;from localstack_ext.services.cloudformation import cloudformation_extended as B;B.patch_cloudformation();C=A();return Service.for_provider(C)
@pro_aws_provider()
def dynamodb():from localstack_ext.services.dynamodb.provider import DynamoDBProviderExt as A;B=A();return Service.for_provider(B,dispatch_table_factory=lambda _provider:HttpFallbackDispatcher(_provider,_provider.get_forward_url))
@pro_aws_provider()
def dynamodbstreams():from localstack_ext.services.dynamodbstreams.provider import DynamoDBStreamsExtProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def events():from localstack_ext.services.events.provider import EventsProviderPro as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def mq():from localstack_ext.services.mq.provider import MQProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def iam():from localstack_ext.services.iam.provider import IamProviderExt as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def kms():from localstack.services.providers import kms as A;from localstack_ext.services.kms import kms_extended as B;B.patch_kms();return A.factory.__wrapped__()
@pro_aws_provider()
def opensearch():from localstack_ext.services.opensearch.provider import OpensearchProvider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def route53():from localstack_ext.services.route53.provider import Route53ProviderPro as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider(api='s3',name='asf_pro')
def s3_asf():from localstack_ext.services.s3.provider import S3ProviderPro as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def s3():from localstack.services.s3 import s3_listener as B,s3_starter as A;from localstack_ext.services.s3 import s3_extended as C;C.patch_s3();return Service('s3',listener=B.UPDATE_S3,start=A.start_s3,check=A.check_s3)
@pro_aws_provider()
def secretsmanager():from localstack_ext.services.secretsmanager.secretsmanager_extended import SecretsmanagerProviderExt as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def ses():from localstack_ext.services.ses.provider import SesProvider as A;B=A();return Service.for_provider(B,dispatch_table_factory=MotoFallbackDispatcher)
@pro_aws_provider()
def sesv2():from localstack_ext.services.sesv2.provider import Sesv2Provider as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def sns():from localstack_ext.services.sns.provider import SnsProviderExt as A;B=A();return Service.for_provider(B)
@pro_aws_provider()
def sqs():from localstack.services import edge;from localstack.services.sqs import query_api as A;from localstack_ext.services.sqs.provider import SqsProvider as B;A.register(edge.ROUTER);C=B();return Service.for_provider(C)
@pro_aws_provider()
def stepfunctions():from localstack.services.stepfunctions.provider import StepFunctionsProvider as A;from localstack_ext.services.stepfunctions.provider import patch_stepfunctions as B;B();C=A();return Service.for_provider(C,dispatch_table_factory=lambda _provider:HttpFallbackDispatcher(_provider,_provider.get_forward_url))
@pro_aws_provider()
def sts():from localstack.services.providers import sts as A;from localstack_ext.services.sts import sts_extended as B;B.patch_sts();return A.factory.__wrapped__()
@pro_aws_provider(name='mock',api='eks')
def eks_mock():from localstack_ext.services.eks.provider import EksMockProvider as A;B=A();return Service.for_provider(B)