import dns.resolver
import flask
import functools
import logging
import os
import passlib.apps
import passlib.utils
import time


application = flask.Flask(__name__)


def check_auth(username, password):
  """Called to check whether a username/password combination is valid.

  """
  expected_name = os.getenv("CHLAUS_USERNAME", None)
  pwhash = os.getenv("CHLAUS_PASSWORD_HASH", None)

  if not (expected_name and pwhash):
    logging.warning("Missing environment variables for username/password")
    return False

  pwd_context = passlib.apps.custom_app_context

  return (passlib.utils.consteq(username, expected_name) and
          pwd_context.verify(password, pwhash))


def authenticate():
  """Send a 401 response enabling basic authentication.

  """
  return flask.Response('Login required', 401, {
    'WWW-Authenticate': 'Basic realm="Login required"',
    })


def requires_auth(f):
  @functools.wraps(f)
  def decorated(*args, **kwargs):
    auth = flask.request.authorization
    if not (auth and check_auth(auth.username, auth.password)):
      return authenticate()
    return f(*args, **kwargs)
  return decorated


@application.route('/')
def root():
  return 'This page intentionally left blank.'


def format_as_text(rdata):
  text = rdata.to_text()

  if isinstance(text, bytes):
    return text.decode("ASCII")

  return text


@application.route('/lookup/v1/<name>/<rdclass>/<rdtype>')
@requires_auth
def lookup(name, rdclass, rdtype):
  start = time.monotonic()

  try:
    answer = dns.resolver.query(name, rdtype=rdtype, rdclass=rdclass)
  except Exception as err:
    result = {
        "error": str(err),
        }
  else:
    result = {
        "canoncial_name": answer.canonical_name.to_unicode(),
        "text": ",".join(sorted(format_as_text(i) for i in answer)),
        }

  result["duration_ms"] = round((time.monotonic() - start) * 1000)

  return flask.json.jsonify(result)


if __name__ == '__main__':
  application.run()

# vim: set sw=2 sts=2 et :
