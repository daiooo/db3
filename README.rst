db3
=======

The Python interface to the SSDB


Installation
------------

To install db3, simply:

.. code-block:: bash

    $ sudo pip install db3

or from source:

.. code-block:: bash

    $ sudo python setup.py install


Getting Started
---------------

.. code-block:: pycon

   >>> from ssdb import SSDB
   >>> ssdb = SSDB(host='localhost', port=8888)
   >>> ssdb.multi_set(set_a='a', set_b='b', set_c='c', set_d='d')

