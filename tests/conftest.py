from unittest.mock import MagicMock, patch

def set_tag_mock():
    set_tag_mock = MagicMock()
    patch("sentry_sdk.set_tag", set_tag_mock)
    return set_tag_mock
