# -*- coding: utf-8 -*-
import logging
import json
import bitjws
import requests
import requests.auth
from bravado.requests_client import *

from bravado.http_future import HttpFuture

log = logging.getLogger(__name__)

__all__ = ['BitJWSRequestsClient', 'BitJWSAuthenticator']


class BitJWSAuthenticator(Authenticator):
    """BitJWS authenticator uses JWS and the CUSTOM-BITCOIN-SIGN algorithm.

    :param host: Host to authenticate for.
    :param privkey: Private key as a WIF string
    """

    def __init__(self, host, privkey):
        super(BitJWSAuthenticator, self).__init__(host)
        self.privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

    def apply(self, request):
        if len(request.data) > 0:
            data = bitjws.sign_serialize(self.privkey, **json.loads(request.data))
        else:
            data = bitjws.sign_serialize(self.privkey, **request.params)
        request.params = {}
        request.data = data
        request.headers['Content-Type'] = 'application/jose'
        return request


class BitJWSRequestsClient(RequestsClient):
    """Synchronous HTTP client implementation.
    """

    def __init__(self):
        self.session = requests.Session()
        self.authenticator = None

    def request(self, request_params, response_callback=None):
        """
        :param request_params: complete request data.
        :type request_params: dict
        :param response_callback: Function to be called on the response
        :returns: HTTP Future object
        :rtype: :class: `bravado_core.http_future.HttpFuture`
        """
        sanitized_params, misc_options = self.separate_params(request_params)
        requests_future = RequestsFutureAdapter(
            self.session,
            self.authenticated_request(sanitized_params),
            misc_options)

        return HttpFuture(
            requests_future,
            BitJWSRequestsResponseAdapter,
            response_callback,
        )

    def set_bitjws_key(self, host, privkey):
        self.authenticator = BitJWSAuthenticator(host=host, privkey=privkey)


class BitJWSRequestsResponseAdapter(RequestsResponseAdapter):
    """Wraps a requests.models.Response object to provide a uniform interface
    to the response innards.
    """

    def json(self, **kwargs):
        jso = {}
        if 'content-type' in self._delegate.headers and \
                'application/jose' in self._delegate.headers['content-type']:
            rawtext = self.text.decode('utf8')
            headers, jwtpayload = bitjws.validate_deserialize(rawtext)
            if 'data' in jwtpayload:
                jso = jwtpayload['data']
        else:
            jso = self._delegate.json(**kwargs)
        return jso

