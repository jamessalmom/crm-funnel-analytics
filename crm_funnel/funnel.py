"""Turns a flat list of CRM deal records into a staged funnel."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass

DEFAULT_STAGE_ORDER = ["lead", "qualified", "proposal", "negotiation", "won", "lost"]


@dataclass(frozen=True)
class Deal:
    deal_id: str
    stage: str
    consultant: str
    amount: float


@dataclass(frozen=True)
class FunnelStage:
    stage: str
    deal_count: int
    total_amount: float
    conversion_from_previous_pct: float | None


def build_funnel(deals: Sequence[Deal], stage_order: list[str] | None = None) -> list[FunnelStage]:
    order = stage_order or DEFAULT_STAGE_ORDER
    counts = Counter(d.stage for d in deals)
    totals: dict[str, float] = defaultdict(float)
    for d in deals:
        totals[d.stage] += d.amount

    stages: list[FunnelStage] = []
    previous_count: int | None = None
    for stage in order:
        count = counts.get(stage, 0)
        conversion = None
        if previous_count is not None and previous_count > 0:
            conversion = round(100.0 * count / previous_count, 2)
        stages.append(
            FunnelStage(
                stage=stage,
                deal_count=count,
                total_amount=round(totals.get(stage, 0.0), 2),
                conversion_from_previous_pct=conversion,
            )
        )
        previous_count = count
    return stages


def ranking_by_consultant(deals: Sequence[Deal], won_stage: str = "won") -> list[dict[str, float]]:
    totals: dict[str, float] = defaultdict(float)
    for d in deals:
        if d.stage == won_stage:
            totals[d.consultant] += d.amount
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    return [{"consultant": name, "won_amount": round(total, 2)} for name, total in ranked]
