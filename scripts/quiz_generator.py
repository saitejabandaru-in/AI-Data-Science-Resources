#!/usr/bin/env python3
import sys
import random
import argparse

# Define the question bank
QUESTIONS = [
    # SQL Questions
    {
        "category": "SQL",
        "question": "Which of the following window functions assigns rankings with gaps in numbering if there are ties?",
        "options": {
            "A": "ROW_NUMBER()",
            "B": "RANK()",
            "C": "DENSE_RANK()",
            "D": "LEAD()"
        },
        "answer": "B",
        "explanation": "RANK() leaves gaps in the ranking sequence when there are ties (e.g., 1, 2, 2, 4). DENSE_RANK() does not leave gaps (e.g., 1, 2, 2, 3), and ROW_NUMBER() always assigns a unique sequential integer regardless of ties."
    },
    {
        "category": "SQL",
        "question": "In the logical execution order of a standard SQL query, which clause is executed immediately AFTER the WHERE clause?",
        "options": {
            "A": "SELECT",
            "B": "HAVING",
            "C": "GROUP BY",
            "D": "ORDER BY"
        },
        "answer": "C",
        "explanation": "The logical query processing order is: FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT. Therefore, GROUP BY is executed immediately after WHERE."
    },
    {
        "category": "SQL",
        "question": "Which index type is most suitable for indexing multi-value fields such as JSONB or Array columns in PostgreSQL?",
        "options": {
            "A": "B-Tree Index",
            "B": "Hash Index",
            "C": "GIN (Generalized Inverted Index)",
            "D": "BRIN (Block Range Index)"
        },
        "answer": "C",
        "explanation": "GIN (Generalized Inverted Index) is designed for handling composite items where we want to index elements inside document/array structures. B-Tree is general-purpose, Hash is only for equality, and BRIN is for physically ordered data."
    },
    # Python Questions
    {
        "category": "Python",
        "question": "What is the average time complexity of searching for an element in a set in Python?",
        "options": {
            "A": "O(1)",
            "B": "O(log N)",
            "C": "O(N)",
            "D": "O(N log N)"
        },
        "answer": "A",
        "explanation": "Python sets are implemented as hash tables. On average, membership tests ('element in my_set') take O(1) constant time, making them highly efficient compared to list searches which take O(N) time."
    },
    {
        "category": "Python",
        "question": "Which decorator from the standard library is best used to preserve the original function name and docstring when writing a custom decorator?",
        "options": {
            "A": "@functools.lru_cache",
            "B": "@functools.wraps",
            "C": "@classmethod",
            "D": "@dataclass"
        },
        "answer": "B",
        "explanation": "@functools.wraps is a helper decorator that copies the metadata (name, docstring, arguments, etc.) of the decorated function back onto the wrapper function, preventing debugging headaches."
    },
    {
        "category": "Python",
        "question": "Which of the following operations is vectorized and therefore executed in fast compiled code (C/Rust) rather than Python bytecode?",
        "options": {
            "A": "df.apply(lambda row: row['a'] * row['b'], axis=1)",
            "B": "df['a'] * df['b']",
            "C": "[row[0] * row[1] for row in df.itertuples()]",
            "D": "df.iterrows()"
        },
        "answer": "B",
        "explanation": "df['a'] * df['b'] leverages Pandas/NumPy vectorization, applying arithmetic operations at the C-level. Using apply, iterrows, or list comprehensions falls back to slower Python-level loops."
    },
    # Machine Learning Questions
    {
        "category": "Machine Learning",
        "question": "L1 regularization (Lasso) differs from L2 regularization (Ridge) primarily because L1:",
        "options": {
            "A": "Penalizes the squared magnitude of coefficients.",
            "B": "Can shrink some coefficient weights all the way to absolute zero.",
            "C": "Is less robust to outliers.",
            "D": "Requires solving a non-convex optimization problem."
        },
        "answer": "B",
        "explanation": "L1 regularization adds a penalty equal to the absolute sum of the weights. This often drives coefficients to exactly zero, resulting in sparse models and serving as a feature selection tool. L2 regularization (Ridge) shrinks weights close to zero but rarely exactly to zero."
    },
    {
        "category": "Machine Learning",
        "question": "In the self-attention formula of the Transformer architecture, what is the purpose of dividing Query-Key dot products by the square root of key dimension (d_k)?",
        "options": {
            "A": "To ensure the output vectors are unit-normalized.",
            "B": "To prevent the softmax function from saturating and producing extremely small gradients.",
            "C": "To keep the learning rate stable across deep layers.",
            "D": "To project the keys into a lower-dimensional subspace."
        },
        "answer": "B",
        "explanation": "Without scaling, the dot products of high-dimensional queries and keys can grow very large. This pushes the softmax function into regions with extremely small gradients (saturating), making model training stall. Scaling by 1/sqrt(d_k) mitigates this."
    },
    {
        "category": "Machine Learning",
        "question": "When evaluating a binary classifier on a highly imbalanced dataset (e.g., 0.1% positive class), which metric is generally preferred over standard ROC-AUC?",
        "options": {
            "A": "Classification Accuracy",
            "B": "Precision-Recall AUC (PR-AUC)",
            "C": "F1-Score macro average",
            "D": "Specificity"
        },
        "answer": "B",
        "explanation": "ROC-AUC can look deceptively good on highly imbalanced data because it includes True Negatives in its calculation (via False Positive Rate). PR-AUC focuses exclusively on Precision and Recall, which isolates classifier performance on the rare positive class."
    }
]

def run_quiz(category=None):
    # Filter questions if a category is specified
    if category and category.lower() != "all":
        questions = [q for q in QUESTIONS if q["category"].lower() == category.lower()]
        if not questions:
            print(f"Error: Category '{category}' not found. Available: SQL, Python, Machine Learning")
            return
    else:
        questions = list(QUESTIONS)
        random.shuffle(questions)

    print("\n" + "="*60)
    print("🎓  AI & Data Science Knowledge Quiz CLI  🎓")
    print("="*60)
    print(f"Total Questions: {len(questions)}")
    print("Type A, B, C, or D to answer. Type 'exit' to quit.\n")

    score = 0
    for idx, q in enumerate(questions, 1):
        print(f"Question {idx}/{len(questions)} [{q['category']}]:")
        print(f"{q['question']}\n")
        
        # Sort keys to ensure A, B, C, D ordering
        for key in sorted(q["options"].keys()):
            print(f"  [{key}] {q['options'][key]}")
        
        print("")
        while True:
            try:
                user_choice = input("Your answer: ").strip().upper()
            except (KeyboardInterrupt, EOFError):
                print("\nQuiz terminated. Goodbye!")
                return
                
            if user_choice == "EXIT":
                print("\nExiting quiz...")
                break
            elif user_choice in ["A", "B", "C", "D"]:
                break
            else:
                print("Invalid input. Please enter A, B, C, or D (or 'exit').")

        if user_choice == "EXIT":
            break

        if user_choice == q["answer"]:
            print("\n✅ Correct! 🎉")
            score += 1
        else:
            print(f"\n❌ Incorrect. The correct answer was [{q['answer']}]")
            
        print("-" * 50)
        print(f"Explanation:\n{q['explanation']}")
        print("=" * 60 + "\n")

    print(f"🏆 Quiz Finished! Final Score: {score}/{len(questions)} ({score/len(questions)*100:.1f}%)")
    print("Keep learning!\n")

def main():
    parser = argparse.ArgumentParser(description="Run an interactive AI and Data Science quiz in the terminal.")
    parser.add_argument(
        "-c", "--category", 
        choices=["sql", "python", "ml", "all"], 
        default="all", 
        help="Specify a category of questions (default: all)"
    )
    args = parser.parse_args()
    
    # Map 'ml' to 'machine learning' in logic
    cat = "Machine Learning" if args.category == "ml" else args.category
    run_quiz(cat)

if __name__ == "__main__":
    main()
