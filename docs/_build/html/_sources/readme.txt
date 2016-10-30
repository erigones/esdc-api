Danube Cloud API
################

`Danube Cloud API <https://danubecloud.org/>`_ Python Library.

* Supported Python versions: >= 2.6 and >= 3.2

.. image:: https://badge.fury.io/py/esdc-api.png
    :target: http://badge.fury.io/py/esdc-api

Installation
------------

.. code:: bash

    pip install esdc-api

**Dependencies:**

- `requests <http://docs.python-requests.org/>`_

Usage
-----

.. code:: python

    >>> from esdc_api import Client
    >>> es = Client(api_url='https://danube.cloud/api', api_key='<your-api-key>')
    >>> es.get('/vm').content

Complete documentation is available at https://erigones.github.io/esdc-api/

Links
-----

- Danube Cloud: https://danubecloud.com
- Danube Cloud API Documentation: https://docs.danubecloud.org/api/
- Bug Tracker: https://github.com/erigones/esdc-api/issues
- Twitter: https://twitter.com/erigones

