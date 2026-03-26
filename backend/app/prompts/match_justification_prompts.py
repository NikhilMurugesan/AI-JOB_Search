MATCH_JUSTIFICATION_PROMPT_TEMPLATE = """You are an assistant helping explain job-match rankings.
Given a resume summary and a scored job, produce a concise, factual rationale.

Output JSON with this schema:
{
  "summary": "string",
  "strengths": ["string"],
  "gaps": ["string"],
  "evidence": {
    "skills_overlap": "string",
    "title_similarity": "string",
    "location_fit": "string"
  }
}

Constraints:
- Do not invent experience not present in inputs.
- Keep each bullet under 20 words.
- Reflect score breakdown exactly.
"""
