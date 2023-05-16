import streamlit as st
import boto3
import requests
import json

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
selected_streamer_name = st.selectbox("検索したい配信者を選択してください", collection_list)
search_word = st.text_input("検索するワードを入力してください。")

# 検索ボタン押した時
if st.button("検索"):
    if search_word and len(datasets_list) > 0:
        st.write("選択配信者＞",selected_streamer_name)
        st.write("検索ワード＞",search_word)
        
        myobj = {"streamer_name": selected_streamer_name, "search_word": search_word}
        # リクエストヘッダー
        headers = {'Content-Type': 'application/json'}
        
        # ベクトル検索用API
        url = 'https://elo69unmp7.execute-api.us-east-1.amazonaws.com/test/posttest'
        
        vector_search_res = requests.post(url, data = json.dumps(myobj), headers=headers)
        vector_search_res_json = json.loads(vector_search_res.text)
        
        comment_youtube_search_result = json.loads(vector_search_res_json["comment_youtube"])
        comment_5ch_search_result = json.loads(vector_search_res_json["comment_5ch"])
        comment_5ch_thread_title = json.loads(vector_search_res_json["comment_5ch_thread"])
        
        if comment_youtube_search_result is not "":
            st.write("youtubeコメントからの検索")
            st.dataframe( comment_youtube_search_result )
        
        if comment_5ch_search_result is not "":
            st.write("5ch書き込みからの検索")
            st.dataframe( comment_5ch_search_result )
            st.write("引用元：",comment_5ch_thread_title)
        
        
        
        #st.text(vector_search_res.text)