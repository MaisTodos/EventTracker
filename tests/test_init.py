from event_tracker import EventTracker


def test_init_sentry_without_tracing(set_init_sentry_mock):
    EventTracker.init(
        environment="production",
        sentry_dsn="SENTRY_DSN",
        sentry_trace_sample_rate=0,
    )

    sentry_integrations = set_init_sentry_mock.call_args[1]["integrations"]
    set_init_sentry_mock.assert_called_once_with(
        dsn="SENTRY_DSN",
        environment="production",
        integrations=sentry_integrations,
        enable_tracing=False,
    )


def test_init_sentry_with_tracing(set_init_sentry_mock):
    EventTracker.init(
        environment="production",
        sentry_dsn="SENTRY_DSN",
        sentry_trace_sample_rate=0.5,
    )

    sentry_integrations = set_init_sentry_mock.call_args[1]["integrations"]
    set_init_sentry_mock.assert_called_once_with(
        dsn="SENTRY_DSN",
        environment="production",
        integrations=sentry_integrations,
        traces_sample_rate=0.5,
        enable_tracing=True,
    )
