import json
import boto3
import os
from decimal import Decimal

from boto3.dynamodb.conditions import Key, Attr	##Keyオブジェクトを利用できるようにする

#Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-northeast-1",
    endpoint_url=os.environ.get("DYNAMODB_ENDPOINT_URL", "https://dynamodb.ap-northeast-1.amazonaws.com"),
)
table = dynamodb.Table("coffee_note")	##指定テーブルのアクセスオブジェクト取得


LPI_COMMON_HEADER = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE",
}

import sentry_sdk
from sentry_sdk import set_user
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[AwsLambdaIntegration(timeout_warning=True)],
    traces_sample_rate=1.0,
)

def coffee_note_handler(event, context):
    # TODO implement
    try:
        print(event)
        user_id = event["requestContext"]["authorizer"]["principalId"]
        set_user({"id": user_id})
        if event["body"] :
            body = json.loads(event["body"])
        if event['httpMethod']=='GET' :
            # scanData = table.scan()
            response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
            )
            items=response['Items']
            print(items)
            return {
                'statusCode': 200,
                'body': json.dumps(items ,default=decimal_to_int),
                "headers": LPI_COMMON_HEADER,

            }
        if event['httpMethod']=='POST' :
            putResponse = table.put_item(	##put_item()メソッドで追加・更新レコードを設定
            Item={	##追加・更新対象レコードのカラムリストを設定
                'user_id': user_id,
                'memo': body["memo"],
                'date': body["date"],
                'star': body["star"],
            }
            )
            return {
            'statusCode': 200,
            'body': json.dumps('Hello from PostLambda!'),
            "headers": LPI_COMMON_HEADER,
            }
            
        if event["httpMethod"] == "DELETE":
            delResponse = table.delete_item(
                Key={
                    'user_id': user_id,
                    'date': body["date"],

                }
            )
            return {
                'body': json.dumps('Hello from Lambda!'),
                'statusCode': 200,
                "headers": LPI_COMMON_HEADER,
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e)),
            "headers": LPI_COMMON_HEADER,
        }
    return {
        'statusCode': 404,
        'body': json.dumps('function not found!'),
        "headers": LPI_COMMON_HEADER,
    }

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)