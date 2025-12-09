"""
Pandas Essentials for ML/CV Interviews
Author: Joey Tung
"""

import pandas as pd
import numpy as np

# === FILTERING ===
df[df["score"] > 0.5]  # Single condition
df[(df["score"] > 0.5) & (df["weather"] == "sunny")]  # Multiple conditions (use & | not and/or)
df[df["weather"].isin(["sunny", "rainy"])]  # Match list

# === GROUPBY ===
df.groupby("weather").size()  # Count per group
df.groupby("weather")["score"].mean()  # Mean per group
df.groupby(["weather", "time"]).agg({"score": ["mean", "std"]})  # Multi-column agg

# === SAMPLING ===
df.sample(n=100, random_state=42)  # Random sample (fixed seed)
df.sample(frac=0.1)  # Sample 10%
df.groupby("weather").sample(n=10)  # Sample N per group

# === MERGING ===
pd.concat([df1, df2], ignore_index=True)  # Stack vertically
df1.merge(df2, on="id", how="inner")  # SQL-style join

# === USEFUL TRICKS ===
df["new_col"] = df["a"] + df["b"]  # Add column
df.drop_duplicates(subset=["id"])  # Remove duplicates
df.sort_values("score", ascending=False)  # Sort
df.reset_index(drop=True)  # Reset index after filtering
