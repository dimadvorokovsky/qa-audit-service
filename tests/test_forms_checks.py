import pytest

from checks.forms_checks import get_forms


@pytest.mark.integration
def test_get_forms_returns_list():
    result = get_forms("https://www.python.org")

    assert isinstance(result, list)


@pytest.mark.integration
def test_python_org_has_at_least_one_form():
    result = get_forms("https://www.python.org")

    assert len(result) >= 1


@pytest.mark.integration
def test_form_contains_required_keys():
    result = get_forms("https://www.python.org")

    first_form = result[0]

    assert "form_number" in first_form
    assert "action" in first_form
    assert "method" in first_form
    assert "fields" in first_form
    assert "submit_buttons" in first_form


@pytest.mark.integration
def test_python_org_first_form_uses_get_method():
    result = get_forms("https://www.python.org")

    assert result[0]["method"] == "GET"


@pytest.mark.integration
def test_python_org_form_contains_search_field():
    result = get_forms("https://www.python.org")

    fields = result[0]["fields"]

    assert any(
        field["type"] == "search"
        for field in fields
    )