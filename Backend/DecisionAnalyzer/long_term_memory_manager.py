import os
import json
import glob
from openai import OpenAI
import datetime

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ Missing OPENAI_API_KEY environment variable.")

client = OpenAI()

# Dynamically target the DecisionAnalyzer/Data directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)

LOG_FILE = os.path.join(DATA_DIR, "chat_log.txt")
SUMMARY_FILE = os.path.join(DATA_DIR, "summary.json")
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
# Max size that designates a rotation
MAX_LOG_SIZE_BYTES = 500 * 1024  # 500 KB (Roughly 7,000 to 10,000 lines of dialogue)

# =====================================================================
#  UTILITIES

def load_profile() -> dict:
    """Loads profile.json from the disk. Raises FileNotFoundError if missing,
    and lets JSONDecodeError happen so we don't overwrite corrupt data.
    """
    if not os.path.exists(PROFILE_FILE):
        raise FileNotFoundError(f"❌ Critical error: '{PROFILE_FILE}' missing. System cannot sync.")
    
    # Let JSONDecodeError raise naturally to stop script 
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profile(profile_data: dict):
    """Saves profile.json to disk using UTF-8 encoding to support unicode characters."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)

def load_summary() -> dict:
    """Loads existing long-term summary from disk. Raises FileNotFoundError if missing,
    and lets JSONDecodeError propagate happen so we don't overwrite corrupt data.
    """
    if not os.path.exists(SUMMARY_FILE):
        raise FileNotFoundError(f"❌ Critical error: '{SUMMARY_FILE}' missing. System cannot sync.")
        
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_summary(summary: dict):
    """Saves summary.json to disk using UTF-8 encoding to support unicode characters."""
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

def rotate_logs():
    """Checks the size of chat_log.txt in Data/. If it exceeds the maximum size,
    archives it inside Data/ to keep parsing fast.
    """
    if not os.path.exists(LOG_FILE):
        return

    file_size = os.path.getsize(LOG_FILE)
    if file_size < MAX_LOG_SIZE_BYTES:
        return  # No rotation needed

    print("📁 Main log file size threshold exceeded. Initiating rotation...")
    
    # 1. Search for existing archives strictly inside DATA_DIR
    archive_pattern = os.path.join(DATA_DIR, "chat_log_archive_*.txt")
    existing_archives = glob.glob(archive_pattern)
    archive_index = len(existing_archives) + 1
    
    # 2. Build full target path inside DATA_DIR
    archive_path = os.path.join(DATA_DIR, f"chat_log_archive_{archive_index}.txt")
    
    try:
        # Rename the log file inside Data/
        os.rename(LOG_FILE, archive_path)
        
        # Seed a brand new, empty log file
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("--- New Log Segment Initialized ---\n\n")
            
        print(f"📦 Archival successful. Records moved to: {archive_path}")
    except OSError as e:
        print(f"❌ Log rotation failed: {e}")

# =====================================================================
# DUAL-LAYER CONSOLIDATION SYSTEM

def consolidate_long_term_memory():
    if not os.path.exists(LOG_FILE):
        print("No chat logs found to consolidate.")
        return

    print("Cortana is extracting long-term summary from your chat logs...")

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        raw_logs = f.read()

    current_summary = load_summary()
    current_profile = load_profile()

    consolidation_prompt = f"""You are the long-term memory optimization engine for Cortana. 
Your task is to review the raw chronological chat logs between the user and Cortana, extract critical high-level updates about the user's life, and merge them into the existing summary database.

CRITICAL OBJECTIVE:
As Cortana learns more about the user (their evolving worldview, new interests, completed goals, updated relationship standards, or changes in academic/career timelines), she must dynamically update and overwrite the profile database to keep it free from outdated informtation and 
to keep it completely true to who the user is becoming. Do not update/overwrite a particular section if the user is showing signs of lying to themselves, making excuses, acting emotionally, or anything that can stop them from being true to themselves.
Note: If no change has occurred there 


1. PROFILE DATABASE (Core Identity, Static-leaning but evolving):
- Update 'core_values' if they display a shift in philosophy.
- Update 'operating_principles' if their execution methods change.
- Update 'interests' if they pick up new games, books, anime, or drop old ones.
- Update 'relationship_boundaries' based on recent relational experiences or realizations.
- Update 'current_long_term_goals' as they make progress or shift direction.
- Update the 'meta' field (specifically 'last_updated' to the current year/date if changes are made).
- Update the 'personality' field as they display new stable traits, temperaments, humors, or behavioral patterns.
- Update the 'character_evolution' field as the user displays breakthroughs in character development, mindset changes, or core value changes.

2. Summary DATABASE (Recent milestones and short-to-mid term tracking):
- Capture specific ongoing details (e.g., specific assignments, interview tracks, current gym splits, temporary setbacks). dynamically update and overwrite as needed to prevent outdated information. 

EXISTING LONG-TERM SUMMARY DATABASE:
{json.dumps(current_summary, indent=2)}

RAW CHAT LOGS TO PROCESS:
{raw_logs}

OUTPUT INSTRUCTION:
You must return a single JSON object containing exactly three top-level keys:
- "changes": A list of objects detailing every modification made. Each object MUST have:
    * "field": The specific field or category changed (e.g., "core_values", "interests", "summary").
    * "action": Either "added", "updated", or "removed".
    * "details": A short summary of the specific piece of data changed.
    * "reasoning": The explicit rationale or trigger from the chat logs.
- "updated_profile": The complete profile object matching the schema.
- "updated_summary": The complete summary object matching the schema.

If no changes are detected, return an empty list [] for "changes".
Do not alter keys, omit fields, or include Markdown code blocks/text commentary. Return ONLY the raw JSON object."""

    try:
        # Query model
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": consolidation_prompt}],
            temperature=0.2
        )
        # Get response, parse format, and update memory
        response_text = completion.choices[0].message.content.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        payload = json.loads(response_text)
        
        # extract new profile and summary from payload. Second parameter is just default value.
        updated_profile = payload.get("updated_profile", current_profile)
        updated_summary = payload.get("updated_summary", current_summary)
        # Get changes
        changes_list = payload.get("changes", [])

        save_summary(updated_summary)
        save_profile(updated_profile)
        print("Long-term memory synchronization complete.")
        print("profile.json has been dynamically updated and evolved.")
        print("summary.json has been calibrated.")


        # --- TERMINAL LOG FORMATTER ---
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n\033[1;33m[{timestamp}] [MEMORY_MGR] 🔄 DUAL-LAYER SYNCHRONIZATION COMPLETE\033[0m")
        print("=" * 80)
        
        if not changes_list:
            print("\033[90m  No modifications detected during this session.\033[0m")
        else:
            for change in changes_list:
                field = change.get("field", "unknown")
                action = change.get("action", "modified")
                details = change.get("details", "")
                reason = change.get("reasoning", "")
                
                # Format: "core_values - added: React Development | reasoning: User is building a GUI"
                print(f"🔹 \033[1m{field}\033[0m - \033[36m{action}\033[0m: {details} | \033[90mreasoning:\033[0m {reason}")
                
        print("-" * 80)
        print("\033[32m✔ Databases synced and flushed to disk successfully.\033[0m")
        print("=" * 80 + "\n")
        
        # Run log cleanup directly after a successful consolidation pass
        rotate_logs()

    except Exception as e:
        print(f"❌ Profile/Memory consolidation failed: {e}")

if __name__ == "__main__":
    consolidate_long_term_memory()