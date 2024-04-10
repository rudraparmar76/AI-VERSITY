import streamlit as st
import pycountry
import requests
import pandas as pd
import os
from datetime import datetime
from firebase_admin import auth
from api import apiKey

# Check if the user is signed in
if 'signedin' in st.session_state and st.session_state.signedin:
    st.set_page_config(page_title="News Wave", page_icon="📰", layout="wide")
    st.markdown("# News Wave 📰")
    st.sidebar.header(" News Wave 📰")

    # Define the path to save the usage data
    usage_data_path = r'UsageData\news_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Country', 'Category', 'Timestamp'])
    
    # Columns
    col1, col2 = st.columns([3, 1])

    with col1:
        # Text Input
        user = st.text_input("Entry Country Name:", "India")
    with col2:
        category = st.radio("Choose a news category", ('Technology', 'General', 'Health', 'Sports', 'Business'))
        btn = st.button("Enter")
    if btn:
        country = pycountry.countries.get(name=user)
        with st.spinner('Fetching news data...'):
            if country:
                country_code = country.alpha_2
                url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={apiKey}"
                r = requests.get(url)
                r = r.json()
                articles = r['articles']
                for article in articles:
                    st.header(article['title'])
                    st.write("Published at:", article['publishedAt'])
                    if article['author']:
                        st.write("Author:", article['author'])
                    st.write("Source:", article['source']['name'])
                    if article['urlToImage']:
                        st.image(article['urlToImage'])
                    content = article['content']
                    if article['content'] is not None:
                        content = article['content'].replace('...', '')
                        st.write(content)
                    else:
                        st.write("No content available.")
                    st.write("Read more at:", article['url'])
                # Save the visit data
                usage_data = usage_data.append({'Country': user, 'Category': category, 'Timestamp': datetime.now()}, ignore_index=True)
                usage_data.to_csv(usage_data_path, index=False)

            else:
                st.warning(f"Country '{user}' not recognized.")
else:
    st.warning("Please sign in to view the news.")
