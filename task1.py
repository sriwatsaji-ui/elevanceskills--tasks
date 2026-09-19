import time

def analyze_sentiment(message):
    msg = message.lower()
    
    # 1. High-Risk Cases
    if "hack" in msg or "compromise" in msg or "legal" in msg or "court" in msg:
        return "HIGH-RISK", 0.99
    if "fraud" in msg or "duplicate payment" in msg:
        return "HIGH-RISK", 0.99
        
    # 2. Urgent / Frustrated / Negative / Sarcastic
    if "urgent" in msg or "immediately" in msg or "khatra" in msg:
        return "URGENT", 0.95
    if "bad" in msg or "worst" in msg or "bekar" in msg or "ghatiya" in msg:
        return "NEGATIVE", 0.85
    if "funny" in msg or "joke" in msg or "haha" in msg:
        return "SARCASTIC", 0.70
        
    # 3. Positive / Neutral
    if "good" in msg or "thanks" in msg or "dhanyawad" in msg:
        return "POSITIVE", 0.90
    
    return "NEUTRAL", 0.50

def process_chat(message, duration_unresolved=0):
    sentiment, confidence = analyze_sentiment(message)
    print(f"\n[Message]: {message}")
    print(f"[Sentiment]: {sentiment} ({confidence})")
    
    if sentiment == "HIGH-RISK":
        print("🚨 CRITICAL: High-risk issue! Immediate escalation triggered.")
        return "Escalated"
    elif sentiment == "NEGATIVE" and duration_unresolved >= 15:
        print("⏰ TIMEOUT: Unresolved negative chat > 15 mins. Auto-escalating.")
        return "Auto-Escalated"
    
    print("✅ Chat routed normally to regular support.")
    return "Normal"

if __name__ == "__main__":
    # Test Cases
    process_chat("I will take legal action against your company!")
    process_chat("Aapki service bahut ghatiya hai, billing problem hai")
    process_chat("Still facing error, nobody is helping me.", duration_unresolved=20)
