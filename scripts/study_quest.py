#!/usr/bin/env python3
import os
import json
import time
import sys
import random

SAVE_FILE = ".study_quest.json"

# Quest definitions
QUESTS = {
    "1": {
        "title": "🛡️ The Relational Rift",
        "description": "Master SQL query execution, window functions, and indexing (Read sql/README.md).",
        "xp": 100,
        "title_reward": "SQL Knight",
        "question": "Which SQL window function assigns rankings to rows WITHOUT leaving gaps in numbers when ties occur?",
        "answer": "DENSE_RANK",
        "options": ["A) RANK()", "B) DENSE_RANK()", "C) ROW_NUMBER()", "D) LEAD()"],
        "correct_option": "B"
    },
    "2": {
        "title": "🐍 Pythonic Pathways",
        "description": "Understand advanced Python data structures complexity and OOP (Read python/README.md).",
        "xp": 120,
        "title_reward": "Python Sage",
        "question": "What is the average time complexity to check if an item exists inside a Python 'set'?",
        "answer": "O(1)",
        "options": ["A) O(N)", "B) O(log N)", "C) O(1)", "D) O(N log N)"],
        "correct_option": "C"
    },
    "3": {
        "title": "🧬 Gradient Descent Ascent",
        "description": "Learn deep learning, backpropagation, self-attention, and RAG architectures (Read machine-learning/README.md).",
        "xp": 150,
        "title_reward": "Gradient Guru",
        "question": "Which PEFT method injects trainable low-rank decomposition matrices into attention layers while freezing base weights?",
        "answer": "LoRA",
        "options": ["A) QLoRA", "B) Prefix Tuning", "C) LoRA", "D) Full Fine-Tuning"],
        "correct_option": "C"
    },
    "4": {
        "title": "⚡ The Benchmark Battle",
        "description": "Run the scientific computing speed benchmarks (Execute scripts/benchmark_lab.py).",
        "xp": 80,
        "title_reward": "Rust Rider",
        "question": "Which blazingly-fast Rust-based DataFrame library utilizes lazy evaluation and avoids GIL constraints?",
        "answer": "Polars",
        "options": ["A) Pandas", "B) NumPy", "C) Dask", "D) Polars"],
        "correct_option": "D"
    },
    "5": {
        "title": "🏰 The System Architect Trials",
        "description": "Review ML System Design cases like Fraud Detection and Recommendation pipelines (Read interviews/README.md).",
        "xp": 200,
        "title_reward": "System Shaper",
        "question": "What is the very first stage in a large-scale industrial Recommendation System funnel?",
        "answer": "Retrieval",
        "options": ["A) Ranking", "B) Retrieval / Candidate Generation", "C) Re-ranking", "D) Deduplication"],
        "correct_option": "B"
    }
}

# Mock Leaderboard data
MOCK_LEADERBOARD = [
    {"name": "Andrej Karpathy", "level": 15, "xp": 4800, "title": "Neural Overlord"},
    {"name": "Andrew Ng", "level": 12, "xp": 3600, "title": "Gradient Sovereign"},
    {"name": "Yann LeCun", "level": 10, "xp": 2800, "title": "Convolution Wizard"},
]

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    
    # Default character sheet
    return {
        "name": "Novice Developer",
        "level": 1,
        "xp": 0,
        "title": "Code Squire",
        "completed_quests": [],
        "last_daily": ""
    }

def save_game(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving progress: {e}")

def get_next_level_xp(level):
    # Level formula: Level 1 -> 100 XP, Level 2 -> 250 XP, Level 3 -> 450 XP, etc.
    return int(100 * (level ** 1.5))

def add_xp(data, amount):
    data["xp"] += amount
    print(f"\n✨ +{amount} XP Gained!")
    
    # Check level up loop
    while True:
        next_xp = get_next_level_xp(data["level"])
        if data["xp"] >= next_xp:
            data["xp"] -= next_xp
            data["level"] += 1
            print(f"🎉 LEVEL UP! You reached Level {data['level']}! 🎉")
            # Upgrade base title depending on level milestones
            if data["level"] == 3:
                data["title"] = "AI Journeyman"
            elif data["level"] == 5:
                data["title"] = "Data Wizard"
            elif data["level"] == 8:
                data["title"] = "Neural Alchemist"
            elif data["level"] >= 10:
                data["title"] = "AI Overlord"
            print(f"Your base title upgraded to: {data['title']}")
        else:
            break

def view_character(data):
    print("\n" + "="*50)
    print("👤  STUDY RPG CHARACTER SHEET  👤")
    print("="*50)
    print(f"Name:         {data['name']}")
    print(f"Title:        🛡️ {data['title']}")
    print(f"Level:        {data['level']}")
    next_xp = get_next_level_xp(data["level"])
    progress_bar = int((data["xp"] / next_xp) * 20)
    bar_str = "█" * progress_bar + "░" * (20 - progress_bar)
    print(f"XP Progress:  [{bar_str}] {data['xp']}/{next_xp} XP")
    print(f"Completed Quests: {len(data['completed_quests'])}/{len(QUESTS)}")
    print("="*50 + "\n")

def view_quest_board(data):
    print("\n" + "="*60)
    print("📋  THE GRAND STUDY QUEST BOARD  📋")
    print("="*60)
    for q_id, q_info in QUESTS.items():
        status = "✅ [COMPLETED]" if q_id in data["completed_quests"] else "❌ [INCOMPLETE]"
        print(f"Quest #{q_id}: {q_info['title']} - {status}")
        print(f"   Objective: {q_info['description']}")
        print(f"   Rewards:   {q_info['xp']} XP | Special Title: '{q_info['title_reward']}'")
        print("-" * 60)
    print("\n")

def verify_quest(data):
    incomplete = [q_id for q_id in QUESTS if q_id not in data["completed_quests"]]
    if not incomplete:
        print("\n🏆 Congratulations! You have completed all study quests on the board!")
        return
        
    print("\nSelect an incomplete Quest to submit verification:")
    for q_id in incomplete:
        print(f"  [{q_id}] {QUESTS[q_id]['title']}")
    
    choice = input("Enter Quest number (or 'exit' to cancel): ").strip()
    if choice in incomplete:
        quest = QUESTS[choice]
        print(f"\n🧪 VERIFICATION TESTING FOR: {quest['title']}")
        print("Answer this question to verify your study objectives:")
        print(f"\n{quest['question']}")
        for opt in quest['options']:
            print(f"  {opt}")
            
        ans = input("\nYour answer (A, B, C, or D): ").strip().upper()
        if ans == quest['correct_option']:
            print("\n✅ Verification Successful! You proved your mastery!")
            data["completed_quests"].append(choice)
            # Update title to the quest title reward
            data["title"] = quest["title_reward"]
            print(f"🏆 New Title Equipped: {quest['title_reward']}!")
            add_xp(data, quest["xp"])
            save_game(data)
        else:
            print("\n❌ Incorrect verification answer. Read the module again and return to retry!")
    elif choice.lower() != "exit":
        print("Invalid choice or quest already completed.")

def run_daily_challenge(data):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if data["last_daily"] == today:
        print("\n📅 You have already completed your Daily Check-in Challenge today! Return tomorrow.")
        return
        
    print("\n📅  DAILY STUDY QUEST CHECK-IN  📅")
    print("Data Science is built on daily habits! Answer this quick question for 15 XP:")
    
    # Simple randomized logic question
    num1 = random.randint(2, 9)
    num2 = random.randint(2, 9)
    print(f"If a dataset has {num1} samples in class A and {num2} in class B, what is the total sample size?")
    try:
        ans = int(input("Your Answer: ").strip())
    except ValueError:
        ans = -1
        
    if ans == (num1 + num2):
        print("\n✅ Correct Daily Habit check-in!")
        data["last_daily"] = today
        add_xp(data, 15)
        save_game(data)
    else:
        print("\n❌ Incorrect. Try again!")

def view_leaderboard(data):
    # Merge user data with mock leaderboard
    combined = list(MOCK_LEADERBOARD)
    # Estimate total XP accumulated across levels
    total_user_xp = data["xp"]
    for l in range(1, data["level"]):
        total_user_xp += get_next_level_xp(l)
        
    combined.append({
        "name": f"{data['name']} (You)",
        "level": data["level"],
        "xp": total_user_xp,
        "title": data["title"]
    })
    
    # Sort by total XP
    combined.sort(key=lambda x: x["xp"], reverse=True)
    
    print("\n" + "="*60)
    print("🏆  GLOBAL STUDY LEADERBOARD  🏆")
    print("="*60)
    for rank, entry in enumerate(combined, 1):
        accent = "⭐️ " if "(You)" in entry["name"] else "  "
        print(f"{rank}. {accent}{entry['name']:<25} | Lvl {entry['level']:<2} | {entry['xp']:<4} Total XP | {entry['title']}")
    print("="*60 + "\n")

import datetime

def main():
    data = load_game()
    
    # Prompt for character name if default
    if data["name"] == "Novice Developer":
        print("="*55)
        print("🎮 Welcome to the AI & Data Science Study RPG! 🎮")
        print("="*55)
        name = input("Enter your hero character name: ").strip()
        if name:
            data["name"] = name
            save_game(data)
            
    while True:
        # Clear console (optional, clean prints preferred here)
        print("\n" + "⚔️  AI STUDY QUEST MENU  ⚔️")
        print("-" * 30)
        print("  [1] View Character Sheet")
        print("  [2] View Quest Board")
        print("  [3] Submit Quest Verification")
        print("  [4] Daily Habit Check-in")
        print("  [5] View Global Leaderboard")
        print("  [6] Rename Character")
        print("  [7] Exit Game")
        
        choice = input("\nAction: ").strip()
        
        if choice == "1":
            view_character(data)
        elif choice == "2":
            view_quest_board(data)
        elif choice == "3":
            verify_quest(data)
        elif choice == "4":
            run_daily_challenge(data)
        elif choice == "5":
            view_leaderboard(data)
        elif choice == "6":
            name = input("Enter new name: ").strip()
            if name:
                data["name"] = name
                save_game(data)
        elif choice == "7":
            print("\nSaving adventure progress... See you in the next study quest!")
            break
        else:
            print("Invalid command. Choose a number from 1 to 7.")

if __name__ == "__main__":
    main()
