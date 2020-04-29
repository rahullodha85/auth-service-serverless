import json

import datetime

import jwt


def get_token(value):
    token = jwt.encode(
        {'token_val': value, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        'my_secret_key')

    return token.decode('UTF-8')


def extract_body(event):

    body = event.get('body', None)
    return json.load(body)


def return_data(body, code):
    return {
        "statusCode": code,
        "body": json.dumps(body)
    }


def login(data):

    username = data.get('username', None)
    password = data.get('password', None)

    return get_token(username)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    data = extract_body(event)

    token = login(data)

    response_data = json.dumps({
        "token": token
    })

    return return_data(response_data, 200)

    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": "hello world",
    #         "body": body,
    #         "event": event,
    #         "token": get_token("test")
    #     }),
    # }
