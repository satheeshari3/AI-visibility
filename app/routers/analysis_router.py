"""HTTP router for the analysis endpoint."""

from fastapi import APIRouter, HTTPException

from app.models.analysis_models import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["analysis"])
_analysis_service: AnalysisService | None = None


def get_analysis_service() -> AnalysisService:
    """Lazy-initialize and return the analysis service."""
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service


@router.post("", response_model=AnalysisResponse)
async def analyse(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze AI visibility for a website in a given category.

    Accepts website URL/domain and category, runs prompts against ChatGPT,
    detects mentions, and returns visibility score and detailed results.
    """
    if not request.website or not request.category:
        raise HTTPException(
            status_code=400,
            detail="Both 'website' and 'category' are required",
        )
    try:
        service = get_analysis_service()
    except ValueError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    return await service.run_analysis(request)
