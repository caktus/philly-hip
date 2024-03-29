from .factories import (
    CodeRedCodeBlueSubscriberFactory,
    CommunityResponseSubscriberFactory,
    DrugOverdoseSubscriberFactory,
    InternalEmployeeAlertSubscriberFactory,
    PublicHealthPreparednessSubscriberFactory,
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


def test_drug_overdose_subscriber_string_representation(db):
    """Test the string representation for an InternalEmployeeAlertSubscriber."""
    drug_subscriber = DrugOverdoseSubscriberFactory()
    expected_string = (
        f"Drug Overdose Notification Subscriber: {drug_subscriber.first_name} "
        f"{drug_subscriber.last_name}"
    )
    assert expected_string == str(drug_subscriber)


def test_codered_codeblue_subscriber_string_representation(db):
    """Test the string representation for a CodeRedCodeBlueSubscriber."""
    codered_codeblue_subscriber = CodeRedCodeBlueSubscriberFactory()
    expected_string = (
        f"Code Red/Code Blue Notification Subscriber: {codered_codeblue_subscriber.first_name} "
        f"{codered_codeblue_subscriber.last_name}"
    )
    assert expected_string == str(codered_codeblue_subscriber)


def test_public_health_preparedness_subscriber_string_representation(db):
    """Test the string representation for a PublicHealthPreparednessSubscriber."""
    php_subscriber = PublicHealthPreparednessSubscriberFactory()
    expected_string = (
        f"Public Health Preparedness Subscriber: {php_subscriber.first_name} "
        f"{php_subscriber.last_name}"
    )
    assert expected_string == str(php_subscriber)
