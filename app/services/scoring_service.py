"""Service for calculating AI visibility score."""

from app.models.analysis_models import PromptResult


def calculate_visibility_score(
    mentions_found: int,
    prompts_tested: int,
) -> tuple[float, float]:
    """Calculate visibility score and mention rate.

    Args:
        mentions_found: Number of prompts where website was mentioned
        prompts_tested: Total number of prompts tested

    Returns:
        Tuple of (visibility_score 0-100, mention_rate 0.0-1.0)
    """
    if prompts_tested <= 0:
        return 0.0, 0.0

    mention_rate = mentions_found / prompts_tested
    visibility_score = (mentions_found / prompts_tested) * 100

    return round(visibility_score, 2), round(mention_rate, 4)


def build_prompt_results(
    prompts: list[str],
    mentioned_indices: set[int],
) -> list[PromptResult]:
    """Build list of PromptResult from prompts and mention flags.

    Args:
        prompts: List of prompts tested
        mentioned_indices: Set of indices where website was mentioned

    Returns:
        List of PromptResult
    """
    return [
        PromptResult(prompt=prompt, mentioned=i in mentioned_indices)
        for i, prompt in enumerate(prompts)
    ]
