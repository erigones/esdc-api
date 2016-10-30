# -*- coding: utf-8 -*-
"""
esdc_api.response
~~~~~~~~~~~~~~~~~

This module provides the Response object returned by Danube Cloud API :class:`.Client` request methods.
"""

import json
from collections import namedtuple

from .exceptions import ESAPIRuntimeError, ServerError, ClientError, TaskError, TaskFailure, TaskRevoked

__all__ = (
    'Response',
    'Content'
)

#: Danube Cloud API Response content tuple returned by :attr:`.Response.content` property.
Content = namedtuple('Content', ('result', 'dc', 'task_status', 'task_id'))


class Response(object):
    """
    Danube Cloud API Response (wrapper around :class:`requests.Response <requests.Response>` class).

    :param response: The :class:`requests.Response <requests.Response>` object.
    """
    def __init__(self, response):
        """Initialize the response object."""
        self._response = response
        self._content = None
        self._raw_content = None
        self._status_code = None
        headers = response.headers
        #: Danube Cloud API version.
        self.version = headers.get('es_version', '???')
        self.task_id = headers.get('es_task_id', None)
        self.stream = headers.get('es_stream', None)  # Only set for stream responses
        self.dc = headers.get('es_dc', None)

    def __getstate__(self):
        # Fetch raw content before serializing
        if self._raw_content is None:
            self.consume_raw_content()

        return self.__dict__

    def __repr__(self):
        return '<Danube Cloud API :: %s [%s]>' % (self.__class__.__name__, self.status_code)

    def __bool__(self):
        return self.ok

    def __nonzero__(self):
        return self.__bool__()

    @staticmethod
    def is_status_code_ok(status_code):
        """Helper method for checking the HTTP status code.

        :param int status_code: HTTP status code.
        :return: `True` if status_code < 400.
        :rtype: bool
        """
        if 400 <= status_code < 600:
            return False
        else:
            return True

    @staticmethod
    def _get_exception(status_code, task_status, task_response):
        """Return Danube Cloud API exception class according to status_code (and other parameters)."""
        if status_code >= 500:
            return ServerError

        if task_response:
            if task_status == 'FAILURE':
                return TaskFailure
            elif task_status == 'REVOKED':
                return TaskRevoked
            else:
                return TaskError

        return ClientError

    def parse_raw_content(self, raw_content):
        """Parse raw content and return content tuple or API error exception (without raising it).

        :param raw_content: Last item yielded by :func:`fetch_raw_content`.
        :return: :class:`.ESAPIError` or :class:`.Content`.
        """
        assert isinstance(raw_content, bytes), 'Raw content must be an instance of bytes'

        task_id = self.task_id
        task_status = detail = None
        raw_content = raw_content.decode('utf-8')

        # noinspection PyBroadException
        try:
            content = json.loads(raw_content)
        except:
            content = raw_content
        else:
            if isinstance(content, dict):
                task_status = content.get('status', None)
                self.task_id = content.get('task_id', task_id)
                detail = content.get('detail', None)

                if 'result' in content:
                    content = content['result']

        if self.is_status_code_ok(self.status_code):
            return Content(content, self.dc, task_status, self.task_id)

        if detail is None:
            detail = content

        exc = self._get_exception(self.status_code, task_status, self._response.headers.get('es_task_response', None))

        return exc(self.status_code, detail, self.dc, task_status, self.task_id)

    def fetch_raw_content(self):
        """Fetch content from the server and yield `None` while waiting for some data.
        The last yielded item is always the raw content (`bytes`).

        :return: Generator which yields `None` until it yields the raw content (`bytes`).
        :rtype: generator
        """
        if self._raw_content is not None:
            raise ESAPIRuntimeError('The raw content for this response was already consumed')

        if self.stream:  # Streaming response
            content = None

            for chunk in self._response.iter_content(chunk_size=1):
                if chunk.isspace():
                    yield None
                else:
                    try:
                        data = chunk + self._response.content
                        data = data.strip().split(b'\n', 1)
                        content = data.pop()
                        self._status_code = int(data[0])
                    except Exception as e:
                        raise ESAPIRuntimeError('Could not read status code from streaming response: %s', e)
                    else:
                        break
        else:
            content = self._response.content

        self._raw_content = content

        yield content

    def consume_raw_content(self):
        """Iterate over the generator returned by :func:`fetch_raw_content` and return the last item - the raw content.

        :return: Raw content.
        :rtype: bytes
        """
        return list(self.fetch_raw_content())[-1]

    @property
    def raw_content(self):
        """Return raw content. Fetch and cache it by using :func:`consume_raw_content`; if not already consumed.

        :return: Raw content.
        :rtype: bytes
        """
        if self._raw_content is None:
            return self.consume_raw_content()
        else:
            return self._raw_content

    @property
    def status_code(self):
        """Return HTTP status code of this response.

        :return: HTTP status code.
        :rtype: int
        """
        return self._status_code or self._response.status_code

    @property
    def ready(self):
        """Indicate whether raw content was already consumed from server.

        :return: Raw content status.
        :rtype: bool
        """
        return self._raw_content is not None

    @property
    def content(self):
        """Parse raw content and return a content tuple.

        :return: Content namedtuple with :attr:`.Content.result` attribute.
        :rtype: :class:`.Content`
        :raise: :class:`.ESAPIError`
        """
        if self._content is None:
            self._content = self.parse_raw_content(self.raw_content)

        if isinstance(self._content, Exception):
            raise self._content
        else:
            return self._content

    @property
    def ok(self):
        """Return `True` if response status code is < 400. Also fetch the raw content if needed.

        :return: Response status according to the HTTP status code.
        :rtype: bool
        """
        if self._raw_content is None:
            self.consume_raw_content()

        return self.is_status_code_ok(self.status_code)

    @property
    def url(self):
        """Return the request URL."""
        return self._response.url

    @property
    def method(self):
        """Return the request method."""
        return self._response.method

    @property
    def headers(self):
        """Return the response headers."""
        return self._response.headers
