"""Expected schemas and lightweight schema helpers."""

from __future__ import annotations

from collections.abc import Iterable

from src.data.config import (
    EXPERIMENT_GROUPS,
    MODULE_TYPES,
    NORMALISED_EVENT_TYPES,
    TARGET_COLUMNS,
)


EVENTS_COLUMNS = [
    "session_id",
    "event_id",
    "event_index",
    "timestamp",
    "seconds_from_session_start",
    "item_id",
    "category_id",
    "event_type",
    "transaction_id",
    "source_type",
]

PRODUCTS_COLUMNS = [
    "item_id",
    "category_id",
    "parent_category_id",
    "available",
    "price",
    "selected_item_properties",
    "source_type",
]

SESSIONS_COLUMNS = [
    "session_id",
    "session_start",
    "session_end",
    "session_duration_seconds",
    "number_of_events",
    "number_of_views",
    "number_of_add_to_cart_events",
    "number_of_transactions",
    "number_of_unique_items",
    "number_of_unique_categories",
    "first_item_id",
    "first_category_id",
    "last_item_id",
    "last_category_id",
    "converted",
    "source_type",
]

LABELS_COLUMNS = [
    "session_id",
    "decision_event_index",
    "next_item_id",
    "next_category_id",
    "will_add_to_cart_after_decision",
    "will_purchase_after_decision",
    "final_conversion_stage",
    "intent_proxy",
]

HOMEPAGE_IMPRESSIONS_COLUMNS = [
    "session_id",
    "decision_event_index",
    "impression_timestamp",
    "experiment_group",
    "strategy",
    "module_id",
    "module_type",
    "content_item_id",
    "content_category_id",
    "rank",
    "simulated_click",
    "is_synthetic",
]

SPLITS_COLUMNS = ["session_id", "split"]

DECISION_FEATURES_COLUMNS = [
    "session_id",
    "decision_event_index",
    "decision_timestamp",
    "prefix_event_count",
    "prefix_view_count",
    "prefix_add_to_cart_count",
    "prefix_unique_items",
    "prefix_unique_categories",
    "first_item_id",
    "first_category_id",
    "last_item_id",
    "last_category_id",
    "most_frequent_category_id",
    "seconds_from_session_start",
    "source_type",
]

REQUIRED_COLUMNS_BY_TABLE = {
    "events": EVENTS_COLUMNS,
    "products": PRODUCTS_COLUMNS,
    "sessions": SESSIONS_COLUMNS,
    "labels": LABELS_COLUMNS,
    "homepage_impressions": HOMEPAGE_IMPRESSIONS_COLUMNS,
    "splits": SPLITS_COLUMNS,
    "decision_features": DECISION_FEATURES_COLUMNS,
}

NON_NULL_COLUMNS_BY_TABLE = {
    "events": [
        "session_id",
        "event_id",
        "event_index",
        "timestamp",
        "seconds_from_session_start",
        "item_id",
        "event_type",
        "source_type",
    ],
    "products": ["item_id", "selected_item_properties", "source_type"],
    "sessions": [
        "session_id",
        "session_start",
        "session_end",
        "number_of_events",
        "converted",
        "source_type",
    ],
    "labels": [
        "session_id",
        "decision_event_index",
        "will_add_to_cart_after_decision",
        "will_purchase_after_decision",
        "final_conversion_stage",
        "intent_proxy",
    ],
    "homepage_impressions": [
        "session_id",
        "decision_event_index",
        "impression_timestamp",
        "experiment_group",
        "strategy",
        "module_id",
        "module_type",
        "rank",
        "simulated_click",
        "is_synthetic",
    ],
    "splits": ["session_id", "split"],
    "decision_features": [
        "session_id",
        "decision_event_index",
        "decision_timestamp",
        "prefix_event_count",
        "source_type",
    ],
}


def missing_columns(columns: Iterable[str], required: Iterable[str]) -> list[str]:
    present = set(columns)
    return [column for column in required if column not in present]


def target_columns_in_feature_table(columns: Iterable[str]) -> list[str]:
    present = set(columns)
    return sorted(present.intersection(TARGET_COLUMNS))


def valid_event_types() -> set[str]:
    return set(NORMALISED_EVENT_TYPES)


def valid_module_types() -> set[str]:
    return set(MODULE_TYPES)


def valid_experiment_groups() -> set[str]:
    return set(EXPERIMENT_GROUPS)
