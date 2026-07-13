from sqlmodel import Field
from app.models.base import BaseModel


class EvalRun(BaseModel, table=True):
    __tablename__ = "eval_runs"
    commit_sha: str
    context_precision: float
    context_recall: float
    faithfulness: float
    answer_relevancy: float
    retrieval_latency_ms: float
    first_token_latency_ms: float
    total_latency_ms: float