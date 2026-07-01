import json

from google import genai

from app.core.config import settings


class JobSummaryAI:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = settings.GEMINI_MODEL

    def generate(
        self,
        total_spend_inr: float,
        total_spend_usd: float,
        anomaly_count: int,
        risk_level: str,
        category_breakdown: dict,
        top_merchants: dict,
    ) -> tuple[str, bool]:

        prompt = f"""
You are a financial analyst.

Generate a professional executive summary.

Data:

Total INR Spend:
{total_spend_inr}

Total USD Spend:
{total_spend_usd}

Risk Level:
{risk_level}

Anomaly Count:
{anomaly_count}

Category Breakdown:
{json.dumps(category_breakdown, indent=2)}

Top Merchants:
{json.dumps(top_merchants, indent=2)}

Requirements:

- Maximum 120 words
- Professional tone
- Mention highest spending categories
- Mention anomaly count
- Mention risk level
- Mention total spend
- Return ONLY the summary text
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            return response.text.strip(), False

        except Exception as e:

            print("\n========== SUMMARY AI ERROR ==========")
            print(e)
            print("======================================\n")

            return (
                "AI summary generation failed.",
                True,
            )