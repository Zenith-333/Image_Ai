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

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d27 0%, #12151f 100%);
        border-right: 1px solid #2d3047;
    }

    /* Chat messages */
    .user-bubble {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 2px 12px rgba(79, 70, 229, 0.3);
    }
    .assistant-bubble {
        background: #1e2130;
        color: #e2e8f0;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 80%;
        font-size: 15px;
        line-height: 1.5;
        border: 1px solid #2d3047;
    }
    .bubble-label {
        font-size: 11px;
        color: #6b7280;
        margin-bottom: 4px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .right-label { text-align: right; }

    /* Image card */
    .img-card {
        background: #1e2130;
        border: 1px solid #2d3047;
        border-radius: 16px;
        padding: 16px;
        margin-top: 12px;
    }

    /* Title styling */
    .app-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .app-subtitle {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* Mode badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-chat { background: #312e81; color: #a5b4fc; }
    .badge-img  { background: #4a1d96; color: #d8b4fe; }

    /* Divider */
    hr { border-color: #2d3047; }

    /* Input box override */
    .stTextArea textarea {
        background: #1e2130 !important;
        color: #e2e8f0 !important;
        border: 1px solid #3d4263 !important;
        border-radius: 12px !important;
    }
    .stTextInput input {
        background: #1e2130 !important;
        color: #e2e8f0 !important;
        border: 1px solid #3d4263 !important;
        border-radius: 12px !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #1e2130;
        border: 1px solid #2d3047;
        border-radius: 12px;
        padding: 10px;
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


# ── Image generation via Pollinations.ai (free, no key) ────────────────────────
def generate_image_url(prompt: str, width: int = 768, height: int = 512, seed: int = None) -> str:
    encoded = urllib.parse.quote(prompt)
    seed_str = f"&seed={seed}" if seed else ""
    return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true{seed_str}"


def enhance_prompt_with_groq(raw_prompt: str) -> str:
    """Ask Groq to improve the image prompt for better results."""
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

    # Stats
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


# ── Main area ──────────────────────────────────────────────────────────────────

# ── CHAT MODE ──────────────────────────────────────────────────────────────────
if "💬" in mode:
    st.markdown("## 💬 Chat with AI")
    st.caption(f"Powered by Groq · {GROQ_MODEL}")
    st.markdown("---")

    # Display conversation
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.info("👋 Start a conversation below!")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="right-label bubble-label">You</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bubble-label">🤖 Assistant</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="assistant-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Input
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
    st.markdown("## 🎨 AI Image Generator")
    st.caption("Powered by Pollinations.ai · Free & unlimited")
    st.markdown("---")

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

        # Add style preset
        if img_style != "None":
            final_prompt += f", {img_style} style"

        # Enhance with Groq
        if enhance:
            with st.spinner("✨ Enhancing prompt with AI…"):
                final_prompt = enhance_prompt_with_groq(final_prompt)
            st.info(f"**Enhanced prompt:** {final_prompt}")

        # Generate image
        with st.spinner("🎨 Generating image…"):
            seed = int(time.time())
            img_url = generate_image_url(final_prompt, img_width, img_height, seed)
            # Small delay so Pollinations renders it
            time.sleep(2)

        st.markdown('<div class="img-card">', unsafe_allow_html=True)
        st.image(img_url, caption=final_prompt[:80] + "…" if len(final_prompt) > 80 else final_prompt, use_container_width=True)
        st.markdown(f"[🔗 Open full image]({img_url})")
        st.markdown('</div>', unsafe_allow_html=True)

        # Save to history
        st.session_state.image_history.append({"prompt": final_prompt, "url": img_url})
        st.session_state.total_images += 1

    # Image history gallery
    if st.session_state.image_history:
        st.markdown("---")
        st.markdown("### 🖼️ Generated Gallery")
        cols = st.columns(3)
        for i, item in enumerate(reversed(st.session_state.image_history[-9:])):
            with cols[i % 3]:
                st.image(item["url"], caption=item["prompt"][:40] + "…", use_container_width=True)


# ── COMBINED MODE ──────────────────────────────────────────────────────────────
else:
    st.markdown("## 🔀 Multi-Modal AI — Chat + Image")
    st.caption("Chat with Groq LLaMA · Generate images with Pollinations.ai")
    st.markdown("---")

    tab1, tab2 = st.tabs(["💬 Chat", "🎨 Image Generator"])

    # --- Chat tab ---
    with tab1:
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.info("👋 Start a conversation below!")
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="right-label bubble-label">You</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bubble-label">🤖 Assistant</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="assistant-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

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

    # --- Image tab ---
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
                st.info(f"**Enhanced:** {final_prompt}")

            with st.spinner("🎨 Generating image…"):
                seed = int(time.time())
                img_url = generate_image_url(final_prompt, w2, h2, seed)
                time.sleep(2)

            st.image(img_url, caption=final_prompt[:80], use_container_width=True)
            st.markdown(f"[🔗 Open full image]({img_url})")
            st.session_state.image_history.append({"prompt": final_prompt, "url": img_url})
            st.session_state.total_images += 1

        if st.session_state.image_history:
            st.markdown("---")
            st.markdown("### 🖼️ Gallery")
            gcols = st.columns(3)
            for i, item in enumerate(reversed(st.session_state.image_history[-6:])):
                with gcols[i % 3]:
                    st.image(item["url"], caption=item["prompt"][:40] + "…", use_container_width=True)
