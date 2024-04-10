import streamlit as st 
import openai
from api import Openai_key
import os
import pandas as pd
from datetime import datetime
openai.api_key = Openai_key

if 'signedin' in st.session_state and st.session_state.signedin:

    st.set_page_config(page_title="Vision Vortex", page_icon="🖼️", layout="wide")
    st.markdown("# Vision Vortex 🖼️")
    st.sidebar.header(" Vision Vortex 🖼️")

    usage_data_path = r'UsageData/imagegen_usage_data.csv'
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Prompt','image','Timestamp'])

    def generate_images_using_openai(text):
        response = openai.Image.create(prompt=text, n=1, size="512x512")
        image_url = response['data'][0]['url']
        return image_url

    input_prompt = st.text_area("Enter your text prompt", placeholder="Enter the image description you want to generate")
    generate_image = st.button('Generate')
    if generate_image:
        with st.spinner('Generating Image...'):
            image_url = generate_images_using_openai(input_prompt)
            st.image(image_url, caption=f"{input_prompt}-Generated Image")
            usage_data = usage_data._append({'Prompt': input_prompt,'image':image_url,'Timestamp': datetime.now()}, ignore_index=True)
            usage_data.to_csv(usage_data_path, index=False)
            # Store the image_url in session state
            st.session_state['image_url'] = image_url

    if st.button("Regenerate"):
        with st.spinner('Regenerating Image...'):
            image_url = generate_images_using_openai(input_prompt)
            st.image(image_url, caption=f"{input_prompt}-Generated Image")
            # Update the image_url in session state
            st.session_state['image_url'] = image_url

    if st.button("Download"):
        # Check if image_url is in session state
        if 'image_url' in st.session_state:
            download_link = f'<a href="{st.session_state["image_url"]}" download="generated_image.png">Download Image</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.warning("Please generate an image first before downloading.")
else:
    st.warning("Please sign in to generate images.")
