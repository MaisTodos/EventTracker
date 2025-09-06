


def test_track_when_string_event(): ...


def test_track_when_exception_event(): ...


def test_track_when_all_infos(): ...


def test_track_when_already_infos_set_and_new_infos(logger_provider):
    logger_provider.set_contexts({"session": {"id": "abcd"}})
    logger_provider.set_tags({"user": "jane.doe"})

    logger_provider.track(
        "test_message",
        tags={"new": "tag"},
        contexts={"new": {"info": "value"}},
    )
