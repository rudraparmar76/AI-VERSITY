import streamlit as st
import pandas as pd
import os
from datetime import datetime


if 'signedin' in st.session_state and st.session_state.signedin:

    st.markdown('# Usage History 🕵️')
    st.divider()

    
    # Define the path to load the news_usage data
    news_usage_data_path = r'UsageData\news_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(news_usage_data_path):
        n_usage_data = pd.read_csv(news_usage_data_path)
    else:
        n_usage_data = pd.DataFrame(columns=['Country', 'Category', 'Timestamp'])

    st.markdown('## Usage Data for News Wave 📰:')
    st.write(n_usage_data)

    # Error handling for setting index and creating the chart
    if not n_usage_data.empty:
        try:
            # Create a graph of all the visited pages
            visit_counts = n_usage_data.groupby(['Country', 'Category'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['Country', 'Category'], inplace=True)  # Ensure to set the index correctly
            visit_counts.reset_index(inplace=True)  # Reset the index before passing it to bar_chart
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")

    # Define the path to load the weather_usage data
    weather_usage_data_path = r'UsageData\weather_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(weather_usage_data_path):
        w_usage_data = pd.read_csv(weather_usage_data_path)
    else:
        w_usage_data = pd.DataFrame(columns=['City', 'Temperature', 'Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Weather Vista ☁️:')

    st.write(w_usage_data)

    # Error handling for setting index and creating the chart
    if not w_usage_data.empty:
        try:
            # Create a graph of all the visited pages
            visit_counts = w_usage_data.groupby(['City', 'Temperature'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['City', 'Temperature'], inplace=True)  # Ensure to set the index correctly
            visit_counts.reset_index(inplace=True)  # Reset the index before passing it to bar_chart
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")

    # Define the path to load the translation_usage data
    translator_usage_data_path = r'UsageData/translator_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(translator_usage_data_path):
        t_usage_data = pd.read_csv(translator_usage_data_path)
    else:
        t_usage_data = pd.DataFrame(columns=['Source Lang','Destination Lang', 'Text','Translation','Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Linguo Verse 🌐:')

    st.write(t_usage_data)

    # Error handling for setting index and creating the chart
    # if not t_usage_data.empty:
    #     try:
    #         # Create a graph of all the visited pages
    #         visit_counts = w_usage_data.groupby(['Source Lang','Destination Lang', 'Text','Translation'])['Timestamp'].count().reset_index()
    #         visit_counts.set_index(['Source Lang','Destination Lang', 'Text','Translation'], inplace=True)  # Ensure to set the index correctly
    #         visit_counts.reset_index(inplace=True)  # Reset the index before passing it to bar_chart
    #         st.bar_chart(visit_counts)
    #     except KeyError as e:
    #         st.error(f"An error occurred: {e}")
    # else:
    #     st.warning("Usage data is empty. No chart to display.")

    # Define the path to load the imagegen_usage data
    imagegen_usage_data_path = r'UsageData/imagegen_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(imagegen_usage_data_path):
        i_usage_data = pd.read_csv(imagegen_usage_data_path)
    else:
        i_usage_data = pd.DataFrame(columns=['Prompt','image','Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Vision Vertex 🖼️:')

    st.write(i_usage_data)

    # Error handling for setting index and creating the chart
    if not i_usage_data.empty:
        try:
            visit_counts = i_usage_data.groupby(['Prompt','image'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['Prompt','image'], inplace=True)
            visit_counts.reset_index(inplace=True)
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")
        
    # Define the path to load the pptegen_usage data
    pptgen_usage_data_path = r'UsageData/pptgen_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(pptgen_usage_data_path):
        p_usage_data = pd.read_csv(pptgen_usage_data_path)
    else:
        p_usage_data = pd.DataFrame(columns=['Prompt','slides','Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Slide Craft 🎓:')

    st.write(p_usage_data)

    # Error handling for setting index and creating the chart
    if not p_usage_data.empty:
        try:
            visit_counts = p_usage_data.groupby(['Prompt','slides'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['Prompt','slides'], inplace=True)
            visit_counts.reset_index(inplace=True)
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")

    # Define the path to load the aibot_usage data
    bot_usage_data_path = r'UsageData/chatbot_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(bot_usage_data_path):
        b_usage_data = pd.read_csv(bot_usage_data_path)
    else:
        b_usage_data = pd.DataFrame(columns=['Prompt','Response','Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Bot Buddy 🤖:')

    st.write(b_usage_data)

    # Error handling for setting index and creating the chart
    if not b_usage_data.empty:
        try:
            # Create a graph of all the visited pages
            visit_counts = b_usage_data.groupby(['Prompt','Response'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['Prompt','Response'], inplace=True)  # Ensure to set the index correctly
            visit_counts.reset_index(inplace=True)  # Reset the index before passing it to bar_chart
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")
    
    # Define the path to load the sales_usage data
    dashboard_usage_data_path = r'UsageData/dashboard_usage_data.csv'

    # Check if the usage data file exists and load it, otherwise create an empty DataFrame
    if os.path.exists(dashboard_usage_data_path):
        d_usage_data = pd.read_csv(dashboard_usage_data_path)
    else:
        d_usage_data = pd.DataFrame(columns=['UploadedFile','Timestamp'])

    st.divider()

    st.markdown('## Usage Data for Sales Dashboard 📊:')

    st.write(d_usage_data)

    # Error handling for setting index and creating the chart
    if not d_usage_data.empty:
        try:
            # Create a graph of all the visited pages
            visit_counts = d_usage_data.groupby(['UploadedFile'])['Timestamp'].count().reset_index()
            visit_counts.set_index(['UploadedFile'], inplace=True)  # Ensure to set the index correctly
            visit_counts.reset_index(inplace=True)  # Reset the index before passing it to bar_chart
            st.bar_chart(visit_counts)
        except KeyError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Usage data is empty. No chart to display.")
    
    
else:
    st.warning("Please sign in to view the usage history.")