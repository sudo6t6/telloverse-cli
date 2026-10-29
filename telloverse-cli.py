import sys
import time
import json
import argparse
requests = None

def get_session():
    try:
        import requests
        return requests
    except ImportError:
        print("[!] Error: The 'requests' library is not installed.")
        print("[!] Run: pip install requests")
        sys.exit(1)

def fetch_and_build_dataset(username):
    req = get_session()
    base_url = "https://tellonym.me/api"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Tellonym-Client": "web:3.204.0",
        "Content-Type": "application/json;charset=utf-8",
        "Referer": f"https://tellonym.me/{username}"
    }

    all_answers = []
    
    print(f"[*] Fetching profile data for u/{username}...")
    profile_url = f"{base_url}/profiles/name/{username}?limit=31"
    
    try:
        res = req.get(profile_url, headers=headers)
        if res.status_code == 404:
            print(f"[!] Error: User '{username}' not found.")
            return []
        elif res.status_code != 200:
            print(f"[!] Error fetching profile: HTTP {res.status_code}")
            return []

        data = res.json()
        user_id = data.get("id")
        display_name = data.get("displayName", username)
        initial_answers = data.get("answers", [])
        
        all_answers.extend(initial_answers)
        print(f"[+] Found profile: {display_name} (ID: {user_id})")
        print(f"[+] Retrieved initial {len(initial_answers)} tells.")

        if not initial_answers:
            print("[!] No public answers found for this user.")
            return all_answers

        
        page = 1
        while True:
            oldest_id = all_answers[-1]["id"]
            print(f"[*] Page {page}: Fetching tells older than ID {oldest_id}...")
            
            answers_url = f"{base_url}/answers/{user_id}?oldestId={oldest_id}&userId={user_id}&limit=100"
            
            resp = req.get(answers_url, headers=headers)
            if resp.status_code != 200:
                print(f"[!] Request stopped with status {resp.status_code}.")
                break
                
            page_data = resp.json()
            new_answers = page_data.get("answers", [])
            
            if not new_answers:
                print("[+] Reached the end of tells!")
                break
                
            all_answers.extend(new_answers)
            print(f"[+] Added {len(new_answers)} tells (Total collected: {len(all_answers)})")
            
            page += 1
            time.sleep(0.4)
            
    except Exception as e:
        print(f"[!] An error occurred during fetching: {e}")
        
    return all_answers

def export_to_jsonl(answers, username):
    output_file = f"{username}_dataset.jsonl"
    count = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for item in answers:
            tell_text = item.get("tell")
            answer_text = item.get("answer")
            
            if tell_text and answer_text:
                record = {
                    "tell": tell_text.strip(),
                    "answer": answer_text.strip()
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
                
    print(f"\n[✔] Successfully exported {count} training pairs to '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Tellonym Data Scraper & ML Dataset Generator")
    parser.add_argument("username", nargs="?", help="Tellonym username to scrape")
    args = parser.parse_args()

    target_user = args.username
    if not target_user:
        target_user = input("Enter Tellonym username: ").strip()

    if target_user:
        answers_data = fetch_and_build_dataset(target_user)
        if answers_data:
            export_to_jsonl(answers_data, target_user)
    else:
        print("[!] No username provided.")
