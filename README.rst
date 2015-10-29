bravado-bitjws |PyPi version| |Build Status| |Coverage| |Gitter|
================================================================

Bravado-bitjws is an add on for
`Bravado <https://github.com/Yelp/bravado>`__ that allows
`bitjws <https://github.com/g-p-g/bitjws>`__ authentication.

Install
-------

By default it's expected that
`secp256k1 <https://github.com/bitcoin/secp256k1>`__ is available, so
install it before proceeding; make sure to run
``./configure --enable-module-recovery``. If you're using some other
library that provides the functionality necessary for this, check the
**Using a custom library** section of the bitjws README.

Bravado-bitjws can be installed by running:

``pip install bravado-bitjws``

Building secp256k1
''''''''''''''''''

In case you need to install the ``secp256k1`` C library, the following
sequence of commands is recommended. If you already have ``secp256k1``,
make sure it was compiled from the expected git commit or it might fail
to work due to API incompatibilities.

::

    git clone git://github.com/bitcoin/secp256k1.git libsecp256k1
    cd libsecp256k1
    git checkout d7eb1ae96dfe9d497a26b3e7ff8b6f58e61e400a
    ./autogen.sh
    ./configure --enable-module-recovery
    make
    sudo make install

Usage
-----

Bravado-bitjws is used just like Bravado. The primary difference users
need to be aware of is the management of bitjws keys.

Create a client with existing keys
''''''''''''''''''''''''''''''''''

.. code:: Python

    # Your bitjws private key in WIF
    privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

    # the URL of the swagger spec
    url = "http://0.0.0.0:8002/static/swagger.json"

    # initialize your client
    client = BitJWSSwaggerClient.from_url(url, privkey=privkey)

If no key is provided to BitJWSSwaggerClient, one will be generated.
However the private key originated, it is important to store private key
somewhere secure.

Known Limitations
-----------------

Currently there is no management of server keys. This means that
Bravado-bitjws checks the signature of server responses, but trusts all
keys. It is up to the Bravado-bitjws user to match the server's key
against a trusted list.

.. |PyPi version| image:: https://img.shields.io/pypi/v/bravado-bitjws.svg
   :target: https://pypi.python.org/pypi/bravado-bitjws/
.. |Build Status| image:: https://travis-ci.org/deginner/bravado-bitjws.svg?branch=master
   :target: https://travis-ci.org/deginner/bravado-bitjws
.. |Coverage| image:: https://coveralls.io/repos/deginner/bravado-bitjws/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/deginner/bravado-bitjws?branch=master
.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/deginner/bitjws?utm_source=share-link&utm_medium=link&utm_campaign=share-link
