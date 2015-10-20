# bravado-bitjws

Bravado-bitjws is an add on for [Bravado](https://github.com/Yelp/bravado) that allows [bitjws](https://github.com/g-p-g/bitjws) authentication.

## Installation

At the moment, installing from source is the only supported method.

`python setup.py install`

## Usage

Bravado-bitjws is used just like Bravado. The primary difference users need to be aware of is the management of bitjws keys.

##### Create a client with existing keys

``` Python
# Your bitjws private key in WIF
privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

# the URL of the swagger spec
url = "http://0.0.0.0:8002/static/swagger.json"

# initialize your client
client = BitJWSSwaggerClient.from_url(url, privkey=privkey)
```

If no key is provided to BitJWSSwaggerClient, one will be generated. However the private key originated, it is important to store private key somewhere secure.

## Known Limitations

Currently there is no management of server keys. This means that Bravado-bitjws checks the signature of server responses, but trusts all keys. It is up to the Bravado-bitjws user to match the server's key against a trusted list.