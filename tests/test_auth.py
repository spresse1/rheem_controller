import rheem_controller.auth
from mock import patch
from mock import Mock
import responses
import unittest
import re


class test__get_token(unittest.TestCase):
    urlre = re.compile(".*/auth/token")

    def setUp(self):
        self.timer_patcher = patch("rheem_controller.auth.threading.Timer")
        self.mock_timer = self.timer_patcher.start()

    def tearDown(self):
        responses.reset()
        self.timer_patcher.stop()

    @responses.activate
    def test__get_token_success_success(self):
        responses.add(
            responses.POST, self.urlre, json={
                "access_token": "aToken",
                "refresh_token": "someRefresh",
            }, status=200
        )
        ra = rheem_controller.auth.Auth()
        ra._get_token(
            "username=test%40example&password=password&grant_type=password")
        self.assertEqual(ra._access_token, "aToken")
        self.assertEqual(ra._refresh_token, "someRefresh")
        self.mock_timer.assert_called_with(2000, ra.refresh)

    @responses.activate
    def test__get_token_success_success_with_timer(self):
        responses.add(
            responses.POST, self.urlre, json={
                "access_token": "aToken",
                "refresh_token": "someRefresh",
            }, status=200
        )
        ra = rheem_controller.auth.Auth()
        ra.refresh_timer = self.mock_timer
        ra._get_token(
            "username=test%40example&password=password&grant_type=password")
        self.assertEqual(ra._access_token, "aToken")
        self.assertEqual(ra._refresh_token, "someRefresh")
        self.mock_timer.cancel.assert_called_with()
        self.mock_timer.assert_called_with(2000, ra.refresh)

    @responses.activate
    def test__get_token_success_ValueError(self):
        responses.add(
            responses.POST, self.urlre, body="", status=200
        )
        ra = rheem_controller.auth.Auth()
        with self.assertRaises(
                rheem_controller.auth.InvalidAPIResponseException):
            ra._get_token(
                "username=test%40example&password=password&grant_type=password"
            )

    @responses.activate
    def test__get_token_success_InvalidAuthenticationException(self):
        responses.add(
            responses.POST, self.urlre, json={
                "error": "Invalid"
            }, status=400
        )
        ra = rheem_controller.auth.Auth()
        with self.assertRaises(
                rheem_controller.auth.InvalidAuthenticationException):
            ra._get_token(
                "username=test%40example&password=password&grant_type=password"
            )

    @responses.activate
    def test__get_token_success_InvalidKeyError(self):
        responses.add(
            responses.POST, self.urlre, json={
                "error": "Invalid"
            }, status=200
        )
        ra = rheem_controller.auth.Auth()
        with self.assertRaises(
                rheem_controller.auth.InvalidAPIResponseException):
            ra._get_token(
                "username=test%40example&password=password&grant_type=password"
            )


class test___call__(unittest.TestCase):
    def setUp(self):
        self.ra = rheem_controller.auth.Auth()
        self.mock_r = Mock()
        self.mock_r.headers = {}

    def test_success(self):
        self.ra.token = "SomeToken"
        self.ra.client_id = "Some ID"
        self.ra(self.mock_r)
        self.assertEqual(self.mock_r.headers["Authorization"],
                         "Basic SomeToken")
        self.assertEqual(self.mock_r.headers["X-ClientID"], "Some ID")

    def test_need_start(self):
        with self.assertRaises(rheem_controller.auth.NotStartedException):
            self.ra(self.mock_r)


class test_start(unittest.TestCase):
    urlre = re.compile(".*/auth/token")

    def setUp(self):
        # Most tests don't use this patcher
        self.get_token_patcher = patch("rheem_controller.auth.Auth._get_token")
        self.mock_get_token = self.get_token_patcher.start()

        # Most do use this one (or don't get to it)
        self.timer_patcher = patch("rheem_controller.auth.threading.Timer")
        self.mock_timer = self.timer_patcher.start()

    def tearDown(self):
        responses.reset()
        self.timer_patcher.stop()
        self.get_token_patcher.stop()

    def test_start(self):
        ra = rheem_controller.auth.Auth()
        ra.start("test@example", "password")

        self.mock_get_token.assert_called_with(
            "username=test%40example&password=password&grant_type=password")

    def test_refresh(self):
        ra = rheem_controller.auth.Auth()
        ra._refresh_token = "refresh_token"
        ra.refresh()

        self.mock_get_token.assert_called_with(
            "grant_type=refresh&refresh_token=refresh_token")
