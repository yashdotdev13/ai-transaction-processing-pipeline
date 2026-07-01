from enum import Enum


class Category(str, Enum):
    FOOD = "Food"
    SHOPPING = "Shopping"
    TRAVEL = "Travel"
    TRANSPORT = "Transport"
    UTILITIES = "Utilities"
    CASH_WITHDRAWAL = "Cash Withdrawal"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"
    UNCATEGORIZED = "Uncategorized"