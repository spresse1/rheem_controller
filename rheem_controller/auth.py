from base64 import b64encode
from time import time
from json import loads
from six.moves.urllib.parse import quote
from base64 import b64encode
import logging
import requests
import threading


class Auth(requests.auth.AuthBase):
    """A subclass of python requests which manages adding Rheem's magic headers
    and authentication data to any requests made.  By providing this as an
    authentication class, it should be easy enough for a user to include it
    with all requests calls.

    Note that this class is designed to persist.  That is, as long as there is
    a reference to it, it will manage all the necessary token refreshing.

    Use as::
        >>> auth = RheemAuth()
        >>> RheemAuth.start_auth("username", "password")
        True
        >>> requests.get(url, auth=auth)
    """
    logger = logging.getLogger(__name__)
    token_lock = threading.Lock()
    creds_lock = threading.Lock()
    refresh_timer = None

    # API initial Auth URL
    _API_TOKEN_FETCH = "/auth/token"

    # Characters not to url-encode in username/passwd:
    _SAFE_CHARS = ",/?:&=+$#"

    _AUTH_HEADERS = {
        "Authorization":
            "Basic " + b64encode(
                b"com.rheem.econet_api:stablekernel").decode('UTF-8'),
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
    }

    _access_token = None
    _refresh_token = None

    def __init__(self, base_url="https://econet-api.rheemcert.com",
                 client_id="4890422047775.apps.rheemapi.com", timeout=10):
        """
        Initializes the session object.
        :param client_id:  The Rheem client id to use.  You probably shouldn't
            change this unless you actually have a client ID.
        :return: :class:`Auth <Auth>` object
        :rtype: rheem_controller.Auth
        """
        super(Auth, self).__init__()
        self.base_url = base_url
        self.client_id = client_id
        self.timeout = timeout

    def __call__(self, r):
        """
        :return: :class:`Request <Request>` object
        :rtype: requests.Request
        :raises: InvalidAuthenticationException
        """
        try:
            r.headers["Authorization"] = "Basic " + self.token
            r.headers["X-ClientID"] = self.client_id
            r.headers["X-Timestamp"] = int(time() * 1000)
            return r
        except AttributeError:
            raise NotStartedException("Must call Auth.start before "
                                      "using the instance for authentication")

    def start(self, user, passwd):
        """
        Sets up the authentication using a username and password.
        :param user: The username to authenticate with (typically an email
            address).
        :param passwd: The password to authenticate with.
        :return: None
        :raises: InvalidAuthenticationException
        """
        data = "username=" + quote(user, self._SAFE_CHARS) + '&password=' + \
            quote(passwd, self._SAFE_CHARS) + '&grant_type=password'
        self._get_token(data)

    def refresh(self):
        data = "grant_type=refresh&refresh_token=" + self._refresh_token
        self._get_token(data)

    def _get_token(self, data):
        response = requests.post(
            self.base_url + self._API_TOKEN_FETCH, headers=self._AUTH_HEADERS,
            data=data, timeout=self.timeout)
        try:
            json = loads(response.text)
        except ValueError as e:
            raise InvalidAPIResponseException(e, response)
        if response.status_code >= 400:
            raise InvalidAuthenticationException(
                response.status_code,
                "Authentication failed (%d): %s" %
                (response.status_code, json["error"]))
        with self.creds_lock:
            try:
                self._access_token = json["access_token"]
                self._refresh_token = json["refresh_token"]
            except KeyError as e:
                raise InvalidAPIResponseException(
                    "Invalid API response: %s" % e, response)

            # Now we're going to set up a thread to manage refreshing these
            # credentials... Make sure creds dont change under us.  Also
            # locks the refresh_timer
            # First, terminate any waiting thread (change of credentials)
            if self.refresh_timer:
                self.refresh_timer.cancel()
            # Build a timer that fires after 2000 seconds.  This matches the
            # value used in teh rheem implementation.
            self.refresh_timer = threading.Timer(2000, self.refresh)
            self.refresh_timer.setDaemon(True)
            self.refresh_timer.start()


class InvalidAuthenticationException(Exception):
    def __init__(self, status, message):
        self.status = status
        super(InvalidAuthenticationException, self).__init__(message)


class NotStartedException(Exception):
    pass


class InvalidAPIResponseException(Exception):

    def __init__(self, exception, response):
        super(InvalidAPIResponseException, self).__init__(
            str(exception) + "\nResponse was:\n%s" % response.content)
