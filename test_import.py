import sys
import os

sys.path.append('D:/YZW_SDE/PythonProject/HumanReaction/OfficalVersion_V1')

print(sys.path)

try:
    from human_reaction_test.database.db_operations import save_participant
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")

# Test if the function is callable
try:
    save_participant({})
    print("save_participant function is callable!")
except Exception as e:
    print(f"Function test failed: {e}")
