import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 AI Language Translator")
st.write("Translate text from one language to another")

languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Arabic": "ar"
}

text = st.text_area(
    "Enter Text",
    height=150,
    placeholder="Type or paste text here..."
)

st.write(f"📊 Character Count: {len(text)}")

source_lang = st.selectbox(
    "Source Language",
    list(languages.keys()),
    index=0
)

target_lang = st.selectbox(
    "Target Language",
    list(languages.keys())[1:],
    index=0
)

if st.button("Translate"):

    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:

            translated_text = GoogleTranslator(
                source="auto" if languages[source_lang] == "auto" else languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.subheader("Translated Text")
            st.success(translated_text)

        except Exception as e:
            st.error(f"Translation Error: {e}")

st.markdown("---")
st.caption("Developed by Shashi Valluri")