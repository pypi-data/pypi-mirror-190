
import urllib3
import json
import logging
from flask import jsonify, request
from functools import wraps
import constants

http = urllib3.PoolManager()
    
def validate_token(request_method,validate_token_url):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                access_token = request.headers.get(constants.HEADER_AUTHORIZATION)
                content_type = request.headers.get(constants.CONTENT_TYPE_HEADER)
                if access_token is None or access_token == "":
                    logging.error(constants.HEADER_AUTHORIZATION_MISSING)
                    return jsonify({"error-code": 403, "error-desc": "header missing", "error-msg": constants.HEADER_AUTHORIZATION_MISSING}), 403
                elif constants.BEARER_STRING not in access_token:
                    logging.error(constants.BEARER_STRING_MISSING)
                    return jsonify({"error-code": 401, "error-desc": "unauthorized", "error-msg": constants.BEARER_STRING_MISSING}), 401
                if content_type is None or content_type == "":
                    logging.error(constants.HEADER_CONTENT_TYPE_MISSING)
                    return jsonify({"error-code": 403, "error-desc": "header missing", "error-msg": constants.HEADER_CONTENT_TYPE_MISSING}), 403

                response=http.request(request_method,validate_token_url,headers={constants.CONTENT_TYPE_HEADER:content_type, constants.HEADER_AUTHORIZATION:access_token})
                response_data = json.loads(response.data.decode('utf-8'))
                logging.info(response_data)
                logging.info(response.status)
                token_status = response_data['active']
                logging.info(token_status)
                if token_status == False:
                    logging.error(constants.TOKEN_INVALID_STATUS)
                    return jsonify({"error-code": 401, "error-desc": "unauthorized", "error-msg": constants.TOKEN_INVALID_STATUS}), 401
                elif token_status != True:
                    logging.error(constants.TOKEN_STATUS_VALUE_ERROR)
                    return jsonify({"error-code": 401, "error-desc": "unauthorized", "error-msg": constants.TOKEN_STATUS_VALUE_ERROR}), 401
            except Exception as err:
                logging.error("Error: {}".format(err))
                return jsonify(str(err)), 405
            return function(*args, **kwargs)
        return wrapper
    return decorator