import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture()
def set_tag_mock():
    with patch("sentry_sdk.set_tag", new_callable=MagicMock) as set_tag_mock:
        yield set_tag_mock


@pytest.fixture()
def set_context_mock():
    with patch("sentry_sdk.set_context", new_callable=MagicMock) as set_context_mock:
        yield set_context_mock
