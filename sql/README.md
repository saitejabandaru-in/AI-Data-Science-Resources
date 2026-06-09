# 📊 SQL Core & Advanced Notes

SQL is the foundational language of data retrieval, transformation, and analysis. This module covers core relational engine concepts, advanced window functions, and query optimization strategies crucial for database engineering and data science.

---

## 🗺️ Table of Contents
1. [SQL Query Execution Order](#1-sql-query-execution-order)
2. [Advanced Window Functions](#2-advanced-window-functions)
3. [CTEs vs. Subqueries vs. Temporary Tables](#3-ctes-vs-subqueries-vs-temporary-tables)
4. [Query Optimization & Performance Tuning](#4-query-optimization--performance-tuning)

---

## 1. SQL Query Execution Order

While SQL code is written starting with the `SELECT` keyword, the database engine executes commands in a logical order that dictates variable availability and performance behaviors.

### Written Order vs. Logical Execution Order

```
[Written Order]                      [Logical Execution Order]
1. SELECT                            1. FROM & JOIN (Loads & compiles dataset)
2. FROM & JOIN                       2. ON (Applies join filters)
3. WHERE                             3. WHERE (Filters rows before grouping)
4. GROUP BY                          4. GROUP BY (Aggregates data)
5. HAVING                            5. HAVING (Filters aggregated groups)
6. WINDOW                            6. SELECT (Selects columns & calculates functions)
7. ORDER BY                          7. DISTINCT (Removes duplicates)
8. LIMIT / OFFSET                    8. ORDER BY (Sorts results)
                                     9. LIMIT / OFFSET (Slices rows)
```

> [!WARNING]
> Because `SELECT` is executed *after* `WHERE` and `HAVING`, column aliases defined in your `SELECT` clause cannot be referenced in `WHERE` or `HAVING` filters in standard SQL.

---

## 2. Advanced Window Functions

Window functions perform calculations across a set of table rows that are somehow related to the current row, without collapsing them into a single row like `GROUP BY` does.

### Core Syntax
```sql
FUNCTION() OVER (
    PARTITION BY column_a
    ORDER BY column_b
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### Row Numbering & Ranking Comparison
Given a dataset with duplicate scores:
- `ROW_NUMBER()`: Assigns a unique sequential integer (e.g., 1, 2, 3, 4).
- `RANK()`: Assigns ranking, leaving gaps for ties (e.g., 1, 2, 2, 4).
- `DENSE_RANK()`: Assigns ranking without leaving gaps (e.g., 1, 2, 2, 3).

| Employee | Department | Salary | ROW_NUMBER() | RANK() | DENSE_RANK() |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Alice | Engineering | 150,000 | 1 | 1 | 1 |
| Bob | Engineering | 120,000 | 2 | 2 | 2 |
| Charlie | Engineering | 120,000 | 3 | 2 | 2 |
| David | Engineering | 100,000 | 4 | 4 | 3 |

### Boundary Tracking (`LEAD` & `LAG`)
Accesses data from another row in the same result set without using self-joins.
- `LAG(column, offset)`: Retrieves a value from the row *before* the current row. Excellent for month-over-month growth calculations.
- `LEAD(column, offset)`: Retrieves a value from the row *after* the current row.

```sql
SELECT 
    revenue_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY revenue_month) as prev_month_revenue,
    monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY revenue_month) as net_change
FROM sales_records;
```

---

## 3. CTEs vs. Subqueries vs. Temporary Tables

Selecting the correct temporary storage mechanism depends on scope, readability, and performance.

### 1. Common Table Expressions (CTEs)
Defined using the `WITH` clause. They exist only during the execution of the query.
*   **Best for:** Code readability, hierarchical query design, and recursive tasks (e.g., parsing org charts).
*   **Performance Note:** Historically, PostgreSQL and other RDBMS materialized CTEs (creating temp tables in memory). Modern optimizers inline CTEs, making them perform similarly to subqueries.

### 2. Subqueries
Nested inside other queries.
*   **Best for:** Short, inline filters (e.g., `WHERE salary > (SELECT AVG(salary) FROM employees)`).
*   **Disadvantage:** Can lead to unreadable "spaghetti SQL" if nested deeply.

### 3. Temporary Tables (`CREATE TEMP TABLE`)
Physically instantiated tables stored in memory or temporary disk segments that last for the duration of the session.
*   **Best for:** Complex multi-step processing pipelines where intermediate results are reused multiple times, or require indexing.

---

## 4. Query Optimization & Performance Tuning

High-performance SQL requires optimizing how the execution engine reads and processes tables.

### Indexing: The B-Tree and Beyond
Indexes are lookup structures that prevent full table scans.
*   **B-Tree Indexes:** Default. Ideal for equality operations (`=`) and range queries (`>`, `<`).
*   **Hash Indexes:** Excellent for exact matches (`=`) but cannot perform range scans or sort values.
*   **GIN (Generalized Inverted Index) Indexes:** Perfect for multi-value columns (JSONB, Arrays) and text search.

### Partitioning
Dividing large tables into smaller, physical tables behind the scenes.
*   **Range Partitioning:** (e.g., by Transaction Date).
*   **List Partitioning:** (e.g., by Country Code).
*   **Hash Partitioning:** Distributes rows evenly based on a hash key.

### Reading Execution Plans (`EXPLAIN ANALYZE`)
Prepend `EXPLAIN ANALYZE` to your query to see how the engine plans and executes it.

Key operations to audit:
*   **Seq Scan (Sequential Scan):** The engine is reading the entire table from disk. Bad for large tables; solve by adding an index.
*   **Index Scan:** The engine uses an index to locate rows. Very fast.
*   **Hash Join vs. Nested Loop:**
    *   *Nested Loop:* Compares every row of table A with table B. Fine for small datasets, terrible for large ones.
    *   *Hash Join:* Builds a hash table in memory of the smaller relation, then scans the larger relation. Highly efficient.
