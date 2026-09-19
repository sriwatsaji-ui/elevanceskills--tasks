import time
import hashlib

# सिमुलेटेड स्टोरेज
KNOWLEDGE_BASE = {}
QUARANTINE_ZONE = {}
VERSION_HISTORY = []

def get_file_hash(content):
    """फाइल की यूनिक पहचान (Hash) बनाना"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def process_document_pipeline(file_name, content, version="v1"):
    """
    टास्क 3 के अनुसार न्यू डॉक्यूमेंट पाइपलाइन
    """
    file_hash = get_file_hash(content)
    
    # 1. डुप्लिकेट फाइल डिटेक्शन और क्वारंटाइन
    for existing_file, data in KNOWLEDGE_BASE.items():
        if data["hash"] == file_hash:
            print(f"⚠️ DUP DETECTED: '{file_name}' is a duplicate of '{existing_file}'. Quarantining file.")
            QUARANTINE_ZONE[file_name] = {"content": content, "hash": file_hash, "reason": "Duplicate File"}
            return "Quarantined"
            
    # 2. वर्जन मेंटेन करना और बैकअप (Rollback के लिए)
    if file_name in KNOWLEDGE_BASE:
        print(f"🔄 Updating '{file_name}' to version {version}. Backing up old version.")
        VERSION_HISTORY.append({"file_name": file_name, "old_data": KNOWLEDGE_BASE[file_name].copy()})
    
    # 3. नॉलेज बेस में फाइल सेव करना
    KNOWLEDGE_BASE[file_name] = {
        "content": content,
        "hash": file_hash,
        "version": version,
        "timestamp": time.time()
    }
    print(f"✅ Successfully processed and added '{file_name}' ({version}) to Knowledge Base.")
    return "Success"

def run_health_check(simulate_fail=False):
    """5 मिनट के अंदर हेल्थ चेक रन करना"""
    print("⏳ Running system health checks on new production update...")
    if simulate_fail:
        print("❌ HEALTH CHECK FAILED! Triggering automated rollback mechanism immediately.")
        return False
    print("🟢 Health check passed successfully!")
    return True

def trigger_rollback():
    """अगर हेल्थ चेक फेल हो जाए तो रोलबैक करना"""
    if not VERSION_HISTORY:
        print("ℹ️ No previous versions found to rollback.")
        return False
        
    last_version = VERSION_HISTORY.pop()
    file_name = last_version["file_name"]
    KNOWLEDGE_BASE[file_name] = last_version["old_data"]
    print(f"⏪ Automated Rollback complete! Restored '{file_name}' to its stable previous version.")
    return True

# --- टेस्ट रन (Testing Task 3 Pipeline) ---
if __name__ == "__main__":
    print("--- ⚙️ Running Task 3: Knowledge Base Pipeline & Rollback ---")
    
    # टेस्ट 1: पहली फाइल अपलोड करना
    process_document_pipeline("policy_2026.txt", "Welcome to ElevanceSkills. Office timing is 9 AM to 6 PM.")
    
    # टेस्ट 2: ठीक वही फाइल दोबारा अपलोड करना (डुप्लिकेट चेक)
    process_document_pipeline("policy_copy.txt", "Welcome to ElevanceSkills. Office timing is 9 AM to 6 PM.")
    
    # टेस्ट 3: फाइल का नया वर्जन अपलोड करना और फेल होने पर रोलबैक टेस्ट करना
    print("\n--- Deploying an Update with Simulated System Failure ---")
    import time
import hashlib

# सिमुलेटेड स्टोरेज
KNOWLEDGE_BASE = {}
QUARANTINE_ZONE = {}
VERSION_HISTORY = []

def get_file_hash(content):
    """फाइल की यूनिक पहचान (Hash) बनाना"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def process_document_pipeline(file_name, content, version="v1"):
    """
    टास्क 3 के अनुसार न्यू डॉक्यूमेंट पाइपलाइन
    """
    file_hash = get_file_hash(content)
    
    # 1. डुप्लिकेट फाइल डिटेक्शन और क्वारंटाइन
    for existing_file, data in KNOWLEDGE_BASE.items():
        if data["hash"] == file_hash:
            print(f"⚠️ DUP DETECTED: '{file_name}' is a duplicate of '{existing_file}'. Quarantining file.")
            QUARANTINE_ZONE[file_name] = {"content": content, "hash": file_hash, "reason": "Duplicate File"}
            return "Quarantined"
            
    # 2. वर्जन मेंटेन करना और बैकअप (Rollback के लिए)
    if file_name in KNOWLEDGE_BASE:
        print(f"🔄 Updating '{file_name}' to version {version}. Backing up old version.")
        VERSION_HISTORY.append({"file_name": file_name, "old_data": KNOWLEDGE_BASE[file_name].copy()})
    
    # 3. नॉलेज बेस में फाइल सेव करना
    KNOWLEDGE_BASE[file_name] = {
        "content": content,
        "hash": file_hash,
        "version": version,
        "timestamp": time.time()
    }
    print(f"✅ Successfully processed and added '{file_name}' ({version}) to Knowledge Base.")
    return "Success"

def run_health_check(simulate_fail=False):
    """5 मिनट के अंदर हेल्थ चेक रन करना"""
    print("⏳ Running system health checks on new production update...")
    if simulate_fail:
        print("❌ HEALTH CHECK FAILED! Triggering automated rollback mechanism immediately.")
        return False
    print("🟢 Health check passed successfully!")
    return True

def trigger_rollback():
    """अगर हेल्थ चेक फेल हो जाए तो रोलबैक करना"""
    if not VERSION_HISTORY:
        print("ℹ️ No previous versions found to rollback.")
        return False
        
    last_version = VERSION_HISTORY.pop()
    file_name = last_version["file_name"]
    KNOWLEDGE_BASE[file_name] = last_version["old_data"]
    print(f"⏪ Automated Rollback complete! Restored '{file_name}' to its stable previous version.")
    return True

# --- टेस्ट रन (Testing Task 3 Pipeline) ---
if __name__ == "__main__":
    print("--- ⚙️ Running Task 3: Knowledge Base Pipeline & Rollback ---")
    
    # टेस्ट 1: पहली फाइल अपलोड करना
    process_document_pipeline("policy_2026.txt", "Welcome to ElevanceSkills. Office timing is 9 AM to 6 PM.")
    
    # टेस्ट 2: ठीक वही फाइल दोबारा अपलोड करना (डुप्लिकेट चेक)
    process_document_pipeline("policy_copy.txt", "Welcome to ElevanceSkills. Office timing is 9 AM to 6 PM.")
    
    # टेस्ट 3: फाइल का नया वर्जन अपलोड करना और फेल होने पर रोलबैक टेस्ट करना
    print("\n--- Deploying an Update with Simulated System Failure ---")
    process_document_pipeline("policy_2026.txt", "Office timing changed to 24/7 hours.", version="v2")
    
    # सिस्टम फेलियर सिमुलेट करना (हेल्थ चेक फेल)
    if not run_health_check(simulate_fail=True):
        trigger_rollback()
        
    # फाइनल स्टेट चेक करना
    print(f"\n📢 Current Active Policy Version: {KNOWLEDGE_BASE['policy_2026.txt']['version']}")
    print(f"📢 Active Content: {KNOWLEDGE_BASE['policy_2026.txt']['content']}")("policy_2026.txt", "Office timing changed to 24/7 hours.", version="v2")
    
    # सिस्टम फेलियर सिमुलेट करना (हेल्थ चेक फेल)
    if not run_health_check(simulate_fail=True):
        trigger_rollback()
        
    # फाइनल स्टेट चेक करना
    print(f"\n📢 Current Active Policy Version: {KNOWLEDGE_BASE['policy_2026.txt']['version']}")
    print(f"📢 Active Content: {KNOWLEDGE_BASE['policy_2026.txt']['content']}")
