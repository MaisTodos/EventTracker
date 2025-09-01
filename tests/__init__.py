from event_tracker import EventTracker


def test_set_tags(set_tag_mock):
    EventTracker.set_tags({"user": "john.doe", "blah": 123})

    import ipdb
    ipdb.set_trace()



def test_set_tags_when_none():
    ...


def test_set_tags_when_not_allowed_type_tag():
    # Should not raise error, only not call sentry. And call log
    ...


def test_set_contexts():
    ...


def test_set_contexts_when_none():
    ...


def test_set_contexts_when_not_allowed_type_context():
    # Should not raise error, only not call sentry. And call log
    ...


def test_track_when_string_event():
    ...


def test_track_when_exception_event():
    ...


def test_track_when_not_allowed_type_event():
    # Should not raise error, only not call sentry. And call log
    ...
