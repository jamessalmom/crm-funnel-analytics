# crm-funnel-analytics

Builds a sales funnel and a consultant ranking from CRM export data, and adds a correction layer that never overwrites the original CRM values. It started as part of a commercial dashboard fed by RD Station CSV exports and was generalized from there.

## What is included

- `build_funnel()`: deal count, total amount and stage-to-stage conversion for any ordered list of pipeline stages.
- `ranking_by_consultant()`: ranking by won deals.
- `OverrideStore`: lets an analyst correct a number (say, a freight cost added by hand) while keeping the original CRM value for audit.

## Corrections without overwriting

The CRM export is the source of truth, but real dashboards always end up needing a few manual fixes: a deal split between two consultants, a typo in an amount. Overwriting the imported data loses the history. `OverrideStore` keeps the original value, the correction, who made it and why, and `resolve()` returns whichever value is current.

```python
from crm_funnel.overrides import OverrideStore

store = OverrideStore()
store.set_override("deal-42", "amount", 1000, 1200, author="tiago", reason="freight added manually")
store.resolve("deal-42", "amount", raw_value=1000)  # 1200; the original 1000 stays on record
```

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT, see [LICENSE](LICENSE).
