import datetime

# नकली डेटाबेस (सिम्युलेटेड टिकट्स और डुप्लिकेट्स चेक करने के लिए)
EXISTING_TICKETS = []

def calculate_sla_expiry(start_time, hours_allowed=24):
    """
    शनिवार (5) और रविवार (6) को छोड़कर SLA एक्सपायरी की गणना करना
    """
    current_time = start_time
    hours_added = 0
    
    while hours_added < hours_allowed:
        current_time += datetime.timedelta(hours=1)
        # अगर शनिवार या रविवार है, तो समय काउंट नहीं होगा (SLA से बाहर रहेगा)
        if current_time.weekday() in[5,6]:
            continue
        hours_added += 1
        
    return current_time

def check_sla_status(start_time, expiry_time, current_time=None):
    """
    SLA का स्टेटस चेक करना: 75% समय बीतने पर चेतावनी देना या ब्रीच घोषित करना
    """
    if not current_time:
        current_time = datetime.datetime.now()
        
    total_sla_time = (expiry_time - start_time).total_seconds()
    time_elapsed = (current_time - start_time).total_seconds()
    
    if current_time >= expiry_time:
        return "🚨 SLA BREACHED: Automated Escalation Triggered!"
    elif time_elapsed >= (total_sla_time * 0.75):
        return "⚠️ SLA WARNING: 75% of allowed time consumed!"
    
    return "✅ Within SLA Limits"

def create_support_ticket(customer_msg, order_id, agent_skill, severity="MEDIUM"):
    """
    टास्क 2 के नियमों के अनुसार नया सपोर्ट टिकट जेनरेट करना
    """
    # 1. डुप्लिकेट टिकट ढूंढना (सिस्टम एरर रोकने के लिए)
    for ticket in EXISTING_TICKETS:
        if ticket["order_id"] == order_id and ticket["status"] == "Open":
            print(f"📌 Duplicate request detected for Order {order_id}. Grouping with existing ticket.")
            return ticket

    # 2. नया टिकट ऑब्जेक्ट बनाना
    start_time = datetime.datetime.now()
    expiry_time = calculate_sla_expiry(start_time, hours_allowed=8) # 8 घंटे का SLA
    
    # 3. डेटा को मास्क (सुरक्षित) करना (Handoff Summary के लिए)
    masked_msg = customer_msg[:15] + "..." if len(customer_msg) > 15 else customer_msg
    
    new_ticket = {
        "ticket_id": len(EXISTING_TICKETS) + 101,
        "order_id": order_id,
        "severity": severity,
        "assigned_skill": agent_skill,
        "start_time": start_time,
        "expiry_time": expiry_time,
        "status": "Open",
        "handoff_summary": f"Order {order_id} requires {agent_skill} support. Msg: {masked_msg}"
    }
    
    EXISTING_TICKETS.append(new_ticket)
    return new_ticket

# --- टेस्ट रन (Testing Task 2 Workflows) ---
if __name__ == "__main__":
    print("--- ⚙️ Running Task 2: Support Ticket & SLA Calculations ---")
    
    # टेस्ट 1: नया टिकट बनाना और SLA कैलकुलेट करना
    t1 = create_support_ticket("Product not received", order_id="ORD12345", agent_skill="Logistics", severity="HIGH")
    print(f"🎟️ Ticket Created: ID {t1['ticket_id']} | Assigned to: {t1['assigned_skill']}")
    print(f"⏰ SLA Deadline (Excluding Weekends): {t1['expiry_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # टेस्ट 2: डुप्लिकेट रिक्वेस्ट को पहचानना
    print("\n--- Trying to create a duplicate request ---")
    create_support_ticket("Where is my order?", order_id="ORD12345", agent_skill="Logistics")
    
    # टेस्ट 3: SLA वार्निंग सिमुलेशन (75% समय बीतने पर)
    print("\n--- Simulating SLA Time Tracking ---")
    simulated_future_time = t1["start_time"] + datetime.timedelta(hours=7) # 7 घंटे बाद (8 में से)
    status = check_sla_status(t1["start_time"], t1["expiry_time"], current_time=simulated_future_time)
    print(f"Status After 7 Hours: {status}")
