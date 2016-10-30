# -*- coding: utf-8 -*-
"""
esdc_api.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains all exceptions used by the Danube Cloud API library.
"""

__all__ = (
    'ESAPIException',
    'ESAPIRuntimeError',
    'ESAPIError',
    'ServerError',
    'ClientError',
    'TaskError',
    'TaskFailure',
    'TaskRevoked'
)


class ESAPIException(Exception):
    """Danube Cloud API base exception."""
    def __repr__(self):
        return '<Danube Cloud API :: %s>' % self.__class__.__name__


class ESAPIRuntimeError(ESAPIException, RuntimeError):
    """Danube Cloud API HTTP client errors.

    Can be raised during HTTP content fetching and parsing.
    """
    pass


class ESAPIError(ESAPIException):
    """Raised for all API errors incoming from Danube Cloud server.

    :param status_code: HTTP response status code.
    :param detail: Detailed information about the API error.
    :param dc: Danube Cloud virtual datacenter in which the error occurred.
    :param task_status: Task status (optional).
    :param task_id: Task ID (optional).
    """
    def __init__(self, status_code, detail, dc, task_status=None, task_id=None):
        if isinstance(detail, dict):
            if 'detail' in detail:
                detail = detail['detail']
            elif 'message' in detail:
                detail = detail['message']

        self.status_code = status_code
        self.detail = detail
        self.dc = dc
        self.task_status = task_status
        self.task_id = task_id

        super(ESAPIError, self).__init__(status_code)

    def __repr__(self):
        return '<Danube Cloud API :: %s [%s]>' % (self.__class__.__name__, self.status_code)

    def __str__(self):
        return 'Error %s: %s' % (self.status_code, self.detail)


class ServerError(ESAPIError):
    """Danube Cloud API 5xx server errors."""
    def __str__(self):
        return 'Server Error %s: %s' % (self.status_code, self.detail)


class ClientError(ESAPIError):
    """Danube Cloud API 4xx errors."""
    def __str__(self):
        return 'Client Error %s: %s' % (self.status_code, self.detail)


class TaskError(ESAPIError):
    """Base class for all Danube Cloud task errors."""
    def __str__(self):
        return 'Task Error %s: %s' % (self.status_code, self.detail)


class TaskFailure(TaskError):
    """The task has failed.

    The :attr:`detail` attribute will contain details about the failure.
    """
    pass


class TaskRevoked(TaskError):
    """The task has been revoked.

    The :attr:`detail` attribute will contain the revocation reason.
    """
    pass
