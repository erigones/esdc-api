# -*- coding: utf-8 -*-
"""
esdc_api.client
~~~~~~~~~~~~~~~

This module contains the Danube Cloud API :class:`Client` class used to access the Danube Cloud HTTP API.
"""

import json
import requests

from . import __version__
from .response import Response

__all__ = (
    'Client',
)


class Client(object):
    """
    Danube Cloud API HTTP client.

    :param str api_url: Danube Cloud API base URL.
    :param str api_key: Optional API key used to perform authenticated requests.
    :param tuple auth: Optional auth tuple to enable Basic/Digest/Custom HTTP authentication.
    :param float timeout: How long to wait for the server to send data before giving up (default: `None`).
    :param bool ssl_verify: If `True`, the SSL cert will be verified (default: `True`).
    """
    def __init__(self, api_url='https://danube.cloud/api', api_key=None, auth=None, timeout=None, ssl_verify=True):
        """Initialize Danube Cloud API object."""
        assert not api_url.endswith('/'), 'trailing slash in api_url is not allowed'

        self.api_url = api_url
        self.auth = auth
        self.timeout = timeout
        self.ssl_verify = ssl_verify
        self.headers = {
            'User-Agent': 'esdc-api/python-client/%s' % __version__,
            'Accept': 'application/json; indent=4',
            'Content-Type': 'application/json; indent=4',
            'ES-STREAM': 'es',
        }

        if api_key:
            self.headers['ES-API-KEY'] = api_key

    def __repr__(self):
        return '<Danube Cloud API :: %s [%s]>' % (self.__class__.__name__, self.api_url)

    def _get_request_url(self, resource):
        """Return complete URL send to the server."""
        assert resource.startswith('/'), 'resource should begin with a slash'

        url = self.api_url + resource

        if not url.endswith('/'):  # Every URL must have a trailing slash
            url += '/'

        return url

    def request(self, method, resource, timeout=None, stream=True, **params):
        """Perform request to server and return :class:`.Response` or
         raise an :class:`.ESAPIException`. This method is used by all public request methods in this class.

        :param str method: HTTP method.
        :param str resource: Danube Cloud API resource beginning with a slash (e.g. `/vm/<hostname>`).
        :param int timeout: Optional timeout for the request (default `None`).
        :param bool stream: Whether to wait for asynchronous API calls to finish (default `True`).
        :param dict params: Request parameters internally translated into POST/PUT/DELETE JSON encoded data or
         GET query string.

        :return: Response object.
        :rtype: :class:`.Response`
        :raise: :class:`.ESAPIException`
        """
        url = self._get_request_url(resource)

        if timeout is None:
            timeout = self.timeout

        if stream:
            headers = self.headers
        else:
            headers = self.headers.copy()
            del headers['ES-STREAM']

        if method.upper() == 'GET':
            data = None
        else:
            data = json.dumps(params)
            params = None

        return Response(requests.request(method, url, params=params, data=data, headers=headers,
                                         auth=self.auth, timeout=timeout, allow_redirects=False,
                                         stream=stream, verify=self.ssl_verify))

    def get(self, resource, **kwargs):
        """Perform GET :func:`request <request>` to Danube Cloud API."""
        return self.request('GET', resource, **kwargs)

    def post(self, resource, **kwargs):
        """Perform POST :func:`request <request>` to Danube Cloud API."""
        return self.request('POST', resource, **kwargs)

    def create(self, resource, **kwargs):
        """Alias for :func:`post`."""
        return self.post(resource, **kwargs)

    def put(self, resource, **kwargs):
        """Perform PUT :func:`request <request>` to Danube Cloud API."""
        return self.request('PUT', resource, **kwargs)

    def set(self, resource, **kwargs):
        """Alias for :func:`put`."""
        return self.put(resource, **kwargs)

    def delete(self, resource, **kwargs):
        """Perform DELETE :func:`request <request>` to Danube Cloud API."""
        return self.request('DELETE', resource, **kwargs)

    def options(self, resource, **kwargs):
        """Perform OPTIONS :func:`request <request>` to Danube Cloud API."""
        return self.request('OPTIONS', resource, **kwargs)

    def logout(self):
        """Logout from Danube Cloud API (:func:`GET <get>` /accounts/logout)."""
        response = self.get('/accounts/logout')

        if response.ok:
            self.headers.pop('Authorization', None)

        return response

    def login(self, username, password):
        """Login to Danube Cloud API (:func:`POST <post>` /accounts/login) using username and password.

        :param str username: Danube Cloud username.
        :param str password: Danube Cloud password.
        """
        self.headers.pop('Authorization', None)
        response = self.post('/accounts/login', username=username, password=password)

        if response.ok:
            self.headers['Authorization'] = 'Token %s' % response.content.result['token']

        return response

    def is_authenticated(self):
        """Return `True` if api_key is set or authorization token was saved by the :func:`login` method."""
        return 'ES-API-KEY' in self.headers or 'Authorization' in self.headers

    def ping(self):
        """:func:`GET <get>` /ping"""
        return self.get('/ping').content.result
