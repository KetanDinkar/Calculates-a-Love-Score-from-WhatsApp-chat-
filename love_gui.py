import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import datetime
from collections import defaultdict

# -------------------------
# CHAT PARSING & ANALYSIS
# -------------------------
def count_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    return len(emoji_pattern.findall(text))

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

def analyze_love_score(chat_lines):
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

    score = (
        (100 / avg_reply) * 5 +
        emoji_count * 0.8 +
        message_count * 0.6 +
        late_night_bonus * 0.5
    )
    score = min(100, round(score))

    if score >= 90:
        verdict = "❤️🔥 True Soulmates"
    elif score >= 75:
        verdict = "😊 Great Connection"
    elif score >= 55:
        verdict = "😬 Talking Stage"
    else:
        verdict = "💤 Just Casual"

    return {
        "Messages": message_count,
        "Emojis": emoji_count,
        "Avg Reply Time (sec)": round(avg_reply),
        "Late Night Msgs": late_night_bonus,
        "Love Score": score,
        "Verdict": verdict
    }

# -------------------------
# GUI SECTION
# -------------------------

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            chat_lines = f.readlines()
        result = analyze_love_score(chat_lines)
        update_table(result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file.\n\n{e}")

def update_table(data):
    for item in table.get_children():
        table.delete(item)
    for key, value in data.items():
        table.insert('', 'end', values=(key, value))

    verdict_label.config(text=data["Verdict"], font=("Segoe UI", 20, "bold"))
    animate_heart()

def animate_heart():
    def pulse(size=18, grow=True):
        if grow:
            size += 1
        else:
            size -= 1
        verdict_label.config(font=("Segoe UI", size, "bold"))
        if size >= 26:
            root.after(80, pulse, size, False)
        elif size <= 18:
            root.after(80, pulse, size, True)
        else:
            root.after(80, pulse, size, grow)
    pulse()

# -------------------------
# TKINTER WINDOW
# -------------------------

root = tk.Tk()
root.title("💘 Love Score Analyzer")
root.geometry("600x500")
root.configure(bg="#fff5f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

title = tk.Label(root, text="💌 Love Score Analyzer", font=("Segoe UI", 24, "bold"), bg="#fff5f9", fg="#ff4d88")
title.pack(pady=20)

upload_btn = tk.Button(root, text="📁 Upload Chat File", font=("Segoe UI", 12), command=upload_file,
                       bg="#ff4d88", fg="white", relief="flat", padx=10, pady=5)
upload_btn.pack(pady=10)

table = ttk.Treeview(root, columns=("Metric", "Value"), show="headings")
table.heading("Metric", text="Metric")
table.heading("Value", text="Value")
table.pack(pady=20, fill="x", padx=40)

verdict_label = tk.Label(root, text="", bg="#fff5f9", fg="#cc0066")
verdict_label.pack(pady=10)

root.mainloop()
