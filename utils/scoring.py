from pydantic import BaseModel

class Scores(BaseModel):
    clarity: int
    depth: int
    accuracy: int
    communication: int
    completeness: int

class Flags(BaseModel):
    is_weak: bool
    is_strong: bool
    needs_followup: bool
    is_off_topic: bool

class EvaluationResult(BaseModel):
    scores: Scores
    flags: Flags
    reasoning: str
