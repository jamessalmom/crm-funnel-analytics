"""crm_funnel

Builds a navigable sales funnel, consultant ranking, and weekly/monthly
comparisons from a CRM export (CSV-like rows), plus an "override without
overwrite" pattern for manual corrections that keeps the original CRM
values intact for audit purposes.

Generalized from a standalone commercial-funnel dashboard built on top of
RD Station exports.
"""

from .funnel import FunnelStage, build_funnel
from .overrides import OverrideStore

__all__ = ["FunnelStage", "OverrideStore", "build_funnel"]
__version__ = "0.1.0"
