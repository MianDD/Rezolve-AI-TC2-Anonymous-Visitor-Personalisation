window.TC2_DEMO_DATA = {
  "generated_from": "data\\processed",
  "session_count": 12,
  "metrics": {
    "next_category_recent_rule_test_accuracy": 0.7941176470588235,
    "next_item_recent_rule_test_accuracy": 0.2431544359255202,
    "add_to_cart_early_cart_test_f1": 0.4288354898336414,
    "purchase_early_cart_test_f1": 0.4532710280373832,
    "homepage_control_test_match_rate": 0.0064622124863088,
    "homepage_rule_based_test_match_rate": 0.7090909090909091
  },
  "sessions": [
    {
      "session_id": "s_00327658",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-26T18:27:22.813000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-26T18:23:05.122000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 322810,
          "category_id": 332
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-26T18:25:56.484000",
          "seconds_from_session_start": 171.362,
          "event_type": "add_to_cart",
          "item_id": 322810,
          "category_id": 332
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-26T18:27:12.922000",
          "seconds_from_session_start": 247.8,
          "event_type": "view",
          "item_id": 44986,
          "category_id": 212
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-26T18:27:22.813000",
        "seconds_from_session_start": 257.691,
        "event_type": "add_to_cart",
        "item_id": 44986,
        "category_id": 212
      },
      "future_summary": {
        "events_after_decision": 26,
        "add_to_cart_events_after_decision": 9,
        "transactions_after_decision": 3
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 11316,
          "content_category_id": 332.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 49676,
          "content_category_id": 332.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 233691,
          "content_category_id": 332.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 362214,
          "content_category_id": 332.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 58093,
          "content_category_id": 332.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00329732",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-27T15:10:01.230000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-27T15:09:26.745000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 7942,
          "category_id": 1578
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-27T15:09:53.930000",
          "seconds_from_session_start": 27.185,
          "event_type": "add_to_cart",
          "item_id": 55364,
          "category_id": 1578
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-27T15:09:53.946000",
          "seconds_from_session_start": 27.201,
          "event_type": "add_to_cart",
          "item_id": 55364,
          "category_id": 1578
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-27T15:10:01.230000",
        "seconds_from_session_start": 34.485,
        "event_type": "add_to_cart",
        "item_id": 7942,
        "category_id": 1578
      },
      "future_summary": {
        "events_after_decision": 5,
        "add_to_cart_events_after_decision": 2,
        "transactions_after_decision": 1
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 192875,
          "content_category_id": 1578.0,
          "rank": 1,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 366732,
          "content_category_id": 1578.0,
          "rank": 2,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 154638,
          "content_category_id": 1578.0,
          "rank": 3,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 203594,
          "content_category_id": 1578.0,
          "rank": 4,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 147595,
          "content_category_id": 1578.0,
          "rank": 5,
          "simulated_click": true,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00330781",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-27T21:10:59.185000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-27T21:08:30.507000",
          "seconds_from_session_start": 0.0,
          "event_type": "add_to_cart",
          "item_id": 187602,
          "category_id": 1645
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-27T21:09:38.155000",
          "seconds_from_session_start": 67.648,
          "event_type": "add_to_cart",
          "item_id": 301113,
          "category_id": 1542
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-27T21:10:31.906000",
          "seconds_from_session_start": 121.399,
          "event_type": "view",
          "item_id": 254656,
          "category_id": 34
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-27T21:10:59.185000",
        "seconds_from_session_start": 148.678,
        "event_type": "view",
        "item_id": 120990,
        "category_id": 34
      },
      "future_summary": {
        "events_after_decision": 15,
        "add_to_cart_events_after_decision": 3,
        "transactions_after_decision": 3
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 390799,
          "content_category_id": 1542.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 358348,
          "content_category_id": 1542.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 387451,
          "content_category_id": 1542.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 187934,
          "content_category_id": 1542.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 411959,
          "content_category_id": 1542.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00330820",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-27T21:24:48.562000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-27T21:21:49.206000",
          "seconds_from_session_start": 0.0,
          "event_type": "add_to_cart",
          "item_id": 319900,
          "category_id": 84
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-27T21:23:10.629000",
          "seconds_from_session_start": 81.423,
          "event_type": "view",
          "item_id": 380212,
          "category_id": 973
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-27T21:23:46.501000",
          "seconds_from_session_start": 117.295,
          "event_type": "view",
          "item_id": 380212,
          "category_id": 973
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-27T21:24:48.562000",
        "seconds_from_session_start": 179.356,
        "event_type": "view",
        "item_id": 220003,
        "category_id": 973
      },
      "future_summary": {
        "events_after_decision": 4,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 23762,
          "content_category_id": 84.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 277794,
          "content_category_id": 84.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 360825,
          "content_category_id": 84.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 153961,
          "content_category_id": 84.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 374759,
          "content_category_id": 84.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00332978",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-28T18:11:42.445000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-28T18:03:42.060000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 437520,
          "category_id": 1679
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-28T18:10:51.227000",
          "seconds_from_session_start": 429.167,
          "event_type": "add_to_cart",
          "item_id": 437520,
          "category_id": 1679
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-28T18:11:39.803000",
          "seconds_from_session_start": 477.743,
          "event_type": "view",
          "item_id": 148529,
          "category_id": 176
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-28T18:11:42.445000",
        "seconds_from_session_start": 480.385,
        "event_type": "add_to_cart",
        "item_id": 148529,
        "category_id": 176
      },
      "future_summary": {
        "events_after_decision": 6,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 76126,
          "content_category_id": 1679.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 359547,
          "content_category_id": 1679.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 151883,
          "content_category_id": 1679.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 170222,
          "content_category_id": 1679.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 238633,
          "content_category_id": 1679.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00337587",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-30T18:36:25.231000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-30T18:32:43.872000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 107352,
          "category_id": 1530
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-30T18:33:31.374000",
          "seconds_from_session_start": 47.502,
          "event_type": "view",
          "item_id": 107352,
          "category_id": 1530
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-30T18:35:03.240000",
          "seconds_from_session_start": 139.368,
          "event_type": "add_to_cart",
          "item_id": 107352,
          "category_id": 1530
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-30T18:36:25.231000",
        "seconds_from_session_start": 221.359,
        "event_type": "view",
        "item_id": 2838,
        "category_id": 1578
      },
      "future_summary": {
        "events_after_decision": 4,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 109890,
          "content_category_id": 1530.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 295337,
          "content_category_id": 1530.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 110164,
          "content_category_id": 1530.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 400577,
          "content_category_id": 1530.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 65187,
          "content_category_id": 1530.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00337648",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-30T19:05:23.426000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-30T18:53:16.926000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 415837,
          "category_id": 628
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-30T18:53:27.537000",
          "seconds_from_session_start": 10.611,
          "event_type": "add_to_cart",
          "item_id": 415837,
          "category_id": 628
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-30T19:05:21.480000",
          "seconds_from_session_start": 724.554,
          "event_type": "view",
          "item_id": 277328,
          "category_id": 1051
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-30T19:05:23.426000",
        "seconds_from_session_start": 726.5,
        "event_type": "add_to_cart",
        "item_id": 277328,
        "category_id": 1051
      },
      "future_summary": {
        "events_after_decision": 25,
        "add_to_cart_events_after_decision": 2,
        "transactions_after_decision": 1
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 204832,
          "content_category_id": 628.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 88446,
          "content_category_id": 628.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 427472,
          "content_category_id": 628.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 299384,
          "content_category_id": 628.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 63846,
          "content_category_id": 628.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00337886",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-30T20:30:50.967000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-30T20:21:38.197000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 33993,
          "category_id": 1179
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-30T20:29:21.864000",
          "seconds_from_session_start": 463.667,
          "event_type": "add_to_cart",
          "item_id": 33993,
          "category_id": 1179
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-30T20:30:29.522000",
          "seconds_from_session_start": 531.325,
          "event_type": "view",
          "item_id": 33993,
          "category_id": 1179
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-30T20:30:50.967000",
        "seconds_from_session_start": 552.77,
        "event_type": "add_to_cart",
        "item_id": 333227,
        "category_id": 1179
      },
      "future_summary": {
        "events_after_decision": 4,
        "add_to_cart_events_after_decision": 2,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 33993,
          "content_category_id": 1179.0,
          "rank": 1,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 347113,
          "content_category_id": 1179.0,
          "rank": 2,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 348056,
          "content_category_id": 1179.0,
          "rank": 3,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 92391,
          "content_category_id": 1179.0,
          "rank": 4,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 333227,
          "content_category_id": 1179.0,
          "rank": 5,
          "simulated_click": true,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00338177",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-30T22:23:35.515000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-30T22:19:29.233000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 217584,
          "category_id": 1578
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-30T22:19:48.167000",
          "seconds_from_session_start": 18.934,
          "event_type": "add_to_cart",
          "item_id": 217584,
          "category_id": 1578
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-30T22:20:12.171000",
          "seconds_from_session_start": 42.938,
          "event_type": "view",
          "item_id": 217584,
          "category_id": 1578
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-30T22:23:35.515000",
        "seconds_from_session_start": 246.282,
        "event_type": "view",
        "item_id": 135918,
        "category_id": 1578
      },
      "future_summary": {
        "events_after_decision": 4,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 192875,
          "content_category_id": 1578.0,
          "rank": 1,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 366732,
          "content_category_id": 1578.0,
          "rank": 2,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 154638,
          "content_category_id": 1578.0,
          "rank": 3,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 203594,
          "content_category_id": 1578.0,
          "rank": 4,
          "simulated_click": true,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 147595,
          "content_category_id": 1578.0,
          "rank": 5,
          "simulated_click": true,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00338452",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-31T00:47:04.815000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-31T00:19:41.209000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 386947,
          "category_id": 959
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-31T00:20:40.887000",
          "seconds_from_session_start": 59.678,
          "event_type": "add_to_cart",
          "item_id": 386947,
          "category_id": 959
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-31T00:24:07.247000",
          "seconds_from_session_start": 266.038,
          "event_type": "view",
          "item_id": 386947,
          "category_id": 959
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-31T00:47:04.815000",
        "seconds_from_session_start": 1643.606,
        "event_type": "view",
        "item_id": 315543,
        "category_id": 1279
      },
      "future_summary": {
        "events_after_decision": 7,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 441852,
          "content_category_id": 959.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 463280,
          "content_category_id": 959.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 116624,
          "content_category_id": 959.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 183511,
          "content_category_id": 959.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 345279,
          "content_category_id": 959.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00340596",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-08-31T21:19:25.025000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-08-31T21:16:32.764000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 36184,
          "category_id": 618
        },
        {
          "event_index": 1,
          "timestamp": "2015-08-31T21:17:26.161000",
          "seconds_from_session_start": 53.397,
          "event_type": "view",
          "item_id": 209050,
          "category_id": null
        },
        {
          "event_index": 2,
          "timestamp": "2015-08-31T21:18:59.960000",
          "seconds_from_session_start": 147.196,
          "event_type": "add_to_cart",
          "item_id": 209050,
          "category_id": null
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-08-31T21:19:25.025000",
        "seconds_from_session_start": 172.261,
        "event_type": "view",
        "item_id": 94120,
        "category_id": 1421
      },
      "future_summary": {
        "events_after_decision": 9,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 197077,
          "content_category_id": 618.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 231655,
          "content_category_id": 618.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 205582,
          "content_category_id": 618.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 217278,
          "content_category_id": 618.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 306086,
          "content_category_id": 618.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    },
    {
      "session_id": "s_00342709",
      "split": "test",
      "decision_event_index": 3,
      "decision_timestamp": "2015-09-01T19:12:37.201000",
      "intent_proxy": "purchase_intent",
      "final_conversion_stage": "purchase",
      "will_add_to_cart_after_decision": true,
      "will_purchase_after_decision": true,
      "prefix": [
        {
          "event_index": 0,
          "timestamp": "2015-09-01T19:11:12.567000",
          "seconds_from_session_start": 0.0,
          "event_type": "view",
          "item_id": 182738,
          "category_id": 394
        },
        {
          "event_index": 1,
          "timestamp": "2015-09-01T19:11:32.237000",
          "seconds_from_session_start": 19.67,
          "event_type": "view",
          "item_id": 182738,
          "category_id": 394
        },
        {
          "event_index": 2,
          "timestamp": "2015-09-01T19:11:57.139000",
          "seconds_from_session_start": 44.572,
          "event_type": "add_to_cart",
          "item_id": 182738,
          "category_id": 394
        }
      ],
      "next_event": {
        "event_index": 3,
        "timestamp": "2015-09-01T19:12:37.201000",
        "seconds_from_session_start": 84.634,
        "event_type": "add_to_cart",
        "item_id": 7943,
        "category_id": 398
      },
      "future_summary": {
        "events_after_decision": 3,
        "add_to_cart_events_after_decision": 1,
        "transactions_after_decision": 2
      },
      "impressions": [
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "hero_banner",
          "content_item_id": 309778,
          "content_category_id": null,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "category_carousel",
          "content_item_id": 257040,
          "content_category_id": 683.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "trending_products",
          "content_item_id": 461686,
          "content_category_id": 1037.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "sale_carousel",
          "content_item_id": 369447,
          "content_category_id": 48.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "control",
          "strategy": "training_global_popularity",
          "module_type": "recommended_products",
          "content_item_id": 9877,
          "content_category_id": 858.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "hero_banner",
          "content_item_id": 186260,
          "content_category_id": 394.0,
          "rank": 1,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "category_carousel",
          "content_item_id": 70387,
          "content_category_id": 394.0,
          "rank": 2,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "trending_products",
          "content_item_id": 193304,
          "content_category_id": 394.0,
          "rank": 3,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "sale_carousel",
          "content_item_id": 127712,
          "content_category_id": 394.0,
          "rank": 4,
          "simulated_click": false,
          "is_synthetic": true
        },
        {
          "experiment_group": "rule_based",
          "strategy": "early_session_category_rule",
          "module_type": "recommended_products",
          "content_item_id": 135091,
          "content_category_id": 394.0,
          "rank": 5,
          "simulated_click": false,
          "is_synthetic": true
        }
      ]
    }
  ],
  "limitations": [
    "Homepage impressions are simulated.",
    "Simulated clicks are not observed CTR.",
    "Synthetic match rates do not establish causal uplift.",
    "Intent labels are behavioural proxies, not human-labelled intent."
  ]
};
