from app.services.ai.llm_categorizer import LLMCategorizer

llm = LLMCategorizer()

category, failed = llm.categorize(
    merchant="Swiggy",
    notes="Dinner with friends",
    current_category="Other",
)

print(category)
print(failed)