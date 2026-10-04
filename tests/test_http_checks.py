import pytest

from checks.http_checks import (
    check_url,
    get_performance_status
)


@pytest.mark.integration
def test_example_com_returns_200():
    result = check_url("https://example.com")

    assert result["status_code"] == 200


@pytest.mark.integration
def test_example_com_is_available():
    result = check_url("https://example.com")

    assert result["is_available"] is True


@pytest.mark.integration
def test_invalid_domain_is_unavailable():
    result = check_url(
        "https://this-domain-does-not-exist-123456789.com"
    )

    assert result["is_available"] is False


def test_performance_status_pass():
    result = get_performance_status(0.5)

    assert result == "PASS"


def test_performance_status_warn():
    result = get_performance_status(2.0)

    assert result == "WARN"


def test_performance_status_fail():
    result = get_performance_status(4.0)

    assert result == "FAIL"