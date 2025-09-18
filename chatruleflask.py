# Generated from OpenAI, 2025

from flask import Flask, request, jsonify, render_template_string
import nltk
from nltk.tokenize import word_tokenize

# Make sure tokenizers are available (downloads once, then cached)
nltk.download("punkt", quiet=True)

app = Flask(__name__)

# Keyword buckets
KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "morning", "afternoon"],
    "hours": ["hours", "open", "close", "time", "schedule"],
    "library": ["library", "book", "books", "study", "reading"],
    "goodbye": ["bye", "goodbye", "see", "later"]
}

def bot_reply(text: str) -> str:
    tokens = word_tokenize(text.lower())
    if any(w in tokens for w in KEYWORDS["greeting"]):
        return "Hello! How can I help you today?"
    if any(w in tokens for w in KEYWORDS["hours"]):
        return "We're open from 8 AM to 8 PM, Monday to Friday."
    if any(w in tokens for w in KEYWORDS["library"]):
        return "The library is on the 2nd floor and open until 6 PM."
    if any(w in tokens for w in KEYWORDS["goodbye"]):
        return "Goodbye! Have a great day!"
    return "I'm not sure about that. Could you rephrase your question?"

# Simple HTML UI (no separate template files needed)
PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>CampusBot</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui, Arial, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 16px; }
    .chat { border: 1px solid #ddd; border-radius: 10px; padding: 16px; min-height: 320px; }
    .msg { margin: 8px 0; }
    .you { text-align: right; }
    .bubble { display: inline-block; padding: 10px 14px; border-radius: 14px; max-width: 80%; }
    .you .bubble { background: #e6f0ff; }
    .bot .bubble { background: #f3f3f3; }
    form { display: flex; gap: 8px; margin-top: 12px; }
    input[type=text] { flex: 1; padding: 10px; border-radius: 10px; border: 1px solid #ccc; }
    button { padding: 10px 14px; border-radius: 10px; border: 1px solid #333; background: #333; color: white; }
  </style>
</head>
<body>
  <h1>CampusBot (NLTK + Flask)</h1>
  <div class="chat" id="chat">
    <div class="msg bot"><span class="bubble">Hi! I'm your campus assistant. Ask me about hours, the library, etc.</span></div>
  </div>
  <form id="form">
    <input id="input" type="text" placeholder="Type your message..." autocomplete="off" required />
    <button type="submit">Send</button>
  </form>

<script>
const form = document.getElementById('form');
const input = document.getElementById('input');
const chat = document.getElementById('chat');

function addMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  const bubble = document.createElement('span');
  bubble.className = 'bubble';
  bubble.textContent = text;
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  addMsg('you', message);
  input.value = '';

  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ message })
  });
  const data = await res.json();
  addMsg('bot', data.reply);
});
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    user_msg = data.get("message", "")
    reply = bot_reply(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # For local dev only; use a proper server (e.g., gunicorn) in production.
    app.run(host="127.0.0.1", port=5000, debug=True)
