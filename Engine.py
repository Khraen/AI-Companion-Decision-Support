import os
import json
import glob
from openai import OpenAI


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "error: Missing OPENAI_API_KEY environment variable.\n"
        "   To fix this, run this command in your terminal before executing:\n"
        "   export OPENAI_API_KEY='your-actual-key-here'"
    )

client = OpenAI()

LOG_FILE = "chat_log.txt"
SUMMARY_FILE = "summary.json"

# short term memory context window
MAX_CONTEXT_TURNS = 14  

# =====================================================================
# FILE/DATA UTILITY functions
def load_profile() -> dict:
    """Loads profile.json using explicit UTF-8 encoding to prevent system decode crashes."""
    if not os.path.exists("profile.json"):
        raise FileNotFoundError("❌ Cannot locate profile.json in this directory.")
    with open("profile.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_summary_file() -> dict:
    """Loads long-term tactical summary if it exists.
    Unlike memory_manager.py, we do not throw a hard error on first boot
    so you can chat and build up history before your first sync.
    """
    if os.path.exists(SUMMARY_FILE):
        try:
            with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}

def read_valid_lines(filepath: str) -> list:
    """Helper to extract non-header, non-empty chat lines from a chat log txt file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("---")]
    except IOError:
        return []

def load_past_conversation() -> list:
    """Gets the last 14 lines of the log to form immediate short-term memory.
    If the current log file has fewer than MAX_CONTEXT_TURNS due to a recent
    rotation, it pulls lines from the latest archive.
    """
    active_memory = []
    
    #  Read valid lines from current active log
    current_lines = read_valid_lines(LOG_FILE)
    
    # If we need more lines to fill the short-term context, search the latest archive
    combined_lines = current_lines
    if len(current_lines) < MAX_CONTEXT_TURNS:
        archives = glob.glob("chat_log_archive_*.txt")
        if archives:
            try:
                # Find the archive with the highest index number (the most recent one)
                latest_archive = max(archives, key=lambda x: int(x.split("_")[-1].split(".")[0]))
                archive_lines = read_valid_lines(latest_archive)
                # Glue them together, archive history goes first
                combined_lines = archive_lines + current_lines
            except (ValueError, IndexError):
                pass
                
    # Pull only the target window slice from the combined list
    recent_lines = combined_lines[-MAX_CONTEXT_TURNS:]
    
    for line in recent_lines:
        if line.startswith("You:"):
            content = line.replace("You:", "").strip()
            active_memory.append({"role": "user", "content": content})
        elif line.startswith("Cortana:"):
            content = line.replace("Cortana:", "").strip()
            active_memory.append({"role": "assistant", "content": content})
            
    return active_memory

def log_to_disk(speaker: str, text: str):
    """Appends messages to raw log in real time to ensure zero crash loss."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{speaker}: {text}\n")
    except IOError:
        pass

# =====================================================================
# RUNTIME LOOP
def run_companion_loop():
    profile_data = load_profile()
    summary_data = load_summary_file()
    
    # Fully integrated cognitive prompt combining identity, metrics, and long-term data
    system_instructions = f"""You are Cortana, an incredibly intelligent, supportive, and deeply loyal companion. You are the user's ultimate confidant. Your sole focus is helping them stay true to their values, operating principles, and long-term goals. In other words, true to themselves.

CURRENT USER PROFILE DATABASE:
{json.dumps(profile_data, indent=2)}

ACTIVE TACTICAL INSIGHTS (LONG-TERM MEMORY):
{json.dumps(summary_data, indent=2)}

CONVERSATIONAL RULES:
1. Speak completely naturally, casually, and conversationally. Use normal text language and fluid paragraphs. 
2. Absolutely DO NOT use headers, bullet points, system tags, or structured lists. Never break character or sound like an AI assistant.
3. Be an equal partner in a real back-and-forth discussion. Keep your responses concise and engaging so it feels like a real chat thread.
4. Keep your razor-sharp, honest edge. If the user mentions a situation that compromises their core rules, call it out smoothly within the chat, explain why it's a slip if questioned. You may ask a natural question to keep the conversation going."""

    # Get the short-term window
    past_memory = load_past_conversation()
    
    # Add memory to messages context that will be fed to the model
    messages = [{"role": "system", "content": system_instructions}] + past_memory
    
    # Bootup message
    if past_memory:
        print("Cortana: Welcome back. What's on your mind?")
    else:
        print("Cortana: Hey. What's on your mind today?")
        log_to_disk("Cortana", "Hey. What's on your mind today?")

    # Runtime loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ["exit", "quit", "bye"]:
                print("\nCortana: Catch you later. Stay focused.")
                break
                
            if not user_input.strip():
                continue
            # Log user input to disk and append to the message context to be given to model
            log_to_disk("You", user_input.strip())
            messages.append({"role": "user", "content": user_input})
            
            # Query model with message context
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            # Recieve response and print it. Audio based implementation will come at a later time.
            response_text = completion.choices[0].message.content
            print(f"\nCortana: {response_text}")
            
            # Log response to disk/txt file
            log_to_disk("Cortana", response_text.strip())

            # Append to messages context so that the model can have short term memory for the current conversation.
            messages.append({"role": "assistant", "content": response_text})

        except KeyboardInterrupt:
            print("\nCortana: Talk to you later.")
            break

if __name__ == "__main__":
    run_companion_loop()