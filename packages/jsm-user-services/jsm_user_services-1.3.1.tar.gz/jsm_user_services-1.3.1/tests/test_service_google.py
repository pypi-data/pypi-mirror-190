from unittest.mock import patch

from django.test import TestCase
from requests_mock import Mocker

from jsm_user_services.exception import MissingRequiredConfiguration
from jsm_user_services.services.google import perform_recaptcha_validation
from jsm_user_services.support.local_threading_utils import add_to_local_threading


class GoogleServiceTest(TestCase):
    @patch("jsm_user_services.support.settings_utils.getattr", side_effect=["test", None])
    def test_should_raise_if_missing_secret(self, mocked_getattr):

        with self.assertRaises(MissingRequiredConfiguration):
            perform_recaptcha_validation("")

    @patch(
        "jsm_user_services.support.settings_utils.getattr",
        side_effect=["http://test.com", "test", "0.8", 'true-client-ip']
    )
    def test_should_perform_request_if_both_vars_exists(self, mocked_getattr):

        with Mocker(real_http=True) as mocker:
            add_to_local_threading("user_ip", "random-fake-ip")
            mocked_request = mocker.post("http://test.com", status_code=200, json={"success": True, "score": 0.8})
            assert perform_recaptcha_validation("")
            assert mocked_request.called
            assert mocked_request.last_request.headers["true-client-ip"] == "random-fake-ip"
            assert mocked_request.last_request.body == "response=&secret=test&remoteip=random-fake-ip"