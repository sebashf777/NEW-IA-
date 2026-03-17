import streamlit as st
import anthropic
import requests
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="NEXUS — AI Intelligence Platform",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg:       #04050a;
    --surface:  #090b12;
    --border:   #1a1f2e;
    --accent:   #6366f1;
    --accent2:  #22d3ee;
    --accent3:  #a78bfa;
    --text:     #e2e8f0;
    --muted:    #475569;
    --success:  #10b981;
    --warning:  #f59e0b;
}

html, body, .stApp { background: var(--bg) !important; color: var(--text); }
section[data-testid="stSidebar"] { display:none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
* { font-family: 'Space Grotesk', sans-serif; box-sizing: border-box; }

/* ── HEADER ── */
.nexus-header {
    background: linear-gradient(180deg, #0d0f1a 0%, var(--bg) 100%);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(20px);
}
.nexus-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #6366f1, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nexus-logo-hex {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: white;
    -webkit-text-fill-color: white;
}
.nexus-tagline {
    font-size: 11px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── MODEL SELECTOR ── */
.model-bar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.model-label {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}

/* ── CHAT AREA ── */
.chat-container {
    max-width: 860px;
    margin: 0 auto;
    padding: 2rem 2rem 120px 2rem;
    min-height: calc(100vh - 130px);
}

/* ── MESSAGES ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0;
    animation: slideUp 0.3s ease;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    margin: 1rem 0;
    animation: slideUp 0.3s ease;
    gap: 12px;
    align-items: flex-start;
}
.msg-avatar {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 4px;
}
.avatar-nexus {
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}
.avatar-perplexity {
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 50%;
}
.bubble-user {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: #fff;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 4px 24px rgba(99,102,241,0.25);
}
.bubble-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 14px 18px;
    border-radius: 4px 18px 18px 18px;
    max-width: 80%;
    font-size: 15px;
    line-height: 1.7;
    position: relative;
}
.bubble-ai code {
    font-family: 'JetBrains Mono', monospace;
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 13px;
    color: var(--accent2);
}
.bubble-ai pre {
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #e2e8f0;
    margin: 10px 0;
}
.msg-meta {
    font-size: 10px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px;
    padding: 0 4px;
}
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    padding: 2px 8px;
    border-radius: 99px;
    margin-bottom: 4px;
}
.badge-claude  { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
.badge-perplexity { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }

/* ── WELCOME ── */
.welcome-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    gap: 1.5rem;
}
.welcome-hex {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    margin-bottom: 0.5rem;
    animation: pulse 3s ease-in-out infinite;
}
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    line-height: 1.1;
}
.welcome-sub {
    font-size: 16px;
    color: var(--muted);
    max-width: 480px;
    line-height: 1.6;
}
.suggestion-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 1rem;
    max-width: 580px;
    width: 100%;
}
.suggestion-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
}
.suggestion-card:hover {
    border-color: var(--accent);
    background: rgba(99,102,241,0.08);
    transform: translateY(-2px);
}
.suggestion-icon { font-size: 18px; margin-bottom: 6px; }
.suggestion-title { font-size: 13px; font-weight: 600; color: var(--text); }
.suggestion-sub { font-size: 11px; color: var(--muted); margin-top: 2px; }

/* ── INPUT AREA ── */
.input-wrapper {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(0deg, var(--bg) 60%, transparent);
    padding: 1rem 1rem 1.5rem;
    z-index: 50;
}
.input-inner {
    max-width: 860px;
    margin: 0 auto;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    display: flex;
    align-items: flex-end;
    gap: 8px;
    padding: 10px 12px;
    transition: border-color 0.2s;
    box-shadow: 0 -4px 40px rgba(0,0,0,0.4);
}
.input-inner:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12), 0 -4px 40px rgba(0,0,0,0.4);
}

/* ── TYPING INDICATOR ── */
.typing-dots {
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 4px 0;
}
.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: bounce 1.2s ease-in-out infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

/* ── STATUS BAR ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    padding: 0 2rem;
    height: 28px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
}
.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30%            { transform: translateY(-6px); }
}

/* Streamlit overrides */
.stTextArea textarea {
    background: transparent !important;
    border: none !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    resize: none !important;
    padding: 0 !important;
    line-height: 1.6 !important;
    box-shadow: none !important;
}
.stTextArea textarea:focus { box-shadow: none !important; outline: none !important; border: none !important; }
.stTextArea { border: none !important; }
[data-testid="stTextArea"] > div { border: none !important; background: transparent !important; }
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
div[data-testid="column"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "model"         not in st.session_state: st.session_state.model         = "claude-sonnet-4-5"
if "total_tokens"  not in st.session_state: st.session_state.total_tokens  = 0
if "msg_count"     not in st.session_state: st.session_state.msg_count     = 0

MODELS = {
    "claude-sonnet-4-5": {
        "label": "Claude Sonnet",
        "provider": "anthropic",
        "badge": "claude",
        "color": "#6366f1",
        "icon": "⬡",
        "desc": "Fast, intelligent — best for most tasks"
    },
    "claude-opus-4-5": {
        "label": "Claude Opus",
        "provider": "anthropic",
        "badge": "claude",
        "color": "#a78bfa",
        "icon": "⬡",
        "desc": "Most capable — complex reasoning & analysis"
    },
    "perplexity-sonar": {
        "label": "Perplexity Sonar",
        "provider": "perplexity",
        "badge": "perplexity",
        "color": "#10b981",
        "icon": "◎",
        "desc": "Web-connected — real-time search & news"
    },
    "perplexity-sonar-pro": {
        "label": "Perplexity Sonar Pro",
        "provider": "perplexity",
        "badge": "perplexity",
        "color": "#34d399",
        "icon": "◎",
        "desc": "Advanced web search with deeper reasoning"
    },
}

SUGGESTIONS = [
    {"icon": "📊", "title": "Financial analysis",   "sub": "Analyze a stock, sector or market trend", "prompt": "Give me a detailed financial analysis of Apple (AAPL) including recent performance, valuation, and outlook."},
    {"icon": "⚡", "title": "Explain anything",     "sub": "Break down complex concepts clearly",      "prompt": "Explain how large language models work, from training to inference, in a way that's technically accurate but easy to understand."},
    {"icon": "🌐", "title": "Latest news",          "sub": "Search the web for real-time info",        "prompt": "What are the most important financial and economic news stories happening right now?"},
    {"icon": "💡", "title": "Strategic thinking",   "sub": "Business strategy & decision frameworks",  "prompt": "Help me think through a framework for evaluating whether to accept a new job offer versus staying at my current position."},
]

# ── API CALLS ─────────────────────────────────────────────────
def call_anthropic(messages, model_id):
    try:
        client = anthropic.Anthropic()
        api_msgs = [{"role": m["role"], "content": m["content"]}
                    for m in messages if m["role"] in ("user","assistant")]
        response = client.messages.create(
            model=model_id,
            max_tokens=2048,
            system=("You are NEXUS, an advanced AI intelligence platform. "
                    "You are sharp, insightful, and direct. You provide high-quality, "
                    "well-structured responses. Use markdown formatting when helpful. "
                    "Be conversational but precise."),
            messages=api_msgs)
        text   = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        return text, tokens
    except Exception as e:
        return f"❌ Anthropic API error: {e}", 0

def call_perplexity(messages, model_id):
    try:
        PERPLEXITY_KEY = st.secrets.get("PERPLEXITY_API_KEY", "")
        if not PERPLEXITY_KEY:
            return ("❌ Perplexity API key not set.\n\n"
                    "Add `PERPLEXITY_API_KEY` to your Streamlit secrets "
                    "(`Settings → Secrets` in Streamlit Cloud)."), 0

        model_map = {
            "perplexity-sonar":     "sonar",
            "perplexity-sonar-pro": "sonar-pro",
        }
        api_model = model_map.get(model_id, "sonar")
        api_msgs  = [{"role": m["role"], "content": m["content"]}
                     for m in messages if m["role"] in ("user","assistant")]

        headers = {
            "Authorization": f"Bearer {PERPLEXITY_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": api_model,
            "messages": [
                {"role": "system",
                 "content": ("You are NEXUS, an AI platform with real-time web search. "
                             "When answering, cite sources where relevant. "
                             "Be concise, accurate, and insightful.")},
                *api_msgs
            ],
            "max_tokens": 2048,
        }
        r = requests.post("https://api.perplexity.ai/chat/completions",
                          headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data   = r.json()
        text   = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        return text, tokens
    except Exception as e:
        return f"❌ Perplexity API error: {e}", 0

def send_message(user_input):
    if not user_input.strip(): return
    st.session_state.messages.append({"role":"user","content":user_input.strip(),"model":st.session_state.model,"time":datetime.now().strftime("%H:%M")})
    model_cfg = MODELS[st.session_state.model]
    if model_cfg["provider"] == "anthropic":
        reply, tokens = call_anthropic(st.session_state.messages, st.session_state.model)
    else:
        reply, tokens = call_perplexity(st.session_state.messages, st.session_state.model)
    st.session_state.messages.append({"role":"assistant","content":reply,"model":st.session_state.model,"time":datetime.now().strftime("%H:%M")})
    st.session_state.total_tokens += tokens
    st.session_state.msg_count    += 1

# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="nexus-header">
  <div style="display:flex;align-items:center;gap:12px">
    <div class="nexus-logo">
      <div class="nexus-logo-hex">⬡</div>
      NEXUS
    </div>
    <span class="nexus-tagline">AI Intelligence Platform</span>
  </div>
  <div style="display:flex;align-items:center;gap:16px">
    <span style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace">
      v2.0 · multi-model
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STATUS BAR ───────────────────────────────────────────────
cur = MODELS[st.session_state.model]
st.markdown(f"""
<div class="status-bar">
  <div class="status-dot"></div>
  <span>ONLINE</span>
  <span style="color:#1e293b">|</span>
  <span style="color:{cur['color']}">{cur['icon']} {cur['label']}</span>
  <span style="color:#1e293b">|</span>
  <span>{st.session_state.msg_count} messages</span>
  <span style="color:#1e293b">|</span>
  <span>{st.session_state.total_tokens:,} tokens used</span>
</div>
""", unsafe_allow_html=True)

# ── MODEL SELECTOR BAR ────────────────────────────────────────
st.markdown("<div class='model-bar'><span class='model-label'>Model</span>", unsafe_allow_html=True)
mc = st.columns([1,1,1,1,4])
model_keys = list(MODELS.keys())
for i, (mk, mv) in enumerate(MODELS.items()):
    with mc[i]:
        is_active = st.session_state.model == mk
        badge_col = "#6366f1" if mv["badge"]=="claude" else "#10b981"
        btn_style = (f"background:rgba({','.join(str(int(badge_col.lstrip('#')[j:j+2],16)) for j in (0,2,4))},0.2);"
                     f"border:1px solid {badge_col};" if is_active else "")
        if st.button(f"{mv['icon']} {mv['label']}", key=f"model_{mk}",
                     help=mv["desc"], use_container_width=True):
            st.session_state.model = mk
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ── CHAT MESSAGES ─────────────────────────────────────────────
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-screen">
      <div class="welcome-hex">⬡</div>
      <div class="welcome-title">Hello, I'm NEXUS</div>
      <div class="welcome-sub">
        Your multi-model AI platform. Switch between Claude and Perplexity
        to get the best answer for every question.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='suggestion-grid' style='max-width:580px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:10px'>", unsafe_allow_html=True)
    s_cols = st.columns(2)
    for i, s in enumerate(SUGGESTIONS):
        with s_cols[i % 2]:
            if st.button(f"{s['icon']} {s['title']}\n{s['sub']}", key=f"sug_{i}", use_container_width=True):
                send_message(s["prompt"])
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    for msg in st.session_state.messages:
        m_cfg   = MODELS.get(msg.get("model", "claude-sonnet-4-5"), MODELS["claude-sonnet-4-5"])
        badge_c = "badge-claude" if m_cfg["badge"]=="claude" else "badge-perplexity"
        t       = msg.get("time","")

        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
              <div>
                <div class="bubble-user">{msg['content']}</div>
                <div class="msg-meta" style="text-align:right">{t}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            import re
            content = msg["content"]
            # Format code blocks
            content = re.sub(r'```(\w+)?\n(.*?)```',
                lambda m: f'<pre><code>{m.group(2)}</code></pre>',
                content, flags=re.DOTALL)
            # Bold
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            # Inline code
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            # Line breaks
            content = content.replace('\n', '<br>')

            st.markdown(f"""
            <div class="msg-ai">
              <div class="msg-avatar avatar-{'perplexity' if m_cfg['badge']=='perplexity' else 'nexus'}">{m_cfg['icon']}</div>
              <div>
                <div class="model-badge {badge_c}">{m_cfg['icon']} {m_cfg['label']}</div>
                <div class="bubble-ai">{content}</div>
                <div class="msg-meta">{t}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── INPUT BAR ────────────────────────────────────────────────
st.markdown("<div class='input-wrapper'><div class='input-inner'>", unsafe_allow_html=True)

with st.container():
    in_col, btn_col = st.columns([11, 1])
    with in_col:
        user_input = st.text_area(
            label="",
            placeholder=f"Message NEXUS via {MODELS[st.session_state.model]['label']}...",
            key="chat_input",
            height=52,
            label_visibility="collapsed")
    with btn_col:
        st.markdown("<div style='padding-top:6px'>", unsafe_allow_html=True)
        send = st.button("Send", key="send_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

if send and user_input and user_input.strip():
    send_message(user_input)
    st.rerun()

# Ctrl+Enter hint
st.markdown("""
<div style='text-align:center;font-size:10px;color:#1e293b;
font-family:"JetBrains Mono",monospace;margin-top:-8px;
padding-bottom:8px'>
  Press Send or click the button · Switch models anytime
</div>
""", unsafe_allow_html=True)
