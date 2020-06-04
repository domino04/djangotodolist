from .models import List, Comment
from todolist.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
import boto3
from boto3.session import Session 
from datetime import datetime 
from django.contrib.auth.models import User 

def upload_and_save(request, file_to_upload, new_list):

    session = Session(
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        region_name = AWS_S3_REGION_NAME
    )
    s3 = session.resource('s3')

    now = datetime.now().strftime("%Y%H%M%S")


    img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        Key = str(new_list.pk) + '/' + new_list.title,
        Body = file_to_upload
    )

    s3_url = "https://to-do-list-danbi.s3.ap-northeast-2.amazonaws.com/" + now + user_pk + "Sorry"
    picture = Picture.objects.create(
        list = new_list,
        author = new_list.author,
        content = s3_url + str(new_list.pk) + '/' + new_list.title
    )