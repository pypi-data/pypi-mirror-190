
HEADER_AUTHORIZATION = "Authorization"
HEADER_AUTHORIZATION_MISSING = "Authorization header is missing in the request."
HEADER_CONTENT_TYPE_MISSING = "Content type header is missing in the request."
BEARER_STRING = "Bearer "
BEARER_STRING_MISSING = "Bearer keyword is missing in the access token"
CONTENT_TYPE_HEADER = 'Content-Type'
CONTENT_TYPE_VALUE = 'application/json'
TOKEN_INVALID_STATUS = "Access token is invalid. Please try again with valid token."
TOKEN_VALID_STATUS = "Access token validated successfully."
TOKEN_STATUS_VALUE_ERROR = "Access token status value is invalid."
SUCCESS_STATUS="Success"
ERROR_STATUS="Error"

import urllib3
import json
import logging

http = urllib3.PoolManager()

def validate_token(request_method,validate_token_url,access_token, content_type):
    try:
        if access_token is None or access_token == "":
            logging.error(HEADER_AUTHORIZATION_MISSING)
            return (HEADER_AUTHORIZATION_MISSING, 403)
        elif BEARER_STRING not in access_token:
            return (BEARER_STRING_MISSING, False)
        if content_type is None or content_type == "":
            logging.error(HEADER_CONTENT_TYPE_MISSING)
            return (HEADER_CONTENT_TYPE_MISSING, 403)

        response=http.request(request_method,validate_token_url,headers={CONTENT_TYPE_HEADER:content_type, HEADER_AUTHORIZATION:access_token})
        response_data = json.loads(response.data.decode('utf-8'))
        logging.info(response_data)
        logging.info(response.status)
        token_status = response_data['active']
        logging.info(token_status)
        if token_status == True:
            return (TOKEN_VALID_STATUS, token_status)
        elif token_status == False:
            return (TOKEN_INVALID_STATUS, token_status)
        else:
            return (TOKEN_STATUS_VALUE_ERROR, token_status)
    except Exception as err:
        return (ERROR_STATUS, str(err))