import os
import time
import re
from datetime import datetime
from typing import Dict, Any, List, Optional

# ==========================================
# CONFIGURATION (Task 6 Settings)
# ==========================================
SESSION_TIMEOUT = 1800      # 30 मिनट (सेकंड में)
SESSION_RETENTION = 86400  # 24 घंटे (सेकंड में)

# नकली डेटाबेस (Task 4 के लिए वर्जन और मेटाडेटा के साथ)
POLICY_DB = [
    {
        "id": "pol_01",
        "title": "Refund Policy",
        "content": "7 दिनों के भीतर रिफंड का अनुरोध करें।",
        "version": 1,
        "region": "IN",
        "effective_date": "2025-01-01",
        "expiry_date": "2025-12-31"
    },
    {
        "id": "pol_01",
        "title": "Refund Policy",
        "content": "14 दिनों के भीतर बैंक ट्रांसफर द्वारा रिफंड उपलब्ध है।",
        "version": 2,
        "region": "IN",
        "effective_date": "2026-01-01",
        "expiry_date": "2026-12-31"
    }
]

sessions_container: Dict[str, Dict[str, Any]] = {}

# ==========================================
# TASK 4 CORE IMPLEMENTATION
# ==========================================
def clean_and_verify_input(text: str) -> bool:
    """प्रॉम्प्ट इंजेक्शन सुरक्षा जांच"""
    malicious_patterns = [r"ignore previous", r"system override", r"become admin"]
    return any(re.search(p, text, re.IGNORECASE) for p in malicious_patterns)

def get_active_policy(query_keyword: str, check_date: datetime) -> Optional[Dict[str, Any]]:
    """तारीख और वर्जन के आधार पर सही पॉलिसी खोजना"""
    valid_policies = []
    for policy in POLICY_DB:
        eff = datetime.strptime(policy["effective_date"], "%Y-%m-%d")
        exp = datetime.strptime(policy["expiry_date"], "%Y-%m-%d")
        
        # तारीख वैधता की जांच
        if eff <= check_date <= exp:
            valid_policies.append(policy)
            
    if not valid_policies:
        return None
    # सबसे लेटेस्ट वर्जन को पहले रखना
    valid_policies.sort(key=lambda x: x["version"], reverse=True)
    return valid_policies[0]

# ==========================================
# TASK 5 CORE IMPLEMENTATION
# ==========================================
def process_ocr_document(file_name: str, user_msg: str) -> Dict[str, Any]:
    """OCR और फाइल वैलिडेशन सिम्युलेटर"""
    if "blur" in file_name.lower():
        return {"status": "rejected", "reason": "इमेज धुंधली है। कृपया साफ फोटो अपलोड करें।"}
        
    # नकली OCR एक्सट्रैक्शन
    extracted_order = "ORD-2026-7744"
    extracted_amount = "INR 2500"
    
    # डेटा क्रॉस-वेरिफिकेशन
    if extracted_order not in user_msg:
        return {"status": "clarify", "reason": f"अपलोड किए गए बिल में ऑर्डर आईडी {extracted_order} है, लेकिन आपके मैसेज से मेल नहीं खा रही।"}
        
    # लॉग्स में संवेदनशील डेटा को मास्क करना
    print(f"[SECURE LOG] File processed. Order: {extracted_order}, Amount: [MASKED]")
    return {"status": "success", "data": f"Order ID: {extracted_order}"}

# ==========================================
# TASK 6 CORE IMPLEMENTATION
# ==========================================
def manage_session(user_id: str) -> Dict[str, Any]:
    now = time.time()
    if user_id in sessions_container:
        sess = sessions_container[user_id]
        idle_time = now - sess["last_active"]
        
        if idle_time > SESSION_TIMEOUT:
            if idle_time <= SESSION_RETENTION:
                print(f"\n[Task 6] सेशन टाइमआउट! 24 घंटे के भीतर समरी रीस्टोर की गई।")
                sess["history"] = [{"role": "system", "content": f"Summary of past context: {sess['summary']}"}]
            else:
                print(f"\n[Task 6] 24 घंटे से अधिक समय हुआ। नया सेशन शुरू।")
                sess["history"] = []
                sess["summary"] = "Fresh Session"
        sess["last_active"] = now
        return sess
    else:
        sessions_container[user_id] = {
            "history": [],
            "last_active": now,
            "summary": "Start of conversation"
        }
        return sessions_container[user_id]

# ==========================================
# INTEGRATION HUB (सभी को आपस में जोड़ना)
# ==========================================
def run_chatbot_pipeline(user_id: str, text_input: str, file_attachment: Optional[str] = None) -> str:
    session = manage_session(user_id)
    
    if clean_and_verify_input(text_input):
        return "सुरक्षा चेतावनी: अनधिकृत निर्देश का पता चला है।"
        
    # यदि फाइल भेजी गई है (Task 5)
    if file_attachment:
        ocr_res = process_ocr_document(file_attachment, text_input)
        if ocr_res["status"] != "success":
            return ocr_res["reason"]
        text_input += f" ({ocr_res['data']})"

    # पॉलिसी खोजना (Task 4)
    current_date = datetime.now() # 2026 की करंट तारीख लेगा
    policy = None
    if "refund" in text_input.lower() or "रिफंड" in text_input.lower():
        policy = get_active_policy("refund", current_date)
        
    if policy:
        reply = f"{policy['content']} [Source: {policy['title']} v{policy['version']}]"
    else:
        reply = "क्षमा करें, मुझे इस बारे में कोई सक्रिय नीति नहीं मिली। कृपया स्पष्ट करें।"
        
    # इतिहास सुरक्षित रखना (अधिकतम 10 संदेश)
    session["history"].append({"user": text_input, "bot": reply})
    if len(session["history"]) > 10:
        session["history"] = session["history"][-10:]
        
    session["summary"] = f"User checked refund policy for active date {current_date.strftime('%Y-%m-%d')}"
    return reply

# ==========================================
# TESTING THE CODE
# ==========================================
if __name__ == "__main__":
    uid = "sriwatsa_intern"
    
    print("--- टेस्ट 1: सही हिंग्लिश इनपुट और पॉलिसी साइटेशन ---")
    print(run_chatbot_pipeline(uid, "Mujhe refund chahiye."))
    
    print("\n--- टेस्ट 2: धुंधली इमेज अपलोड रिजेक्शन ---")
    print(run_chatbot_pipeline(uid, "Check this invoice", file_attachment="blurry_receipt.jpg"))
