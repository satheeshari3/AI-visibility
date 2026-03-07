"""Service for generating category-related prompts for ChatGPT."""

# Prompt templates - each uses {category} placeholder
PROMPT_TEMPLATES: list[str] = [
    "best {category}",
    "top {category}",
    "best free {category}",
    "free online {category}",
    "best {category} online",
    "websites for {category}",
    "tools for {category}",
    "best {category} tools",
    "best {category} 2024",
    "best {category} 2025",
    "tools like {category}",
    "alternatives to {category}",
    "best {category} software",
    "online {category} tools",
    "free {category} tools",
    "best {category} for [use case]",
    "what are the best {category}",
    "recommend {category}",
    "popular {category}",
    "{category} comparison",
    "best {category} for beginners",
    "best {category} for professionals",
    "free {category} no sign up",
    "best {category} reddit",
    "{category} recommendations",
    "which {category} is best",
    "best {category} free",
    "top 10 {category}",
    "best {category} apps",
    "{category} apps",
    "best {category} services",
    "reliable {category}",
    "trusted {category}",
    "best {category} alternatives",
    "{category} tools online",
    "best web based {category}",
    "cloud {category}",
    "best {category} for work",
    "best {category} for students",
    "best {category} for business",
    "best {category} for personal use",
    "{category} software recommendations",
    "best {category} websites",
    "free {category} websites",
    "best {category} free online",
    "simple {category}",
    "easy {category}",
    "best paid {category}",
    "premium {category} tools",
]

MIN_PROMPTS = 20
MAX_PROMPTS = 50


def generate_prompts(category: str, count: int | None = None) -> list[str]:
    """Generate prompts related to the given category.

    Args:
        category: The product or service category (e.g., "pdf editor")
        count: Desired number of prompts (20-50). If None, uses all available.

    Returns:
        List of unique prompts for the category
    """
    category = category.strip()
    if not category:
        return []

    # Use templates with category filled in
    prompts: list[str] = []
    seen: set[str] = set()

    for template in PROMPT_TEMPLATES:
        prompt = template.format(category=category).strip()
        # Deduplicate (templates may produce same result)
        prompt_lower = prompt.lower()
        if prompt_lower not in seen:
            seen.add(prompt_lower)
            prompts.append(prompt)

    # Trim to requested count
    target = count if count is not None else len(prompts)
    target = max(MIN_PROMPTS, min(MAX_PROMPTS, target, len(prompts)))

    return prompts[:target]
