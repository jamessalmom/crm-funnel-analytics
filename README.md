# crm-funnel-analytics

Builds a navigable sales funnel, consultant ranking, and an **override-
without-overwrite** correction layer from CRM export data — generalized
from a standalone commercial dashboard built on top of RD Station CSV
exports.

## Features

- `build_funnel()` — deal counts, totals, and stage-to-stage conversion % for any ordered list of pipeline stages
- `ranking_by_consultant()` — won-deal ranking
- `OverrideStore` — lets an analyst correct a figure (e.g. a manually-added freight cost) **without ever mutating the original CRM value**, keeping both for audit

## Why "override without overwrite"

CRM exports are the source of truth, but real dashboards always need the
occasional manual correction (a deal amount split across two
consultants, a data-entry fix). Overwriting the raw import destroys the
audit trail; `OverrideStore` keeps the original value, the correction,
who made it, and why — `resolve()` just returns whichever is current.

```python
from crm_funnel.overrides import OverrideStore

store = OverrideStore()
store.set_override("deal-42", "amount", 1000, 1200, author="tiago", reason="freight added manually")
store.resolve("deal-42", "amount", raw_value=1000)  # -> 1200, but original_value=1000 stays on record
```

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
