from flask import request, render_template, jsonify, current_app as app
from .. import db
from google_auth import CheckLogin
from botocore.client import Config
import os, boto3

@app.route('/files/')
@CheckLogin()
def files_test():
    return render_template('files.html')

@app.route('/sign_s3/post')
@CheckLogin()
def sign_s3_post():
  S3_BUCKET = os.environ.get('S3_BUCKET')
  S3_REGION = os.environ.get('S3_REGION')

  file_name = request.args.get('file_name')
  file_type = request.args.get('file_type')

  s3 = boto3.client('s3', config = Config(region_name=S3_REGION, signature_version='s3v4'))

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return jsonify({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })
