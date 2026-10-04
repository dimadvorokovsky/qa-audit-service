import pytest

from checks.link_checks import (
    check_link,
    check_page_links,
    get_internal_links,
    normalize_url
)


@pytest.mark.integration
def test_get_internal_links_returns_only_internal_links():
    links = get_internal_links("https://www.python.org")

    assert all(
        link.startswith("https://www.python.org")
        for link in links
    )


@pytest.mark.integration
def test_check_link_returns_200_for_example():
    result = check_link("https://example.com")

    assert result["status_code"] == 200
    assert result["is_broken"] is False


@pytest.mark.integration
def test_invalid_domain_is_marked_as_broken():
    result = check_link(
        "https://this-domain-does-not-exist-123456789.com"
    )

    assert result["is_broken"] is True


@pytest.mark.integration
def test_check_page_links_returns_max_20_links():
    results = check_page_links("https://www.python.org")

    assert len(results) <= 20


def test_normalize_root_url_removes_trailing_slash():
    result = normalize_url("https://www.python.org/")

    assert result == "https://www.python.org"


def test_normalize_path_removes_trailing_slash():
    result = normalize_url(
        "https://www.python.org/about/"
    )

    assert result == "https://www.python.org/about"


def test_normalize_domain_converts_to_lowercase():
    result = normalize_url(
        "HTTPS://WWW.PYTHON.ORG/about/"
    )

    assert result == "https://www.python.org/about"


def test_normalize_url_removes_fragment():
    result = normalize_url(
        "https://www.python.org/about/#history"
    )

    assert result == "https://www.python.org/about"


def test_normalize_url_keeps_query_parameters():
    result = normalize_url(
        "https://www.python.org/search/?q=selenium"
    )

    assert result == (
        "https://www.python.org/search?q=selenium"
    )