import json
import time
import jwt
import os
import requests
import certifi
import grpc
import pub_sub.stubs.pubsub_api_pb2_grpc as pb2_grpc
import pub_sub.stubs.pubsub_api_pb2 as pb2
import avro.io
import io
import structlog
from datetime import datetime

from api import pem

logger = structlog.get_logger()

ISSUER = os.getenv("SALESFORCE_CONSUMER_KEY")
DOMAIN = os.getenv("SALESFORCE_DOMAIN")
SUBJECT = os.getenv("SALESFORCE_USERNAME")
CREATOR_CONTACT_ID = os.getenv("CREATOR_CONTACT_ID")
INSTANCE_URL = os.getenv("INSTANCE_URL")
TENANT_ID = os.getenv("TENANT_ID")
BATCH_SIZE = os.getenv("BATCH_SIZE", 400)

UPDATE_TOPIC = "/event/updated_contacts_batched__e"

def send_pipeline_update_messages(contacts_list):
    pem_file = pem.find_pem_file()  #TODO: Could we get here (and get errors) if we didn't have a pem file?
    with open(pem_file) as fd:
        private_key = fd.read()
    logger.info('Loaded PEM certificate')

    claim = {
        'iss': ISSUER,
        'exp': int(time.time()) + 300,
        'aud': 'https://{}.salesforce.com'.format(DOMAIN),
        'sub': SUBJECT,
    }
    assertion = jwt.encode(claim, private_key, algorithm='RS256', headers={'alg': 'RS256'})
    logger.info('Generated JWT')

    r = requests.post('https://{}.salesforce.com/services/oauth2/token'.format(DOMAIN), data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': assertion,
    })
    access_token = r.json()['access_token']
    logger.info('Made OAuth call to get access token')

    with open(certifi.where(), 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    with grpc.secure_channel('api.pubsub.salesforce.com:7443', creds) as channel:
        auth_meta_data = (('accesstoken', access_token),
                          ('instanceurl', INSTANCE_URL),
                          ('tenantid', TENANT_ID))


        stub = pb2_grpc.PubSubStub(channel)
        schema_id = stub.GetTopic(pb2.TopicRequest(topic_name=UPDATE_TOPIC), metadata=auth_meta_data).schema_id
        schema = stub.GetSchema(pb2.SchemaRequest(schema_id=schema_id), metadata=auth_meta_data).schema_json


        batches = 0
        while len(contacts_list) > 0:
            if len(contacts_list) > BATCH_SIZE:
                current_batch = contacts_list[:BATCH_SIZE]
                del contacts_list[:BATCH_SIZE]
            else:
                current_batch = contacts_list
                contacts_list = []

            root_object = {
                "updatedContactsJson" : current_batch
            }
            message = {
                "CreatedById": CREATOR_CONTACT_ID,
                "CreatedDate": int(datetime.now().timestamp()),
                "updated_contacts_json__c": json.dumps(root_object)
            }
            buf = io.BytesIO()
            encoder = avro.io.BinaryEncoder(buf)
            writer = avro.io.DatumWriter(avro.schema.parse(schema))
            writer.write(message, encoder)
            payload = {
                "schema_id": schema_id,
                "payload": buf.getvalue()
            }

            stub.Publish(pb2.PublishRequest(topic_name=UPDATE_TOPIC, events=[payload]), metadata=auth_meta_data)
            logger.info('Sent %s contacts in message', len(current_batch))
            batches = batches + 1


    logger.info('completed sending platform messages, %s messages sent', batches)

