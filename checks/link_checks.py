from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


MAX_LINKS_TO_CHECK = 20


def get_internal_links(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    base_domain = urlparse(url).netloc
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        if not href:
            continue

        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        if parsed_url.scheme not in ("http", "https"):
            continue

        if parsed_url.netloc != base_domain:
            continue

        clean_url = full_url.split("#")[0]
        links.add(clean_url)

    return sorted(links)


def check_link(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        return {
            "url": url,
            "status_code": response.status_code,
            "is_broken": response.status_code >= 400
        }

    except requests.RequestException as error:
        return {
            "url": url,
            "status_code": None,
            "is_broken": True,
            "error": str(error)
        }


def check_page_links(url):
    links = get_internal_links(url)

    links_to_check = links[:MAX_LINKS_TO_CHECK]

    results = []

    for link in links_to_check:
        results.append(check_link(link))

    return results