# 💼 Interview Prep & Case Studies

A structured prep guide featuring high-yield questions, clean coding implementations, and blueprints for machine learning system design interviews.

---

## 🗺️ Table of Contents
1. [Advanced SQL Questions](#1-advanced-sql-questions)
2. [Python Algorithmic Coding](#2-python-algorithmic-coding)
3. [Machine Learning System Design Blueprints](#3-machine-learning-system-design-blueprints)

---

## 1. Advanced SQL Questions

### Scenario 1: Month-over-Month Active Users Growth
**Question:** Write a query to find the Month-over-Month (MoM) growth rate of Active Users. Assume you have a table `user_logins` with columns `login_id`, `user_id`, and `login_date`.

#### SQL Solution (PostgreSQL):
```sql
WITH monthly_active_users AS (
    SELECT 
        DATE_TRUNC('month', login_date)::date AS login_month,
        COUNT(DISTINCT user_id) AS active_users
    FROM user_logins
    GROUP BY 1
),
prev_month_metrics AS (
    SELECT 
        login_month,
        active_users,
        LAG(active_users, 1) OVER (ORDER BY login_month) AS prev_active_users
    FROM monthly_active_users
)
SELECT 
    login_month,
    active_users,
    prev_active_users,
    ROUND(
        100.0 * (active_users - prev_active_users) / prev_active_users, 
        2
    ) AS mom_growth_percent
FROM prev_month_metrics;
```

---

### Scenario 2: Gaps & Islands (Consecutive Login Streak)
**Question:** Write a SQL query to identify users who have logged in on 3 or more consecutive days.

#### SQL Solution (PostgreSQL):
```sql
WITH distinct_logins AS (
    -- Deduplicate logins per user per day
    SELECT DISTINCT 
        user_id, 
        login_date::date AS login_day
    FROM user_logins
),
login_groups AS (
    -- Group consecutive dates using row numbering difference
    SELECT 
        user_id,
        login_day,
        login_day - ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_day)::int AS island_id
    FROM distinct_logins
),
streak_aggregations AS (
    SELECT 
        user_id,
        MIN(login_day) AS streak_start,
        MAX(login_day) AS streak_end,
        COUNT(*) AS streak_length
    FROM login_groups
    GROUP BY user_id, island_id
)
SELECT DISTINCT user_id, streak_length
FROM streak_aggregations
WHERE streak_length >= 3;
```

---

## 2. Python Algorithmic Coding

### Problem 1: Merging Overlapping Intervals
**Question:** Given an array of intervals where `intervals[i] = [start, end]`, merge all overlapping intervals.

#### Python Solution:
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    
    # Sort intervals by start time: O(N log N)
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current
        
        # If current interval overlaps with the previous one, merge them
        if curr_start <= prev_end:
            merged[-1][1] = max(prev_end, curr_end)
        else:
            merged.append(current)
            
    return merged

# Complexity: Time: O(N log N), Space: O(N) (for sorting/storage)
```

---

### Problem 2: Length of Longest Substring Without Repeating Characters
**Question:** Find the length of the longest substring without repeating characters using a sliding window.

#### Python Solution:
```python
def length_of_longest_substring(s: str) -> int:
    char_index_map = {}
    max_len = 0
    left = 0
    
    for right, char in enumerate(s):
        # If char was seen and is inside the current window, move the left boundary
        if char in char_index_map and char_index_map[char] >= left:
            left = char_index_map[char] + 1
            
        char_index_map[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

# Complexity: Time: O(N), Space: O(min(M, N)) where M is character alphabet size
```

---

## 3. Machine Learning System Design Blueprints

### Case Study: Real-Time Fraud Detection System
Design a system to detect fraudulent credit card transactions in real-time (latency constraint < 50ms).

```
[Transaction Request] 
      │
      ▼
┌───────────┐         ┌───────────────┐
│ API Rule  │ ──────> │ Feature Store │ (Fetches historical/aggregate profile metrics)
│ Engine    │         └───────┬───────┘
└─────┬─────┘                 │
      │ (Fast Pass)           ▼
      │               ┌───────────────┐
      └─────────────> │ XGBoost Model │ (Online Inference Node)
                      └───────┬───────┘
                              │
                    ┌─────────┴─────────┐
             [Fraud] │           │ [Legit]
                     ▼           ▼
             ┌───────────┐   ┌───────────────┐
             │ Block/    │   │ Allow         │
             │ Challenge │   │ Transaction   │
             └───────────┘   └───────────────┘
```

#### 1. Requirements & Constraints
*   **Latency:** Hard limit of 50ms per transaction. Must use lightweight models or cached feature lookups.
*   **High Class Imbalance:** Fraud transactions typically represent < 0.1% of dataset.

#### 2. Feature Engineering & Feature Store
*   **Real-time Features:** Transaction amount, geographic distance from last transaction, time elapsed since last transaction.
*   **Aggregate Profile Features (from Feature Store):** Number of transactions in the last 24 hours, average transaction amount in the last 30 days.

#### 3. Handling Class Imbalance
*   **Resampling:** Downsample major class (legit transactions) combined with SMOTE (Synthetic Minority Over-sampling Technique) on minority class.
*   **Algorithmic:** Use class-weights (e.g., `scale_pos_weight` in XGBoost) to penalize false negatives more heavily.
*   **Loss Functions:** Use Focal Loss to focus training on hard-to-classify samples.

#### 4. Modeling & Inference
*   **Model Selection:** XGBoost or LightGBM. They offer exceptional latency-performance characteristics compared to deep neural networks for tabular data.
*   **Fallback Mechanism:** If feature store query times out, fallback to a heuristic rules-engine.

#### 5. Evaluation Metrics
*   **Do NOT use Accuracy:** High accuracy is trivial on imbalanced datasets (predicting all legit transactions yields 99.9% accuracy).
*   **Primary Metrics:**
    *   **Precision-Recall AUC (PR-AUC):** More informative than ROC-AUC because it focuses on the performance of the minority fraud class.
    *   **Recall at 99% Precision:** We want to catch as much fraud as possible while maintaining a low false-positive rate (to protect user experience).
