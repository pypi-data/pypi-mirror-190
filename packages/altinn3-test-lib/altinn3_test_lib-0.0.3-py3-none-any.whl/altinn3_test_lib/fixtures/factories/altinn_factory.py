import pytest
from ssb_altinn3_util.models.altinn3_cloud_event import Altinn3CloudEvent


@pytest.fixture(scope="function")
def altinn_event_factory():
    def create_test_event(
            alternative_subject: str = "subject",
            event_id: str = "123",
            event_type: str = "test_event",
            subject: str = "test_subject",
            source: str = "test_app",
            time: str = "2022-01-01"
    ) -> Altinn3CloudEvent:
        """Creates an event"""
        event = Altinn3CloudEvent(
            alternativesubject=alternative_subject,
            id=event_id,
            source=source,
            specversion="1.0",
            subject=subject,
            time=time,
            type=event_type,
        )
        return event
    return create_test_event
