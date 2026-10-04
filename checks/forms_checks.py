import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_forms(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    forms = []

    for index, form in enumerate(soup.find_all("form"), start=1):
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
                    "value": button.get("value", "")
                })

        forms.append({
            "form_number": index,
            "action": full_action,
            "method": method,
            "fields": fields,
            "submit_buttons": submit_buttons
        })

    return forms