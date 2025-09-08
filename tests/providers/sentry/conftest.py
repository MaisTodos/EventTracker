from unittest.mock import Mock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_init():
    with patch("sentry_sdk.init") as mock_init:
        yield mock_init


@pytest.fixture()
def set_tag_mock():
    with patch("sentry_sdk.set_tag") as mock_set_tag:
        yield mock_set_tag


@pytest.fixture()
def set_context_mock():
    with patch("sentry_sdk.set_context") as mock_set_context:
        yield mock_set_context


@pytest.fixture()
def capture_exception_mock():
    with patch("sentry_sdk.capture_exception") as mock_capture_exception:
        yield mock_capture_exception


@pytest.fixture()
def capture_message_mock():
    with patch("sentry_sdk.capture_message") as mock_capture_message:
        yield mock_capture_message


@pytest.fixture()
def sentry_core_mock():
    return Mock()
