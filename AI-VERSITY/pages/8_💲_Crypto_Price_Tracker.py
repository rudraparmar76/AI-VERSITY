import streamlit as st
import pandas as pd
import plotly.express as px
import requests


if 'signedin' in st.session_state and st.session_state.signedin:
    st.set_page_config(page_title="Crypto Price Tracker", page_icon="💲", layout="wide")
    st.markdown("# CryptoCurrency Price Tracker 📊")
    st.sidebar.header(" CryptoCurrency Price Tracker 📊 ")
    st.markdown("### Track Crypto Prices in Real-Time")


    @st.cache_data
    def get_crypto_data():
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'inr', # Change to INR
            'per_page': 100,
            'page': 1,
            'sparkline': False
        }
        response = requests.get(url, params=params)
        data = response.json()
        return pd.DataFrame(data)

    crypto_data = get_crypto_data()

    # Display top 10 cryptocurrencies by market capitalization
    top_10_crypto = crypto_data.sort_values(by='market_cap', ascending=False).head(10)
    fig = px.bar(top_10_crypto, x='name', y='current_price', title='Top 10 Cryptocurrencies by Market Capitalization')
    st.plotly_chart(fig)
    st.divider()
    st.markdown("### Cryptocurrency Information")
    # Display information for each cryptocurrency in rows
    num_cols = 3 # Number of columns for layout
    num_cryptos = len(crypto_data)
    num_rows = (num_cryptos + num_cols - 1) // num_cols # Calculate number of rows needed

    # Create columns for layout
    cols = st.columns(num_cols)

    # Define custom CSS for uniform tile size
    custom_css = """
    <style>
        .crypto-tile {
            width: 300px; /* Adjust width as needed */
            height: 100px; /* Adjust height as needed */
            padding: = 5px;
            box-sizing: border-box;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    for i in range(num_rows):
        row_data = crypto_data.iloc[i * num_cols:(i + 1) * num_cols]

        for idx, crypto in row_data.iterrows():
            # Place content in the current column
            with cols[idx % num_cols]:
                with st.container():
                    st.markdown('<div class="crypto-tile">', unsafe_allow_html=True)
                    st.subheader(f"{crypto['name']} ({crypto['symbol'].upper()})")
                    st.image(crypto['image'], width=100) # Display cryptocurrency image
                    st.write(f"**Price**: ₹{crypto['current_price']:.2f}") # Display cryptocurrency price in INR
                    st.write(f"**Market Cap**: ₹{crypto['market_cap']:,.0f}") # Display market cap in INR
                    st.write(f"**Volume (24h)**: ₹{crypto['total_volume']:,.0f}") # Display 24-hour trading volume in INR
                    st.markdown("<hr>", unsafe_allow_html=True) # Add a separator
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Please sign in to turn data into interactive dashboard.")