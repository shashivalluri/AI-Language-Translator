import streamlit as st
from googletrans import Translator
import time
import html

# ==========================================
# 1. Configuration & Setup
# ==========================================
st.set_page_config(
    page_title="Translate Pro | Modern Language Translation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
APP_VERSION = "2.0.0"
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
    "Chinese": "zh-cn",
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
# 3. Custom CSS Injection
# ==========================================
def inject_custom_css():
    """Injects premium custom CSS for a modern SaaS look."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Main Container */
        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        
        /* Hero Section */
        .hero-title {
            text-align: center;
            font-weight: 800;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }
        .hero-subtitle {
            text-align: center;
            color: #6B7280;
            font-size: 1.15rem;
            margin-bottom: 3rem;
            font-weight: 400;
        }
        
        /* Card Styles */
        .output-card, .history-card {
            background-color: var(--secondary-background-color);
            border-radius: 16px;
            padding: 24px;
            font-size: 1.05rem;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.1);
            color: var(--text-color);
        }
        .output-card {
            min-height: 250px;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .history-card {
            margin-bottom: 20px;
            transition: all 0.3s ease;
            background: var(--background-color);
        }
        .history-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.1);
            border-color: rgba(79, 70, 229, 0.3);
        }
        
        /* Text Area overriding */
        .stTextArea textarea {
            border-radius: 16px !important;
            padding: 20px !important;
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
            transition: all 0.3s ease !important;
            background-color: var(--background-color) !important;
            min-height: 250px !important;
        }
        .stTextArea textarea:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
        }
        
        /* History Elements */
        .history-meta {
            font-size: 0.85rem;
            color: #6B7280;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(128, 128, 128, 0.1);
            display: flex;
            justify-content: space-between;
        }
        .history-text {
            max-height: 120px;
            overflow-y: auto;
            white-space: pre-wrap;
            padding-right: 10px;
        }
        
        @media (max-width: 768px) {
            .history-flex {
                flex-direction: column;
                gap: 12px !important;
            }
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #D1D5DB;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9CA3AF;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 6rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(128, 128, 128, 0.1);
            color: #9CA3AF;
            font-size: 0.9rem;
            line-height: 1.8;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. Core Logic & Helper Functions
# ==========================================
@st.cache_resource
def get_translator():
    """Cache the translator instance for optimal performance."""
    return Translator()

def clear_text():
    """Callback to clear the workspace."""
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.translation_stats = None

def swap_languages():
    """Callback to swap source and target languages."""
    src = st.session_state.source_lang
    tgt = st.session_state.target_lang
    if src != "Auto Detect":
        st.session_state.source_lang = tgt
        st.session_state.target_lang = src
    else:
        st.toast("Cannot swap when 'Auto Detect' is active.", icon="⚠️")

def escape_html(text):
    """Escapes HTML characters to prevent XSS in custom divs."""
    return html.escape(text)

def perform_translation(text, src_lang, tgt_lang):
    """Handles translation logic and updates session state."""
    translator = get_translator()
    start_time = time.time()
    try:
        # API Call
        result = translator.translate(text, src=src_lang, dest=tgt_lang)
        end_time = time.time()
        
        st.session_state.translated_text = result.text
        
        # Determine detected language name
        detected_lang_code = result.src
        detected_lang_name = "Unknown"
        for name, code in LANGUAGES.items():
            if code.lower() == detected_lang_code.lower():
                detected_lang_name = name
                break
                
        # Generate statistics
        st.session_state.translation_stats = {
            "chars": len(text),
            "words": len(text.split()),
            "detected": detected_lang_name,
            "time": round(end_time - start_time, 2)
        }
        
        # Save to history
        new_entry = {
            "source": text,
            "translated": result.text,
            "src_lang": st.session_state.source_lang if st.session_state.source_lang != "Auto Detect" else f"Auto ({detected_lang_name})",
            "tgt_lang": st.session_state.target_lang,
            "time": time.strftime("%I:%M %p")
        }
        st.session_state.history.insert(0, new_entry)
        st.session_state.history = st.session_state.history[:10]  # Keep last 10
        
    except Exception as e:
        st.session_state.translated_text = f"Error: {str(e)}"
        st.session_state.translation_stats = None

# ==========================================
# 5. Main UI Application
# ==========================================
def main():
    init_state()
    inject_custom_css()

    # --- Hero Section ---
    st.markdown('<div class="hero-title">Translate Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Fast, accurate, and seamless language translation for professionals.</div>', unsafe_allow_html=True)

    st.write("") # Spacing

    # --- Main Workspace ---
    with st.container():
        # Toolbar Row
        col_src, col_swap, col_tgt = st.columns([5, 1, 5], gap="small", vertical_alignment="center")
        
        with col_src:
            st.selectbox("Source Language", options=list(LANGUAGES.keys()), key="source_lang", label_visibility="collapsed")
            
        with col_swap:
            st.button("⇄", on_click=swap_languages, help="Swap Languages", use_container_width=True)
            
        with col_tgt:
            target_opts = list(LANGUAGES.keys())
            if "Auto Detect" in target_opts:
                target_opts.remove("Auto Detect")
            st.selectbox("Target Language", options=target_opts, key="target_lang", label_visibility="collapsed")

        st.write("") # Spacing

        # Text Area Row
        text_col1, text_col2 = st.columns(2, gap="large")
        
        with text_col1:
            # Input Text Area
            st.text_area(
                "Source Text", 
                key="input_text",
                placeholder="Type or paste your text here to begin translation...",
                label_visibility="collapsed"
            )
            
            # Action Buttons Below Input
            btn_col1, btn_col2, _ = st.columns([2, 2, 4])
            with btn_col1:
                translate_clicked = st.button("✨ Translate", type="primary", use_container_width=True)
            with btn_col2:
                st.button("🗑️ Clear", on_click=clear_text, use_container_width=True)

        with text_col2:
            # Execute Translation if button clicked
            if translate_clicked:
                if st.session_state.input_text.strip():
                    with st.spinner("Translating via AI..."):
                        perform_translation(
                            st.session_state.input_text, 
                            LANGUAGES[st.session_state.source_lang], 
                            LANGUAGES[st.session_state.target_lang]
                        )
                else:
                    st.warning("⚠️ Please enter text to translate.")

            # Render Output Area
            if st.session_state.translated_text == "":
                st.markdown('<div class="output-card" style="color: #9CA3AF; display: flex; align-items: center; justify-content: center; height: 100%;">Translation will appear here...</div>', unsafe_allow_html=True)
            elif st.session_state.translated_text.startswith("Error:"):
                st.error(st.session_state.translated_text)
            else:
                safe_output = escape_html(st.session_state.translated_text)
                st.markdown(f'<div class="output-card">{safe_output}</div>', unsafe_allow_html=True)
                
                # Copy utility via expander natively in Streamlit
                with st.expander("📋 Click to Copy / View Raw Text"):
                    st.code(st.session_state.translated_text, language=None)

    # --- Statistics Section ---
    st.write("")
    if st.session_state.translation_stats:
        stats = st.session_state.translation_stats
        st.markdown("### 📊 Translation Statistics")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Characters", stats["chars"])
        s2.metric("Words", stats["words"])
        s3.metric("Detected Language", stats["detected"])
        s4.metric("Translation Time", f"{stats['time']}s")

    st.divider()

    # --- Translation History ---
    st.markdown("### 🕒 Translation History")
    if not st.session_state.history:
        st.info("Your recent translations will appear here.")
    else:
        for item in st.session_state.history:
            safe_source = escape_html(item['source'])
            safe_translated = escape_html(item['translated'])
            
            card_html = f"""
            <div class="history-card">
                <div class="history-meta">
                    <span><strong>{item['src_lang']}</strong> ➔ <strong>{item['tgt_lang']}</strong></span>
                    <span>{item['time']}</span>
                </div>
                <div class="history-flex" style="display: flex; gap: 24px;">
                    <div style="flex: 1; color: #6B7280;" class="history-text">{safe_source}</div>
                    <div style="flex: 1; font-weight: 500;" class="history-text">{safe_translated}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown(f"""
    <div class="footer">
        <p><strong>Translate Pro</strong> v{APP_VERSION} &copy; 2026</p>
        <p>Developed with ❤️ by <strong>{DEVELOPER}</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()