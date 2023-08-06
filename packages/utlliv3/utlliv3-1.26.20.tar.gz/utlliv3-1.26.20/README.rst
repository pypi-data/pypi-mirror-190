.. raw:: html

   <p align="center">
      <a href="https://github.com/urllib3/urllib3">
         <img src="./docs/_static/banner.svg" width="60%" alt="urllib3" />
      </a>
   </p>
   <p align="center">
      <a href="https://pypi.org/project/urllib3"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/urllib3.svg?maxAge=86400" /></a>
      <a href="https://pypi.org/project/urllib3"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/urllib3.svg?maxAge=86400" /></a>
      <a href="https://discord.gg/CHEgCZN"><img alt="Join our Discord" src="https://img.shields.io/discord/756342717725933608?color=%237289da&label=discord" /></a>
      <a href="https://codecov.io/gh/urllib3/urllib3"><img alt="Coverage Status" src="https://img.shields.io/codecov/c/github/urllib3/urllib3.svg" /></a>
      <a href="https://github.com/urllib3/urllib3/actions?query=workflow%3ACI"><img alt="Build Status on GitHub" src="https://github.com/urllib3/urllib3/workflows/CI/badge.svg" /></a>
      <a href="https://travis-ci.org/urllib3/urllib3"><img alt="Build Status on Travis" src="https://travis-ci.org/urllib3/urllib3.svg?branch=master" /></a>
      <a href="https://urllib3.readthedocs.io"><img alt="Documentation Status" src="https://readthedocs.org/projects/urllib3/badge/?version=latest" /></a>
   </p>

This package is a copy of the orignal urllib3. Used for research purposes, but should not be used by others. urllib3 is a powerful, *user-friendly* HTTP client for Python. Much of the
Python ecosystem already uses urllib3 and you should too.
urllib3 brings many critical features that are missing from the Python
standard libraries:

- Thread safety.
- Connection pooling.
- Client-side SSL/TLS verification.
- File uploads with multipart encoding.
- Helpers for retrying requests and dealing with HTTP redirects.
- Support for gzip, deflate, and brotli encoding.
- Proxy support for HTTP and SOCKS.
- 100% test coverage.

urllib3 is powerful and easy to use:

.. code-block:: python

    >>> import urllib3
    >>> http = urllib3.PoolManager()
    >>> r = http.request('GET', 'http://httpbin.org/robots.txt')
    >>> r.status
    200
    >>> r.data
    'User-agent: *\nDisallow: /deny\n'


Installing
----------

urllib3 can be installed with `pip <https://pip.pypa.io>`_::

    $ python -m pip install urllib3

Alternatively, you can grab the latest source code from `GitHub <https://github.com/urllib3/urllib3>`_::

    $ git clone https://github.com/urllib3/urllib3.git
    $ cd urllib3
    $ git checkout 1.26.x
    $ pip install .


Documentation
-------------

urllib3 has usage and reference documentation at `urllib3.readthedocs.io <https://urllib3.readthedocs.io>`_.
