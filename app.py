import streamlit as st
import requests
import urllib.parse
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MultiModal AI App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Light Glassmorphism ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

/* ── Root & animated background ── */
:root {
    --glass-bg:       rgba(255,255,255,0.60);
    --glass-border:   rgba(255,255,255,0.80);
    --glass-shadow:   0 8px 32px rgba(99,102,241,0.10);
    --primary:        #6366f1;
    --primary-light:  #818cf8;
    --primary-soft:   rgba(99,102,241,0.08);
    --secondary:      #a78bfa;
    --accent:         #38bdf8;
    --text-main:      #1e1b4b;
    --text-muted:     #6b7280;
    --surface:        rgba(255,255,255,0.75);
    --border:         rgba(209,213,219,0.6);
    --success:        #10b981;
    --radius-lg:      20px;
    --radius-xl:      28px;
}

/* Animated gradient background */
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(165,180,252,0.30) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(56,189,248,0.20) 0%, transparent 60%),
        radial-gradient(ellipse 70% 60% at 60% 20%, rgba(167,139,250,0.18) 0%, transparent 55%),
        linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #f0f9ff 100%);
    background-attachment: fixed;
    animation: bgShift 12s ease-in-out infinite alternate;
    min-height: 100vh;
}
@keyframes bgShift {
    0%   { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(20deg); }
}

/* ── Sidebar glass ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.70) !important;
    backdrop-filter: blur(20px) saturate(1.8) !important;
    -webkit-backdrop-filter: blur(20px) saturate(1.8) !important;
    border-right: 1px solid var(--glass-border) !important;
    box-shadow: 4px 0 24px rgba(99,102,241,0.08) !important;
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }
[data-testid="stSidebar"] .stCaption { color: var(--text-muted) !important; }

/* ── App title ── */
.app-title {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 2px;
}
.app-subtitle {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.3px;
    margin-bottom: 16px;
}

/* ── Page header ── */
.page-header {
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-xl);
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: var(--glass-shadow);
    animation: slideDown 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes slideDown {
    from { opacity:0; transform: translateY(-16px); }
    to   { opacity:1; transform: translateY(0); }
}
.page-header h2 {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-main);
    margin: 0 0 4px 0;
}
.page-header p {
    color: var(--text-muted);
    font-size: 13px;
    margin: 0;
}

/* ── Chat bubbles ── */
.bubble-wrap {
    animation: bubbleIn 0.35s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes bubbleIn {
    from { opacity:0; transform: translateY(10px) scale(0.97); }
    to   { opacity:1; transform: translateY(0) scale(1); }
}
.user-bubble {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 20px 20px 5px 20px;
    margin: 6px 0 2px auto;
    max-width: 78%;
    font-size: 14.5px;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(99,102,241,0.25), 0 1px 4px rgba(99,102,241,0.15);
    word-break: break-word;
}
.assistant-bubble {
    background: rgba(255,255,255,0.80);
    backdrop-filter: blur(12px);
    color: var(--text-main);
    padding: 14px 18px;
    border-radius: 20px 20px 20px 5px;
    margin: 6px auto 2px 0;
    max-width: 78%;
    font-size: 14.5px;
    line-height: 1.6;
    border: 1px solid var(--glass-border);
    box-shadow: 0 4px 16px rgba(99,102,241,0.07);
    word-break: break-word;
}
.bubble-label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.right-label { text-align: right; }

/* ── Image card ── */
.img-card {
    background: rgba(255,255,255,0.80);
    backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-xl);
    padding: 20px;
    margin-top: 16px;
    box-shadow: 0 8px 32px rgba(99,102,241,0.10);
    animation: fadeScale 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes fadeScale {
    from { opacity:0; transform: scale(0.96); }
    to   { opacity:1; transform: scale(1); }
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    margin-right: 6px;
}
.badge-chat {
    background: rgba(99,102,241,0.10);
    color: #6366f1;
    border: 1px solid rgba(99,102,241,0.20);
}
.badge-img {
    background: rgba(167,139,250,0.12);
    color: #7c3aed;
    border: 1px solid rgba(167,139,250,0.25);
}

/* ── Stat chips ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 12px 14px !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.07) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.13) !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
[data-testid="stMetricValue"] { color: var(--text-main) !important; font-weight: 800 !important; }

/* ── Inputs ── */
.stTextArea textarea,
.stTextInput input {
    background: rgba(255,255,255,0.80) !important;
    color: var(--text-main) !important;
    border: 1.5px solid rgba(209,213,219,0.7) !important;
    border-radius: 14px !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.05) !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder,
.stTextInput input::placeholder { color: #9ca3af !important; }
label[data-testid="stWidgetLabel"] p { color: var(--text-main) !important; font-weight: 600 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.22s cubic-bezier(0.16,1,0.3,1) !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.30) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.40) !important;
    filter: brightness(1.06) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
}
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    transition: all 0.22s cubic-bezier(0.16,1,0.3,1) !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.30) !important;
}
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.40) !important;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.70) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 8px 14px !important;
    margin-bottom: 6px !important;
    transition: all 0.18s ease !important;
    color: var(--text-main) !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] label:hover {
    background: rgba(99,102,241,0.07) !important;
    border-color: rgba(99,102,241,0.30) !important;
}

/* ── Select / Slider ── */
.stSelectbox div[data-baseweb="select"] > div,
.stSelectSlider .stSlider {
    background: rgba(255,255,255,0.80) !important;
    border: 1.5px solid rgba(209,213,219,0.7) !important;
    border-radius: 12px !important;
    color: var(--text-main) !important;
}
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div { color: var(--text-main) !important; }

/* ── Toggle ── */
[data-testid="stToggle"] span { color: var(--text-main) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.65) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid var(--glass-border) !important;
    gap: 4px !important;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    transition: all 0.2s ease !important;
    padding: 8px 18px !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    box-shadow: 0 3px 10px rgba(99,102,241,0.30) !important;
}

/* ── Info / Alert boxes ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(56,189,248,0.30) !important;
    border-radius: 14px !important;
    color: var(--text-main) !important;
}
[data-testid="stAlert"] p { color: var(--text-main) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: var(--text-muted) !important; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(209,213,219,0.5) !important;
    margin: 16px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.25);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.45); }

/* ── Main content area ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* ── Caption / small text ── */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
}

/* ── Markdown headers ── */
h1, h2, h3, h4 { color: var(--text-main) !important; }

/* ── Image ── */
[data-testid="stImage"] img {
    border-radius: 16px !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.12) !important;
}

/* ── Pulse animation for send buttons ── */
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(99,102,241,0.40); }
    70%  { box-shadow: 0 0 0 8px rgba(99,102,241,0); }
    100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
}

/* ── Empty state card ── */
.empty-state {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(12px);
    border: 1.5px dashed rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    color: var(--text-muted);
    font-size: 15px;
    animation: fadeIn 0.6s ease both;
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}
.empty-state .emoji { font-size: 36px; margin-bottom: 12px; }
.empty-state strong { color: var(--text-main); }

/* ── Footer caption ── */
.footer-note {
    font-size: 11px;
    color: var(--text-muted);
    background: rgba(255,255,255,0.55);
    border-radius: 10px;
    padding: 6px 10px;
    border: 1px solid var(--border);
    display: inline-block;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


# ── Groq API helper ────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
GROQ_MODEL   = "llama-3.1-8b-instant"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"


def chat_with_groq(messages: list, system_prompt: str = "") -> str:
    if not GROQ_API_KEY:
        return "⚠️ No GROQ_API_KEY found. Add it in `.streamlit/secrets.toml`."

    payload_messages = []
    if system_prompt:
        payload_messages.append({"role": "system", "content": system_prompt})
    payload_messages.extend(messages)

    try:
        resp = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": payload_messages,
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"❌ Groq API Error: {e.response.status_code} — {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ── Image generation via Pollinations.ai ───────────────────────────────────────
def generate_image_url(prompt: str, width: int = 768, height: int = 512, seed: int = None) -> str:
    encoded = urllib.parse.quote(prompt)
    seed_str = f"&seed={seed}" if seed else ""
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true{seed_str}"


def enhance_prompt_with_groq(raw_prompt: str) -> str:
    messages = [{"role": "user", "content": f"Improve this image generation prompt into a detailed, vivid, artistic description in 1-2 sentences. Only return the improved prompt, nothing else.\n\nOriginal: {raw_prompt}"}]
    return chat_with_groq(messages)


# ── Session state init ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "image_history" not in st.session_state:
    st.session_state.image_history = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "total_images" not in st.session_state:
    st.session_state.total_images = 0


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">🧠 MultiModal AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Artificial Intelligence Lab 10.0 · NLP</div>', unsafe_allow_html=True)

    st.markdown("---")

    mode = st.radio(
        "**Select Mode**",
        ["💬 Chat", "🎨 Image Generator", "🔀 Combined"],
        index=0,
    )

    st.markdown("---")

    # System prompt for chat
    if "💬" in mode or "🔀" in mode:
        st.markdown("**🤖 Assistant Persona**")
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful, smart, and friendly AI assistant. Be concise but informative.",
            height=100,
            label_visibility="collapsed",
        )
    else:
        system_prompt = ""

    # Image settings
    if "🎨" in mode or "🔀" in mode:
        st.markdown("**🖼️ Image Settings**")
        img_width  = st.select_slider("Width",  options=[512, 640, 768, 1024], value=768)
        img_height = st.select_slider("Height", options=[512, 640, 768, 1024], value=512)
        enhance    = st.toggle("✨ Auto-enhance prompt with AI", value=True)
        img_style  = st.selectbox(
            "Style Preset",
            ["None", "photorealistic", "anime", "watercolor", "oil painting",
             "digital art", "cinematic", "pixel art", "3D render"],
        )

    st.markdown("---")

    col1, col2 = st.columns(2)
    col1.metric("💬 Chats", st.session_state.total_messages)
    col2.metric("🖼️ Images", st.session_state.total_images)

    st.markdown("---")
    st.caption(f"**Model:** {GROQ_MODEL}")
    st.caption("**Images:** Pollinations.ai (free)")

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.image_history = []
        st.rerun()


# ── CHAT MODE ──────────────────────────────────────────────────────────────────
if "💬" in mode:
    st.markdown("""
    <div class="page-header">
        <h2>💬 Chat with AI</h2>
        <p>Powered by Groq · llama-3.1-8b-instant · Ask anything, get instant answers</p>
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="empty-state">
                <div class="emoji">👋</div>
                <strong>Start a conversation!</strong><br>
                Type your message below to chat with the AI assistant.
            </div>
            """, unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown('<div class="bubble-wrap"><div class="right-label bubble-label">You</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bubble-wrap"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="bubble-wrap"><div class="bubble-label">🤖 Assistant</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bubble-wrap"><div class="assistant-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Your message", placeholder="Ask me anything…", height=80, label_visibility="collapsed")
        submitted  = st.form_submit_button("Send ➤", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Thinking…"):
            response = chat_with_groq(st.session_state.chat_history, system_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.total_messages += 1
        st.rerun()


# ── IMAGE GENERATOR MODE ───────────────────────────────────────────────────────
elif "🎨" in mode:
    st.markdown("""
    <div class="page-header">
        <h2>🎨 AI Image Generator</h2>
        <p>Powered by Pollinations.ai · Free & unlimited · AI-enhanced prompts</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("img_form", clear_on_submit=True):
        prompt_input = st.text_area(
            "Image Prompt",
            placeholder="Describe the image you want to generate…",
            height=80,
            label_visibility="collapsed",
        )
        gen_btn = st.form_submit_button("🎨 Generate Image", use_container_width=True)

    if gen_btn and prompt_input.strip():
        final_prompt = prompt_input.strip()

        if img_style != "None":
            final_prompt += f", {img_style} style"

        if enhance:
            with st.spinner("✨ Enhancing prompt with AI…"):
                final_prompt = enhance_prompt_with_groq(final_prompt)
            st.info(f"**✨ Enhanced prompt:** {final_prompt}")

        with st.spinner("🎨 Generating image…"):
            seed = int(time.time())
            img_url = generate_image_url(final_prompt, img_width, img_height, seed)
            time.sleep(2)

        st.markdown('<div class="img-card">', unsafe_allow_html=True)
        st.image(img_url, caption=final_prompt[:80] + "…" if len(final_prompt) > 80 else final_prompt, use_container_width=True)
        st.markdown(f"[🔗 Open full image]({img_url})")
        st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.image_history.append({"prompt": final_prompt, "url": img_url})
        st.session_state.total_images += 1

    if st.session_state.image_history:
        st.markdown("---")
        st.markdown("### 🖼️ Generated Gallery")
        cols = st.columns(3)
        for i, item in enumerate(reversed(st.session_state.image_history[-9:])):
            with cols[i % 3]:
                st.image(item["url"], caption=item["prompt"][:40] + "…", use_container_width=True)


# ── COMBINED MODE ──────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="page-header">
        <h2>🔀 Multi-Modal AI</h2>
        <p>Chat with Groq LLaMA · Generate images with Pollinations.ai — all in one place</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💬 Chat", "🎨 Image Generator"])

    with tab1:
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="empty-state">
                    <div class="emoji">💬</div>
                    <strong>No messages yet.</strong><br>
                    Start a conversation below!
                </div>
                """, unsafe_allow_html=True)
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown('<div class="bubble-wrap"><div class="right-label bubble-label">You</div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="bubble-wrap"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="bubble-wrap"><div class="bubble-label">🤖 Assistant</div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="bubble-wrap"><div class="assistant-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        with st.form("combined_chat_form", clear_on_submit=True):
            user_input = st.text_area("Your message", placeholder="Ask me anything…", height=80, label_visibility="collapsed")
            submitted  = st.form_submit_button("Send ➤", use_container_width=True)

        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("Thinking…"):
                response = chat_with_groq(st.session_state.chat_history, system_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.total_messages += 1
            st.rerun()

    with tab2:
        with st.form("combined_img_form", clear_on_submit=True):
            prompt_input = st.text_area(
                "Image Prompt",
                placeholder="Describe the image you want to generate…",
                height=80,
                label_visibility="collapsed",
            )
            c1, c2, c3 = st.columns(3)
            w2 = c1.select_slider("Width",  options=[512, 640, 768, 1024], value=768)
            h2 = c2.select_slider("Height", options=[512, 640, 768, 1024], value=512)
            style2 = c3.selectbox("Style", ["None", "photorealistic", "anime", "watercolor", "oil painting", "digital art", "cinematic"])
            enhance2 = st.toggle("✨ Auto-enhance prompt", value=True)
            gen_btn2 = st.form_submit_button("🎨 Generate Image", use_container_width=True)

        if gen_btn2 and prompt_input.strip():
            final_prompt = prompt_input.strip()
            if style2 != "None":
                final_prompt += f", {style2} style"
            if enhance2:
                with st.spinner("✨ Enhancing prompt…"):
                    final_prompt = enhance_prompt_with_groq(final_prompt)
                st.info(f"**✨ Enhanced:** {final_prompt}")

            with st.spinner("🎨 Generating image…"):
                seed = int(time.time())
                img_url = generate_image_url(final_prompt, w2, h2, seed)
                time.sleep(2)

            st.markdown('<div class="img-card">', unsafe_allow_html=True)
            st.image(img_url, caption=final_prompt[:80], use_container_width=True)
            st.markdown(f"[🔗 Open full image]({img_url})")
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.image_history.append({"prompt": final_prompt, "url": img_url})
            st.session_state.total_images += 1

        if st.session_state.image_history:
            st.markdown("---")
            st.markdown("### 🖼️ Gallery")
            gcols = st.columns(3)
            for i, item in enumerate(reversed(st.session_state.image_history[-6:])):
                with gcols[i % 3]:
                    st.image(item["url"], caption=item["prompt"][:40] + "…", use_container_width=True)
