import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(
    page_title="NeuralOS · MultiModal AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PREMIUM TECH UI ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #080b12;
    --bg2:       #0d1117;
    --bg3:       #111827;
    --surface:   rgba(255,255,255,0.03);
    --border:    rgba(255,255,255,0.07);
    --border2:   rgba(255,255,255,0.12);
    --accent:    #00d4ff;
    --accent2:   #7b61ff;
    --accent3:   #00ff9d;
    --text:      #e8eaf0;
    --muted:     #4a5168;
    --muted2:    #6b7494;
}

*, html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    box-sizing: border-box;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

#MainMenu, footer, header { display: none !important; }

.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(0,212,255,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(123,97,255,0.06) 0%, transparent 60%) !important;
}

.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem !important;
}

.logo-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}
.logo-hex {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: #000; font-weight: 800;
    flex-shrink: 0;
}
.logo-name {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text);
    line-height: 1;
}
.logo-name span {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.logo-tag {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding-left: 2px;
    margin-bottom: 18px;
}

.sec-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 18px 0 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.stRadio [data-testid="stMarkdownContainer"] p { display: none; }
.stRadio > div { gap: 6px !important; }
.stRadio label {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    color: var(--muted2) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stRadio label:hover {
    border-color: var(--border2) !important;
    color: var(--text) !important;
}
[data-testid="stWidgetLabel"] { display: none !important; }

.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    padding: 12px 14px !important;
    resize: none !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.08) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder {
    color: var(--muted) !important;
    font-size: 12px !important;
}
.stTextArea label { color: var(--muted2) !important; font-size: 11px !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    padding: 11px 22px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.12) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0,212,255,0.28) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #000 !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-size: 11px !important;
}

[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 12px !important;
}
.stSelectbox svg { fill: var(--muted2) !important; }

.stSlider > div > div > div { background: var(--border2) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.4) !important;
}

.stCheckbox label span,
.stToggle label span { background: var(--accent) !important; }

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted2) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 12px 22px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 20px 0 !important; }

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted2) !important;
}
[data-testid="stMetricValue"] {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

.stSpinner > div { border-top-color: var(--accent) !important; }

.stAlert {
    background: rgba(0,212,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.18) !important;
    border-radius: 10px !important;
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.02em !important;
}

hr { border-color: var(--border) !important; }

.chat-viewport {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    min-height: 420px;
    max-height: 460px;
    overflow-y: auto;
    margin-bottom: 14px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.chat-empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 60px 0;
}
.chat-empty-glyph { font-size: 40px; opacity: 0.1; }
.chat-empty-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--muted2);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.chat-empty-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.1em;
}
.msg-row-user { display: flex; justify-content: flex-end; }
.msg-row-ai   { display: flex; justify-content: flex-start; gap: 10px; align-items: flex-end; }
.ai-avatar {
    width: 28px; height: 28px; flex-shrink: 0;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; color: #000; font-weight: 800;
}
.bubble-user {
    background: linear-gradient(135deg, var(--accent2), #5b4fd4);
    color: #fff;
    padding: 12px 16px;
    border-radius: 16px 16px 4px 16px;
    max-width: 72%;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(123,97,255,0.2);
}
.bubble-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border2);
    color: var(--text);
    padding: 12px 16px;
    border-radius: 16px 16px 16px 4px;
    max-width: 72%;
    font-size: 14px;
    line-height: 1.6;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.page-title {
    font-size: 26px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
}
.page-title span {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted2);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 14px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.img-result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px;
    margin-top: 16px;
}
.img-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    margin-top: 10px;
    line-height: 1.5;
    letter-spacing: 0.03em;
}
.img-open-link {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
}

.gallery-hdr {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.gallery-hdr::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.04em !important;
}

[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)


# ── CONFIG ─────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
GROQ_MODEL   = "llama-3.1-8b-instant"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"


# ── HELPERS ────────────────────────────────────────────────────────────────────
def chat_with_groq(messages: list, system_prompt: str = "") -> str:
    if not GROQ_API_KEY:
        return "⚠️ No GROQ_API_KEY found. Add it in Streamlit Cloud → Settings → Secrets."
    payload = []
    if system_prompt:
        payload.append({"role": "system", "content": system_prompt})
    payload.extend(messages)
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "messages": payload, "temperature": 0.7, "max_tokens": 1024},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"❌ Groq API Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ {str(e)}"


def generate_image_url(prompt: str, width: int = 768, height: int = 512, seed: int = None) -> str:
    encoded = urllib.parse.quote(prompt)
    s = f"&seed={seed}" if seed else ""
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true{s}"


def enhance_prompt(raw: str) -> str:
    msgs = [{"role": "user", "content": f"Rewrite into a vivid, detailed image generation prompt (1-2 sentences). Return ONLY the improved prompt:\n\n{raw}"}]
    return chat_with_groq(msgs)


# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("chat_history", []), ("image_history", []),
              ("total_messages", 0), ("total_images", 0)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
      <div class="logo-hex">N</div>
      <div class="logo-name">Neural<span>OS</span></div>
    </div>
    <div class="logo-tag">Artificial Intelligence · Lab 10.0 · NLP</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Navigation</div>', unsafe_allow_html=True)
    mode = st.radio(
        "mode",
        ["💬  Chat", "🎨  Image Generator", "⬡  Combined"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<div class="sec-label">Chat Config</div>', unsafe_allow_html=True)
    system_prompt = st.text_area(
        "sys",
        value="You are a helpful, smart, and friendly AI assistant. Be concise but informative.",
        height=90,
        label_visibility="collapsed",
        placeholder="System persona…",
    )

    st.markdown('<div class="sec-label">Image Config</div>', unsafe_allow_html=True)
    img_width  = st.select_slider("Width",  options=[512, 640, 768, 1024], value=768)
    img_height = st.select_slider("Height", options=[512, 640, 768, 1024], value=512)
    enhance    = st.toggle("✦ AI Prompt Enhancer", value=True)
    img_style  = st.selectbox(
        "style",
        ["None", "photorealistic", "anime", "watercolor",
         "oil painting", "digital art", "cinematic", "pixel art", "3D render"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sec-label">Session Stats</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Chats", st.session_state.total_messages)
    c2.metric("Images", st.session_state.total_images)

    st.markdown('<div class="sec-label">System</div>', unsafe_allow_html=True)
    st.caption(f"MODEL  ·  {GROQ_MODEL}")
    st.caption("IMAGE  ·  Pollinations.ai (free)")

    if st.button("⬡  Clear Session", use_container_width=True):
        st.session_state.chat_history   = []
        st.session_state.image_history  = []
        st.session_state.total_messages = 0
        st.session_state.total_images   = 0
        st.rerun()


# ── CHAT RENDERER ──────────────────────────────────────────────────────────────
def render_chat(form_key: str, sp: str):
    html = '<div class="chat-viewport">'
    if not st.session_state.chat_history:
        html += """
        <div class="chat-empty">
          <div class="chat-empty-glyph">⬡</div>
          <div class="chat-empty-title">Awaiting Input</div>
          <div class="chat-empty-sub">GROQ · LLAMA-3.1-8B-INSTANT</div>
        </div>"""
    else:
        for msg in st.session_state.chat_history:
            txt = (msg["content"]
                   .replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\n", "<br>"))
            if msg["role"] == "user":
                html += f'<div class="msg-row-user"><div class="bubble-user">{txt}</div></div>'
            else:
                html += f'<div class="msg-row-ai"><div class="ai-avatar">N</div><div class="bubble-ai">{txt}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    with st.form(form_key, clear_on_submit=True):
        user_input = st.text_area(
            "input", placeholder="Transmit a message…",
            height=72, label_visibility="collapsed"
        )
        c1, c2 = st.columns([5, 1])
        with c1:
            sent = st.form_submit_button("Transmit  →", use_container_width=True)
        with c2:
            clr = st.form_submit_button("✕", use_container_width=True)

    if sent and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Processing…"):
            reply = chat_with_groq(st.session_state.chat_history, sp)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.total_messages += 1
        st.rerun()
    if clr:
        st.session_state.chat_history = []
        st.rerun()


# ── IMAGE RENDERER ─────────────────────────────────────────────────────────────
def render_image(form_key: str, w: int, h: int, style: str, enh: bool, sp: str):
    with st.form(form_key, clear_on_submit=True):
        prompt_input = st.text_area(
            "prompt", placeholder="Describe the image to render…",
            height=80, label_visibility="collapsed"
        )
        gen = st.form_submit_button("Render Image  →", use_container_width=True)

    if gen and prompt_input.strip():
        final = prompt_input.strip()
        if style != "None":
            final += f", {style} style"
        if enh:
            with st.spinner("Enhancing prompt…"):
                final = enhance_prompt(final)
            st.info(f"ENHANCED →  {final}")
        with st.spinner("Rendering…"):
            seed    = int(time.time())
            img_url = generate_image_url(final, w, h, seed)
            time.sleep(2)

        st.markdown('<div class="img-result-card">', unsafe_allow_html=True)
        st.image(img_url, use_container_width=True)
        caption = final if len(final) <= 100 else final[:100] + "…"
        st.markdown(f'<div class="img-meta">{caption}</div>', unsafe_allow_html=True)
        st.markdown(f'<a class="img-open-link" href="{img_url}" target="_blank">↗ Open Full Resolution</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.image_history.insert(0, {"prompt": final, "url": img_url})
        st.session_state.total_images += 1

    if st.session_state.image_history:
        st.markdown('<div class="gallery-hdr">Recent Renders</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.image_history[:6]):
            with cols[i % 3]:
                st.image(item["url"], caption=item["prompt"][:40] + "…", use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# CHAT MODE
# ════════════════════════════════════════════════════════════════════════════════
if "Chat" in mode:
    st.markdown("""
    <div class="page-header">
      <div class="page-title"><span>Chat</span> Interface</div>
      <div class="page-badge">Groq · LLaMA 3.1 · 8B Instant</div>
    </div>
    """, unsafe_allow_html=True)
    render_chat("chat_main", system_prompt)


# ════════════════════════════════════════════════════════════════════════════════
# IMAGE MODE
# ════════════════════════════════════════════════════════════════════════════════
elif "Image" in mode:
    st.markdown("""
    <div class="page-header">
      <div class="page-title"><span>Image</span> Generator</div>
      <div class="page-badge">Pollinations.ai · Free · Unlimited</div>
    </div>
    """, unsafe_allow_html=True)
    render_image("img_main", img_width, img_height, img_style, enhance, system_prompt)


# ════════════════════════════════════════════════════════════════════════════════
# COMBINED MODE
# ════════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="page-header">
      <div class="page-title">Multi<span>Modal</span> Studio</div>
      <div class="page-badge">Chat + Image · Unified</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["  ⬡  Chat  ", "  ⬡  Image Generator  "])
    with tab1:
        render_chat("chat_combined", system_prompt)
    with tab2:
        render_image("img_combined", img_width, img_height, img_style, enhance, system_prompt)
