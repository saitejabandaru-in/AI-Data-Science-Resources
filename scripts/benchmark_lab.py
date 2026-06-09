#!/usr/bin/env python3
import time
import random
import sys

# Try importing scientific libraries
try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import polars as pl
except ImportError:
    pl = None

def generate_mock_data(size=100000):
    print(f"⚙️ Generating {size:,} rows of mock transaction data...")
    data = []
    for i in range(size):
        data.append({
            "id": i,
            "amount": random.uniform(1.0, 1000.0),
            "tax_rate": random.uniform(0.05, 0.20)
        })
    return data

def run_pure_python_loop(data):
    start = time.perf_counter()
    results = []
    for row in data:
        results.append(row["amount"] * row["tax_rate"])
    end = time.perf_counter()
    return end - start

def run_pandas_apply(df):
    if df is None:
        return None
    start = time.perf_counter()
    # Row-by-row iteration using apply
    _ = df.apply(lambda row: row["amount"] * row["tax_rate"], axis=1)
    end = time.perf_counter()
    return end - start

def run_pandas_vectorized(df):
    if df is None:
        return None
    start = time.perf_counter()
    # Vectorized column multiplication
    _ = df["amount"] * df["tax_rate"]
    end = time.perf_counter()
    return end - start

def run_polars_vectorized(df_pl):
    if df_pl is None:
        return None
    start = time.perf_counter()
    # Polars optimized vectorized execution
    _ = df_pl.select(pl.col("amount") * pl.col("tax_rate"))
    end = time.perf_counter()
    return end - start

def main():
    print("="*70)
    print("⚡  AI & Data Science Lab: Scientific Computing Benchmark  ⚡")
    print("="*70)
    print("This lab compares the speed of calculations across raw Python loops,")
    print("Pandas (apply vs. vectorization), and Rust-powered Polars.\n")

    # Check dependencies
    missing_deps = []
    if not pd:
        missing_deps.append("pandas")
    if not pl:
        missing_deps.append("polars")
    
    if missing_deps:
        print("⚠️  Optional dependencies missing: " + ", ".join(missing_deps))
        print("To run the full suite, install them using: pip install pandas polars\n")

    # Generate data
    data = generate_mock_data(100000)
    
    # Setup DataFrames if packages are available
    df_pd = pd.DataFrame(data) if pd else None
    df_pl = pl.DataFrame(data) if pl else None
    
    print("\n🚀 Starting Benchmarks...")
    print("-" * 50)
    
    # 1. Pure Python Loop
    print("1. Running Pure Python for-loop...")
    py_time = run_pure_python_loop(data)
    print(f"   ⏱️ Completed in {py_time:.5f} seconds.")
    
    # 2. Pandas Apply
    pd_apply_time = None
    if df_pd is not None:
        print("2. Running Pandas .apply() (Row-by-Row iteration)...")
        pd_apply_time = run_pandas_apply(df_pd)
        print(f"   ⏱️ Completed in {pd_apply_time:.5f} seconds.")
    else:
        print("2. Skipping Pandas apply (pandas not installed).")

    # 3. Pandas Vectorized
    pd_vec_time = None
    if df_pd is not None:
        print("3. Running Pandas Vectorized column multiplication...")
        pd_vec_time = run_pandas_vectorized(df_pd)
        print(f"   ⏱️ Completed in {pd_vec_time:.5f} seconds.")
    
    # 4. Polars Vectorized
    pl_time = None
    if df_pl is not None:
        print("4. Running Polars Vectorized (Rust engine)...")
        pl_time = run_polars_vectorized(df_pl)
        print(f"   ⏱️ Completed in {pl_time:.5f} seconds.")
    else:
        print("4. Skipping Polars benchmark (polars not installed).")

    # Display results
    print("\n" + "="*70)
    print("🏆  BENCHMARK RESULTS DASHBOARD  🏆")
    print("="*70)
    print(f"{'Method / Runtime':<35} | {'Execution Time (s)':<20} | {'Speedup Factor':<15}")
    print("-" * 70)
    
    # Pure Python baseline
    print(f"{'1. Pure Python Loop (Baseline)':<35} | {py_time:<20.5f} | {'1.0x (Baseline)':<15}")
    
    # Pandas apply
    if pd_apply_time:
        factor = py_time / pd_apply_time
        print(f"{'2. Pandas .apply() (Row Loop)':<35} | {pd_apply_time:<20.5f} | {factor:<13.2f}x")
    
    # Pandas vectorized
    if pd_vec_time:
        factor = py_time / pd_vec_time
        print(f"{'3. Pandas Vectorized (C-level)':<35} | {pd_vec_time:<20.5f} | {factor:<13.2f}x")
        
    # Polars
    if pl_time:
        factor = py_time / pl_time
        print(f"{'4. Polars Vectorized (Rust-level)':<35} | {pl_time:<20.5f} | {factor:<13.2f}x")
        
    print("=" * 70)
    print("\n🧠 WHY THE DIFFERENCE?")
    print("1. Pure Python loops run on Python Bytecode interpreter (slow).")
    print("2. Pandas .apply() makes a Python function call for every single row (extremely slow).")
    print("3. Pandas Vectorized operations drop down to pre-compiled C/C++ loops (fast).")
    if pl_time:
        print("4. Polars optimizes query plans and runs multi-threaded loops in compiled Rust (blazingly fast!).")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
