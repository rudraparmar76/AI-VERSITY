import streamlit as st 
from googletrans import Translator
from languages import *
import os
import pandas as pd
from datetime import datetime

if 'signedin' in st.session_state and st.session_state.signedin:
    usage_data_path = r'UsageData/translator_usage_data.csv'
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Source Lang','Destination Lang', 'Text','Translation','Timestamp'])


    st.set_page_config(page_title="Linguo Verse", page_icon="🌐",layout="wide")
    st.markdown("# Linguo Verse 🌐")
    st.sidebar.header(" Linguo Verse 🌐")
    source_language = st.selectbox("Select source language:", languages)
    source_text = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language:", languages)
    translate = st.button('Translate')
    if translate:
        with st.spinner('Translating Text...'):
            translator = Translator()
            out = translator.translate(source_text, src=source_language, dest=target_language)
            st.markdown("## Translated Text :")
            st.write(out.text)
            usage_data = usage_data._append({'Source Lang':source_language, 'Destination Lang': target_language, 'Text':source_text,'Translation':out.text,'Timestamp': datetime.now()}, ignore_index=True)
            usage_data.to_csv(usage_data_path, index=False)

else:
    st.warning("Please sign in to translate the text.")
