import streamlit as st
import anthropic
import requests
from datetime import datetime

st.set_page_config(
    page_title="NEXUS — AI Platform",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #04050a !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stToolbar"] { display: none !important; }

/* Buttons */
.stButton > button {
    background: #0d0f1a !important;
    color: #94a3b8 !important;
    border: 1px solid #1a1f2e !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #13162a !important;
    border-color: #6366f1 !important;
    color: #e2e8f0 !important;
}

/* Active model button */
.active-btn > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border-color: #6366f1 !important;
}

/* Text input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #090b12 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1a1f2e !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}
label { color: #475569 !important; font-size: 11px !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #090b12 !important;
    border: 1px solid #1a1f2e !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* Markdown */
.stMarkdown { color: #e2e8f0 !important; }

/* Divider */
hr { border-color: #1a1f2e !important; }

/* Chat messages */
.user-bubble {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    margin-left: auto;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 4px;
    word-wrap: break-word;
}
.ai-bubble {
    background: #090b12;
    border: 1px solid #1a1f2e;
    color: #e2e8f0;
    padding: 14px 18px;
    border-radius: 4px 18px 18px 18px;
    max-width: 80%;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 4px;
    word-wrap: break-word;
}
.msg-meta {
    font-size: 10px;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 12px;
}
.model-badge-claude {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 99px;
    padding: 1px 8px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 4px;
}
.model-badge-perp {
    display: inline-block;
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 99px;
    padding: 1px 8px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 4px;
}
.nexus-header {
    background: #0d0f1a;
    border-bottom: 1px solid #1a1f2e;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.nexus-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.status-online {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: #10b981;
    font-family: 'JetBrains Mono', monospace;
}
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 8px;
}
.suggestion-card {
    background: #090b12;
    border: 1px solid #1a1f2e;
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s;
    height: 100%;
}
.code-block {
    background: #0d1117;
    border: 1px solid #1a1f2e;
    border-radius: 8px;
    padding: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #e2e8f0;
    overflow-x: auto;
    white-space: pre-wrap;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────
if "messages"     not in st.session_state: st.session_state.messages     = []
if "model"        not in st.session_state: st.session_state.model        = "claude-sonnet-4-5"
if "total_tokens" not in st.session_state: st.session_state.total_tokens = 0
if "input_key"    not in st.session_state: st.session_state.input_key    = 0

MODELS = {
    "claude-sonnet-4-5":  {"label": "Claude Sonnet",      "provider": "anthropic",   "icon": "⬡", "color": "#6366f1"},
    "claude-opus-4-5":    {"label": "Claude Opus",        "provider": "anthropic",   "icon": "⬡", "color": "#a78bfa"},
    "perplexity-sonar":   {"label": "Perplexity Sonar",   "provider": "perplexity",  "icon": "◎", "color": "#10b981"},
    "perplexity-sonar-pro":{"label":"Perplexity Sonar Pro","provider": "perplexity", "icon": "◎", "color": "#34d399"},
}

SUGGESTIONS = [
    ("📊", "Analyze a stock",       "Give me a detailed analysis of Apple (AAPL) — valuation, recent performance, and outlook."),
    ("🌐", "Latest market news",    "What are the most important financial and economic news stories happening right now?"),
    ("💡", "Explain a concept",     "Explain how the Federal Reserve controls inflation, and what tools it actually uses."),
    ("🧠", "Strategic thinking",    "Help me build a framework for deciding whether to take a new job offer vs staying at my current role."),
]

# ── API ───────────────────────────────────────────────────────
def call_anthropic(messages, model_id):
    try:
        client = anthropic.Anthropic()
        api_msgs = [{"role": m["role"], "content": m["content"]}
                    for m in messages if m["role"] in ("user","assistant")]
        r = client.messages.create(
            model=model_id, max_tokens=2048,
            system=("You are NEXUS, a sharp and insightful AI assistant. "
                    "Give high-quality, well-structured answers. "
                    "Use markdown when helpful. Be direct and precise."),
            messages=api_msgs)
        return r.content[0].text, r.usage.input_tokens + r.usage.output_tokens
    except Exception as e:
        return f"❌ Error: {e}", 0

def call_perplexity(messages, model_id):
    try:
        key = st.secrets.get("PERPLEXITY_API_KEY", "")
        if not key:
            return ("❌ **Perplexity API key not set.**\n\n"
                    "Go to Streamlit Cloud → your app → **Manage app → Settings → Secrets** and add:\n"
                    "```\nPERPLEXITY_API_KEY = \"pplx-your-key-here\"\n```"), 0
        model_map = {"perplexity-sonar": "sonar", "perplexity-sonar-pro": "sonar-pro"}
        api_msgs = [{"role": m["role"], "content": m["content"]}
                    for m in messages if m["role"] in ("user","assistant")]
        r = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model_map.get(model_id,"sonar"),
                  "messages": [{"role":"system","content":"You are NEXUS, an AI with real-time web search. Be accurate and cite sources."}, *api_msgs],
                  "max_tokens": 2048},
            timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"], data.get("usage",{}).get("total_tokens",0)
    except Exception as e:
        return f"❌ Perplexity error: {e}", 0

def send_message(text):
    if not text.strip(): return
    st.session_state.messages.append({
        "role": "user", "content": text.strip(),
        "model": st.session_state.model,
        "time": datetime.now().strftime("%H:%M")})
    m = MODELS[st.session_state.model]
    if m["provider"] == "anthropic":
        reply, tokens = call_anthropic(st.session_state.messages, st.session_state.model)
    else:
        reply, tokens = call_perplexity(st.session_state.messages, st.session_state.model)
    st.session_state.messages.append({
        "role": "assistant", "content": reply,
        "model": st.session_state.model,
        "time": datetime.now().strftime("%H:%M")})
    st.session_state.total_tokens += tokens
    st.session_state.input_key    += 1

# ── HEADER ────────────────────────────────────────────────────
cur = MODELS[st.session_state.model]
st.markdown(f"""
<div class="nexus-header">
  <span style="font-size:28px">⬡</span>
  <span class="nexus-title">NEXUS</span>
  <span style="color:#334155;font-size:18px">|</span>
  <span style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;letter-spacing:1px">AI INTELLIGENCE PLATFORM</span>
  <span style="flex:1"></span>
  <span class="status-online">
    <span style="width:7px;height:7px;border-radius:50%;background:#10b981;display:inline-block"></span>
    ONLINE
  </span>
  <span style="color:#334155;margin:0 8px">|</span>
  <span style="font-size:11px;color:{cur['color']};font-family:'JetBrains Mono',monospace">{cur['icon']} {cur['label']}</span>
  <span style="color:#334155;margin:0 8px">|</span>
  <span style="font-size:11px;color:#334155;font-family:'JetBrains Mono',monospace">
    {len(st.session_state.messages)} msgs · {st.session_state.total_tokens:,} tokens
  </span>
</div>
""", unsafe_allow_html=True)

# ── MODEL SELECTOR ────────────────────────────────────────────
st.markdown("""
<div style="background:#090b12;border-bottom:1px solid #1a1f2e;padding:10px 20px">
  <span style="font-size:11px;color:#475569;font-family:'JetBrains Mono',monospace;letter-spacing:1px">SELECT MODEL</span>
</div>
""", unsafe_allow_html=True)

mc = st.columns(4)
model_keys = list(MODELS.keys())
for i, (mk, mv) in enumerate(MODELS.items()):
    with mc[i]:
        is_active = st.session_state.model == mk
        icon_char = "⬡" if mv["provider"] == "anthropic" else "◎"
        label     = f"{icon_char} {mv['label']}"
        if is_active:
            st.markdown('<div class="active-btn">', unsafe_allow_html=True)
        if st.button(label, key=f"model_btn_{mk}", use_container_width=True):
            st.session_state.model = mk
            st.rerun()
        if is_active:
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin:0'>", unsafe_allow_html=True)

# ── CHAT AREA ─────────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        # Welcome screen
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Hello, I\'m NEXUS</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;color:#475569;font-size:16px;max-width:480px;margin:0 auto 32px auto;line-height:1.6">
          Your multi-model AI platform. Switch between Claude and Perplexity<br>to get the best answer for every question.
        </p>
        """, unsafe_allow_html=True)

        # Suggestion cards
        sc = st.columns(2)
        for i, (icon, title, prompt) in enumerate(SUGGESTIONS):
            with sc[i % 2]:
                if st.button(
                    f"{icon} **{title}**",
                    key=f"sug_{i}",
                    use_container_width=True,
                    help=prompt[:80]+"..."):
                    send_message(prompt)
                    st.rerun()
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    else:
        st.markdown("<div style='padding:16px 24px 100px 24px'>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            m_cfg = MODELS.get(msg.get("model","claude-sonnet-4-5"), MODELS["claude-sonnet-4-5"])
            t     = msg.get("time","")

            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin:8px 0 2px 0">
                  <div class="user-bubble">{msg['content']}</div>
                </div>
                <div class="msg-meta" style="text-align:right">{t}</div>
                """, unsafe_allow_html=True)
            else:
                badge_cls = "model-badge-claude" if m_cfg["provider"]=="anthropic" else "model-badge-perp"
                # Format content
                import re
                content = msg["content"]
                # Code blocks
                def fmt_code(m):
                    lang = m.group(1) or ""
                    code = m.group(2)
                    return f'<div class="code-block">{code}</div>'
                content = re.sub(r'```(\w+)?\n?(.*?)```', fmt_code, content, flags=re.DOTALL)
                content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
                content = re.sub(r'`([^`]+)`',
                    r'<code style="background:#0d1117;border:1px solid #1a1f2e;border-radius:4px;padding:1px 5px;font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#22d3ee">\1</code>',
                    content)
                content = content.replace('\n', '<br>')

                st.markdown(f"""
                <div style="margin:8px 0 2px 0">
                  <span class="{badge_cls}">{m_cfg['icon']} {m_cfg['label']}</span>
                  <div class="ai-bubble">{content}</div>
                </div>
                <div class="msg-meta">{t}</div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="position:fixed;bottom:0;left:0;right:0;background:linear-gradient(0deg,#04050a 70%,transparent);padding:12px 20px 20px;z-index:999">
""", unsafe_allow_html=True)

input_col, btn_col = st.columns([10, 1])
with input_col:
    user_input = st.text_input(
        label="",
        placeholder=f"Message NEXUS · {MODELS[st.session_state.model]['label']} · Press Send or Enter",
        key=f"user_input_{st.session_state.input_key}",
        label_visibility="collapsed")
with btn_col:
    st.markdown("<div style='padding-top:4px'>", unsafe_allow_html=True)
    send_clicked = st.button("➤ Send", key="send_main", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Clear conversation
if st.session_state.messages:
    if st.button("🗑 Clear conversation", key="clear_btn"):
        st.session_state.messages = []
        st.session_state.input_key += 1
        st.rerun()

# Trigger send
if send_clicked and user_input and user_input.strip():
    send_message(user_input)
    st.rerun()
elif user_input and user_input.strip() and user_input.endswith("\n"):
    send_message(user_input)
    st.rerun()

