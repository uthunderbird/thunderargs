=========
Thunderargs
=========

Abstract
--------

Bla-bla-bla bla-bla-bla


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

Or you can use it with flask, like this:

.. code-block:: python

    @app.route('/calc_with_expander/')
    def calc_with_expander(x:Arg(int), y:Arg(int),
                           op:Arg(str, default='+', expander=OPERATION)):
        return str(op(x,y))

(Since version 0.3 this feature was moved to `other repo <https://bitbucket.org/dsupiev/flask-thunderargs>`_.)

Or you can write your own proxy to any other framework!

Read the example.py