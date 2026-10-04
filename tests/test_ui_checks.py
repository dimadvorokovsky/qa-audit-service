from checks.ui_checks import check_page_title


def test_page_title_exists():
    url = "data:text/html,<html><head><title>Python Test</title></head><body></body></html>"

    result = check_page_title(url)

    assert result["title_exists"] is True


def test_page_title_contains_python():
    url = "data:text/html,<html><head><title>Python Test</title></head><body></body></html>"

    result = check_page_title(url)

    assert "Python" in result["title"]