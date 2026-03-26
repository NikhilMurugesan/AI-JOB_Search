from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchListResponse
from app.services.match_service import MatchService

router = APIRouter(prefix="/matches", tags=["matches"])


def get_match_service() -> MatchService:
    return MatchService()


@router.get("", response_model=MatchListResponse)
def get_ranked_matches(
    resume_id: int = Query(..., ge=1),
    include_justification_template: bool = Query(False),
    db: Session = Depends(get_db),
    service: MatchService = Depends(get_match_service),
):
    return service.rank_jobs_for_resume(
        db=db,
        resume_id=resume_id,
        include_justification_template=include_justification_template,
    )
