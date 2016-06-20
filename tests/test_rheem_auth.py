import rheem_controller.rheem_auth
from mock import patch
from mock import Mock
import responses
import unittest
import re


class test_RheemAuth(unittest.TestCase):

    def setup(self):
        responses.reset()

    @responses.activate
    def test_start_auth(self):
        urlre = re.compile(".*/v1/eco/authenticate")
        responses.add(
            responses.GET, urlre, json={
                "AccessToken": "ZjJjJjJjJjJj",
                "TokenType": "Bearer",
                "RefreshToken": "ZmZmZmZmZmZmZm"
            }
        )
        ra = rheem_controller.rheem_auth.RheemAuth()
        ra.start_auth("test@example", "password")

        treq = responses.calls[0].request
        self.assertEqual(
            treq.headers["Authorization"],
            "Basic dGVzdEBleGFtcGxlOnBhc3N3b3Jk")
        self.assertEqual(
            treq.headers["X-ClientID"], "4890422047775.apps.rheemapi.com")
        self.assertEqual(ra.token, "ZjJjJjJjJjJj")

    @responses.activate
    def test_start_auth_failed(self):
        urlre = re.compile(".*/v1/eco/authenticate")
        responses.add(
            responses.GET, urlre, json={
                "ErrorList": [
                    "Some", "errors"
                ]
            }, status=401
        )
        ra = rheem_controller.rheem_auth.RheemAuth()

        with self.assertRaises(
                rheem_controller.rheem_auth.InvalidAuthenticationException):
            ra.start_auth("test@example", "password")

    @responses.activate
    def test_start_auth_failed_no_error(self):
        urlre = re.compile(".*/v1/eco/authenticate")
        responses.add(
            responses.GET, urlre, status=401
        )
        ra = rheem_controller.rheem_auth.RheemAuth()

        with self.assertRaises(
                rheem_controller.rheem_auth.InvalidAPIResponseException):
            ra.start_auth("test@example", "password")

    @responses.activate
    def test_start_auth_success_bad_api(self):
        urlre = re.compile(".*/v1/eco/authenticate")
        responses.add(
            responses.GET, urlre, status=200, json={"Nothing": "here"}
        )
        ra = rheem_controller.rheem_auth.RheemAuth()

        with self.assertRaises(
                rheem_controller.rheem_auth.InvalidAPIResponseException):
            ra.start_auth("test@example", "password")

    def test_call(self):
        import requests
        r = requests.Request()
        ra = rheem_controller.rheem_auth.RheemAuth()
        ra.token = "SomeJunkHJHJHJHJHJ"
        res = ra(r)
        self.assertEqual(
            res.headers["Authorization"], "Basic SomeJunkHJHJHJHJHJ")
        self.assertEqual(res.headers["X-ClientID"], ra.client_id)

    @responses.activate
    def test_start_auth_second_call(self):
        urlre = re.compile(".*/v1/eco/authenticate")
        responses.add(
            responses.GET, urlre, json={
                "AccessToken": "ZjJjJjJjJjJj",
                "TokenType": "Bearer",
                "RefreshToken": "ZmZmZmZmZmZmZm"
            }
        )
        ra = rheem_controller.rheem_auth.RheemAuth()
        rtmock = Mock()
        ra.refresh_timer = rtmock
        ra.start_auth("test@example", "password")

        rtmock.cancel.assert_called()
