from checks.http_checks import check_url, get_performance_status


def test_check_url_returns_200_for_available_site():
    result = check_url("https://example.com")

    assert result["status_code"] == 200


def test_check_url_marks_available_site_as_available():
    result = check_url("https://example.com")

    assert result["is_available"] is True


def test_check_url_marks_invalid_site_as_unavailable():
    result = check_url("https://this-site-does-not-exist-123456789.com")

    assert result["is_available"] is False


def test_performance_status_pass():
    assert get_performance_status(0.5) == "PASS"


def test_performance_status_warn():
    assert get_performance_status(2.0) == "WARN"


def test_performance_status_fail():
    assert get_performance_status(4.0) == "FAIL"