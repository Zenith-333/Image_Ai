import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(
    page_title="MultiModal AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Premium Light UI ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"] { display: none !important; }

/* Page background */
.stApp {
    background: #f7f8fc !important;
}
.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 4rem !important;
}

/* ── HEADER ── */
.app-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.app-logo {
    width: 48px; height: 48px;
    background: #fff;
    border: 1px solid #e4e6ef;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    font-size: 22px;
    line-height: 1;
}
.app-title {
    font-size: 22px;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}
.app-sub {
    font-size: 13px;
    color: #9ca3af;
    font-weight: 400;
}
.badge-row {
    display: flex; gap: 6px; justify-content: center; margin-top: 10px;
}
.badge {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.04em;
    padding: 3px 9px;
    border-radius: 20px;
    background: #f0f0f8;
    color: #6b73a8;
    border: 1px solid #e4e6ef;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff !important;
    border: 1px solid #e4e6ef !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #9ca3af !important;
    padding: 8px 20px !important;
    border: none !important;
    transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #f4f3ff !important;
    color: #5b52e8 !important;
    box-shadow: 0 1px 3px rgba(91,82,232,0.15) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── CHAT BUBBLES ── */
.msg-wrap-user {
    display: flex; justify-content: flex-end; margin: 8px 0;
}
.msg-wrap-ai {
    display: flex; justify-content: flex-start; margin: 8px 0;
}
.bubble-user {
    background: #5b52e8;
    color: #fff;
    padding: 11px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 76%;
    font-size: 14px;
    line-height: 1.55;
    font-weight: 400;
}
.bubble-ai {
    background: #fff;
    color: #1f2937;
    padding: 11px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 76%;
    font-size: 14px;
    line-height: 1.55;
    border: 1px solid #e4e6ef;
    font-weight: 400;
}
.chat-box {
    background: #fff;
    border: 1px solid #e4e6ef;
    border-radius: 16px;
    padding: 16px;
    min-height: 380px;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 12px;
}
.chat-empty {
    height: 340px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 10px; color: #9ca3af; text-align: center;
}
.chat-empty-icon {
    font-size: 32px; opacity: 0.4;
}

/* ── INPUTS ── */
.stTextArea textarea {
    background: #fff !important;
    border: 1px solid #e4e6ef !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    color: #1f2937 !important;
    padding: 12px 14px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #5b52e8 !important;
    box-shadow: 0 0 0 3px rgba(91,82,232,0.1) !important;
}
.stTextArea textarea::placeholder { color: #c4c9d9 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #5b52e8 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 4px rgba(91,82,232,0.25) !important;
}
.stButton > button:hover {
    background: #4a43d4 !important;
    box-shadow: 0 4px 12px rgba(91,82,232,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary clear button */
.stButton.secondary > button {
    background: #fff !important;
    color: #6b7280 !important;
    border: 1px solid #e4e6ef !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
.stButton.secondary > button:hover {
    background: #f9fafb !important;
    color: #374151 !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: #fff;
    border: 1px solid #e4e6ef;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
[data-testid="stFormSubmitButton"] > button {
    width: 100%;
    justify-content: center;
}

/* ── SELECTBOX & SLIDERS ── */
.stSelectbox > div > div {
    background: #fff !important;
    border: 1px solid #e4e6ef !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    color: #374151 !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #5b52e8 !important;
    border-color: #5b52e8 !important;
}
.stSlider [data-baseweb="slider"] div[data-testid="stTickBar"] { display: none !important; }

/* ── TOGGLE ── */
.stToggle label span { background: #5b52e8 !important; }

/* ── IMAGE CARD ── */
.img-card {
    background: #fff;
    border: 1px solid #e4e6ef;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.img-caption {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 10px;
    line-height: 1.5;
}
.img-link {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: #5b52e8;
    font-weight: 500;
    margin-top: 8px;
    text-decoration: none;
}

/* ── INFO / ENHANCED PROMPT ── */
.stAlert {
    background: #f4f3ff !important;
    border: 1px solid #d4d0fa !important;
    border-radius: 10px !important;
    color: #4a43d4 !important;
    font-size: 13px !important;
}

/* ── GALLERY ── */
.gallery-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    color: #9ca3af;
    text-transform: uppercase;
    margin: 1.2rem 0 0.6rem;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #5b52e8 !important; }

/* ── DIVIDER ── */
hr { border-color: #f0f0f8 !important; margin: 0.8rem 0 !important; }

/* Column gap fix */
[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)


# ── CONFIG ─────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets.get("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", "")
GROQ_MODEL   = "llama-3.1-8b-instant"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"


# ── HELPERS ────────────────────────────────────────────────────────────────────
def chat_with_groq(messages: list) -> str:
    if not GROQ_API_KEY:
        return "⚠️ No GROQ_API_KEY — add it in Streamlit Cloud Secrets."
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "system", "content": "You are a helpful, smart, concise AI assistant."}] + messages,
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ {str(e)}"


def enhance_prompt(raw: str) -> str:
    msgs = [{"role": "user", "content": f"Rewrite into a vivid, detailed image generation prompt (1-2 sentences). Return ONLY the improved prompt:\n\n{raw}"}]
    return chat_with_groq(msgs)


def image_url(prompt: str, w: int = 768, h: int = 512) -> str:
    seed = int(time.time())
    return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width={w}&height={h}&seed={seed}&nologo=true"


# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("chat_history", []), ("image_history", [])]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-logo">✦</div>
  <div class="app-title">MultiModal AI</div>
  <div class="app-sub">Artificial Intelligence · Lab 10.0 · NLP</div>
  <div class="badge-row">
    <span class="badge">llama-3.1-8b-instant</span>
    <span class="badge">Groq</span>
    <span class="badge">Pollinations.ai</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab_chat, tab_img = st.tabs(["  💬  Chat  ", "  🎨  Image Generator  "])


# ════════════════════════════════════════════════════════════════════════════════
# CHAT TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Message display
    chat_html = '<div class="chat-box">'
    if not st.session_state.chat_history:
        chat_html += '''
        <div class="chat-empty">
          <div class="chat-empty-icon">💬</div>
          <div style="font-size:14px;font-weight:500;color:#6b7280;">Start a conversation</div>
          <div style="font-size:12px;color:#c4c9d9;">Powered by Groq · LLaMA 3.1</div>
        </div>'''
    else:
        for msg in st.session_state.chat_history:
            txt = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            if msg["role"] == "user":
                chat_html += f'<div class="msg-wrap-user"><div class="bubble-user">{txt}</div></div>'
            else:
                chat_html += f'<div class="msg-wrap-ai"><div class="bubble-ai">{txt}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "msg", placeholder="Type your message… (Enter to send)",
            height=80, label_visibility="collapsed"
        )
        c1, c2 = st.columns([4, 1])
        with c1:
            sent = st.form_submit_button("Send  ➤", use_container_width=True)
        with c2:
            cleared = st.form_submit_button("Clear", use_container_width=True)

    if sent and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Thinking…"):
            reply = chat_with_groq(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if cleared:
        st.session_state.chat_history = []
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
# IMAGE TAB
# ════════════════════════════════════════════════════════════════════════════════
with tab_img:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    with st.form("img_form", clear_on_submit=True):
        prompt_input = st.text_area(
            "prompt", placeholder="Describe the image you want to generate…",
            height=90, label_visibility="collapsed"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            style = st.selectbox("Style", ["None", "photorealistic", "anime",
                                           "watercolor", "oil painting",
                                           "digital art", "cinematic", "3D render"],
                                 label_visibility="visible")
        with c2:
            width = st.select_slider("Width", options=[512, 640, 768, 1024], value=768)
        with c3:
            height = st.select_slider("Height", options=[512, 640, 768, 1024], value=512)

        enhance = st.toggle("✦ Enhance prompt with AI", value=True)
        gen = st.form_submit_button("Generate Image  →", use_container_width=True)

    if gen and prompt_input.strip():
        final = prompt_input.strip()
        if style != "None":
            final += f", {style} style"

        if enhance:
            with st.spinner("Enhancing prompt…"):
                final = enhance_prompt(final)
            st.info(f"**Enhanced →** {final}")

        with st.spinner("Generating image…"):
            url = image_url(final, width, height)
            time.sleep(2)

        st.markdown('<div class="img-card">', unsafe_allow_html=True)
        st.image(url, use_container_width=True)
        caption = final if len(final) <= 90 else final[:90] + "…"
        st.markdown(f'<div class="img-caption">{caption}</div>', unsafe_allow_html=True)
        st.markdown(f'<a class="img-link" href="{url}" target="_blank">↗ Open full image</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.image_history.insert(0, {"url": url, "prompt": final})

    # Gallery
    if st.session_state.image_history:
        st.markdown('<div class="gallery-label">Recent</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.image_history[:6]):
            with cols[i % 3]:
                st.image(item["url"], caption=item["prompt"][:38] + "…", use_container_width=True)
