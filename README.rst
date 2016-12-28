=========
Thunderargs
=========

|pypi| |unix_build|

Abstract
--------

This library helps you to validate function parameters.


Installation
------------

.. code-block:: bash

    sudo pip install thunderargs

Usage
-----

You can use it like this:

.. code-block:: python

    from thunderargs import Arg
    from thunderargs.endpoint import Endpoint


    @Endpoint
    def max_int(x: Arg(int), y: Arg(int)):
        return max(x,y)


Read the tests for more examples.

.. |pypi| image:: https://img.shields.io/pypi/v/thunderargs.svg?style=flat-square&label=latest%20version
    :target: https://pypi.python.org/pypi/thunderargs
    :alt: Latest version released on PyPi

.. |unix_build| image:: https://img.shields.io/travis/uthunderbird/thunderargs/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/uthunderbird/thunderargs/
    :alt: Build status of the master branch on Mac/Linux