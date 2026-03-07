"""Orchestrates the full analysis pipeline: prompts, ChatGPT, mention detection, scoring."""

from app.models.analysis_models import AnalysisRequest, AnalysisResponse, PromptResult, Suggestion
from app.services.prompt_generator import generate_prompts
from app.services.chatgpt_client import ChatGPTClient
from app.services.scoring_service import (
    calculate_visibility_score,
    build_prompt_results,
)
from app.services.suggestion_service import generate_suggestions
from app.utils.mention_detector import detect_mention


class AnalysisService:
    """Runs the end-to-end visibility analysis."""

    def __init__(self, chatgpt_client: ChatGPTClient | None = None) -> None:
        self._client = chatgpt_client or ChatGPTClient()

    async def run_analysis(self, request: AnalysisRequest) -> AnalysisResponse:
        """Execute full analysis: generate prompts, call ChatGPT, detect mentions, score.

        Args:
            request: Analysis request with website and category

        Returns:
            Structured analysis response
        """
        website = request.website.strip()
        category = request.category.strip()

        prompts = generate_prompts(category)
        if not prompts:
            return AnalysisResponse(
                website=website,
                category=category,
                visibility_score=0.0,
                prompts_tested=0,
                mentions_found=0,
                mention_rate=0.0,
                prompt_results=[],
                suggestions=[],
            )

        mentioned_indices: set[int] = set()
        for i, prompt in enumerate(prompts):
            response_text = await self._client.complete(prompt)
            if detect_mention(response_text, website):
                mentioned_indices.add(i)

        mentions_found = len(mentioned_indices)
        prompts_tested = len(prompts)
        visibility_score, mention_rate = calculate_visibility_score(
            mentions_found, prompts_tested
        )
        prompt_results = build_prompt_results(prompts, mentioned_indices)
        raw_suggestions = generate_suggestions(
            prompt_results, category, visibility_score
        )
        suggestions = [Suggestion(**s) for s in raw_suggestions]

        return AnalysisResponse(
            website=website,
            category=category,
            visibility_score=visibility_score,
            prompts_tested=prompts_tested,
            mentions_found=mentions_found,
            mention_rate=mention_rate,
            prompt_results=prompt_results,
            suggestions=suggestions,
        )
