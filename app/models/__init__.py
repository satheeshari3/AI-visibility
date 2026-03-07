"""Application models."""

from app.models.analysis_models import (
    AnalysisRequest,
    AnalysisResponse,
    PromptResult,
    Suggestion,
)

__all__ = [
    "AnalysisRequest",
    "AnalysisResponse",
    "PromptResult",
    "Suggestion",
]
