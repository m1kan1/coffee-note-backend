import json
import os
import time
import jwt
import requests
from cryptography.hazmat.primitives import serialization
from jwt.algorithms import RSAAlgorithm

AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
AUTH0_JWKS_URL = os.getenv('AUTH0_JWKS_URL')

jwks_json_str = json.dumps(json.loads(requests.get(AUTH0_JWKS_URL).text)['keys'][0])
public_key = RSAAlgorithm.from_jwk(jwks_json_str)
pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                              format=serialization.PublicFormat.SubjectPublicKeyInfo)


def auth_handler(event, context):
    print(event)
    auth_token = event["headers"]["Authorization"].replace("Bearer ", "")

    try:
        principal_id = jwt_verify(auth_token, pem)
        policy = generate_policy(principal_id, 'Allow', "arn:aws:execute-api:*:*:*/*/*/*")
        return policy
    except Exception as e:
        raise Exception('Unauthorized')


def jwt_verify(auth_token, pub_key):
    payload = jwt.decode(auth_token, pub_key, algorithms=['RS256'], audience=AUTH0_AUDIENCE)
    if time.time() > payload["exp"]:
        raise Exception("Token is expired")
    return payload['sub']


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
