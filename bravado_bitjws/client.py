# -*- coding: utf-8 -*-
"""
The :class:`SwaggerClient` provides an interface for making API calls based on
a swagger spec, and returns responses of python objects which build from the
API response.

Structure Diagram::

        +---------------------+
        |                     |
        |    SwaggerClient    |
        |                     |
        +------+--------------+
               |
               |  has many
               |
        +------v--------------+
        |                     |
        |     Resource        +------------------+
        |                     |                  |
        +------+--------------+         has many |
               |                                 |
               |  has many                       |
               |                                 |
        +------v--------------+           +------v--------------+
        |                     |           |                     |
        |     Operation       |           |    SwaggerModel     |
        |                     |           |                     |
        +------+--------------+           +---------------------+
               |
               |  uses
               |
        +------v--------------+
        |                     |
        |     HttpClient      |
        |                     |
        +---------------------+


To get a client

.. code-block:: python

    client = bravado.client.SwaggerClient.from_url(swagger_spec_url)
"""
import functools
import logging
import sys
import bitjws

from bravado_core.docstring import create_operation_docstring
from bravado_core.exception import MatchingResponseNotFound
from bravado_core.exception import SwaggerMappingError
from bravado_core.param import marshal_param
from bravado_core.response import unmarshal_response
from bravado_core.spec import Spec
import six
from six import iteritems, itervalues
from six.moves.urllib import parse as urlparse

from bravado.docstring_property import docstring_property
from bravado.exception import HTTPError
from bravado.requests_client import RequestsClient
from bravado.swagger_model import Loader
from bravado.warning import warn_for_deprecated_op

from bravado.client import *
from bravado_bitjws.requests_client import BitJWSRequestsClient

log = logging.getLogger(__name__)


__all__ = ['BitJWSSwaggerClient']


class BitJWSSwaggerClient(SwaggerClient):
    """
    A client for accessing a Swagger-documented RESTful service,
    which also uses bitjws authentication.
    """

    def __init__(self, swagger_spec, resource_decorator=None):
        """
        :param swagger_spec: :class:`bravado_core.spec.Spec`
        :param resource_decorator: The ResourceDecorator class to use
        :type  resource_decorator: ResourceDecorator
        """
        super(BitJWSSwaggerClient, self).__init__(swagger_spec,
                resource_decorator=resource_decorator)

    @classmethod
    def from_url(cls, spec_url, http_client=None, request_headers=None,
                 config=None, resource_decorator=None, privkey=None):
        """
        Build a :class:`SwaggerClient` from a url to the Swagger
        specification for a RESTful API.

        :param spec_url: url pointing at the swagger API specification
        :type spec_url: str
        :param http_client: an HTTP client used to perform requests
        :type  http_client: :class:`bravado.http_client.HttpClient`
        :param request_headers: Headers to pass with http requests
        :type  request_headers: dict
        :param config: bravado_core config dict. See
            bravado_core.spec.CONFIG_DEFAULTS
        :param resource_decorator: The ResourceDecorator class to use
        :type  resource_decorator: ResourceDecorator
        """
        log.debug(u"Loading from %s" % spec_url)
        if privkey is None:
            privkey = bitjws.PrivateKey()
        elif isinstance(privkey, str):
            privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

        if http_client is None:
            host = urlparse.urlsplit(spec_url).hostname
            http_client = BitJWSRequestsClient()
            http_client.set_bitjws_key(host,
                    bitjws.privkey_to_wif(privkey.private_key))
        request_headers = request_headers or {}
        request_headers['content-type'] = 'application/jose'
        loader = Loader(http_client, request_headers=request_headers)
        spec_dict = loader.load_spec(spec_url)
        return cls.from_spec(spec_dict, spec_url, http_client, config,
                             resource_decorator, privkey)

    @classmethod
    def from_spec(cls, spec_dict, origin_url=None, http_client=None,
                  config=None, resource_decorator=None, privkey=None):
        """
        Build a :class:`SwaggerClient` from swagger api docs

        :param spec_dict: a dict with a Swagger spec in json-like form
        :param origin_url: the url used to retrieve the spec_dict
        :type  origin_url: str
        :param config: Configuration dict - see spec.CONFIG_DEFAULTS
        :param resource_decorator: The ResourceDecorator class to use
        :type  resource_decorator: ResourceDecorator
        :param str privkey: The WIF private key to use for bitjws signing
        """
        if privkey is None:
            privkey = bitjws.PrivateKey()
        elif isinstance(privkey, str):
            privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))

        if http_client is None:
            host = urlparse.urlsplit(origin_url).hostname
            http_client = BitJWSRequestsClient()
            http_client.set_bitjws_key(host,
                    bitjws.privkey_to_wif(privkey.private_key))

        resource_decorator = resource_decorator or ResourceDecorator
        swagger_spec = Spec.from_dict(
            spec_dict, origin_url, http_client, config)
        return cls(swagger_spec, resource_decorator)

