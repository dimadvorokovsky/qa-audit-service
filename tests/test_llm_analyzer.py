import json
from unittest.mock import MagicMock, patch

from agent.llm_analyzer import LLMAnalyzer


def build_agent_result():
    return {
        "issues": [
            {
                "priority": "HIGH",
                "category": "Links",
                "title": "Broken internal links",
                "description": "Found 2 broken links",
                "evidence": {
                    "broken_links_count": 2,
                    "broken_links": [
                        {
                            "url": "https://example.com/a",
                            "status_code": 404,
                        },
                        {
                            "url": "https://example.com/b",
                            "status_code": 404,
                        },
                    ],
                },
            }
        ],
        "manual_checks": [
            {
                "category": "SEO/UI",
                "title": "Check H1 requirements",
                "reason": "H1 is missing",
                "context": {
                    "h1_exists": False,
                },
            }
        ],
        "summary": "1 confirmed issue, 1 manual check",
        "bug_reports": [
            {
                "id": "BUG-001",
                "title": "Broken internal links",
            }
        ],
    }


def build_success_response():
    response = MagicMock()

    response.output_text = json.dumps(
        {
            "executive_summary": (
                "The audit found broken internal links."
            ),
            "risk_assessment": (
                "Broken navigation can affect user experience."
            ),
            "additional_manual_checks": [
                {
                    "title": "Check affected navigation",
                    "reason": (
                        "Confirm whether users can reach "
                        "the affected sections another way."
                    ),
                }
            ],
            "bug_report_improvements": [
                {
                    "issue": "Broken internal links",
                    "suggestion": (
                        "Add affected URLs and status codes "
                        "to the bug report."
                    ),
                }
            ],
            "confidence_notes": [
                "Broken links are supported by deterministic evidence."
            ],
        },
        ensure_ascii=False,
    )

    return response


def test_llm_analyzer_returns_unavailable_without_configuration(
    monkeypatch,
):
    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False,
    )
    monkeypatch.delenv(
        "OPENAI_MODEL",
        raising=False,
    )

    analyzer = LLMAnalyzer()

    result = analyzer.analyze(
        url="https://example.com",
        agent_result=build_agent_result(),
    )

    assert result["status"] == "unavailable"


@patch("agent.llm_analyzer.OpenAI")
def test_llm_analyzer_returns_success_for_valid_json(
    mock_openai,
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )
    monkeypatch.setenv(
        "OPENAI_MODEL",
        "test-model",
    )

    mock_client = MagicMock()
    mock_client.responses.create.return_value = (
        build_success_response()
    )
    mock_openai.return_value = mock_client

    analyzer = LLMAnalyzer()

    result = analyzer.analyze(
        url="https://example.com",
        agent_result=build_agent_result(),
    )

    assert result["status"] == "success"
    assert (
        result["analysis"]["executive_summary"]
        == "The audit found broken internal links."
    )


@patch("agent.llm_analyzer.OpenAI")
def test_llm_analyzer_returns_error_for_invalid_json(
    mock_openai,
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )
    monkeypatch.setenv(
        "OPENAI_MODEL",
        "test-model",
    )

    mock_response = MagicMock()
    mock_response.output_text = (
        "This is not valid JSON"
    )

    mock_client = MagicMock()
    mock_client.responses.create.return_value = (
        mock_response
    )
    mock_openai.return_value = mock_client

    analyzer = LLMAnalyzer()

    result = analyzer.analyze(
        url="https://example.com",
        agent_result=build_agent_result(),
    )

    assert result["status"] == "error"
    assert result["reason"] == "LLM returned invalid JSON"


@patch("agent.llm_analyzer.OpenAI")
def test_llm_analyzer_returns_error_when_api_fails(
    mock_openai,
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )
    monkeypatch.setenv(
        "OPENAI_MODEL",
        "test-model",
    )

    mock_client = MagicMock()
    mock_client.responses.create.side_effect = (
        RuntimeError("API unavailable")
    )
    mock_openai.return_value = mock_client

    analyzer = LLMAnalyzer()

    result = analyzer.analyze(
        url="https://example.com",
        agent_result=build_agent_result(),
    )

    assert result["status"] == "error"
    assert "API unavailable" in result["reason"]