"""Simple recommendation baselines for next-category prediction."""

from __future__ import annotations

import random
from typing import Any

import pandas as pd


class PopularityBaseline:
    """Always recommend the most popular category observed in training."""

    def __init__(self) -> None:
        self.most_popular_category: Any | None = None

    def fit(self, df: pd.DataFrame, category_col: str = "category_id") -> "PopularityBaseline":
        counts = df[category_col].value_counts()
        self.most_popular_category = counts.index[0] if not counts.empty else None
        return self

    def predict(self, history: pd.DataFrame | None = None) -> Any | None:
        return self.most_popular_category


class LastCategoryBaseline:
    """Recommend the most recent category in the current session history."""

    def __init__(self, category_col: str = "category_id") -> None:
        self.category_col = category_col

    def predict(self, history: pd.DataFrame | None) -> Any | None:
        if history is None or history.empty:
            return None

        return history.iloc[-1][self.category_col]


class RandomBaseline:
    """Recommend a random observed category from training."""

    def __init__(self, random_seed: int | None = None) -> None:
        self.categories: list[Any] = []
        self.random = random.Random(random_seed)

    def fit(self, df: pd.DataFrame, category_col: str = "category_id") -> "RandomBaseline":
        self.categories = list(df[category_col].dropna().unique())
        return self

    def predict(self, history: pd.DataFrame | None = None) -> Any | None:
        if not self.categories:
            return None

        return self.random.choice(self.categories)


class TopKPopularityBaseline:
    """Return the top-k most popular categories observed in training."""

    def __init__(self, k: int = 5) -> None:
        self.k = k
        self.top_categories: list[Any] = []

    def fit(
        self, df: pd.DataFrame, category_col: str = "category_id", k: int | None = None
    ) -> "TopKPopularityBaseline":
        if k is not None:
            self.k = k

        self.top_categories = list(df[category_col].value_counts().head(self.k).index)
        return self

    def predict_top_k(self, history: pd.DataFrame | None = None) -> list[Any]:
        return self.top_categories
