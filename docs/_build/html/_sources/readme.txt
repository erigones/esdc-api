Erigones SDDC API
#################

`Erigones SDDC API <https://www.erigones.com/erigones-sddc/>`_ Python Library.

* Supported Python versions: >= 2.6 and >= 3.2

.. image:: https://badge.fury.io/py/erigones-sddc-api.png
    :target: http://badge.fury.io/py/erigones-sddc-api

Installation
------------

.. code:: bash

    pip install erigones-sddc-api

**Dependencies:**

- `requests <http://docs.python-requests.org/>`_

Usage
-----

.. code:: python

    >>> from erigones_sddc_api import Client
    >>> es = Client(api_url='https://my.erigones.com/api', api_key='<your-api-key>')
    >>> es.get('/vm').content

Complete documentation is available at https://erigones.github.io/erigones-sddc-api/

Links
-----

- Erigones SDDC: http://www.erigones.com/erigones-sddc/
- Erigones SDDC API Documentation: https://my.erigones.com/docs/api/
- Bug Tracker: https://github.com/erigones/erigones-sddc-api/issues
- Twitter: https://twitter.com/erigones

