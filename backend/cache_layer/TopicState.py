from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TopicKey:
    topic_label: str
    modality_filter: str
    retrieval_policy: str


@dataclass
class TopicState:
    key: TopicKey
    score: int
    cached_chunk_ids: List[int]
    access_count: int
    last_access_ts: float
    first_seen_ts: float
    confidence: float  # optional heuristicy
