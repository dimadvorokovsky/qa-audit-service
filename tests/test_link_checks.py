from checks.link_checks import (
    get_internal_links,
    check_link,
    check_page_links,
)


def test_get_internal_links_returns_only_internal_links():
    links = get_internal_links("https://www.python.org")

    assert all(
        link.startswith("https://www.python.org")
        for link in links
    )


def test_check_link_returns_200_for_available_link():
    result = check_link("https://example.com")

    assert result["status_code"] == 200
    assert result["is_broken"] is False


def test_check_link_marks_invalid_link_as_broken():
    result = check_link(
        "https://this-site-does-not-exist-123456789.com"
    )

    assert result["is_broken"] is True


def test_check_page_links_checks_no_more_than_20_links():
    results = check_page_links("https://www.python.org")

    assert len(results) <= 20