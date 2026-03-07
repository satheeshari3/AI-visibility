"""Pydantic models for analysis requests and responses."""

from pydantic import BaseModel, Field


class Suggestion(BaseModel):
    """A single suggestion for improving AI visibility."""

    type: str = Field(
        ...,
        description="Suggestion type: keyword_swap, add_keyword, keep_keyword, general_tip",
    )
    suggestion: str = Field(..., description="Actionable suggestion text")


class AnalysisRequest(BaseModel):
    """Request body for the analysis endpoint."""

    website: str = Field(..., description="Target website URL or domain to analyze")
    category: str = Field(..., description="Product/service category for prompt generation")


class PromptResult(BaseModel):
    """Result for a single prompt tested against ChatGPT."""

    prompt: str = Field(..., description="The prompt that was sent to ChatGPT")
    mentioned: bool = Field(..., description="Whether the website was mentioned in the response")


class AnalysisResponse(BaseModel):
    """Response body for the analysis endpoint."""

    website: str = Field(..., description="The analyzed website")
    category: str = Field(..., description="The product category used")
    visibility_score: float = Field(..., description="AI visibility score (0-100)")
    prompts_tested: int = Field(..., description="Total number of prompts tested")
    mentions_found: int = Field(..., description="Number of prompts where website was mentioned")
    mention_rate: float = Field(..., description="Mention rate as decimal (0.0-1.0)")
    prompt_results: list[PromptResult] = Field(
        ...,
        description="Detailed results for each prompt",
    )
    suggestions: list[Suggestion] = Field(
        default_factory=list,
        description="Suggestions to improve AI visibility (keyword swaps, tips)",
    )
