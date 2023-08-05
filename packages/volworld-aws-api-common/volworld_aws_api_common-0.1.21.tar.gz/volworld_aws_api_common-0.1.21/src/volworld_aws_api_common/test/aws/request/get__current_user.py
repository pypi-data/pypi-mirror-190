from volworld_aws_api_common.api.AA import AA
from volworld_aws_api_common.api.url import authUrl
from volworld_aws_api_common.test.aws.ATestRequest import ATestRequest
from volworld_aws_api_common.test.request import get_request
from volworld_aws_api_common.test.aws.request.request_util import response_to_dict
from volworld_aws_api_common.api.enum.HttpStatus import HttpStatus

def get__current_user(
        req: ATestRequest,
        token: str = None):
    resp_json, resp = get_request(
        authUrl.currentUserUrl, req,
        token=token)
    return response_to_dict(resp_json, resp)

def act__current_user(token: str = None) -> dict:
    resp = get__current_user(ATestRequest(True), token)
    assert resp[AA.HttpStatus] == HttpStatus.Ok_200
    return resp

def act__current_user___error(token: str = None) -> dict:
    resp = get__current_user(ATestRequest(True), token)
    assert AA.___Error___ in resp
    return resp
