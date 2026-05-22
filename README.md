# 🧠 MultiModal AI App — Lab 10.0
**Natural Language Processing · Artificial Intelligence 10.0**

A multi-modal AI web app combining:
- **💬 Chat** powered by Groq (LLaMA 3.1 8B Instant)
- **🎨 Image Generation** powered by Pollinations.ai (free, no key needed)
- **🔀 Combined mode** — both in one interface

---

## 🚀 Deploy to Streamlit Cloud (Step-by-Step)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Lab 10: MultiModal AI App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Connect your GitHub repo
4. Set **Main file path** → `app.py`
5. Click **"Advanced settings"** → **Secrets** tab
6. Add your Groq API key:
```toml
GROQ_API_KEY = "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"
```
7. Click **Deploy!** 🎉

> ⚠️ Never commit your actual API key in secrets.toml to GitHub!

---

## 🗂️ File Structure
```
lab10_multimodal/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .streamlit/
│   ├── config.toml         # Theme settings
│   └── secrets.toml        # API keys (DO NOT push to GitHub)
└── README.md
```

---

## 🔧 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Tech Stack
| Component | Tool |
|-----------|------|
| Web framework | Streamlit |
| Chat model | Groq — LLaMA 3.1 8B Instant |
| Image generation | Pollinations.ai |
| Language | Python 3.10+ |
