import os
import json

def validate_file(filepath, label):
    print(f"🔍 Validating {label} data: {filepath}")
    if not os.path.exists(filepath):
        print(f"❌ {label} file not found: {filepath}\n")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ {label} file loaded successfully. {len(data)} items.\n")
    except Exception as e:
        print(f"⚠️ {label} file exists but couldn't be read: {e}\n")

def validate_instagram(profile_name):
    folder = os.path.join("output", "instagram", profile_name)
    print(f"🔍 Validating Instagram data: {folder}")
    if not os.path.exists(folder):
        print(f"❌ Instagram folder not found: {folder}\n")
        return
    files = os.listdir(folder)
    if files:
        print(f"✅ Instagram folder found with {len(files)} files.\n")
    else:
        print("⚠️ Instagram folder is empty.\n")
