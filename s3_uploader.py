import boto3
from botocore.exceptions import ClientError

class S3Uploader(object):
    """
    Wraps aws boto's client instantiation and file upload methods

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration

    Note: Do not share this an instance of S3Uploader across threads. Each thread shall have it's own copy
    """

    def __init__(self, aws_access_key_id:str, aws_secret_access_key:str, aws_session_token:str=None, logger=None):
        self._aws_access_key_id=aws_access_key_id
        self._aws_secret_access_key=aws_secret_access_key
        self._aws_session_token=aws_session_token
        self._logger=logger
        if self._aws_access_key_id and self._aws_secret_access_key:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key
                )
        else:
            raise Exception("Invalid AWS configuration")

    def upload_file(self, file_name:str, bucket:str, object_name:str=None)->bool:
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        try:
            response = self._s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            if self._logger: self._logger.exception(e)
            return False
        return True