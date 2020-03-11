from dotenv import load_dotenv
load_dotenv()

import os

# List of directories to look for files
# The option is folder name in S3 (This will be prefixed by S3_BUCKET_UPLOAD_DIR_ROOT)
# and suffixed by Date
CONST_DIRECTORIES_TO_WATCH=[
    ('/opt/tomcat/logs', 'tomcat'),
    ]

#Files older than this (in days) will be shipped and deleted
CONST_NUM_DAYS_CUTOFF=2

#delete files ?
CONST_DELETE_FILES=False

#upload to s3 ?
CONST_UPLOAD_TO_s3=False

#AWS credentials
AWS_CONFIG={
    'aws_access_key_id':os.getenv('aws_access_key_id'),
    'aws_secret_access_key':os.getenv('aws_secret_access_key'),
    'aws_session_token':None,
}

#s3 bucket to upload to
S3_BUCKET_NAME=os.getenv('s3_bucket_name')

# The files will be uploaded to /(S3_BUCKET_UPLOAD_DIR_ROOT)/(DIR_PREFIX)/(DATE) in S3
S3_BUCKET_UPLOAD_DIR_ROOT="DEV"


_LOG_LEVEL_CRITICAL = 50
_LOG_LEVEL_ERROR = 40
_LOG_LEVEL_WARNING = 30
_LOG_LEVEL_INFO = 20
_LOG_LEVEL_DEBUG = 10

#set one of the log level from above
LOG_LEVEL=_LOG_LEVEL_DEBUG

#Set this to None, if log to file is not required
SELF_LOG_FILE_PATH='/var/log/log_ship.log'
SELF_LOG_TO_CONSOLE=True
