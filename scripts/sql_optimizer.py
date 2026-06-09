#!/usr/bin/env python3
import sys
import time
import argparse

TEMPLATES = {
    "1": {
        "title": "Simple Filter Query",
        "sql": "SELECT name FROM users WHERE age > 21;",
        "description": "Demonstrates index scanning vs. sequential table scanning.",
        "nodes": [
            "└── [Physical Plan] Project (users.name)",
            "    └── Filter (users.age > 21)",
            "        └── Seq Scan on users  [Cost: High]"
        ],
        "optimized_nodes": [
            "└── [Physical Plan] Project (users.name)",
            "    └── Index Scan on users_age_idx (users.age > 21) [Cost: Low] [Filter Pushed Down]"
        ],
        "details": [
            "1. Parsing: Query parsed to AST nodes.",
            "2. Rewrite: Identified index available on column 'users.age'.",
            "3. Optimization: Replaced sequential table scan with high startup cost with an Index Scan, reducing cost metric from 45.2 to 2.1."
        ]
    },
    "2": {
        "title": "Join Query with Filter",
        "sql": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100;",
        "description": "Demonstrates filter pushdowns and nested loop vs. hash joins.",
        "nodes": [
            "└── [Physical Plan] Project (u.name, o.amount)",
            "    └── Filter (o.amount > 100)",
            "        └── Nested Loop Join (u.id = o.user_id)",
            "            ├── Seq Scan on users u",
            "            └── Seq Scan on orders o"
        ],
        "optimized_nodes": [
            "└── [Physical Plan] Project (u.name, o.amount)",
            "    └── Hash Join (u.id = o.user_id)  [Cost: Medium]",
            "        ├── Hash on users u  [Table size: Small]",
            "        └── Index Scan on orders o (o.amount > 100)  [Filter Pushed Down]"
        ],
        "details": [
            "1. Parsing: Query parsed to AST. Discovered join relation ON u.id = o.user_id.",
            "2. Filter Pushdown: Shifted `o.amount > 100` filter down to the orders table before performing the join, reducing row count.",
            "3. Join Selection: Replaced O(N*M) Nested Loop with O(N+M) Hash Join by building a hash table of the smaller 'users' dataset in memory."
        ]
    },
    "3": {
        "title": "Aggregation & Grouping Query",
        "sql": "SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5;",
        "description": "Demonstrates hash aggregation vs. sort aggregation.",
        "nodes": [
            "└── [Physical Plan] Filter (COUNT(*) > 5)",
            "    └── Sort (employees.department)",
            "        └── Group Aggregate (COUNT(*))",
            "            └── Seq Scan on employees"
        ],
        "optimized_nodes": [
            "└── [Physical Plan] Filter (COUNT(*) > 5)",
            "    └── Hash Aggregate (GROUP BY department, COUNT(*)) [Cost: Low]",
            "        └── Seq Scan on employees"
        ],
        "details": [
            "1. Parsing: Query parsed into grouping and aggregation structures.",
            "2. Optimization: Replaced sorting-based grouping with Hash Aggregation. Instead of sorting all rows in O(N log N) time, the engine aggregates rows into a hash table in O(N) linear time."
        ]
    }
}

def animate_plan(lines, delay=0.15):
    for line in lines:
        print(line)
        time.sleep(delay)

def run_optimizer():
    print("="*60)
    print("🎓  SQL Query Execution Plan Optimizer Simulator  🎓")
    print("="*60)
    print("Welcome! SQL engines optimize queries before executing them. This simulator\n"
          "shows how AST parsers, cost estimators, and physical planners rewrite your SQL\n"
          "statements to save CPU time and memory.\n")
          
    while True:
        print("Select a Query Template to Plan:")
        for key, value in TEMPLATES.items():
            print(f"  [{key}] {value['title']}: {value['sql']}")
        print("  [Q] Exit Simulator\n")
        
        choice = input("Enter choice: ").strip().upper()
        if choice == 'Q':
            print("Exiting SQL Optimizer Simulator. Goodbye!")
            break
            
        if choice not in TEMPLATES:
            print("\n⚠️ Invalid choice. Please try again.\n")
            continue
            
        template = TEMPLATES[choice]
        print("\n" + "="*50)
        print(f"📖 Query: {template['sql']}")
        print(f"ℹ️ {template['description']}")
        print("="*50)
        
        # 1. Show Unoptimized Plan
        print("\n⏳ 1. Initial Naive Physical Plan (Unoptimized):")
        print("-" * 50)
        animate_plan(template['nodes'])
        print("-" * 50)
        
        time.sleep(1.0)
        
        # 2. Show Optimization Process
        print("\n⚡ 2. Optimization Phase (Rewriting & Planning):")
        for detail in template['details']:
            print(f"  * {detail}")
            time.sleep(0.8)
            
        time.sleep(1.0)
        
        # 3. Show Optimized Plan
        print("\n🚀 3. Optimized Physical Plan (High Efficiency):")
        print("-" * 50)
        animate_plan(template['optimized_nodes'])
        print("-" * 50)
        print("\n" + "="*50 + "\n")
        
        input("Press Enter to continue...")
        print("\n")

def main():
    parser = argparse.ArgumentParser(description="Run the interactive SQL execution plan optimizer simulator.")
    args = parser.parse_args()
    run_optimizer()

if __name__ == "__main__":
    main()
