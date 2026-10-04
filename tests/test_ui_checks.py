from urllib.parse import quote

from checks.ui_checks import check_page_title


def build_data_url(
    title="Python Test",
    h1="Python QA Audit",
    include_link=True,
    include_button=True,
    images=None
):
    body = f"<h1>{h1}</h1>"

    if include_link:
        body += '<a href="https://example.com">Example link</a>'

    if include_button:
        body += "<button>Submit</button>"

    if images:
        for image in images:
            src = image.get("src", "")
            alt = image.get("alt")

            if alt is None:
                body += f'<img src="{src}">'
            else:
                body += f'<img src="{src}" alt="{alt}">'

    html = (
        "<html>"
        "<head>"
        '<meta charset="utf-8">'
        f"<title>{title}</title>"
        "</head>"
        f"<body>{body}</body>"
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
        '<a href="https://example.com">Example link</a>'
        "<button>Submit</button>"
        "</body>"
        "</html>"
    )

    url = "data:text/html;charset=utf-8," + quote(html)

    result = check_page_title(url)

    assert result["ui_status"] == "WARN"


def test_links_exist():
    url = build_data_url()

    result = check_page_title(url)

    assert result["links_exist"] is True


def test_links_count():
    url = build_data_url()

    result = check_page_title(url)

    assert result["links_count"] == 1


def test_buttons_exist():
    url = build_data_url()

    result = check_page_title(url)

    assert result["buttons_exist"] is True


def test_buttons_count():
    url = build_data_url()

    result = check_page_title(url)

    assert result["buttons_count"] == 1


def test_missing_link_returns_false():
    url = build_data_url(include_link=False)

    result = check_page_title(url)

    assert result["links_exist"] is False


def test_missing_button_returns_false():
    url = build_data_url(include_button=False)

    result = check_page_title(url)

    assert result["buttons_exist"] is False


def test_images_count():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg",
                "alt": "Image one"
            },
            {
                "src": "https://example.com/image2.jpg",
                "alt": "Image two"
            }
        ]
    )

    result = check_page_title(url)

    assert result["images_count"] == 2


def test_images_with_alt_count():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg",
                "alt": "Image one"
            },
            {
                "src": "https://example.com/image2.jpg",
                "alt": "Image two"
            }
        ]
    )

    result = check_page_title(url)

    assert result["images_with_alt_count"] == 2


def test_image_without_alt_detected():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg",
                "alt": "Image one"
            },
            {
                "src": "https://example.com/image2.jpg"
            }
        ]
    )

    result = check_page_title(url)

    assert result["images_without_alt_count"] == 1


def test_image_without_alt_is_added_to_problem_list():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg"
            }
        ]
    )

    result = check_page_title(url)

    assert len(result["images_without_alt"]) == 1


def test_image_without_alt_returns_warn():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg"
            }
        ]
    )

    result = check_page_title(url)

    assert result["ui_status"] == "WARN"


def test_all_images_with_alt_keep_pass_status():
    url = build_data_url(
        images=[
            {
                "src": "https://example.com/image1.jpg",
                "alt": "Image one"
            }
        ]
    )

    result = check_page_title(url)

    assert result["ui_status"] == "PASS"