# Generated from OpenAI, 2025

from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import html

app = Flask(__name__)

# ---- Editable FAQ knowledge base ----
FAQS = [
    {"q": "What textbook do we use?",
     "a": "Sedgewick & Wayne, *An Introduction to Programming in Python*."},
    {"q": "When are office hours?",
     "a": "Tues/Thurs 2-4pm in Room 214, or Zoom by appointment."},
    {"q": "How is the grade calculated?",
     "a": "Projects 50%, quizzes 20%, midterm 15%, final 15%."},
    {"q": "Where do I submit assignments?",
     "a": "Submit on Canvas → Assignments."},
    {"q": "What language do we code in?",
     "a": "Python 3.x. Use VS Code or PyCharm—your choice."},
    {"q": "Do we need to know all algorithms?",
     "a": "No—just get familiar with common ones; depth comes later."},
]

# Combine Q + A for better recall (captures phrasing overlap)
CORPUS = [f"{x['q']} || {x['a']}" for x in FAQS]
VEC = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), stop_words="english").fit(CORPUS)
MATRIX = VEC.transform(CORPUS)
SIM_THRESHOLD = 0.35  # raise to be stricter, lower to be more forgiving


def best_matches(user_text, top_k=3):
    if not user_text.strip():
        return []
    q_vec = VEC.transform([user_text])
    sims = cosine_similarity(q_vec, MATRIX)[0]
    ranked = sorted(enumerate(sims), key=lambda t: t[1], reverse=True)[:top_k]
    hits = []
    for idx, score in ranked:
        if score >= SIM_THRESHOLD:
            hits.append({
                "question": FAQS[idx]["q"],
                "answer": FAQS[idx]["a"],
                "score": round(float(score), 3)
            })
    return hits


@app.route("/", methods=["GET"])
def home():
    # Minimal chat UI (HTML+CSS+JS) served inline for a self-contained example
    html_page = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Class FAQ Chatbot</title>
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
      <h1>Class FAQ Chatbot</h1>
      <p class="subtitle">Ask anything about the course (textbook, grading, office hours, submissions…).</p>

      <div id="chat" class="chat"></div>

      <div class="row">
        <input id="input" type="text" placeholder="Type your question… (e.g., How are grades calculated?)" />
        <button id="send">Send</button>
      </div>
      <div class="hint">Tip: Try “Do we need to know all algorithms?” or “Where do I submit assignments?”</div>
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

function addMeta(text) {
  const m = document.createElement('div');
  m.className = 'meta';
  m.textContent = text;
  chat.appendChild(m);
  chat.scrollTop = chat.scrollHeight;
}

async function ask(question) {
  send.disabled = true;
  try {
    const res = await fetch('/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ question }) });
    const data = await res.json();
    if (data.answer) {
      addMsg(data.answer, 'bot');
      if ((data.alternatives || []).length) {
        addMeta('Similar: ' + data.alternatives.map(a => a.matched_faq || a.question).join(' • '));
      }
    } else {
      addMsg("Hmm, I couldn't find an exact match. Try rephrasing or check the syllabus.", 'bot');
    }
  } catch (e) {
    addMsg('Error reaching server. Check the console & server logs.', 'bot');
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
addMsg("Hi! I'm the class FAQ bot. Ask about grading, office hours, textbook, or where to submit.");
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
        return jsonify({"answer": "Please type a question.", "alternatives": []})

    hits = best_matches(user_q, top_k=3)
    if hits:
        best = hits[0]
        alts = [{"matched_faq": h["question"], "score": h["score"]} for h in hits[1:]]
        return jsonify({"answer": best["answer"], "matched_faq": best["question"], "alternatives": alts})

    # Simple rule-based fallbacks (optional)
    low = user_q.lower()
    if "hello" in low or "hi" in low:
        return jsonify({"answer": "Hello! Ask me about textbook, grading, office hours, or submissions."})
    if "syllabus" in low:
        return jsonify({"answer": "The syllabus is on Canvas → Files → Syllabus.pdf."})

    return jsonify({
        "answer": "I couldn't find an exact match. Try rephrasing or check the syllabus/Canvas.",
        "alternatives": []
    })


if __name__ == "__main__":
    # Tip: set host='0.0.0.0' if deploying to a server
    app.run(debug=True)
