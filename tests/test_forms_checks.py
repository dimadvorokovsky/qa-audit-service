from checks.forms_checks import get_forms


def test_get_forms_returns_list():
    forms = get_forms("https://www.python.org")

    assert isinstance(forms, list)


def test_python_org_has_at_least_one_form():
    forms = get_forms("https://www.python.org")

    assert len(forms) >= 1


def test_form_contains_required_keys():
    forms = get_forms("https://www.python.org")
    form = forms[0]

    assert "form_number" in form
    assert "action" in form
    assert "method" in form
    assert "fields" in form
    assert "submit_buttons" in form


def test_python_org_search_form_uses_get_method():
    forms = get_forms("https://www.python.org")
    form = forms[0]

    assert form["method"] == "GET"


def test_python_org_search_form_has_search_field():
    forms = get_forms("https://www.python.org")
    form = forms[0]

    assert any(
        field["type"] == "search"
        for field in form["fields"]
    )