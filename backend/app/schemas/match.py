from pydantic import BaseModel, Field

from app.schemas.job import JobRead


class MatchScoreBreakdown(BaseModel):
    skills_overlap: float = Field(ge=0.0, le=1.0)
    title_similarity: float = Field(ge=0.0, le=1.0)
    location_fit: float = Field(ge=0.0, le=1.0)


class MatchJustificationSchema(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    evidence: dict[str, str]


class MatchJustificationScaffold(BaseModel):
    prompt_template: str
    expected_response_schema: MatchJustificationSchema


class RankedJobMatch(BaseModel):
    rank: int
    total_score: float = Field(ge=0.0, le=1.0)
    score_breakdown: MatchScoreBreakdown
    matched_skills: list[str]
    job: JobRead
    justification_scaffold: MatchJustificationScaffold | None = None


class MatchListResponse(BaseModel):
    resume_id: int
    total_jobs_evaluated: int
    results: list[RankedJobMatch]
