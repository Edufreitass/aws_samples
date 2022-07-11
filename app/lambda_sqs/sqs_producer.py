import json
import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()


def send_sqs_message(event):
    try:
        msg = json.dumps(event)
        sqs_client = boto3.client('sqs')
        sqs_queue_url = os.getenv("SQS_QUEUE_URL")

        logger.info(f"Sending message to queue")
        response = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                           MessageBody=msg)
    except ClientError as e:
        logger.error(e)
        return None
    logger.info(f"Message has been sent with success")
    return response
