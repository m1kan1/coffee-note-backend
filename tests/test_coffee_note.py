import os
import requests

def test_coffee_note():
    # 環境変数からクライアントIDを取得する
    client_id = os.environ['AUTH0_CLIENT_ID']

    # 環境変数からクライアントシークレットを取得する
    client_secret = os.environ['AUTH0_CLIENT_SECRET']

    # 環境変数からトークン取得URLを取得する
    token_request_url = os.environ['AUTH0_TOKEN_REQUEST_URL']

    # 環境変数からオーディエンスを取得する
    audience = os.environ['AUTH0_AUDIENCE']

    # リクエストボディを作成する
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience,
        'grant_type': 'client_credentials'
    }

    # トークンを取得する
    response = requests.post(token_request_url, json=payload)

    # トークンを取得できなかった場合は、テストを失敗させる
    if response.status_code != 200:
        assert False

    # トークンを取得する
    token = response.json()['access_token']

    # TOKENを使用してAPIを呼び出す
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(os.environ['ENDPOINT_URL'], headers=headers)

    # 結果をアサーションする
    assert response.text == '[]'

