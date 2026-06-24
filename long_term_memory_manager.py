import os
import json
import glob
from openai import OpenAI

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("❌ Missing OPENAI_API_KEY environment variable.")

client = OpenAI()

LOG_FILE = "chat_log.txt"
SUMMARY_FILE = "summary.json"
PROFILE_FILE = "profile.json"

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
    """Checks the size of chat_log.txt. If it exceeds the maximum size,
    archives it to keep parsing fast.
    """
    if not os.path.exists(LOG_FILE):
        return

    file_size = os.path.getsize(LOG_FILE)
    if file_size < MAX_LOG_SIZE_BYTES:
        return  # No rotation needed

    print("📁 Main log file size threshold exceeded. Initiating rotation...")
    
    # Find the next available archive index number 
    existing_archives = glob.glob("chat_log_archive_*.txt")
    archive_index = len(existing_archives) + 1
    archive_name = f"chat_log_archive_{archive_index}.txt"
    
    try:
        # Rename the current log file to an archive one
        os.rename(LOG_FILE, archive_name)
        
        # Seed a brand new, empty log file for you the next active conversation
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("--- New Log Segment Initialized ---\n\n")
            
        print(f"📦 Archival successful. Records moved to: {archive_name}")
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
to keep it completely true to who the user is becoming.

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
You must return a single JSON object containing two top-level keys: "updated_profile" and "updated_summary". 
Both must strictly match the schemas of their original databases. 
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

        save_summary(updated_summary)
        save_profile(updated_profile)
        print("Long-term memory synchronization complete.")
        print("profile.json has been dynamically updated and evolved.")
        print("summary.json has been calibrated.")
        
        # Run log cleanup directly after a successful consolidation pass
        rotate_logs()

    except Exception as e:
        print(f"❌ Profile/Memory consolidation failed: {e}")

if __name__ == "__main__":
    consolidate_long_term_memory()