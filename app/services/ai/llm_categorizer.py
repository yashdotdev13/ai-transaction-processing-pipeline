import json

from google import genai

from app.core.config import settings


class LLMCategorizer:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def categorize_merchants(
        self,
        merchants: list[str],
    ) -> dict[str, str]:

        if not merchants:
            return {}

        prompt = f"""
You are a financial transaction classifier.

For every merchant below, return ONLY one category.

Allowed categories:

Food
Travel
Shopping
Bills
Entertainment
Healthcare
Investment
Transfer
Utilities
Salary
Other

Return ONLY valid JSON.

Example:

{{
    "Amazon":"Shopping",
    "Swiggy":"Food",
    "IRCTC":"Travel"
}}

Merchants:

{json.dumps(merchants, indent=2)}
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "", 1)

            if text.startswith("```"):
                text = text.replace("```", "", 1)

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            merchant_map = json.loads(text)

            return merchant_map

        except Exception as e:

            print("\n========== GEMINI ERROR ==========")
            print(e)
            print("=================================\n")

            return {merchant: "Other" for merchant in merchants}