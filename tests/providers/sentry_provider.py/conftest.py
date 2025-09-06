from unittest.mock import MagicMock, patch

import pytest

from event_tracker.providers.sentry_provider import (
    SentryConfig,
    SentryProvider,
)


@pytest.fixture()
def set_tag_mock():
    with patch("sentry_sdk.set_tag", new_callable=MagicMock) as set_tag_mock:
        yield set_tag_mock


@pytest.fixture()
def set_context_mock():
    with patch("sentry_sdk.set_context", new_callable=MagicMock) as set_context_mock:
        yield set_context_mock


@pytest.fixture()
def capture_message_mock():
    with patch("sentry_sdk.capture_message", new_callable=MagicMock) as context_mock:
        yield context_mock


@pytest.fixture()
def capture_exception_mock():
    with patch(
        "sentry_sdk.capture_exception", new_callable=MagicMock
    ) as capture_exception_mock:
        yield capture_exception_mock


@pytest.fixture()
def init_sentry_mock():
    with patch("sentry_sdk.init", new_callable=MagicMock) as init_sentry_mock:
        yield init_sentry_mock


@pytest.fixture()
def sentry_provider(init_sentry_mock):
    return SentryProvider(SentryConfig(dsn="test_dsn", environment="test_env"))
