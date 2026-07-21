# Dataset Summary

## Source Dataset

- Source: retailrocket
- Source type in event tables: retailrocket
- Retailrocket files expected in: `data\raw\retailrocket`
- Missing metadata files during this run: none
- Processing date: 2026-07-21T10:06:19.110334+00:00

Retailrocket is a public e-commerce behavioural dataset distributed through Kaggle. Follow Kaggle's dataset page for attribution and licence requirements before using the full dataset in shared or commercial work.

## Configuration

```json
{
  "source": "retailrocket",
  "raw_dir": "data\\raw\\retailrocket",
  "output_dir": "data\\processed",
  "report_path": "reports\\dataset_summary.md",
  "session_gap_minutes": 30,
  "min_session_events": 2,
  "decision_event_index": 3,
  "seed": 42,
  "max_events": null,
  "max_sessions": 50000,
  "sample_strategy": "evenly_spaced"
}
```

## Volumes

- Raw event rows loaded: 2756101
- Retained event rows: 175770
- Retained sessions: 50000
- Unique items: 49986
- Unique categories: 961
- Synthetic homepage impressions: 127300

## Event-Type Counts

- view: 165147
- add_to_cart: 8019
- transaction: 2604

## Session Length Distribution

- min: 2.0
- p25: 2.0
- median: 2.0
- p75: 4.0
- max: 248.0

## Conversion Rates

- Session conversion rate: 0.0347
- Session add-to-cart rate: 0.1030

## Train/Validation/Test Sizes

- train: 35000
- validation: 7500
- test: 7500

## Missing-Value Summary

```json
{
  "events": {
    "transaction_id": 173166,
    "category_id": 37221
  },
  "products": {
    "category_id": 3732,
    "parent_category_id": 3732,
    "available": 3732,
    "price": 49986
  },
  "sessions": {
    "first_category_id": 10798,
    "last_category_id": 10482
  },
  "labels": {
    "next_category_id": 2450
  },
  "decision_features": {
    "first_category_id": 1436,
    "last_category_id": 1436,
    "most_frequent_category_id": 1436
  },
  "homepage_impressions": {
    "content_category_id": 12730
  },
  "splits": {}
}
```

## Output Schemas

{
  "events": [
    "session_id",
    "event_id",
    "event_index",
    "timestamp",
    "seconds_from_session_start",
    "item_id",
    "category_id",
    "event_type",
    "transaction_id",
    "source_type"
  ],
  "products": [
    "item_id",
    "category_id",
    "parent_category_id",
    "available",
    "price",
    "selected_item_properties",
    "source_type"
  ],
  "sessions": [
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
    "source_type"
  ],
  "labels": [
    "session_id",
    "decision_event_index",
    "next_item_id",
    "next_category_id",
    "will_add_to_cart_after_decision",
    "will_purchase_after_decision",
    "final_conversion_stage",
    "intent_proxy"
  ],
  "homepage_impressions": [
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
    "is_synthetic"
  ],
  "splits": [
    "session_id",
    "split"
  ],
  "decision_features": [
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
    "source_type"
  ]
}

## Validation Results

- [x] events_file_exists: ok
- [x] products_file_exists: ok
- [x] sessions_file_exists: ok
- [x] labels_file_exists: ok
- [x] homepage_impressions_file_exists: ok
- [x] splits_file_exists: ok
- [x] decision_features_file_exists: ok
- [x] events_required_columns: ok
- [x] events_required_non_nulls: ok
- [x] products_required_columns: ok
- [x] products_required_non_nulls: ok
- [x] sessions_required_columns: ok
- [x] sessions_required_non_nulls: ok
- [x] labels_required_columns: ok
- [x] labels_required_non_nulls: ok
- [x] homepage_impressions_required_columns: ok
- [x] homepage_impressions_required_non_nulls: ok
- [x] splits_required_columns: ok
- [x] splits_required_non_nulls: ok
- [x] decision_features_required_columns: ok
- [x] decision_features_required_non_nulls: ok
- [x] valid_event_types: ok
- [x] unique_event_ids: ok
- [x] monotonic_timestamps_within_sessions: ok
- [x] valid_event_indexes: ok
- [x] non_empty_train_validation_test: ok
- [x] one_split_per_session: ok
- [x] valid_split_names: ok
- [x] valid_intent_proxy_values: ok
- [x] decision_features_use_prefix_only: ok
- [x] events_has_no_label_targets: ok
- [x] products_has_no_label_targets: ok
- [x] decision_features_has_no_label_targets: ok
- [x] homepage_impressions_all_synthetic: ok
- [x] valid_homepage_experiment_groups: ok
- [x] valid_homepage_module_types: ok
- [x] no_raw_visitor_id_in_model_ready_files: ok
- [x] manifest_contains_seed: ok

## Intent Proxy Derivation

- `purchase_intent`: a transaction occurs after the decision point.
- `cart_intent`: no future transaction, but an add-to-cart occurs after the decision point.
- `product_focused`: no future cart or purchase, but early-session behaviour revisits the same item or category.
- `browsing`: none of the above.

These proxy labels are stored only in `labels.parquet` and are intended for evaluation or weak supervision, not as input features.

## Limitations

- Homepage impressions are simulated because the public Retailrocket data does not contain homepage module impressions.
- Simulated clicks do not establish causal CTR uplift.
- Intent labels are behavioural proxies rather than human-labelled intent.
- Offline evaluation cannot fully reproduce a deployed A/B test.
- Category and product metadata can be missing or time-varying; event categories are assigned using item metadata known at or before the event timestamp.
