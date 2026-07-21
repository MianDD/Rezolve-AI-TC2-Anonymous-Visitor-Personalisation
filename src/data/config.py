"""Configuration for the reproducible Retailrocket dataset pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_RANDOM_SEED = 42
DEFAULT_SESSION_GAP_MINUTES = 30
DEFAULT_MIN_SESSION_EVENTS = 2
DEFAULT_DECISION_EVENT_INDEX = 3

EXPECTED_RETAILROCKET_FILES = (
    "events.csv",
    "item_properties_part1.csv",
    "item_properties_part2.csv",
    "category_tree.csv",
)

VALID_SOURCES = {"retailrocket", "fixture"}
REAL_SOURCE_TYPE = "retailrocket"
FIXTURE_SOURCE_TYPE = "fixture_retailrocket"
SYNTHETIC_HOMEPAGE_SOURCE_TYPE = "synthetic_homepage_impression"

EVENT_TYPE_MAP = {
    "view": "view",
    "click": "view",
    "clicks": "view",
    "addtocart": "add_to_cart",
    "add_to_cart": "add_to_cart",
    "cart": "add_to_cart",
    "transaction": "transaction",
    "purchase": "transaction",
    "order": "transaction",
}

NORMALISED_EVENT_TYPES = {"view", "add_to_cart", "transaction"}

MODULE_TYPES = (
    "hero_banner",
    "category_carousel",
    "trending_products",
    "sale_carousel",
    "recommended_products",
)

EXPERIMENT_GROUPS = ("control", "rule_based")

INTENT_PROXIES = (
    "browsing",
    "product_focused",
    "cart_intent",
    "purchase_intent",
)

TARGET_COLUMNS = {
    "next_item_id",
    "next_category_id",
    "will_add_to_cart_after_decision",
    "will_purchase_after_decision",
    "final_conversion_stage",
    "intent_proxy",
}


@dataclass(frozen=True)
class DatasetConfig:
    """Runtime options for dataset preparation."""

    source: str = "retailrocket"
    raw_dir: Path = Path("data/raw/retailrocket")
    output_dir: Path = Path("data/processed")
    report_path: Path = Path("reports/dataset_summary.md")
    session_gap_minutes: int = DEFAULT_SESSION_GAP_MINUTES
    min_session_events: int = DEFAULT_MIN_SESSION_EVENTS
    decision_event_index: int = DEFAULT_DECISION_EVENT_INDEX
    seed: int = DEFAULT_RANDOM_SEED
    max_events: int | None = None
    max_sessions: int | None = None

    @property
    def source_type(self) -> str:
        if self.source == "fixture":
            return FIXTURE_SOURCE_TYPE
        return REAL_SOURCE_TYPE

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["raw_dir"] = str(self.raw_dir)
        values["output_dir"] = str(self.output_dir)
        values["report_path"] = str(self.report_path)
        return values
