Chlaus
======

This is an implementation of a miniature HTTP API to resolve DNS names via
HTTP. Only a single API user with a static password is supported. The username
must be passed in the environment variable `CHLAUS_USERNAME` and a hash of the
password in `CHLAUS_PASSWORD_HASH`.


Generate password hash
----------------------

The necessary password hash can be generated using the `mkpasswd` command
usually part of the `whois` package.

```
$ mkpasswd -m sha-512 --rounds 10000
Password:
$6$rounds=10000$FV71UF5DU3fPi80$ScjXip...
```


Usage
-----

The only resource is `/lookup/v1/<name>/<class>/<type>` where `name` is the
name to resolve, `class` the query class (usually `IN`, sometimes `CH`) and
`type` the query type (e.g. `A` or `MX`). The result is a JSON object with the
following keys:

| Field | Description |
| --- | --- |
| error | Error message as a string (failure only) |
| duration\_ms | Query duration in milliseconds |
| canonical\_name | Looked up name in canonical form |
| text | Query result sorted alphabetically and joined by commas |


Examples
--------

```
$ curl http://admin:pass@localhost:8000/lookup/v1/www.example.com/IN/A
{
  "canoncial_name": "www.example.com.",
  "duration_ms": 1,
  "text": "192.0.2.1,192.0.2.90"
}
```

```
$ curl http://admin:pass@localhost:8000/lookup/v1/example.net/IN/MX
{
  "canoncial_name": "example.net.",
  "duration_ms": 237,
  "text": "10 sfo.example.net.,5 fra.example.net."
}
```


Test environment
----------------

Install all dependencies in a
[virtual Python environment](http://pypi.python.org/pypi/virtualenv),
activate the environment and run the application:

```
CHLAUS_USERNAME=user \
CHLAUS_PASSWORD_HASH='$6$…' \
gunicorn --reload wsgi
```

<!-- vim: set sw=2 sts=2 et : -->
