# Coffee Note Backend

このプロジェクトは、Coffee Note アプリのバックエンドを構築するためのものです。  
フロントエンドは[こちら](https://github.com/m1kan1/coffee-note-web)

## 構成

このプロジェクトでは、以下のリソースが構築されます。

- AWS Lambda 関数
  - `auth`: 認証を行う関数
  - `coffeeNote`: Coffee Note の CRUD 処理を行う関数
- Amazon DynamoDB テーブル
  - `coffee_note`: Coffee Note のデータを保存するテーブル

## 使い方

このプロジェクトをデプロイするには、以下の手順を実行します。

1. 事前に、AWS のアクセスキーとシークレットアクセスキーを設定します。
```bash
export AWS_ACCESS_KEY_ID=xxxxx
export AWS_SECRET_ACCESS_KEY=xxxxx
export AWS_DEFAULT_REGION=ap-northeast-1
```
2. `.env` ファイル内の項目を、お使いの環境に合わせて更新します。

```bash
cd serverless
cp env.template .env
vi .env
```

3. 以下のコマンドを実行します。
```bash
# 必要なパッケージをインストール
npm install -g serverless

# デプロイ
sls deploy
```