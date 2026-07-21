# Baseline Evaluation

Generated: 2026-07-21T10:06:29.480275+00:00

Data directory: `data\processed`

Baselines are fitted using the chronological training split only. Validation and test sessions are used only for evaluation.

## Next-Item And Next-Category Baselines

Validation:

| task | model | split | evaluated_rows | covered_rows | coverage | accuracy | accuracy_on_covered | correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| next_item_prediction | GlobalItemPopularity | validation | 1809 | 1809 | 1.0000 | 0.0000 | 0.0000 | 0 |
| next_item_prediction | RecentItemRule | validation | 1809 | 1809 | 1.0000 | 0.2869 | 0.2869 | 519 |
| next_item_prediction | CategoryItemPopularity | validation | 1809 | 1809 | 1.0000 | 0.0271 | 0.0271 | 49 |
| next_category_prediction | GlobalCategoryPopularity | validation | 1715 | 1715 | 1.0000 | 0.0461 | 0.0461 | 79 |
| next_category_prediction | RecentCategoryRule | validation | 1715 | 1711 | 0.9977 | 0.8198 | 0.8217 | 1406 |
| next_category_prediction | EarlyCategoryPopularity | validation | 1715 | 1715 | 1.0000 | 0.7464 | 0.7464 | 1280 |

Test:

| task | model | split | evaluated_rows | covered_rows | coverage | accuracy | accuracy_on_covered | correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| next_item_prediction | GlobalItemPopularity | test | 1826 | 1826 | 1.0000 | 0.0000 | 0.0000 | 0 |
| next_item_prediction | RecentItemRule | test | 1826 | 1826 | 1.0000 | 0.2432 | 0.2432 | 444 |
| next_item_prediction | CategoryItemPopularity | test | 1826 | 1826 | 1.0000 | 0.0268 | 0.0268 | 49 |
| next_category_prediction | GlobalCategoryPopularity | test | 1734 | 1734 | 1.0000 | 0.0490 | 0.0490 | 85 |
| next_category_prediction | RecentCategoryRule | test | 1734 | 1720 | 0.9919 | 0.7941 | 0.8006 | 1377 |
| next_category_prediction | EarlyCategoryPopularity | test | 1734 | 1734 | 1.0000 | 0.6955 | 0.6955 | 1206 |

## Add-To-Cart And Purchase Baselines

Validation:

| task | model | split | evaluated_rows | actual_positive_rate | predicted_positive_rate | accuracy | precision | recall | f1 | true_positive | false_positive | true_negative | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_to_cart_prediction | AlwaysNegative | validation | 1809 | 0.1570 | 0.0000 | 0.8430 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 1525 | 284 |
| add_to_cart_prediction | EarlyCartRule | validation | 1809 | 0.1570 | 0.1520 | 0.8259 | 0.4436 | 0.4296 | 0.4365 | 122 | 153 | 1372 | 162 |
| add_to_cart_prediction | ProductFocusRule | validation | 1809 | 0.1570 | 0.9502 | 0.1891 | 0.1559 | 0.9437 | 0.2676 | 268 | 1451 | 74 | 16 |
| add_to_cart_prediction | CartOrFocusRule | validation | 1809 | 0.1570 | 0.9541 | 0.1918 | 0.1587 | 0.9648 | 0.2726 | 274 | 1452 | 73 | 10 |
| purchase_prediction | AlwaysNegative | validation | 1809 | 0.0779 | 0.0000 | 0.9221 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 1668 | 141 |
| purchase_prediction | EarlyCartRule | validation | 1809 | 0.0779 | 0.1520 | 0.8530 | 0.2727 | 0.5319 | 0.3606 | 75 | 200 | 1468 | 66 |
| purchase_prediction | ProductFocusRule | validation | 1809 | 0.0779 | 0.9502 | 0.1222 | 0.0791 | 0.9645 | 0.1462 | 136 | 1583 | 85 | 5 |
| purchase_prediction | CartOrFocusRule | validation | 1809 | 0.0779 | 0.9541 | 0.1183 | 0.0788 | 0.9645 | 0.1457 | 136 | 1590 | 78 | 5 |

Test:

| task | model | split | evaluated_rows | actual_positive_rate | predicted_positive_rate | accuracy | precision | recall | f1 | true_positive | false_positive | true_negative | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_to_cart_prediction | AlwaysNegative | test | 1826 | 0.1462 | 0.0000 | 0.8538 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 1559 | 267 |
| add_to_cart_prediction | EarlyCartRule | test | 1826 | 0.1462 | 0.1501 | 0.8308 | 0.4234 | 0.4345 | 0.4288 | 116 | 158 | 1401 | 151 |
| add_to_cart_prediction | ProductFocusRule | test | 1826 | 0.1462 | 0.9425 | 0.1785 | 0.1418 | 0.9139 | 0.2455 | 244 | 1477 | 82 | 23 |
| add_to_cart_prediction | CartOrFocusRule | test | 1826 | 0.1462 | 0.9491 | 0.1829 | 0.1466 | 0.9513 | 0.2540 | 254 | 1479 | 80 | 13 |
| purchase_prediction | AlwaysNegative | test | 1826 | 0.0843 | 0.0000 | 0.9157 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 1672 | 154 |
| purchase_prediction | EarlyCartRule | test | 1826 | 0.0843 | 0.1501 | 0.8719 | 0.3540 | 0.6299 | 0.4533 | 97 | 177 | 1495 | 57 |
| purchase_prediction | ProductFocusRule | test | 1826 | 0.0843 | 0.9425 | 0.1276 | 0.0819 | 0.9156 | 0.1504 | 141 | 1580 | 92 | 13 |
| purchase_prediction | CartOrFocusRule | test | 1826 | 0.0843 | 0.9491 | 0.1254 | 0.0837 | 0.9416 | 0.1537 | 145 | 1588 | 84 | 9 |

## Homepage Synthetic Match

| task | model | split | evaluated_rows | simulated_match_rate | note |
| --- | --- | --- | --- | --- | --- |
| homepage_synthetic_match | control | test | 9130 | 0.0065 | Synthetic match signal only; not observed CTR or causal uplift. |
| homepage_synthetic_match | rule_based | test | 9130 | 0.7091 | Synthetic match signal only; not observed CTR or causal uplift. |
| homepage_synthetic_match | control | train | 45475 | 0.0081 | Synthetic match signal only; not observed CTR or causal uplift. |
| homepage_synthetic_match | rule_based | train | 45475 | 0.5827 | Synthetic match signal only; not observed CTR or causal uplift. |
| homepage_synthetic_match | control | validation | 9045 | 0.0080 | Synthetic match signal only; not observed CTR or causal uplift. |
| homepage_synthetic_match | rule_based | validation | 9045 | 0.7410 | Synthetic match signal only; not observed CTR or causal uplift. |

This homepage table reports synthetic match rates only. It is not observed CTR and must not be interpreted as causal personalisation uplift.

## Notes

- `GlobalItemPopularity` and `GlobalCategoryPopularity` use train-period event popularity only.
- `RecentItemRule` and `RecentCategoryRule` use only decision-time prefix features.
- `EarlyCategoryPopularity` maps early-session category context to the modal train next-category, with a train global fallback.
- Binary baselines are deliberately simple prefix rules and are not calibrated machine-learning models.
