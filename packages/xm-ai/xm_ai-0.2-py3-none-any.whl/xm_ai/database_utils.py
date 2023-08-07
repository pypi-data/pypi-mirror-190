from botocore.exceptions import ClientError, EndpointConnectionError
from pymongo import MongoClient
import base64
import boto3
import json
from enum import Enum


class xMentiumMongoSecret(Enum):
    username = 'username'
    password = 'password'
    address = 'address'
    port = 'port'
    database = 'database'
    production_name: str = 'production'


def get_secret(keyname: str) -> dict or bytes:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-2"
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=keyname
        )
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
    except ClientError as e:
        raise e


try:
    # connstring for production/staging
    secret = get_secret("xmentium_mongo")
    remote_db_connstring = f"mongodb:" \
                           f"//{secret[xMentiumMongoSecret.username.value]}" \
                           f":{secret[xMentiumMongoSecret.password.value]}" \
                           f"@{secret[xMentiumMongoSecret.address.value]}" \
                           f":{secret[xMentiumMongoSecret.port.value]}" \
                           f"/{secret[xMentiumMongoSecret.database.value]}"

    # noinspection PyTypeChecker
    db = MongoClient(remote_db_connstring)[secret[xMentiumMongoSecret.production_name.value]]
    staging_db = MongoClient(remote_db_connstring)["staging"]

    # connstring for ai database
    secret = get_secret("ai_mongo")
    ai_db_connstring = f"mongodb+srv:" \
                       f"//{secret[xMentiumMongoSecret.username.value]}" \
                       f":{secret[xMentiumMongoSecret.password.value]}" \
                       f"@{secret[xMentiumMongoSecret.address.value]}" \
                       f"/{secret[xMentiumMongoSecret.database.value]}"
    ai_db = MongoClient(ai_db_connstring)

except EndpointConnectionError as error:
    print(error)
    print("You are offline, so Boto3 could not create a session")
