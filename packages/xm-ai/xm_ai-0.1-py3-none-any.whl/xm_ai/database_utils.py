from botocore.exceptions import ClientError, EndpointConnectionError
from pymongo import MongoClient
import base64
import boto3
import json


def access_database(secret_key):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-2"
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_key
        )
        if 'SecretString' in get_secret_value_response:
            aws = json.loads(get_secret_value_response['SecretString'])
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
    except ClientError as e:
        raise e

    if secret_key == "xmentium_mongo":
        client = MongoClient(
            f"mongodb://{aws['username']}:{aws['password']}@{aws['address']}:{aws['port']}/{aws['database']}")
        return client
    elif secret_key == "ai_mongo":
        auth_source = "ai.kra4x.mongodb.net/test?authSource=admin&replicaSet=atlas-l3om2j-shard-0&readPreference=primary&ssl=true"
        conn_string = f"mongodb+srv://{aws['username']}:{aws['password']}@{auth_source}"
        client = MongoClient(conn_string)
        return client


try:
    db = access_database("xmentium_mongo")["ft-01"]
    ai_db = access_database("ai_mongo")
    staging_db = access_database("xmentium_mongo")["staging"]
# this enables me to use features of eTimeInput while offline
except EndpointConnectionError as error:
    print(error)
    print("You are offline.")