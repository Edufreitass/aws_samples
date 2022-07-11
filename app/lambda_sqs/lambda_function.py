import json

from aws_lambda_powertools import Logger

from app.lambda_sqs.sqs_producer import send_sqs_message

logger = Logger()


def lambda_handler(event, context):
    try:
        logger.info(f"## Receiving event: {event}")
        sqs_response = send_sqs_message(event)
        if sqs_response is not None:
            logger.info(f'Sent SQS message ID: {sqs_response["MessageId"]}')
        response = {
            'statusCode': sqs_response["ResponseMetadata"]["HTTPStatusCode"],
            'body': json.dumps(sqs_response["ResponseMetadata"])
        }
        logger.info(response)
        return response
    except Exception as error:
        logger.error(f"Lambda processing error: {error} ")
