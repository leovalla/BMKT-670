#-------------------------------------------------------------------------------
# ds_business_chatbot.py
# This generate a simple chatbot for a data analytics business using Flask
# Author: Leonardo Valladares
# Date: 2025-09-18
#-------------------------------------------------------------------------------

# import necessary libraries
import re           # for regex pattern matching
import random       # for random response selection
from flask import Flask, request, jsonify, render_template_string # for web app

# Initialize Flask app
app = Flask(__name__)

# --- Exit options ---
exit_keywords = ["exit", "quit", "bye", "goodbye", "stop"]

# --- Responses grouped by category ---
responses = {
    "services": [
        "We provide tailored analytics solutions for small and mid-sized businesses in Montana. Our focus is on dashboards, automation, and forecasting tools.",
        "Our services include organizing data, creating clear dashboards, and building forecasting tools for SMBs in Montana.",
        "We help businesses turn messy data into clear insights with dashboards, automation, and predictive analytics."
    ],
    "pricing": [
        "Costs vary depending on the project’s size and complexity. We recommend starting with a free consultation.",
        "We usually provide flexible packages that fit small business budgets. A free consultation is the best first step.",
        "Pricing depends on your needs. We suggest starting with a free consultation so we can prepare an estimate."
    ],
    "experience": [
        "We specialize in helping small and mid-sized Montana businesses use data effectively.",
        "Our company focuses on Montana’s SMBs, providing practical and affordable analytics solutions.",
        "We understand the challenges small businesses face with data and design solutions tailored to their needs."
    ],
    "availability": [
        "We’re available Monday through Friday, 9 AM to 5 PM.",
        "Our normal business hours are weekdays from 9 AM to 5 PM, but we aim to reply within 24 hours.",
        "We’re open standard hours, Monday to Friday, and do our best to respond quickly to all questions."
    ]
}

# --- Regex patterns for each category ---
patterns = {
    "services": re.compile(r"\b(service|services|offer|help|dashboard|dashboars|data|automation|forecast)\b", re.IGNORECASE),
    "pricing": re.compile(r"\b(price|pricing|cost|charge|fee|package|afford|support)\b", re.IGNORECASE),
    "experience": re.compile(r"\b(experience|qualification|background|team|different|industry)\b", re.IGNORECASE),
    "availability": re.compile(r"\b(hour|hours|availability|open|time|respond|start|support)\b", re.IGNORECASE)
}

# --- Helper function to get a response ---
def get_response(user_input):
    low = user_input.lower()
    if any(word in low for word in exit_keywords):
        return "Thanks for stopping by! Have a great day."

    for category, pattern in patterns.items():
        if pattern.search(user_input):
            return random.choice(responses[category])

    return "I’m not sure about that. Could you ask about our services, pricing, experience, or availability?"


@app.route("/", methods=["GET"])
def home():
    # Dark-themed UI (copied & adapted from your example)
    html_page = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Data Analytics Chatbot</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root { --bg:#0b1020; --card:#141a32; --ink:#e8ecff; --muted:#9aa3c7; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial; background:var(--bg); color:var(--ink); }
  .wrap { max-width:820px; margin:0 auto; padding:24px; }
  .card { background:var(--card); border-radius:16px; padding:18px; box-shadow:0 10px 30px rgba(0,0,0,.25); }
  h1 { font-size:22px; margin:0 0 4px; }
  p.subtitle { margin:0 0 16px; color:var(--muted); }
  .chat { height:56vh; overflow:auto; padding:8px; display:flex; flex-direction:column; gap:10px; border-radius:12px; background:#0f1530; border:1px solid rgba(255,255,255,.06); }
  .msg { max-width:78%; padding:10px 12px; border-radius:12px; line-height:1.35; white-space:pre-wrap; }
  .you { align-self:flex-end; background:#3243ff; color:white; border-bottom-right-radius:4px; }
  .bot { align-self:flex-start; background:#1b2242; border-bottom-left-radius:4px; }
  .meta { font-size:12px; color:var(--muted); margin-top:2px; }
  .row { display:flex; gap:8px; margin-top:12px; }
  input[type=text]{ flex:1; padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,.12); background:#0f1530; color:var(--ink); }
  button { padding:12px 14px; border-radius:10px; border:0; background:#3243ff; color:white; cursor:pointer; }
  button:disabled{ opacity:.6; cursor:not-allowed; }
  .hint { margin-top:10px; font-size:13px; color:var(--muted); }
  a { color:#cbd4ff; }
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Data Analytics Chatbot</h1>
      <p class="subtitle">Ask me about services, pricing, experience, or availability.</p>

      <div id="chat" class="chat"></div>

      <div class="row">
        <input id="input" type="text" placeholder="Type your question…" />
        <button id="send">Send</button>
      </div>
      <div class="hint">Tip: Try “What services do you offer?” or “How much does it cost?”</div>
    </div>
  </div>

<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const send = document.getElementById('send');

function addMsg(text, who='bot') {
  const wrap = document.createElement('div');
  wrap.className = 'msg ' + (who === 'you' ? 'you' : 'bot');
  wrap.textContent = text;
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

async function ask(question) {
  send.disabled = true;
  try {
    const res = await fetch('/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ question }) });
    const data = await res.json();
    if (data.answer) {
      addMsg(data.answer, 'bot');
    } else {
      addMsg("Hmm, I couldn't find a good match. Try rephrasing.", 'bot');
    }
  } catch (e) {
    addMsg('Error reaching server.', 'bot');
    console.error(e);
  } finally {
    send.disabled = false;
  }
}

send.addEventListener('click', () => {
  const q = input.value.trim();
  if (!q) return;
  addMsg(q, 'you');
  input.value = '';
  ask(q);
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') send.click();
});

// Greeting
addMsg("Hi! Welcome to our Data Analytics chatbot. Ask about services, pricing, experience, or availability.");
</script>
</body>
</html>
    """
    return render_template_string(html_page)


@app.post("/chat")
def chat_endpoint():
    payload = request.get_json(silent=True) or {}
    user_q = payload.get("question", "").strip()
    if not user_q:
        return jsonify({"answer": "Please type a question."})
    return jsonify({"answer": get_response(user_q)})


if __name__ == "__main__":
    app.run(debug=True)
