import os
import unittest
from unittest import mock

import boto3
from moto import mock_sqs
from moto.server import ThreadedMotoServer

from app.lambda_sqs import sqs_producer

URL = "http://127.0.0.1:5000"
QUEUE_NAME = "test_queue"


class TestSqsProducer(unittest.TestCase):

    def setUp(self):
        self.event = {
            "body": {
                "firstname": "John",
                "lastname": "Doe"
            },
            "headers": {
                "Content-Type": "application/json"
            }
        }
        self.server = ThreadedMotoServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    @mock_sqs
    @mock.patch.dict(os.environ, {"SQS_QUEUE_URL": f"{URL}/{QUEUE_NAME}"})
    def test_sqs_producer(self):
        server_client = boto3.client("sqs", endpoint_url=URL)
        server_client.create_queue(QueueName=QUEUE_NAME)

        response = sqs_producer.send_sqs_message(self.event)

        self.assertEqual(200, response['ResponseMetadata']['HTTPStatusCode'])
