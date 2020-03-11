"""
1. Find all files not modified in last 2 days.
2. For each file push to S3 and delete file.

The time limit will be configurable
S3 bucket will be configurable
"""

import os

from datetime import datetime

import file_finder
import settings
import s3_uploader
import logger

logger = logger.get_logger()

def find_all_files(current_datetime):
    # get directories from settigs
    # get days cutoff from settings
    found_files_info=[]
    cutoff_days=settings.CONST_NUM_DAYS_CUTOFF
    for dir_path, dir_s3_key in settings.CONST_DIRECTORIES_TO_WATCH:
        for file_info in file_finder.find_files_in_dir(dir_path, cutoff_days, current_datetime):
            found_files_info.append((file_info, dir_s3_key))
    return found_files_info

def upload_to_s3(s3_uploader_obj, file_info, dir_s3_key, current_datetime):
    try:
        #eg. QA/tomcat/20-2-2020/logmanager.txt
        file_s3_upload_key=f"{settings.S3_BUCKET_UPLOAD_DIR_ROOT}/{dir_s3_key}/{current_datetime.date()}/{file_info.name}"
        if s3_uploader_obj.upload_file(
            file_info.path, settings.S3_BUCKET_NAME, file_s3_upload_key):
            logger.info(f"[upload_to_s3]:[Uploaded][{file_info.path}][{settings.S3_BUCKET_NAME}][{file_s3_upload_key}]")
            return True
        else:
            logger.info(f"[upload_to_s3]:[Upload failed][{file_info.path}][{settings.S3_BUCKET_NAME}][{file_s3_upload_key}]")
    except Exception as e:
        logger.exception(e)
    return False

def delete_file(file_info):
    #delete file here
    deleted=False
    try:
        os.remove(file_info.path)
        logger.info(f"[delete_file]:[Deleted][{file_info.path}]")
    except OSError as e:
        logger.exception(e)

if __name__=="__main__":
    current_datetime=datetime.now()

    logger.info(f"[started]")

    found_files_info=find_all_files(current_datetime)
    logger.debug(f"[found files][{found_files_info}]")

    if settings.CONST_UPLOAD_TO_s3:
        s3_uploader_obj = s3_uploader.S3Uploader(
            settings.AWS_CONFIG['aws_access_key_id'],
            settings.AWS_CONFIG['aws_secret_access_key'],
            None
            )

    try:
        for file_info, dir_s3_key in found_files_info:
            can_delete=True
            if settings.CONST_UPLOAD_TO_s3:
                can_delete=upload_to_s3(s3_uploader_obj, file_info, dir_s3_key, current_datetime)
            if settings.CONST_DELETE_FILES:
                if can_delete: delete_file(file_info)
    except Exception as e:
        logger.exception(e)

    logger.info(f"[ended]")
