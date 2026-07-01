import json
import time

from google import genai

from app.core.config import settings


class LLMCategorizer:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL
        self.max_retries = 3

    def categorize_merchants(
            self,
            merchants: list[str]
    ) -> dict[str, str]:

        prompt = f"""
    You are a financial transaction classifier.

    Classify each merchant into ONE category.

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

        for attempt in range(1, self.max_retries + 1):

            try:

                print(
                    f"\nGemini Categorization "
                    f"(Attempt {attempt}/{self.max_retries})"
                )

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

                data = json.loads(text)

                print("\nMerchant Categories")
                print(data)

                return data

            except Exception as e:

                print(f"\nGemini Error (Attempt {attempt})")
                print(e)

                if attempt < self.max_retries:
                    wait = 2 ** attempt

                    print(f"Retrying in {wait} seconds...\n")

                    time.sleep(wait)

        print("\nGemini unavailable after retries.")

        return {}