from .factories import InternalEmployeeAlertSubscriberFactory


def test_internal_alert_subscriber_string_representation(db):
    """Test the string representation for an InternalEmployeeAlertSubscriber."""
    internal_alert_subscriber = InternalEmployeeAlertSubscriberFactory()
    expected_string = f"Internal Employee Alerts Subscriber: {internal_alert_subscriber.first_name} {internal_alert_subscriber.last_name}"
    assert expected_string == str(internal_alert_subscriber)
