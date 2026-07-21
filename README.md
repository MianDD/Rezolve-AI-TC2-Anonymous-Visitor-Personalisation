# TC2 Anonymous Visitor Personalisation

This project builds a reproducible dataset pipeline for anonymous homepage personalisation. The goal is to turn public e-commerce clickstream data into clean train, validation and test datasets for early baselines such as global popularity, category popularity, recent-category rules, next-item prediction, next-category prediction, add-to-cart prediction and purchase prediction.

The project deliberately does not claim causal personalisation uplift from offline public data. It prepares leakage-aware datasets for modelling and prototype demos.

## Dataset Choice

The primary behavioural dataset is the public Retailrocket e-commerce dataset, commonly distributed through Kaggle as `retailrocket/ecommerce-dataset`.

Expected files:

```text
data/raw/retailrocket/events.csv
data/raw/retailrocket/item_properties_part1.csv
data/raw/retailrocket/item_properties_part2.csv
data/raw/retailrocket/category_tree.csv
```

Follow the dataset page for attribution and licence requirements. Do not commit downloaded raw data to Git.

## Why Not Synthetic-Only

Synthetic-only data is useful for smoke tests and UI prototypes, but it can hide the messiness that matters in real clickstream modelling: missing metadata, sparse purchases, time-varying item properties, anonymous visitors without explicit sessions and highly imbalanced event types.

This repository keeps legacy synthetic generators under `src/synthetic/`, clearly labelled as synthetic. The main pipeline uses Retailrocket-style events as the behavioural base. Synthetic data is added only for homepage module impressions because public Retailrocket clickstream data does not contain homepage impression logs.

## Setup

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS/Linux, replace the Python executable path with `.venv/bin/python`.

## Public Data Acquisition

Optional Kaggle helper:

```bash
.venv\Scripts\python.exe -m src.data.download_retailrocket --raw-dir data/raw/retailrocket
```

This helper does not hard-code credentials. Configure Kaggle normally, for example by placing `kaggle.json` in your Kaggle config directory or setting the environment variables expected by the Kaggle CLI.

Manual download is also supported. Download the Retailrocket dataset from Kaggle and place the four CSV files in `data/raw/retailrocket/`.

## Fixture-Based Development

The repository includes a tiny deterministic Retailrocket-schema fixture in `data/fixtures/retailrocket/`. It lets tests and local pipeline checks run without Kaggle credentials or the full dataset.

```bash
.venv\Scripts\python.exe -m src.data.prepare_dataset ^
  --source fixture ^
  --raw-dir data/fixtures/retailrocket ^
  --output-dir data/processed ^
  --session-gap-minutes 30 ^
  --decision-event-index 3 ^
  --seed 42

.venv\Scripts\python.exe -m src.data.validate_dataset --data-dir data/processed
.venv\Scripts\python.exe -m pytest -q
```

## Full Preprocessing

After manually downloading the full Retailrocket files:

```bash
.venv\Scripts\python.exe -m src.data.prepare_dataset ^
  --source retailrocket ^
  --raw-dir data/raw/retailrocket ^
  --output-dir data/processed ^
  --session-gap-minutes 30 ^
  --decision-event-index 3 ^
  --seed 42
```

Development sampling is deterministic and preserves complete sessions:

```bash
.venv\Scripts\python.exe -m src.data.prepare_dataset ^
  --source retailrocket ^
  --raw-dir data/raw/retailrocket ^
  --output-dir data/processed ^
  --max-sessions 5000 ^
  --sample-strategy evenly_spaced ^
  --seed 42
```

`evenly_spaced` is the default sampling strategy for `--max-sessions`. It selects complete sessions across the full chronological range, which gives a more representative development sample than taking only the earliest sessions.

## Outputs

Processed outputs are written as Parquet files under `data/processed/`, which is ignored by Git:

- `events.parquet`
- `products.parquet`
- `sessions.parquet`
- `labels.parquet`
- `decision_features.parquet`
- `homepage_impressions.parquet`
- `splits.parquet`
- `dataset_manifest.json`

`reports/dataset_summary.md` is generated with the run configuration, counts, validation results and limitations.

## Output Schemas

`events.parquet`:

```text
session_id, event_id, event_index, timestamp, seconds_from_session_start,
item_id, category_id, event_type, transaction_id, source_type
```

`products.parquet`:

```text
item_id, category_id, parent_category_id, available, price,
selected_item_properties, source_type
```

`sessions.parquet`:

```text
session_id, session_start, session_end, session_duration_seconds,
number_of_events, number_of_views, number_of_add_to_cart_events,
number_of_transactions, number_of_unique_items, number_of_unique_categories,
first_item_id, first_category_id, last_item_id, last_category_id,
converted, source_type
```

`labels.parquet`:

```text
session_id, decision_event_index, next_item_id, next_category_id,
will_add_to_cart_after_decision, will_purchase_after_decision,
final_conversion_stage, intent_proxy
```

`decision_features.parquet` contains only information available before the decision event index.

`homepage_impressions.parquet`:

```text
session_id, decision_event_index, impression_timestamp, experiment_group,
strategy, module_id, module_type, content_item_id, content_category_id,
rank, simulated_click, is_synthetic
```

## Leakage Safeguards

- Splits are chronological by `session_start`: first 70% train, next 15% validation, final 15% test.
- A session appears in only one split.
- `visitorid` is used only for sessionisation and is not written to model-ready outputs.
- Event categories are joined from item properties known at or before each event timestamp.
- Control homepage recommendations use only training-period global popularity.
- Rule-based homepage recommendations use only early-session prefix events before the decision point.
- `intent_proxy` and future outcome labels are stored only in `labels.parquet`.
- Synthetic homepage impressions and simulated clicks are always marked with `is_synthetic=True`.

## Limitations

- Homepage impressions are simulated because Retailrocket does not contain homepage module impressions.
- Simulated clicks are not observed CTR and do not establish causal CTR uplift.
- Intent labels are behavioural proxies, not human-labelled intent.
- Offline evaluation cannot fully reproduce a deployed A/B test.
- Missing or changing item metadata can leave some category, price or availability fields missing.

## Project Structure

```text
data/
|-- raw/
|   `-- retailrocket/
|-- interim/
|-- processed/
`-- fixtures/
    `-- retailrocket/

src/
|-- data/
|   |-- config.py
|   |-- schemas.py
|   |-- download_retailrocket.py
|   |-- load_retailrocket.py
|   |-- sessionize.py
|   |-- build_products.py
|   |-- build_sessions.py
|   |-- build_labels.py
|   |-- simulate_homepage.py
|   |-- split_dataset.py
|   |-- validate_dataset.py
|   `-- prepare_dataset.py
`-- synthetic/
    |-- pure_random_dataset.py
    `-- reasonable_random_dataset.py
```

## Next Development Steps

- Add first baseline notebooks over `decision_features.parquet` and `labels.parquet`.
- Add category-aware popularity and recent-category baselines.
- Add a simple prototype homepage renderer using `homepage_impressions.parquet`.
- Add stronger metadata handling for full Retailrocket item property history.
- Add later contextual bandit experiments only after the dataset contract is stable.
