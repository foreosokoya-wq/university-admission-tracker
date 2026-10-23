import re

RULES = {
    "direct_entry": [
        "direct entry",
        "alevel"
    ],
    "admission_list": [
        "admission list",
        "list of admitted candidates",
        "provisional admission",
        "offer of admission",
    ],
    "deadline": [
        "deadline",
        "closing date",
        "last date",
        "extension of deadline",
        "application closes",
    ],
    "screening": [
        "screening",
        "verification of credentials",
        "document upload",
    ],
    "application": [
        "post utme",
        "admission form",
        "admission application",
        "application for admission",
        "registration",
    ],
    "fees": [
        "schedule of fees",
        "schedule of fee payment",
        "acceptance fee",
        "acceptance fees",
        "school fees",
        "payment of fees",
        "tuition fees",
    ],
    "resumption": [
        "resumption",
        "commencement of lectures",
    ],
    }

def normalize_title(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()

def classify_announcement(item):
    title = item.get("title", "")
    normalized_title = normalize_title(title)

    matched_categories = []
    matched_keywords = []

    for category, keywords in RULES.items():
        for keyword in keywords:
            if keyword in normalized_title:
                matched_categories.append(category)
                matched_keywords.append(keyword)

    if matched_categories:
        primary_category = matched_categories[0]

        if primary_category == "resumption":
            relevance = "medium"

        else:
            relevance = "high"

        reason = (
            "Matched title keywords: "
            + ", ".join(matched_keywords)
        )

    else:
        primary_category = "needs review"
        relevance = "uncertain"
        reason = "No configured keywords match the title."

    return {
        **item,
        "category": primary_category,
        "matched_category": matched_categories,
        "relevance": relevance,
        "reason": reason
    }

