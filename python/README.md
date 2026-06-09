# 🐍 Python & Scientific Computing

Python is the lingua franca of data engineering, machine learning, and AI research. This module details core language concepts, Object-Oriented Programming (OOP), advanced execution patterns, and performance tuning techniques for large-scale data manipulation.

---

## 🗺️ Table of Contents
1. [Core Data Structures & Complexity](#1-core-data-structures--complexity)
2. [Object-Oriented Programming (OOP) & Dataclasses](#2-object-oriented-programming-oop--dataclasses)
3. [Advanced Patterns: Decorators, Generators, Context Managers](#3-advanced-patterns-decorators-generators-context-managers)
4. [High-Performance Scientific Computing (Pandas vs. Polars)](#4-high-performance-scientific-computing-pandas-vs-polars)

---

## 1. Core Data Structures & Complexity

Writing performant code begins with selecting the correct built-in data structure.

| Structure | Syntax | Ordering | Mutability | Average Access | Average Insertion | Common Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **List** | `[1, 2]` | Ordered | Mutable | $O(1)$ | $O(1)$ (append) | Storing sequences |
| **Tuple** | `(1, 2)` | Ordered | Immutable | $O(1)$ | N/A | Static coordinates, database keys |
| **Set** | `{1, 2}` | Unordered | Mutable | $O(1)$ | $O(1)$ | Membership testing, deduplication |
| **Dict** | `{'a': 1}`| Ordered* | Mutable | $O(1)$ | $O(1)$ | Key-value associative mapping |

*\*Note: Dictionaries maintain insertion order starting in Python 3.7+.*

---

## 2. Object-Oriented Programming (OOP) & Dataclasses

AI systems require robust engineering. Clean OOP structures make codebases modular and reusable.

### Abstract Base Classes (ABCs)
Enforce interfaces on child classes. Useful for defining common steps in model pipelines.

```python
from abc import ABC, abstractmethod

class BasePredictor(ABC):
    @abstractmethod
    def fit(self, X, y):
        """Train the model."""
        pass
    
    @abstractmethod
    def predict(self, X):
        """Output predictions."""
        pass
```

### Magic (Dunder) Methods
Enable built-in operators on custom objects.
- `__init__`: Constructor.
- `__repr__`: Official developer string representation.
- `__call__`: Allows instances of classes to be called as functions (e.g., PyTorch models).

### Modern Dataclasses (`@dataclass`)
Simplifies class definitions for structured data storage by automatically generating `__init__`, `__repr__`, and `__eq__`.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)  # frozen=True makes the instances immutable
class Hyperparameters:
    learning_rate: float = 1e-3
    batch_size: int = 64
    optimizer: str = "Adam"
    epochs: int = field(default=10, metadata={"help": "Number of passes"})
```

---

## 3. Advanced Patterns: Decorators, Generators, Context Managers

### 1. Decorators
Modify the behavior of functions or classes without permanently altering their code.

```python
import time
from functools import wraps

def time_execution(func):
    @wraps(func)  # Preserves target function's metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ {func.__name__} completed in {end - start:.4f}s")
        return result
    return wrapper

@time_execution
def train_dummy_model():
    time.sleep(1.5)  # Simulate model training
```

### 2. Generators
Functions that use `yield` instead of `return` to return an iterator that yields one item at a time.
*   **Memory Efficiency:** Crucial when reading large datasets (e.g., multi-gigabyte text files) that shouldn't load entirely into RAM.

```python
def stream_large_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()
```

### 3. Context Managers
Manage setup and teardown resources cleanly via the `with` statement.
*   Implemented using `__enter__` and `__exit__` methods, or the `@contextmanager` decorator.

---

## 4. High-Performance Scientific Computing (Pandas vs. Polars)

### Vectorization over Iteration
Never use `for` loops or `.apply()` in Pandas if a vectorized solution exists. Vectorized operations run in compiled C/C++ or Fortran.

```python
# 🛑 AVOID (Slow row-by-row iteration)
df['new_col'] = df.apply(lambda row: row['a'] * row['b'], axis=1)

# ✅ PREFER (Vectorized operation)
df['new_col'] = df['a'] * df['b']
```

### Downcasting Data Types
Saves RAM. Convert generic `float64` to `float32`, or strings to `category`.
```python
# Convert categorical strings to category
df['user_country'] = df['user_country'].astype('category')
```

### Polars: The Next Generation
Polars is a blazingly fast DataFrame library written in Rust. It utilizes:
1.  **Lazy Evaluation:** Optimization queries prior to execution.
2.  **No GIL constraints:** Fully multithreaded query plans.

```python
import polars as pl

# Expressing lazy pipeline (won't execute until collect() is called)
lazy_query = (
    pl.scan_csv("large_dataset.csv")
    .filter(pl.col("age") > 30)
    .group_by("occupation")
    .agg(pl.col("salary").mean())
)

# Runs execution with optimal Rust query planer
results = lazy_query.collect()
```
