from .factories import (  # isort: skip
    CommunityResponseSubscriberFactory,
    InternalEmployeeAlertSubscriberFactory,
)


def test_internal_alert_subscriber_string_representation(db):
    """Test the string representation for an InternalEmployeeAlertSubscriber."""
    internal_alert_subscriber = InternalEmployeeAlertSubscriberFactory()
    expected_string = f"Internal Employee Alerts Subscriber: {internal_alert_subscriber.first_name} {internal_alert_subscriber.last_name}"
    assert expected_string == str(internal_alert_subscriber)


def test_community_response_subscriber_string_representation(db):
    """Test the string representation for an InternalEmployeeAlertSubscriber."""
    community_response_subscriber = CommunityResponseSubscriberFactory()
    expected_string = (
        f"Community Response Network Subscriber: {community_response_subscriber.first_name} "
        f"{community_response_subscriber.last_name}"
    )
    assert expected_string == str(community_response_subscriber)
