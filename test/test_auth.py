import json
import requests
import os
import pytest
from bravado.swagger_model import load_file
from bravado_bitjws.client import BitJWSSwaggerClient
from bravado_bitjws.requests_client import BitJWSAuthenticator
import bitjws

specurl = "%s/example/swagger.json" % os.path.realpath(os.path.dirname(__file__))
wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_apply_auth():
    url = 'http://0.0.0.0:8002'
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)
    data = ""
    headers = {}
    params = {'message': 'goes here for sure'}
    request = requests.Request(method='GET', url=url, headers=headers,
                               data=data, params=params)
    req = bjauth.apply(request)
    assert len(req.params) == 0
    assert req.headers['Content-Type'] == 'application/jose'

    h, p = bitjws.validate_deserialize(req.data)
    assert 'message' in p
    assert p['message'] == params['message']


def test_apply_auth_json():
    url = 'http://0.0.0.0:8002'
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)
    rawdata = {'message': 'goes here for sure'}
    data = json.dumps(rawdata)
    headers = {'Content-Type': 'application/json'}
    params = {'mess': 'couldgohere'}
    request = requests.Request(method='GET', url=url, headers=headers,
                               data=data, params=params)
    req = bjauth.apply(request)
    assert len(req.params) == 0
    assert req.headers['Content-Type'] == 'application/jose'

    h, p = bitjws.validate_deserialize(req.data)
    assert 'message' in p
    assert p['message'] == rawdata['message']

