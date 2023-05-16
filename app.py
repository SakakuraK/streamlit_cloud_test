import streamlit as st
import boto3

import pandas as pd

import sqlite3

# TODO implement
s3 = boto3.client('s3',
    region_name='us-east-1',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id='AKIAXIRPBBKHFJW5NCGI',
    aws_secret_access_key='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'
)

S3_BUCKET = "streamer-review"
SQLITE_FILE = "streamer_db.sqlite"


response = s3.list_objects_v2(
    Bucket=S3_BUCKET,
    Prefix=SQLITE_FILE,
)

#s3.download_file(S3_BUCKET, SQLITE_FILE, SQLITE_FILE)

 #データベースに接続
#filepath = SQLITE_FILE
#conn = sqlite3.connect(filepath)
#conn.row_factory = sqlite3.Row
#cur = conn.cursor()


st.title("Stream lit IN cloud")

st.text("streamlit cloud動作テスト\ngithubにpy置いてそれをstreamlit cloudから呼び出す")
st.text("S3読み込みからDB接続までテスト中")
