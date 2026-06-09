#!/usr/bin/env python3
import sys
import os
import re
import base64
import json
import hashlib

def verify_token(token):
    try:
        # Decode base64
        payload_bytes = base64.b64decode(token.encode('utf-8'))
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        name = payload.get("name")
        date_str = payload.get("date")
        score_str = payload.get("score")
        signature = payload.get("signature")
        
        if not all([name, date_str, score_str, signature]):
            return None, "Missing fields in token payload."
            
        # Parse score
        score = int(score_str.split('/')[0])
        if score < 8:
            return None, f"Insufficient score: {score}/9. Need >= 8."
            
        # Re-calculate hash
        salt = "AI_DATA_SCIENCE_QUEST_SALT_2026"
        hash_input = f"{name}|{date_str}|{score}|{salt}"
        expected_sig = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        
        if signature != expected_sig:
            return None, "Signature mismatch. Invalid verification token."
            
        return payload, None
    except Exception as e:
        return None, f"Decoding error: {e}"

def main():
    cert_path = "CERTIFICATE.md"
    hof_path = "HALL_OF_FAME.md"
    
    if not os.path.exists(cert_path):
        print(f"Error: {cert_path} not found in this Pull Request.")
        sys.exit(1)
        
    with open(cert_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find verification token comment
    match = re.search(r"<!-- VERIFICATION_TOKEN:\s*([A-Za-z0-9+/=]+)\s*-->", content)
    if not match:
        print("Error: No verification token found in CERTIFICATE.md.")
        sys.exit(1)
        
    token = match.group(1)
    payload, err = verify_token(token)
    if err:
        print(f"Verification Failed: {err}")
        sys.exit(1)
        
    name = payload["name"]
    date_str = payload["date"]
    score_str = payload["score"]
    
    print(f"✅ Certificate verified successfully for {name} on {date_str} with score {score_str}!")
    
    # Check if HALL_OF_FAME.md exists, otherwise create it
    if not os.path.exists(hof_path):
        with open(hof_path, "w", encoding="utf-8") as f:
            f.write("# 🏆 Graduates Hall of Fame\n\nThis page celebrates the scholars who have conquered all six paths of the Grand Archive and passed the Certification Arena exam!\n\n---\n\n| Graduate | Date of Graduation | Score | Verification Status |\n| :--- | :--- | :--- | :--- |\n")
            
    with open(hof_path, "r", encoding="utf-8") as f:
        hof_content = f.read()
        
    # Check if already added
    if name in hof_content and date_str in hof_content:
        print(f"Graduate {name} is already registered in the Hall of Fame.")
        sys.exit(0)
        
    # Append to table
    new_row = f"| {name} | {date_str} | {score_str} | 🌟 Verified |\n"
    
    # If the file doesn't end with a newline, add one
    if not hof_content.endswith("\n"):
        hof_content += "\n"
        
    with open(hof_path, "a", encoding="utf-8") as f:
        f.write(new_row)
        
    print(f"🎉 Successfully added {name} to {hof_path}!")

if __name__ == "__main__":
    main()
