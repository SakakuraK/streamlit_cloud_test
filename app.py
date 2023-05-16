import streamlit as st
import boto3

import pandas as pd

import sqlite3

# TODO implement
s3 = boto3.client('s3')

S3_BUCKET = "streamer-review"
SQLITE_FILE = "streamer_db.sqlite"


s3.download_file(S3_BUCKET, SQLITE_FILE, SQLITE_FILE)

#データベースに接続
filepath = SQLITE_FILE
conn = sqlite3.connect(filepath)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


st.title("Stream lit IN cloud")

st.text("streamlit cloud動作テスト\ngithubにpy置いてそれをstreamlit cloudから呼び出す")
st.text("S3読み込みからDB接続→検索フォームテスト中")


# 検索可能なデータセット一覧取得
collection_list = []
# データベースから取得
cur.execute("""SELECT streamer_name, streamer_comment_data_youtube, streamer_comment_data_dataset_5ch FROM streamer_datasets""")
datasets_list = cur.fetchall()


for dataset in datasets_list:
    # youtube,5chどちらかのデータセットがあれば選択肢表示
    if dataset['streamer_comment_data_youtube'] is not None or dataset['streamer_comment_data_dataset_5ch'] is not None:
        collection_list.append(dataset['streamer_name'])


# プルダウンリストと検索ボックスを表示する
selected_collection = st.selectbox("検索したい配信者を選択してください", collection_list)
search_word = st.text_input("検索するワードを入力してください。")