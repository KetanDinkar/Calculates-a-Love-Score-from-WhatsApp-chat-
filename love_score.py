import re
from datetime import datetime
from collections import defaultdict

# 🔍 Path to your chat file
CHAT_FILE = r"D:\programs\python\GUI\love calculator\chat.txt"

# -------------------------
# Emoji Detector
# -------------------------
def count_emojis(text):
    emoji_pattern = re.compile("[" 
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols
        u"\U0001F680-\U0001F6FF"  # transport
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE)
    return len(emoji_pattern.findall(text))

# -------------------------
# Chat Line Parser
# -------------------------
def parse_chat_line(line):
    match = re.match(r"\[(.*?)\] (.*?): (.*)", line)
    if match:
        timestamp_str, sender, message = match.groups()
        for fmt in ("%m/%d/%Y %I:%M %p", "%d/%m/%Y %I:%M %p", "%d/%m/%Y %H:%M"):
            try:
                timestamp = datetime.strptime(timestamp_str, fmt)
                break
            except:
                timestamp = None
        if timestamp:
            return {"time": timestamp, "sender": sender.strip(), "message": message.strip()}
    return None

# -------------------------
# Strict Love Score Analyzer
# -------------------------
def analyze_love_score_strict(chat_lines):
    chat_data = [parse_chat_line(line.strip()) for line in chat_lines if parse_chat_line(line.strip())]
    emoji_count = 0
    message_count = 0
    late_night_bonus = 0
    reply_gaps = []

    last_time = None
    last_sender = None

    for entry in chat_data:
        emoji_count += count_emojis(entry["message"])
        message_count += 1

        hour = entry["time"].hour
        if hour >= 22 or hour < 6:
            late_night_bonus += 1

        if last_time and last_sender != entry["sender"]:
            gap = (entry["time"] - last_time).total_seconds()
            if 0 < gap < 3600:
                reply_gaps.append(gap)

        last_time = entry["time"]
        last_sender = entry["sender"]

    avg_reply = sum(reply_gaps) / len(reply_gaps) if reply_gaps else 60

    # ✅ STRONGER reply time penalty
    reply_score = max(0, 15 - avg_reply) * 6

    # 📊 Final Love Score Calculation
    score = (
        reply_score +
        emoji_count * 0.8 +
        message_count * 0.6 +
        late_night_bonus * 0.5
    )
    score = min(100, round(score))

    # ❤️ Verdicts
    if score >= 90:
        verdict = "❤️🔥 True Soulmates"
    elif score >= 75:
        verdict = "😊 Great Connection"
    elif score >= 55:
        verdict = "😬 Talking Stage"
    else:
        verdict = "💤 Just Casual"

    return {
        "Total Messages": message_count,
        "Total Emojis": emoji_count,
        "Average Reply Time (seconds)": round(avg_reply),
        "Late Night Msgs": late_night_bonus,
        "Reply Speed Score": round(reply_score),
        "Love Score (Strict)": score,
        "Verdict": verdict
    }

# -------------------------
# MAIN EXECUTION
# -------------------------
if __name__ == "__main__":
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        chat_lines = f.readlines()

    result = analyze_love_score_strict(chat_lines)

    print("\n💘 LOVE SCORE ANALYZER (STRICT MODE) 💘\n")
    for key, value in result.items():
        print(f"{key}: {value}")
