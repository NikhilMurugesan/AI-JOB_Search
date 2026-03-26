import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.prompts.match_justification_prompts import MATCH_JUSTIFICATION_PROMPT_TEMPLATE
from app.repositories.match_repository import MatchRepository
from app.schemas.match import (
    MatchJustificationScaffold,
    MatchJustificationSchema,
    MatchListResponse,
    MatchScoreBreakdown,
    RankedJobMatch,
)

SKILL_KEYWORDS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "sql",
    "aws",
    "gcp",
    "azure",
    "docker",
    "kubernetes",
    "fastapi",
    "django",
    "flask",
    "react",
    "node",
    "machine learning",
    "llm",
    "nlp",
    "pytorch",
    "tensorflow",
}


class MatchService:
    def __init__(self, repo: MatchRepository | None = None) -> None:
        self.repo = repo or MatchRepository()

    def rank_jobs_for_resume(
        self,
        db: Session,
        resume_id: int,
        include_justification_template: bool = False,
    ) -> MatchListResponse:
        resume = self.repo.get_resume(db, resume_id)
        if resume is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

        resume_title = (resume.target_title or resume.title).strip()
        location_preference = (resume.target_location or self._infer_location_preference(resume.raw_text) or "").strip()
        resume_skills = self._extract_skills(resume.raw_text)

        ranked: list[RankedJobMatch] = []
        jobs = self.repo.list_jobs(db)
        for job in jobs:
            job_text = f"{job.title} {job.description}"
            job_skills = self._extract_skills(job_text)
            matched_skills = sorted(resume_skills.intersection(job_skills))
            skill_score = len(matched_skills) / max(1, len(resume_skills))
            title_score = self._jaccard_similarity(resume_title, job.title)
            location_score = self._location_fit(location_preference, job.location)
            total_score = (0.5 * skill_score) + (0.35 * title_score) + (0.15 * location_score)

            scaffold = self._build_justification_scaffold() if include_justification_template else None
            ranked.append(
                RankedJobMatch(
                    rank=0,
                    total_score=round(total_score, 4),
                    score_breakdown=MatchScoreBreakdown(
                        skills_overlap=round(skill_score, 4),
                        title_similarity=round(title_score, 4),
                        location_fit=round(location_score, 4),
                    ),
                    matched_skills=matched_skills,
                    job=job,
                    justification_scaffold=scaffold,
                )
            )

        ranked.sort(key=lambda item: (-item.total_score, -item.score_breakdown.skills_overlap, item.job.id))

        for index, item in enumerate(ranked, start=1):
            item.rank = index

        return MatchListResponse(resume_id=resume_id, total_jobs_evaluated=len(jobs), results=ranked)

    def _extract_skills(self, text: str) -> set[str]:
        normalized = text.lower()
        return {skill for skill in SKILL_KEYWORDS if skill in normalized}

    def _jaccard_similarity(self, left: str, right: str) -> float:
        left_tokens = self._title_tokens(left)
        right_tokens = self._title_tokens(right)
        if not left_tokens and not right_tokens:
            return 0.0
        union = left_tokens.union(right_tokens)
        return len(left_tokens.intersection(right_tokens)) / max(1, len(union))

    def _title_tokens(self, text: str) -> set[str]:
        return {token for token in re.split(r"[^a-z0-9]+", text.lower()) if token}

    def _location_fit(self, preference: str, job_location: str) -> float:
        if not preference:
            return 0.5

        pref = preference.lower()
        location = job_location.lower()

        if "remote" in pref:
            return 1.0 if "remote" in location else 0.0
        if pref in location:
            return 1.0
        return 0.0

    def _infer_location_preference(self, raw_text: str) -> str | None:
        raw = raw_text.lower()
        if "remote" in raw:
            return "remote"
        return None

    def _build_justification_scaffold(self) -> MatchJustificationScaffold:
        return MatchJustificationScaffold(
            prompt_template=MATCH_JUSTIFICATION_PROMPT_TEMPLATE,
            expected_response_schema=MatchJustificationSchema(
                summary="string",
                strengths=["string"],
                gaps=["string"],
                evidence={
                    "skills_overlap": "string",
                    "title_similarity": "string",
                    "location_fit": "string",
                },
            ),
        )
