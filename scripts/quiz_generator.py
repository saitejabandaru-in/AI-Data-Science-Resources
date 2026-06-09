#!/usr/bin/env python3
import sys
import random
import argparse
import datetime
import urllib.parse
import hashlib
import base64
import json

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

def generate_svg_badge(name, date_str):
    """Generates a beautiful personalized SVG certificate badge."""
    svg_content = f"""<svg width="600" height="400" viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
    <!-- Dark Blue Premium Background -->
    <rect width="600" height="400" fill="#1C2B36" rx="15" />
    
    <!-- Outer Border -->
    <rect x="15" y="15" width="570" height="370" fill="none" stroke="#F59E0B" stroke-width="3" rx="10" />
    <!-- Inner Fine Border -->
    <rect x="22" y="22" width="556" height="356" fill="none" stroke="#F59E0B" stroke-width="1" rx="8" opacity="0.6"/>

    <!-- Decorative Top Accent -->
    <path d="M 270 23 L 330 23 L 300 40 Z" fill="#F59E0B" />
    
    <!-- Header Title -->
    <text x="300" y="70" font-family="'Inter', 'Helvetica', sans-serif" font-size="20" fill="#E6EEF3" font-weight="bold" text-anchor="middle" letter-spacing="3">CERTIFICATE OF COMPLETION</text>
    
    <text x="300" y="110" font-family="'Inter', 'Helvetica', sans-serif" font-size="14" fill="#9CA3AF" text-anchor="middle">This is proudly presented to</text>
    
    <!-- Recipient Name -->
    <text x="300" y="160" font-family="'Inter', 'Helvetica', sans-serif" font-size="28" fill="#F59E0B" font-weight="bold" text-anchor="middle" letter-spacing="1">{name}</text>
    
    <line x1="150" y1="180" x2="450" y2="180" stroke="#F59E0B" stroke-width="1" opacity="0.4" />
    
    <!-- Course Description -->
    <text x="300" y="220" font-family="'Inter', 'Helvetica', sans-serif" font-size="14" fill="#E6EEF3" text-anchor="middle">For successfully mastering the core modules of</text>
    <text x="300" y="245" font-family="'Inter', 'Helvetica', sans-serif" font-size="16" fill="#E6EEF3" font-weight="bold" text-anchor="middle">SQL, Python, &amp; Machine Learning Curriculum</text>
    
    <!-- Details & Verification -->
    <text x="75" y="310" font-family="'Inter', 'Helvetica', sans-serif" font-size="10" fill="#9CA3AF" text-anchor="start">ISSUED BY:</text>
    <text x="75" y="325" font-family="'Inter', 'Helvetica', sans-serif" font-size="11" fill="#E6EEF3" font-weight="bold" text-anchor="start">saitejabandaru.com</text>
    <text x="75" y="345" font-family="'Inter', 'Helvetica', sans-serif" font-size="10" fill="#9CA3AF" text-anchor="start">AUTHORIZED SIGNATURE:</text>
    <text x="75" y="360" font-family="'Inter', 'Helvetica', sans-serif" font-size="11" fill="#F59E0B" font-style="italic" text-anchor="start">Sai Teja Bandaru</text>
    
    <text x="525" y="310" font-family="'Inter', 'Helvetica', sans-serif" font-size="10" fill="#9CA3AF" text-anchor="end">DATE COMPLETED:</text>
    <text x="525" y="325" font-family="'Inter', 'Helvetica', sans-serif" font-size="11" fill="#E6EEF3" font-weight="bold" text-anchor="end">{date_str}</text>
    
    <!-- Legal Disclaimer Note -->
    <text x="300" y="380" font-family="'Inter', 'Helvetica', sans-serif" font-size="8" fill="#9CA3AF" opacity="0.6" text-anchor="middle">Disclaimer: Non-academic self-study course verification. Does not constitute a formal degree or license.</text>
    
    <!-- Decorative Stamp Graphic -->
    <circle cx="300" cy="315" r="28" fill="#F59E0B" opacity="0.1" />
    <circle cx="300" cy="315" r="24" fill="none" stroke="#F59E0B" stroke-dasharray="4" stroke-width="1.5" />
    <text x="300" y="319" font-family="'Inter', 'Helvetica', sans-serif" font-size="9" fill="#F59E0B" font-weight="bold" text-anchor="middle">VERIFIED</text>
</svg>"""
    try:
        with open("AI_Data_Science_Badge.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print("\n🎨 Generated a personalized SVG badge: [AI_Data_Science_Badge.svg](file://AI_Data_Science_Badge.svg)")
    except Exception as e:
        print(f"\n⚠️ Could not save SVG badge file: {e}")

def generate_verification_token(name, date_str, score):
    """Generates a cryptographically verifiable token."""
    name_clean = name.strip()
    date_clean = date_str.strip()
    salt = "AI_DATA_SCIENCE_QUEST_SALT_2026"
    
    # Calculate sha256 hash
    hash_input = f"{name_clean}|{date_clean}|{score}|{salt}"
    signature = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    # Create JSON payload
    payload = {
        "name": name_clean,
        "date": date_clean,
        "score": f"{score}/9",
        "signature": signature
    }
    
    # Encode as Base64 string
    payload_json = json.dumps(payload)
    token = base64.b64encode(payload_json.encode('utf-8')).decode('utf-8')
    return token

def generate_markdown_certificate(name, date_str, verification_token):
    """Generates a CERTIFICATE.md file for the user."""
    cert_content = f"""# 🏆 Certificate of Completion

Presented to: **{name}**  
Date of Achievement: **{date_str}**
Issued By: **[saitejabandaru.com](https://saitejabandaru.com)**
Authorized Signature: **Sai Teja Bandaru** (Founder & Instructor)

---

### 🎓 Modules Mastered
- **Advanced SQL Database Systems:** Logical Execution Order, Window Functions, Query Optimization.
- **Python & High-Performance Data Engineering:** Functional Decorators, Generators, Vectorization pipelines (Pandas & Polars).
- **Core Machine Learning & Deep Architectures:** Statistical Math, Tree-based Ensembles, Gradient Descent, Transformers, and Retrieval-Augmented Generation (RAG).

### 🛡️ Verified Achievement
This certificate verifies successful completion of the comprehensive technical examination hosted at [saitejabandaru-in/AI-Data-Science-Resources](https://github.com/saitejabandaru-in/AI-Data-Science-Resources).

> ⚠️ **Disclaimer Note:** This certificate is documentation of course completion and self-paced study validation for an open-source learning path. It does not constitute a formal academic degree, professional license, or accredited credential from any university or licensing body.

---
<div align="center">
  <img src="AI_Data_Science_Badge.svg" width="500" alt="Certificate Badge" />
</div>

<!-- VERIFICATION_TOKEN: {verification_token} -->
"""
    try:
        with open("CERTIFICATE.md", "w", encoding="utf-8") as f:
            f.write(cert_content)
        print("📝 Created your verification document: [CERTIFICATE.md](file://CERTIFICATE.md)")
    except Exception as e:
        print(f"⚠️ Could not save Markdown Certificate file: {e}")

def print_ascii_certificate(name):
    """Prints a beautiful ASCII art certificate border."""
    border = "║"
    width = 65
    print("\n" + "╔" + "═"*(width) + "╗")
    print(f"{border}{'':^{width}}{border}")
    print(f"{border}{'🏆  CERTIFICATE OF ACHIEVEMENT  🏆':^{width}}{border}")
    print(f"{border}{'':^{width}}{border}")
    print(f"{border}{'This is proudly presented to:':^{width}}{border}")
    print(f"{border}{name.upper():^{width}}{border}")
    print(f"{border}{'':^{width}}{border}")
    print(f"{border}{'For successfully completing the comprehensive examination':^{width}}{border}")
    print(f"{border}{'SQL, Python, and Machine Learning Curriculum':^{width}}{border}")
    print(f"{border}{'':^{width}}{border}")
    print(f"{border}{'AI & DATA SCIENCE RESOURCES':^{width}}{border}")
    print(f"{border}{'':^{width}}{border}")
    print("╚" + "═"*(width) + "╝")

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
    
    # Check if they passed (score >= 8 out of 9)
    if score >= 8:
        print("\n🌟 CONGRATULATIONS! You have passed the certification requirements! 🌟")
        try:
            name = input("Enter your name for the certificate: ").strip()
        except (KeyboardInterrupt, EOFError):
            name = "Graduate"
        if not name:
            name = "Graduate"
            
        date_str = datetime.date.today().strftime("%B %d, %Y")
        
        # Generate verification token
        verification_token = generate_verification_token(name, date_str, score)
        
        # Print and generate certificate files
        print_ascii_certificate(name)
        generate_svg_badge(name, date_str)
        generate_markdown_certificate(name, date_str, verification_token)
        
        # Generate LinkedIn parameters
        encoded_name = urllib.parse.quote_plus("AI & Data Science Core Curriculum")
        encoded_org = urllib.parse.quote_plus("AI Data Science Resources")
        encoded_url = urllib.parse.quote_plus("https://github.com/saitejabandaru-in/AI-Data-Science-Resources")
        
        linkedin_add_url = f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name={encoded_name}&organizationName={encoded_org}&certUrl={encoded_url}"
        linkedin_share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
        
        print("\n💼 SHARE YOUR ACHIEVEMENT ON LINKEDIN!")
        print("1. Add to LinkedIn Profile Certifications:")
        print(f"   👉 {linkedin_add_url}")
        print("2. Post a Share Announcement:")
        print(f"   👉 {linkedin_share_url}")
        
        print("\n🏆 JOIN THE OFFICIAL HALL OF FAME!")
        print("To add your name to the public repository Hall of Fame:")
        print("1. Commit your generated CERTIFICATE.md and AI_Data_Science_Badge.svg files.")
        print("2. Push your changes to a new branch and open a Pull Request (PR) to origin/main.")
        print("3. Our automated GitHub Verification Action will verify your certificate token and add you to the Hall of Fame!")
        print("\nNote: Make sure to commit the generated files to show your badge in your repo!")
    else:
        print("\n💡 You need at least 8 correct answers to earn the Certificate & LinkedIn Badge. Run again to retry!")
    print("\nKeep learning!\n")

def main():
    parser = argparse.ArgumentParser(description="Run an interactive AI and Data Science quiz in the terminal.")
    parser.add_argument(
        "-c", "--category", 
        choices=["sql", "python", "ml", "all"], 
        default="all", 
        help="Specify a category of questions (default: all)"
    )
    args = parser.parse_args()
    
    cat = "Machine Learning" if args.category == "ml" else args.category
    run_quiz(cat)

if __name__ == "__main__":
    main()
