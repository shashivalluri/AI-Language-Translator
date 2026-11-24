import streamlit as st
from deep_translator import GoogleTranslator
import time
import html

# ==========================================
# 1. Configuration & Setup
# ==========================================
st.set_page_config(
    page_title="Translate Pro | Awwwards Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
APP_VERSION = "2.1.0"
DEVELOPER = "Shashi Valluri"

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Telugu": "te"
}

# ==========================================
# 2. State Management
# ==========================================
def init_state():
    """Initialize session state variables."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'source_lang' not in st.session_state:
        st.session_state.source_lang = "Auto Detect"
    if 'target_lang' not in st.session_state:
        st.session_state.target_lang = "English"
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""
    if 'translation_stats' not in st.session_state:
        st.session_state.translation_stats = None

# ==========================================
# 3. Custom CSS — Awwwards Light Monochrome Design System
#    Inter Tight · Tonal surfaces · 72px corners
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* ── FONTS ─────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

        /* ── BASE ───────────────────────────────────── */
        html, body,
        [class*="css"],
        .stApp,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stMain"],
        section[data-testid="stSidebar"] {
            font-family: 'Inter Tight', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: #E9E9E9 !important;
            color: #222222 !important;
        }

        header[data-testid="stHeader"] {
            background-color: #E9E9E9 !important;
            border-bottom: 1px solid #A7A7A7 !important;
        }

        /* hide the streamlit deploy/github icons for a cleaner look */
        div[data-testid="stToolbar"] { display: none !important; }

        .block-container {
            max-width: 1320px !important;
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
        }

        /* ── HERO ───────────────────────────────────── */
        .hero-wrap {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .hero-badge {
            display: inline-block;
            background: #FFFFFF;
            border: 1px solid #A7A7A7;
            border-radius: 72px;
            padding: 5px 20px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1.6px;
            text-transform: uppercase;
            color: #222222;
            margin-bottom: 18px;
        }

        .hero-title {
            font-size: clamp(38px, 6vw, 76px);
            font-weight: 600;
            line-height: 1;
            letter-spacing: -1.5px;
            text-transform: uppercase;
            color: #222222;
            margin: 0 0 14px 0;
        }

        .hero-subtitle {
            font-size: 16px;
            font-weight: 300;
            line-height: 1.65;
            color: #4A4A4A;
            max-width: 680px;
            margin: 0 auto;
        }

        /* ── PRIMARY BUTTON (Translate) ─────────────── */
        button[kind="primary"],
        button[data-testid="baseButton-primary"] {
            background-color: #222222 !important;
            color: #FFFFFF !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 0 20px !important;
            height: 42px !important;
            box-shadow: none !important;
            transition: background 0.3s ease, border-color 0.3s ease !important;
            letter-spacing: 0.2px !important;
        }
        button[kind="primary"]:hover,
        button[data-testid="baseButton-primary"]:hover {
            background-color: #383838 !important;
            border-color: #383838 !important;
        }
        button[kind="primary"]:active,
        button[data-testid="baseButton-primary"]:active {
            background-color: #111111 !important;
            border-color: #111111 !important;
        }

        /* ── SECONDARY BUTTON (Clear, Swap) ─────────── */
        button[kind="secondary"],
        button[data-testid="baseButton-secondary"] {
            background-color: #FFF083 !important;
            color: #222222 !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 8px !important;
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            padding: 0 15.6px !important;
            height: 42px !important;
            box-shadow: none !important;
            transition: background 0.3s ease, border-color 0.3s ease !important;
        }
        button[kind="secondary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #F0D940 !important;
            border-color: #222222 !important;
        }

        /* ── SELECTBOX ──────────────────────────────── */
        div[data-baseweb="select"] > div {
            background-color: #F8F8F8 !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 8px !important;
            color: #222222 !important;
            box-shadow: none !important;
            min-height: 42px !important;
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 13px !important;
            transition: border-color 0.3s ease, background 0.3s ease !important;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #222222 !important;
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #222222 !important;
            font-family: 'Inter Tight', sans-serif !important;
        }
        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[data-testid="stSelectboxVirtualDropdown"] {
            background-color: #FFFFFF !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
        }
        li[role="option"] {
            color: #222222 !important;
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 13px !important;
            transition: background 0.2s ease !important;
        }
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: #EDEDED !important;
        }

        /* ── TEXT AREA ──────────────────────────────── */
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 12px !important;
            color: #222222 !important;
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 14px !important;
            font-weight: 300 !important;
            line-height: 2 !important;
            padding: 18px !important;
            box-shadow: none !important;
            transition: border-color 0.3s ease !important;
            min-height: 250px !important;
        }
        .stTextArea textarea:focus {
            border-color: #222222 !important;
            box-shadow: 0 0 0 1px #222222 !important;
            outline: none !important;
        }
        .stTextArea textarea::placeholder {
            color: #999999 !important;
            font-weight: 300 !important;
        }

        /* ── OUTPUT CARD ────────────────────────────── */
        .output-card {
            background-color: #F8F8F8;
            border: 1px solid #A7A7A7;
            border-radius: 12px;
            padding: 22px 24px;
            font-size: 14px;
            font-weight: 300;
            line-height: 2;
            color: #222222;
            min-height: 250px;
            box-shadow: none;
            white-space: pre-wrap;
            transition: border-color 0.3s ease;
            font-family: 'Inter Tight', sans-serif;
        }

        .output-placeholder {
            color: #999999;
            font-size: 13px;
            font-weight: 300;
            font-family: 'Inter Tight', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 210px;
            letter-spacing: 0.3px;
        }

        /* ── SECTION PILL LABEL ─────────────────────── */
        .section-pill {
            display: inline-block;
            background: #FFFFFF;
            border: 1px solid #A7A7A7;
            border-radius: 72px;
            padding: 5px 18px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: #222222;
            margin-bottom: 18px;
        }

        /* ── METRIC GRID ────────────────────────────── */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 0 0 2rem 0;
        }
        @media (max-width: 860px) {
            .metric-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 480px) {
            .metric-grid { grid-template-columns: 1fr; }
        }

        .metric-card {
            background-color: #F8F8F8;
            border: 1px solid #A7A7A7;
            border-radius: 72px;
            padding: 18px 24px;
            text-align: center;
            transition: background 0.3s ease, border-color 0.3s ease;
        }
        .metric-card:hover {
            background-color: #FFFFFF;
            border-color: #222222;
        }
        .metric-label {
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: #666666;
            margin-bottom: 4px;
            font-family: 'Inter Tight', sans-serif;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 600;
            color: #222222;
            line-height: 1.1;
            font-family: 'Inter Tight', sans-serif;
        }

        /* ── HISTORY CARD ───────────────────────────── */
        .history-card {
            background-color: #F8F8F8;
            border: 1px solid #A7A7A7;
            border-radius: 20px;
            padding: 20px 24px;
            margin-bottom: 12px;
            transition: background 0.3s ease, border-color 0.3s ease, transform 0.3s ease;
        }
        .history-card:hover {
            background-color: #FFFFFF;
            border-color: #222222;
            transform: translateY(-2px);
        }

        .history-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #A7A7A7;
        }

        .history-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: #EDEDED;
            border: 1px solid #A7A7A7;
            border-radius: 72px;
            padding: 4px 14px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #222222;
            font-family: 'Inter Tight', sans-serif;
        }

        .history-ts {
            font-size: 12px;
            font-weight: 300;
            color: #666666;
            font-family: 'Inter Tight', sans-serif;
        }

        .history-body {
            display: flex;
            gap: 24px;
        }
        @media (max-width: 768px) {
            .history-body { flex-direction: column; gap: 10px; }
        }

        .history-col {
            flex: 1;
            font-size: 13px;
            line-height: 2.15;
            font-family: 'Inter Tight', sans-serif;
            max-height: 110px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .history-col.src { color: #666666; font-weight: 300; }
        .history-col.tgt { color: #222222; font-weight: 500; }

        /* ── EXPANDER ───────────────────────────────── */
        div[data-testid="stExpander"] {
            background-color: #F8F8F8 !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            margin-top: 10px !important;
        }
        div[data-testid="stExpander"] summary {
            font-family: 'Inter Tight', sans-serif !important;
            font-size: 13px !important;
            font-weight: 400 !important;
            color: #222222 !important;
        }

        /* ── ALERTS / INFO ──────────────────────────── */
        div[data-testid="stAlert"] {
            background-color: #F8F8F8 !important;
            border: 1px solid #A7A7A7 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
            color: #222222 !important;
            font-family: 'Inter Tight', sans-serif !important;
        }

        /* ── DIVIDER ────────────────────────────────── */
        hr {
            border: none !important;
            border-top: 1px solid #A7A7A7 !important;
            margin: 2.5rem 0 !important;
        }

        /* ── SCROLLBAR ──────────────────────────────── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #A7A7A7; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #666666; }

        /* ── FOOTER ─────────────────────────────────── */
        .footer {
            text-align: center;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid #A7A7A7;
            font-family: 'Inter Tight', sans-serif;
        }
        .footer-pill {
            display: inline-block;
            background: #FFFFFF;
            border: 1px solid #A7A7A7;
            border-radius: 72px;
            padding: 4px 16px;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: #222222;
            margin-bottom: 10px;
        }
        .footer-body {
            font-size: 13px;
            font-weight: 300;
            color: #555555;
            line-height: 2.15;
        }

        /* ── CODE BLOCK ─────────────────────────────── */
        div[data-testid="stCodeBlock"] {
            border-radius: 8px !important;
            border: 1px solid #A7A7A7 !important;
        }

        </style>
    """, unsafe_allow_html=True)


# ==========================================
# 4. Core Logic & Helper Functions
# ==========================================
def get_translator(src_lang, tgt_lang):
    return GoogleTranslator(source=src_lang, target=tgt_lang)

def clear_text():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.translation_stats = None

def swap_languages():
    src = st.session_state.source_lang
    tgt = st.session_state.target_lang
    if src != "Auto Detect":
        st.session_state.source_lang = tgt
        st.session_state.target_lang = src
    else:
        st.toast("Cannot swap when 'Auto Detect' is active.", icon="⚠️")

def escape_html(text):
    return html.escape(text)

def perform_translation(text, src_lang, tgt_lang):
    start_time = time.time()
    try:
        dt_src = LANGUAGES[src_lang]
        dt_tgt = LANGUAGES[tgt_lang]
        translator = get_translator(dt_src, dt_tgt)
        translated_text = translator.translate(text)
        end_time = time.time()

        st.session_state.translated_text = translated_text
        detected = src_lang if src_lang != "Auto Detect" else "Auto"

        st.session_state.translation_stats = {
            "chars": len(text),
            "words": len(text.split()),
            "detected": detected,
            "time": round(end_time - start_time, 2)
        }

        st.session_state.history.insert(0, {
            "source": text,
            "translated": translated_text,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang,
            "time": time.strftime("%I:%M %p")
        })
        st.session_state.history = st.session_state.history[:5]

    except Exception as e:
        st.session_state.translated_text = f"Error: {str(e)}"
        st.session_state.translation_stats = None


# ==========================================
# 5. Main UI Application
# ==========================================
def main():
    init_state()
    inject_custom_css()

    # ── HERO ────────────────────────────────────────
    st.markdown("""
        <div class="hero-wrap">
            <div class="hero-badge">Awwwards Design System &bull; Light Monochrome</div>
            <h1 class="hero-title">Translate Pro</h1>
            <p class="hero-subtitle">
                High-precision neural language translation engine — editorial typography,
                tonal surfaces, and instant multi-lingual intelligence.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── WORKSPACE ────────────────────────────────────
    with st.container():
        # Toolbar — language pickers + swap
        col_src, col_swap, col_tgt = st.columns([5, 1, 5], gap="small", vertical_alignment="center")

        with col_src:
            st.selectbox(
                "Source Language",
                options=list(LANGUAGES.keys()),
                key="source_lang",
                label_visibility="collapsed"
            )

        with col_swap:
            st.button("⇄", on_click=swap_languages, help="Swap Languages", use_container_width=True)

        with col_tgt:
            target_opts = [k for k in LANGUAGES if k != "Auto Detect"]
            st.selectbox(
                "Target Language",
                options=target_opts,
                key="target_lang",
                label_visibility="collapsed"
            )

        st.write("")

        # Text areas
        text_col1, text_col2 = st.columns(2, gap="large")

        with text_col1:
            st.text_area(
                "Source Text",
                key="input_text",
                placeholder="Type or paste your text here to begin translation...",
                label_visibility="collapsed"
            )
            btn_col1, btn_col2, _ = st.columns([2, 2, 4])
            with btn_col1:
                translate_clicked = st.button("✨ Translate", type="primary", use_container_width=True)
            with btn_col2:
                st.button("🗑️ Clear", on_click=clear_text, use_container_width=True)

        with text_col2:
            if translate_clicked:
                if st.session_state.input_text.strip():
                    with st.spinner("Translating..."):
                        perform_translation(
                            st.session_state.input_text,
                            st.session_state.source_lang,
                            st.session_state.target_lang
                        )
                else:
                    st.warning("⚠️ Please enter text to translate.")

            if st.session_state.translated_text == "":
                st.markdown(
                    '<div class="output-card">'
                    '<div class="output-placeholder">Translation will appear here...</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            elif st.session_state.translated_text.startswith("Error:"):
                st.error(st.session_state.translated_text)
            else:
                safe_out = escape_html(st.session_state.translated_text)
                st.markdown(f'<div class="output-card">{safe_out}</div>', unsafe_allow_html=True)
                with st.expander("📋 Click to Copy / View Raw Text"):
                    st.code(st.session_state.translated_text, language=None)

    # ── STATISTICS ───────────────────────────────────
    if st.session_state.translation_stats:
        stats = st.session_state.translation_stats
        st.write("")
        st.markdown('<div class="section-pill">Translation Dashboard</div>', unsafe_allow_html=True)

        metric_html = f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Characters</div>
                <div class="metric-value">{stats["chars"]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Words</div>
                <div class="metric-value">{stats["words"]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Detected</div>
                <div class="metric-value" style="font-size:17px;">{stats["detected"]}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Time (sec)</div>
                <div class="metric-value">{stats["time"]}s</div>
            </div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    st.divider()

    # ── HISTORY ──────────────────────────────────────
    st.markdown('<div class="section-pill">Translation History</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("Your recent translations will appear here.")
    else:
        for item in st.session_state.history:
            safe_src = escape_html(item["source"])
            safe_tgt = escape_html(item["translated"])

            card_html = f"""
            <div class="history-card">
                <div class="history-header">
                    <div class="history-pill">
                        {item["src_lang"]}
                        <span style="color:#A7A7A7;">&rarr;</span>
                        {item["tgt_lang"]}
                    </div>
                    <div class="history-ts">{item["time"]}</div>
                </div>
                <div class="history-body">
                    <div class="history-col src">{safe_src}</div>
                    <div class="history-col tgt">{safe_tgt}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    # ── FOOTER ───────────────────────────────────────
    st.markdown(f"""
    <div class="footer">
        <div class="footer-pill">Awwwards · Light Monochrome Edition</div>
        <div class="footer-body">
            <strong>Translate Pro</strong> v{APP_VERSION} &copy; 2026<br>
            Developed with precision by <strong>{DEVELOPER}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
