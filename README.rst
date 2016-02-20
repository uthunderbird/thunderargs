=========
Thunderargs
=========

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