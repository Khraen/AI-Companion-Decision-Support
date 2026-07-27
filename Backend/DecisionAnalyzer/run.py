import subprocess
import sys
import os

print("booting up cortana...")

# start conversation. i.e run engine.py
try:
  chat_process = subprocess.run([sys.executable, "/Users/matthewholguin/Documents/DecisionAIEngine/Backend/DecisionAnalyzer/Engine.py"])
except KeyboardInterrupt:
  print("\n\n Cortana: Talk to you later.")
except subprocess.CalledProcessError:
  print("Called Proccess ERROR: failed to run start conversation/engine.py")
  raise subprocess.CalledProcessError
except FileNotFoundError:
  raise FileNotFoundError

# After exit, save conversation and update long term memory
print("\nConnection closed. Saving conversation and updating long term memory...")

try:
  subprocess.run([sys.executable, "/Users/matthewholguin/Documents/DecisionAIEngine/Backend/DecisionAnalyzer/long_term_memory_manager.py"])
  print("conversation has been saved and updates have occurred accordingly")
except subprocess.CalledProcessError:
  print("Called Proccess ERROR: failed to run start save and update memory through long_term_memory_manager.py")
  raise subprocess.CalledProcessError
except FileNotFoundError:
  print("long_term_memory_manager.py not found")
  raise FileNotFoundError




