import boto3
import s3fs
import sqlalchemy

"""
Connections to different services

boto: Boto3 resource for s3/minio - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#using-boto3
fs: s3fs File System for s3/minio - https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem
"""


fs: s3fs.S3FileSystem = None
boto = None
db_engine = None


def connect_s3(endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str):
    global fs, boto

    s3fs_config = {
        "anon": False,
        "key": aws_access_key_id,
        "secret": aws_secret_access_key,
        "config_kwargs": {
            'signature_version': 's3v4'
        }
    }

    boto3_config = {
        "service_name": "s3",
        "endpoint_url": endpoint_url,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_session_token": None,
        "verify": True
    }

    print("s3fs_config:", s3fs_config)
    print("boto3_config:", boto3_config)

    fs = s3fs.S3FileSystem(**s3fs_config)
    boto = boto3.resource(**boto3_config)

    return fs, boto


def connect_db(connection_string: str):
    global db_engine

    db_engine = sqlalchemy.create_engine(connection_string)

    return db_engine


def get_connection() -> sqlalchemy.engine.Connection:
    global db_engine

    if isinstance(db_engine, sqlalchemy.engine.Connection):
        return db_engine
    else:
        raise Exception("No database connection defined, use connect_db() first")
