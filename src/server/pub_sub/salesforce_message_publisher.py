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

logger = structlog.get_logger()

ISSUER = os.getenv("SALESFORCE_CONSUMER_KEY")
DOMAIN = os.getenv("SALESFORCE_DOMAIN")
SUBJECT = os.getenv("SALESFORCE_USERNAME")
INSTANCE_URL = os.getenv("INSTANCE_URL")
TENANT_ID = os.getenv("TENANT_ID")
PLATFORM_MESSAGE_AUTHOR = os.getenv("PLATFORM_MESSAGE_AUTHOR_RECORD_ID")

UPDATE_TOPIC = "/event/Updated_Contacts_From_Pipeline__e"


def send_pipeline_update_messages(contacts_list):
    pem_file = 'bin/connected-app-secrets.pem'
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

        for contact_dict in contacts_list:
            contact_dict['CreatedDate'] = int(datetime.now().timestamp())
            contact_dict['CreatedById'] = PLATFORM_MESSAGE_AUTHOR

            buf = io.BytesIO()
            encoder = avro.io.BinaryEncoder(buf)
            writer = avro.io.DatumWriter(avro.schema.parse(schema))
            writer.write(contact_dict, encoder)
            payload = {
                "schema_id": schema_id,
                "payload": buf.getvalue()
            }
            stub.Publish(pb2.PublishRequest(topic_name=UPDATE_TOPIC, events=[payload]), metadata=auth_meta_data)
            logger.info('Pipeline update message sent')

    logger.info("%s total pipeline update messages sent", len(contacts_list))