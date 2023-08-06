import logging
import time
from typing import Dict
from typing import List

import boto3
import botocore.exceptions
import neo4j

from cartography.client.core.tx import load_graph_data
from cartography.graph.job import GraphJob
from cartography.graph.querybuilder import build_ingestion_query
from cartography.intel.aws.ec2.util import get_botocore_config
from cartography.models.aws.emr import EMRClusterSchema
from cartography.util import aws_handle_regions
from cartography.util import timeit

logger = logging.getLogger(__name__)

# EMR API is subject to aggressive throttling, so we need to sleep a second between each call.
LIST_SLEEP = 1
DESCRIBE_SLEEP = 1


@timeit
@aws_handle_regions
def get_emr_clusters(boto3_session: boto3.session.Session, region: str) -> List[Dict]:
    client = boto3_session.client('emr', region_name=region, config=get_botocore_config())
    clusters: List[Dict] = []
    paginator = client.get_paginator('list_clusters')
    for page in paginator.paginate():
        cluster = page['Clusters']
        clusters.extend(cluster)
        time.sleep(LIST_SLEEP)
    return clusters


@timeit
def get_emr_describe_cluster(boto3_session: boto3.session.Session, region: str, cluster_id: str) -> Dict:
    client = boto3_session.client('emr', region_name=region, config=get_botocore_config())
    cluster_details: Dict = {}
    try:
        response = client.describe_cluster(ClusterId=cluster_id)
        cluster_details = response['Cluster']
    except botocore.exceptions.ClientError as e:
        logger.warning(
            "Could not run EMR describe_cluster due to boto3 error %s: %s. Skipping.",
            e.response['Error']['Code'],
            e.response['Error']['Message'],
        )
    return cluster_details


@timeit
def load_emr_clusters(
        neo4j_session: neo4j.Session,
        cluster_data: List[Dict],
        region: str,
        current_aws_account_id: str,
        aws_update_tag: int,
) -> None:
    logger.info("Loading EMR %d clusters for region '%s' into graph.", len(cluster_data), region)

    ingestion_query = build_ingestion_query(EMRClusterSchema())

    load_graph_data(
        neo4j_session,
        ingestion_query,
        cluster_data,
        lastupdated=aws_update_tag,
        Region=region,
        AWS_ID=current_aws_account_id,
    )


@timeit
def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict) -> None:
    logger.debug("Running EMR cleanup job.")
    cleanup_job = GraphJob.from_node_schema(EMRClusterSchema(), common_job_parameters)
    cleanup_job.run(neo4j_session)


@timeit
def sync(
    neo4j_session: neo4j.Session, boto3_session: boto3.session.Session, regions: List[str], current_aws_account_id: str,
    update_tag: int, common_job_parameters: Dict,
) -> None:
    for region in regions:
        logger.info("Syncing EMR for region '%s' in account '%s'.", region, current_aws_account_id)

        clusters = get_emr_clusters(boto3_session, region)

        cluster_data: List[Dict] = []
        for cluster in clusters:
            cluster_id = cluster['Id']
            cluster_details = get_emr_describe_cluster(boto3_session, region, cluster_id)
            if cluster_details:
                cluster_data.append(cluster_details)
            time.sleep(DESCRIBE_SLEEP)

        load_emr_clusters(neo4j_session, cluster_data, region, current_aws_account_id, update_tag)

    cleanup(neo4j_session, common_job_parameters)
