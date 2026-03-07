"""Service for generating AI visibility suggestions based on prompt results."""

from app.models.analysis_models import PromptResult

# Modifiers that tend to help AI recognition, with short tips
MODIFIER_TIPS: list[tuple[str, str]] = [
    ("free", "AI often recommends free options when users ask"),
    ("online", "AI recognises web-based tools with this keyword"),
    ("best", "Comparison queries like 'best X' are common in AI recommendations"),
    ("for beginners", "User-intent phrases help AI surface you"),
    ("2025", "Current year adds freshness and improves AI visibility"),
    ("no sign up", "Low-friction tools are favoured by AI"),
    ("recommendations", "AI responds well to recommendation-style queries"),
]


def generate_suggestions(
    prompt_results: list[PromptResult],
    category: str,
    visibility_score: float,
) -> list[dict]:
    """Generate actionable suggestions to improve AI visibility.

    Args:
        prompt_results: Results for each prompt tested
        category: The product category used
        visibility_score: Current visibility score (0-100)

    Returns:
        List of suggestion dicts with 'type' and 'suggestion' keys
    """
    suggestions: list[dict] = []

    mentioned = [p for p in prompt_results if p.mentioned]
    not_mentioned = [p for p in prompt_results if not p.mentioned]

    # 1. Keyword swap: what worked vs what didn't
    if mentioned and not_mentioned:
        best = mentioned[0].prompt
        weak = not_mentioned[0].prompt
        suggestions.append({
            "type": "keyword_swap",
            "suggestion": f"Change '{weak}' into '{best}' - AI recognised you better with this phrasing.",
        })

    # 2. Modifiers that worked (keep using these)
    worked_mods: set[str] = set()
    for pr in mentioned:
        for mod, _ in MODIFIER_TIPS:
            if mod in pr.prompt.lower():
                worked_mods.add(mod)
    for mod, tip in MODIFIER_TIPS:
        if mod in worked_mods:
            suggestions.append({
                "type": "keep_keyword",
                "suggestion": f"Keep using '{mod}': {tip}",
            })

    # 3. Modifiers to add (limit to top 3 that didn't appear in mentioned)
    add_count = 0
    for mod, tip in MODIFIER_TIPS:
        if mod in worked_mods or add_count >= 3:
            continue
        suggestions.append({
            "type": "add_keyword",
            "suggestion": f"Use this type of keyword: add '{mod}' (e.g. '{mod} {category}'). {tip}",
        })
        add_count += 1

    # 4. General tips for low visibility
    if visibility_score < 50:
        suggestions.append({
            "type": "general_tip",
            "suggestion": "Use more specific keywords. AI recognises phrases like 'free online pdf editor for students' better than 'pdf editor'.",
        })
        suggestions.append({
            "type": "general_tip",
            "suggestion": "Target long-tail queries with modifiers like 'best', 'free', 'online' - these help AI understand and recommend you.",
        })

    # Deduplicate and limit
    seen: set[str] = set()
    unique: list[dict] = []
    for s in suggestions:
        t = s["suggestion"]
        if t not in seen:
            seen.add(t)
            unique.append(s)

    return unique[:12]
