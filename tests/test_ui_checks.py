from urllib.parse import quote

from checks.ui_checks import check_page_title


def build_data_url(title="Python Test", h1="Python QA Audit"):
    html = (
        "<html>"
        "<head>"
        '<meta charset="utf-8">'
        f"<title>{title}</title>"
        "</head>"
        "<body>"
        f"<h1>{h1}</h1>"
        "</body>"
        "</html>"
    )

    return "data:text/html;charset=utf-8," + quote(html)


def test_page_title_exists():
    url = build_data_url()

    result = check_page_title(url)

    assert result["title_exists"] is True


def test_page_title_contains_python():
    url = build_data_url()

    result = check_page_title(url)

    assert "Python" in result["title"]


def test_h1_exists():
    url = build_data_url()

    result = check_page_title(url)

    assert result["h1_exists"] is True


def test_h1_text():
    url = build_data_url(h1="Главный заголовок")

    result = check_page_title(url)

    assert result["h1_text"] == "Главный заголовок"


def test_missing_h1_returns_warn():
    html = (
        "<html>"
        "<head>"
        '<meta charset="utf-8">'
        "<title>Python Test</title>"
        "</head>"
        "<body>"
        "<p>No heading</p>"
        "</body>"
        "</html>"
    )

    url = "data:text/html;charset=utf-8," + quote(html)

    result = check_page_title(url)

    assert result["ui_status"] == "WARN"