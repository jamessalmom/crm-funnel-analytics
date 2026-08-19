from crm_funnel.funnel import Deal, build_funnel, ranking_by_consultant

DEALS = [
    Deal("1", "lead", "Ana", 1000),
    Deal("2", "lead", "Bruno", 1000),
    Deal("3", "qualified", "Ana", 1000),
    Deal("4", "won", "Ana", 5000),
    Deal("5", "won", "Bruno", 3000),
    Deal("6", "lost", "Bruno", 2000),
]


def test_build_funnel_counts_and_totals_per_stage():
    funnel = {s.stage: s for s in build_funnel(DEALS)}
    assert funnel["lead"].deal_count == 2
    assert funnel["qualified"].deal_count == 1
    assert funnel["won"].total_amount == 8000


def test_conversion_from_previous_stage():
    funnel = {s.stage: s for s in build_funnel(DEALS)}
    assert funnel["lead"].conversion_from_previous_pct is None
    assert funnel["qualified"].conversion_from_previous_pct == 50.0


def test_ranking_only_counts_won_deals():
    ranking = ranking_by_consultant(DEALS)
    assert ranking[0] == {"consultant": "Ana", "won_amount": 5000.0}
    assert len(ranking) == 2
