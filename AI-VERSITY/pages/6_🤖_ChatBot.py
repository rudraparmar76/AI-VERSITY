import streamlit as st
import openai
import os
from datetime import datetime
import pandas as pd

if 'signedin' in st.session_state and st.session_state.signedin:
    st.set_page_config(page_title="Bot Buddy", page_icon="🤖",layout="wide")
    st.markdown("# Bot Buddy 🤖")
    st.sidebar.header(" Bot Buddy 🤖")

    usage_data_path = r'UsageData/chatbot_usage_data.csv'
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Prompt','Response','Timestamp'])

    st.markdown("### Chat with Bot Buddy")

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"]="gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt=st.chat_input("What is up?")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user","content":prompt})

        # Check if the user asked about the assistant's identity
        if "who are you" in prompt.lower() or "who created you" in prompt.lower():
            full_response = "I'm a chatbot created by AI-Verse."
        else:
            message_placeholder=st.empty()
            full_response=""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role":m["role"],"content":m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response +=response.choices[0].delta.get("content","")
                message_placeholder.markdown(full_response+" ")
            message_placeholder.markdown(full_response)

        with st.chat_message("assistant"):
            st.markdown(full_response)

        st.session_state.messages.append({"role":"assistant","content":full_response})
        usage_data = usage_data._append({'Prompt': prompt,'Response':full_response,'Timestamp': datetime.now()}, ignore_index=True)
        usage_data.to_csv(usage_data_path, index=False)
else:
    st.warning("Please sign in to chat with Bot Buddy.")
