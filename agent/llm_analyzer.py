import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL")

    def is_available(self) -> bool:
        return bool(self.api_key and self.model)

    def analyze(
        self,
        url: str,
        agent_result: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.is_available():
            return {
                "status": "unavailable",
                "reason": (
                    "OPENAI_API_KEY or OPENAI_MODEL "
                    "is not configured"
                ),
            }

        deterministic_payload = {
            "url": url,
            "confirmed_issues": agent_result.get(
                "issues",
                [],
            ),
            "manual_checks": agent_result.get(
                "manual_checks",
                [],
            ),
            "qa_summary": agent_result.get(
                "summary",
                "",
            ),
            "bug_reports": agent_result.get(
                "bug_reports",
                [],
            ),
        }

        instructions = """
You are an experienced QA engineer assisting an automated QA audit system.

You receive structured findings that were already produced by deterministic
checks.

Important rules:

1. Never invent technical facts.
2. Never convert an unconfirmed manual check into a confirmed defect.
3. Never remove or silently change confirmed issues.
4. Never change HTTP status codes, URLs, counts or other evidence.
5. Treat confirmed_issues as factual evidence.
6. Treat manual_checks as items that still require human verification.
7. Your job is interpretation, risk analysis and exploratory QA suggestions.
8. Keep deterministic findings separate from your own recommendations.
9. Do not claim that an issue was reproduced unless the deterministic
   findings explicitly confirm it.
10. Return only JSON and no Markdown.

Return JSON with exactly this structure:

{
  "executive_summary": "string",
  "risk_assessment": "string",
  "additional_manual_checks": [
    {
      "title": "string",
      "reason": "string"
    }
  ],
  "bug_report_improvements": [
    {
      "issue": "string",
      "suggestion": "string"
    }
  ],
  "confidence_notes": [
    "string"
  ]
}
"""

        user_input = (
            "Analyze this deterministic QA result:\n\n"
            + json.dumps(
                deterministic_payload,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        try:
            client = OpenAI(
                api_key=self.api_key,
            )

            response = client.responses.create(
                model=self.model,
                instructions=instructions,
                input=user_input,
            )

            raw_text = response.output_text

            result = json.loads(raw_text)

            return {
                "status": "success",
                "analysis": result,
            }

        except json.JSONDecodeError:
            return {
                "status": "error",
                "reason": "LLM returned invalid JSON",
            }

        except Exception as error:
            return {
                "status": "error",
                "reason": str(error),
            }