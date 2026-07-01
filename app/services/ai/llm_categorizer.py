import json

from google import genai

from app.core.config import settings


class LLMCategorizer:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def categorize(
        self,
        merchant: str,
        notes: str,
        current_category: str,
    ) -> tuple[str, bool]:

        prompt = f"""
You are a financial transaction classifier.

Classify the transaction into ONE category only.

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

Merchant:
{merchant}

Current Category:
{current_category}

Notes:
{notes}

Return ONLY valid JSON.

Example:

{{
    "category":"Food"
}}
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            text = response.text.strip()

            # Remove markdown code fences if Gemini returns them
            if text.startswith("```json"):
                text = text.replace("```json", "", 1)

            if text.startswith("```"):
                text = text.replace("```", "", 1)

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            print("\n========== CLEAN RESPONSE ==========")
            print(text)
            print("===================================\n")

            data = json.loads(text)

            return data["category"], False


        except Exception as e:

            print("\n========== GEMINI ERROR ==========")
            print(e)
            print("=================================\n")
            return current_category, True