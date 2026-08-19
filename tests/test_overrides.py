from crm_funnel.overrides import OverrideStore


def test_resolve_returns_raw_value_without_override():
    store = OverrideStore()
    assert store.resolve("deal-1", "amount", 1000) == 1000


def test_resolve_returns_overridden_value():
    store = OverrideStore()
    store.set_override("deal-1", "amount", 1000, 1200, author="tiago", reason="freight added manually")
    assert store.resolve("deal-1", "amount", 1000) == 1200


def test_original_crm_value_is_preserved_for_audit():
    store = OverrideStore()
    store.set_override("deal-1", "amount", 1000, 1200, author="tiago", reason="correction")
    override = store.get_override("deal-1", "amount")
    assert override.original_value == 1000
    assert override.new_value == 1200
    assert override.author == "tiago"
