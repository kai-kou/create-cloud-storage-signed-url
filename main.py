import time

import urllib

from datetime import datetime, timedelta

import os

import base64

from oauth2client.service_account import ServiceAccountCredentials

API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'


def sign_url(bucket, bucket_object, method, expires_after_seconds=60):
    gcs_filename = '/%s/%s' % (bucket, bucket_object)
    content_md5, content_type = None, None

    credentials = ServiceAccountCredentials.from_json_keyfile_name('[サービスアカウントキーのファイルパス]')
    google_access_id = credentials.service_account_email

    expiration = datetime.now() + timedelta(seconds=expires_after_seconds)
    expiration = int(time.mktime(expiration.timetuple()))

    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        gcs_filename])
    _, signature_bytes = credentials.sign_blob(signature_string)
    signature = base64.b64encode(signature_bytes)

    query_params = {'GoogleAccessId': google_access_id,
                    'Expires': str(expiration),
                    'Signature': signature}

    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=API_ACCESS_ENDPOINT,
        resource=gcs_filename,
        querystring=urllib.parse.urlencode(query_params))


if __name__ == '__main__':
    url = sign_url('[バケット名]', '[オブジェクト名(ファイル名)]', 'GET')
    print(url)
