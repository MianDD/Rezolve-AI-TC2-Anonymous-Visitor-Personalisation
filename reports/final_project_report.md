# TC2 Anonymous Homepage Personalisation - Final Project Report

Generated: 2026-07-21

## Project Objective

Build a reproducible baseline pipeline for anonymous visitor homepage personalisation using public e-commerce clickstream data. The MVP focuses on category-level and homepage-module-level decisions from current-session behaviour, not complex product recommendation or causal uplift estimation.

## What Was Built

- Retailrocket-based dataset pipeline from raw clickstream files to Parquet outputs.
- Anonymous sessionisation with a configurable 30-minute inactivity gap.
- Product/category metadata joining using item properties available at or before the event timestamp.
- Leakage-safe decision-time feature table built only from events before the decision point.
- Labels for next item, next category, future add-to-cart, future purchase and behavioural intent proxies.
- Chronological train/validation/test split by session start time.
- Synthetic homepage-impression layer for prototype demonstrations, clearly marked as synthetic.
- Baseline evaluation for popularity, recent-item/category rules and simple binary intent rules.
- Static interactive homepage demo backed by processed data and baseline metrics.

## Dataset Run Used For Demo

The current committed demo data was generated from a deterministic 50,000-session Retailrocket development sample using `--sample-strategy evenly_spaced` and seed `42`.

| Metric | Value |
| --- | ---: |
| Raw event rows loaded | 2,756,101 |
| Retained events | 175,770 |
| Retained sessions | 50,000 |
| Decision labels | 12,730 |
| Synthetic homepage impressions | 127,300 |
| Unique items | 49,986 |
| Unique categories | 961 |
| Session conversion rate | 3.47% |
| Train / validation / test sessions | 35,000 / 7,500 / 7,500 |

## Baseline Results

| Task | Baseline | Test Result |
| --- | --- | ---: |
| Next category prediction | Recent category rule | 79.41% accuracy |
| Next category prediction | Early category popularity | 69.55% accuracy |
| Next item prediction | Recent item rule | 24.32% accuracy |
| Add-to-cart prediction | Early cart rule | 0.4288 F1 |
| Purchase prediction | Early cart rule | 0.4533 F1 |
| Homepage control | Train-period global popularity | 0.65% synthetic match |
| Homepage rule based | Early-session category rule | 70.91% synthetic match |

Homepage match is a synthetic proxy derived from later observed events. It is useful for demo comparison only and is not observed CTR.

## Validation Status

Dataset validation passes for:

- required schemas and required non-null columns;
- valid normalised event types;
- unique event IDs;
- monotonic timestamps and event indexes within sessions;
- non-empty chronological train, validation and test splits;
- one split per session;
- leakage-safe decision features;
- no visitor IDs or target labels in model-ready feature tables;
- all homepage impressions marked synthetic.

The unit test suite also passes against deterministic fixtures, so development does not require Kaggle credentials or the full Retailrocket dataset.

## Demo

Live demo:

https://tc2-anonymous-demo.zongmian.chatgpt.site

The static demo in `demo/index.html` shows:

- project-level data and baseline metrics;
- representative anonymous sessions from the processed dataset;
- early-session events available before the decision point;
- decision-time signals used by the rule-based strategy;
- control modules based on train-period popularity;
- rule-based modules using only current-session prefix behaviour;
- next observed event and future outcome summary.

## Leakage Safeguards

- Splits are chronological by session start time.
- Popularity tables and control homepage recommendations are fitted from training sessions only.
- Decision features use events before the configured decision event index.
- `visitorid` is excluded from processed model-ready outputs.
- `intent_proxy`, future add-to-cart and future purchase labels are stored only in `labels.parquet`.
- Homepage impressions are generated in a separate synthetic table with `is_synthetic=True`.

## Limitations

- Homepage impressions are simulated because Retailrocket does not include homepage module impression logs.
- Simulated clicks do not establish causal CTR uplift.
- Intent labels are behavioural proxies rather than human-labelled intent.
- Offline evaluation cannot fully reproduce a deployed A/B test.
- The current committed demo uses a deterministic 50,000-session development sample, not a full-dataset benchmark.
- Product prices are mostly unavailable in the public item property files used here.

## Recommended Next Steps

1. Run the same pipeline on the full Retailrocket dataset for a larger benchmark.
2. Add a session-similarity baseline using only decision-time prefix events.
3. Add simple scikit-learn classifiers for add-to-cart and purchase prediction.
4. Add notebook walkthroughs for data exploration, session construction and baseline evaluation.
5. Deploy the static demo page if a shareable browser URL is needed.
