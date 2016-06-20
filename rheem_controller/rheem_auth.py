from base64 import b64encode
from time import mktime, time
from json import loads
from six.moves.urllib.parse import quote
import logging
import requests
import threading


class RheemAuth(requests.auth.AuthBase):
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
    _API_TOKEN_FETCH = "/v1/eco/authenticate"

    # Characters not to url-encode in username/passwd:
    _SAFE_CHARS = ",/?:@&=+$#"

    def __init__(self, base_url="https://io.myrheem.com",
                 client_id="4890422047775.apps.rheemapi.com"):
        """
        Initializes the session object.
        :param client_id:  The Rheem client id to use.  You probably shouldn't
            change this unless you actually have a client ID.
        :return: :class:`RheemAuth <RheemAuth>` object
        :rtype: rheem_controller.RheemAuth
        """
        super(RheemAuth, self).__init__()
        self.base_url = base_url
        self.client_id = client_id

    def __call__(self, r):
        """
        :return: :class:`Request <Request>` object
        :rtype: requests.Request
        :raises: InvalidAuthenticationException
        """
        r.headers["Authorization"] = "Basic " + self.token
        r.headers["X-ClientID"] = self.client_id
        r.headers["X-Timestamp"] = int(time() * 1000)
        return r

    def start_auth(self, user, passwd):
        """
        Sets up the authentication using a username and password.
        :param user: The username to authenticate with (typically an email
            address).
        :param passwd: The password to authenticate with.
        :return: nothing
        :raises: InvalidAuthenticationException
        """
        # Well turn me inside out and fly me on a flagpole.  The Rheem API
        # has no way of actually *refreshing* a token.  In the JS version the
        # URL exists (see reAuthenticateUser()), but it fails with a 404.
        # Because of this, we're going to need to store the username and
        # password somehow.  To anyone reading this: storing a username and
        # password in memory long term (or on disk long term) is a very very
        # bad idea.  There's no way this program can hope to secure it from any
        # local attacker - any motivated attacker will always be able to
        # emulate this process in order to get it back.  The best we can hope
        # to do is make it something that isn't trivially found.  Therefore,
        # we store the b64 encoded auth string, rather than the individual
        # username and password. This makes this item less likely to jump
        # out as credentials, but hopefully to appear more as random bytes.
        # It's really the best we can do.
        # TODO: Contact rheem and let them know that they've got dead code and
        # that they're forcing poor security practice?
        with self.creds_lock:
            self.__authstr = b64encode(
                (
                    quote(user, self._SAFE_CHARS) + ":" +
                    quote(passwd, self._SAFE_CHARS)
                ).encode()
            )

        self.refresh_creds()

        # Now we're going to set up a thread to manage refreshing these
        # credentials...
        # Make sure creds dont change under us.  Also locks the refresh_timer
        with self.creds_lock:
            # First, terminate any waiting thread (change of credentials)
            if self.refresh_timer:
                self.refresh_timer.cancel()
            # Build a timer that fires after 5200 seconds (1.5 hrs)
            self.refresh_timer = threading.Timer(5200, self.refresh_creds())

    def refresh_creds(self):
        headers = {
            "Authorization": "Basic " + self.__authstr.decode('UTF-8'),
            "X-ClientID": self.client_id,
            "X-Timestamp": int(time() * 1000)
        }
        response = requests.get(
            self.base_url + self._API_TOKEN_FETCH,  headers=headers)

        try:
            json = loads(response.text)
        except ValueError as e:
            raise InvalidAPIResponseException(e, response)

        if response.status_code >= 400:
            errors = ""
            errors = '\n'.join(json["ErrorList"])
            raise InvalidAuthenticationException(
                "Authentication failed (%d): %s" %
                (response.status_code, errors))

        with self.token_lock:
            try:
                self.token = json["AccessToken"]
            except KeyError as e:
                raise InvalidAPIResponseException(
                    "Invalid API response: %s" % e, response)


class InvalidAuthenticationException(Exception):
    pass


class InvalidAPIResponseException(Exception):

    def __init__(self, exception, response):
        super(InvalidAPIResponseException, self).__init__(
            str(exception) + "\nResponse was:\n%s" % response.content)
