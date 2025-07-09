💘 Love Score Analyzer (Strict Mode)
This is a fun and creative Python project that analyzes your chat messages and calculates a strict “Love Score” — based on how two people communicate. It's a playful way to blend data, emotion, and code.

📌 What It Does
Reads a .txt chat file (like from WhatsApp)

Parses every message to get:
  Who sent it
  When it was sent
  The message content

Analyzes behavior between the two people based on:
  Reply Speed
  Emoji Usage
  Message Count
  Late-night Conversation Time

🎯 How the Score Is Calculated
The love score is based on four key components:

Reply Speed (Most Important)
  Only quick replies (under 15 seconds) earn high points
  The slower the reply, the lower the score
  If the average reply time is too high, the reply portion gets zero

Emojis Used
  Emojis show emotion and playfulness
  More emojis mean higher emotional expression → small bonus

Total Messages Sent
  More messages = more engagement and effort
  Each message adds to the score, but not heavily

Late-Night Messages (Between 10 PM – 6 AM)
  Chatting late shows deeper emotional connection
  Each late-night message gives a small bonus

These four elements are combined into a final score out of 100.

🧪 The Verdict
Based on the final score, the analyzer gives one of the following verdicts:

❤️🔥 True Soulmates — Only for the most emotionally engaged and responsive chats
😊 Great Connection — Active, responsive, and warm
😬 Talking Stage — Light effort, not deep yet
💤 Just Casual — Dry or distant communication

🎉 Why This Exists
This is a light-hearted, educational project made to show that coding can be creative, fun, and personally meaningful. It's not a serious relationship tool — just a fun way to use Python to analyze something real from everyday life.

Whether you're learning Python, exploring string processing, or just building something cool — this project shows how code can bring joy, humor, and insight to even the simplest of things: a chat.
