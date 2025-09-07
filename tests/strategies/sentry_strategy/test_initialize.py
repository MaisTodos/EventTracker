import pytest

from event_tracker.strategies.sentry_strategy import (
    SentryConfig,
    SentryStrategy,
)


def test_sentry_provider_init_with_tracing(init_sentry_mock):
    SentryStrategy(
        SentryConfig(
            dsn="blah",
            environment="testing",
            traces_sample_rate=0.5,
        )
    )

    log_integration = init_sentry_mock.call_args[1]["integrations"][0]
    init_sentry_mock.assert_called_once_with(
        dsn="blah",
        integrations=[log_integration],
        environment="testing",
        traces_sample_rate=0.5,
        enable_tracing=True,
    )


@pytest.mark.parametrize("traces_sample_rate", [0, -0.1, None])
def test_sentry_provider_init_without_tracing(traces_sample_rate, init_sentry_mock):
    SentryStrategy(
        SentryConfig(
            dsn="blah",
            environment="testing",
            traces_sample_rate=traces_sample_rate,
        )
    )

    log_integration = init_sentry_mock.call_args[1]["integrations"][0]
    init_sentry_mock.assert_called_once_with(
        dsn="blah",
        integrations=[log_integration],
        environment="testing",
        traces_sample_rate=traces_sample_rate,
        enable_tracing=False,
    )
