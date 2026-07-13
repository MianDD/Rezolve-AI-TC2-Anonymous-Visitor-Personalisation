# TC2 Anonymous Visitor Personalisation

## Business Goal

Improve anonymous visitor engagement and conversion potential by adapting homepage categories/modules based on current session behaviour.

## MVP Scope

This MVP focuses on category-level or homepage-module-level personalisation, not product-level recommendation. The first objective is a clean end-to-end baseline pipeline, not a complex model.

## Current Pipeline

```text
raw clickstream data
-> anonymous sessions
-> baseline recommendation
-> offline next-category evaluation
```

## Expected Dataset

The first target dataset is RetailRocket-style event data. Place the raw file here:

```text
data/raw/events.csv
```

Expected columns:

- `timestamp`
- `visitorid`
- `event`
- `itemid`
- `transactionid` optional

If no `category_id` column is available, the pipeline creates a temporary `category_id` column from `itemid`. This is a placeholder until a real item-to-category mapping is added.

## How To Run

From this project folder:

```bash
pip install -r requirements.txt
```

Put `events.csv` into `data/raw/`, then run:

```bash
python -m src.run_baselines
```

If the raw file is missing, the script exits gracefully with a clear instruction.

## Baselines Included

- Popularity baseline
- Last-category baseline
- Random baseline

## Metrics

- Next-category accuracy
- Average reward
- Total reward

Reward design:

- `transaction`, `order`, `purchase` = 5
- `addtocart`, `cart`, `add_to_cart` = 3
- `view`, `click`, `clicks` = 1
- Other events = 0

## Project Structure

```text
tc2_anonymous_personalisation/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|   |-- 01_data_exploration.ipynb
|   |-- 02_session_construction.ipynb
|   `-- 03_baseline_evaluation.ipynb
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- data_loader.py
|   |-- preprocess.py
|   |-- baselines.py
|   |-- evaluation.py
|   `-- run_baselines.py
|-- outputs/
|   |-- figures/
|   `-- tables/
|-- README.md
`-- requirements.txt
```

## Next Steps

- Add real item-to-category mapping
- Add lookalike/session-similarity baseline
- Add contextual bandit model
- Build side-by-side demo
- Evaluate with CTR proxy and add-to-cart proxy
