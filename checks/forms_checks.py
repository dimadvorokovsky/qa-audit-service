import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def _normalize_field(field_info):
    return (
        field_info["tag"],
        field_info["type"],
        field_info["name"],
        field_info["required"],
    )


def _build_form_signature(method, action, fields):
    normalized_fields = tuple(
        sorted(_normalize_field(field) for field in fields)
    )

    return (
        method,
        action,
        normalized_fields,
    )


def get_forms(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    grouped_forms = {}

    for form in soup.find_all("form"):
        action = form.get("action", "")
        method = form.get("method", "get").upper()

        full_action = urljoin(url, action) if action else url

        fields = []

        for field in form.find_all(["input", "textarea", "select"]):
            field_info = {
                "tag": field.name,
                "type": field.get("type", ""),
                "name": field.get("name", ""),
                "required": field.has_attr("required"),
            }

            fields.append(field_info)

        submit_buttons = []

        for button in form.find_all(["button", "input"]):
            button_type = button.get("type", "").lower()

            if button_type == "submit":
                submit_buttons.append({
                    "tag": button.name,
                    "text": button.get_text(strip=True),
                    "value": button.get("value", ""),
                })

        signature = _build_form_signature(
            method=method,
            action=full_action,
            fields=fields,
        )

        if signature not in grouped_forms:
            grouped_forms[signature] = {
                "form_number": len(grouped_forms) + 1,
                "action": full_action,
                "method": method,
                "fields": fields,
                "submit_buttons": submit_buttons,
                "instances": 1,
            }
        else:
            grouped_forms[signature]["instances"] += 1

    return list(grouped_forms.values())