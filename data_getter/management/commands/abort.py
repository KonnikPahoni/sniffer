import boto3
import os
from django.core.management.base import BaseCommand
import logging
from settings import BUCKET_NAME, SPACES_ENDPOINT_URL, REGION_NAME


class Command(BaseCommand):
    help = 'Cancel all pending uploads'

    def handle(self, *args, **kwargs):
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=REGION_NAME,
                                endpoint_url=SPACES_ENDPOINT_URL,
                                aws_access_key_id=os.getenv('SPACES_KEY'),
                                aws_secret_access_key=os.getenv('SPACES_SECRET'))

        response = client.list_multipart_uploads(Bucket=BUCKET_NAME)

        if 'Uploads' not in response:
            self.stdout.write('No uploads to abort', ending='\n')
            return

        for upload in response['Uploads']:
            abort_response = client.abort_multipart_upload(
                Bucket=BUCKET_NAME,
                Key=upload['Key'],
                UploadId=upload['UploadId'],
                RequestPayer='requester',
                ExpectedBucketOwner='string'
            )

            if abort_response['ResponseMetadata']['HTTPStatusCode'] == 204:
                logging.info('Request ' + abort_response['ResponseMetadata']['RequestId'] + ' aborted')
