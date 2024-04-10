import streamlit as st
import requests
import openai
from datetime import datetime
from api import weatherKey
from api import openaiKey
import os
import pandas as pd

if 'signedin' in st.session_state and st.session_state.signedin:

    st.set_page_config(page_title="Weather Vista", page_icon="☁️",layout="wide")
    #Logic to save usagedata
    usage_data_path = r'UsageData\weather_usage_data.csv'
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['City', 'Temperature','Timestamp'])
        

    #Function to get weather
    def get_weather_data(city,weather_api_key):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
        response = requests.get(complete_url)
        return response.json()

    #Function to generate weather model using open ai
    def generate_weather_description(data,open_ai_key):
        openai.api_key = open_ai_key
        try:
            #Convert temp from kelvin to celsius
            temp = data['main']['temp'] - 273.15
            description = data['weather'][0]['description']
            prompt = f"The weather in {city} is {description} with a temperature of {temp:.1f}ºC. Explain this in a simple way for general audience." 
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=60
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return str(e)
    def get_weekly_forecast(weather_api_key,lat,lon):
        base_url = "https://api.openweathermap.org/data/2.5/"
        complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
        response = requests.get(complete_url)
        return response.json()
    def display_weekly_forecast(data):
        try:
            st.divider()
            st.markdown("## Weekly Forecast")
            displayed_dayes = set() #to keep track of dates
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.metric("","Day")
            with c2:
                st.metric("","Desc")
            with c3:
                st.metric("","Min-temp")
            with c4:
                st.metric("","Max-temp")
            for day in data['list']:
                date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
                #check if the date is already been displayed
                if date not in displayed_dayes:
                    displayed_dayes.add(date)
                    
                    min_temp = day['main']['temp_min'] - 273.15
                    max_temp = day['main']['temp_max']-273.15
                    description = day['weather'][0]['description']
                    
                    with c1:
                        st.write(f"{date}")
                    with c2:
                        st.write(f"{description.capitalize()}")
                    with c3:
                        st.write(f"{min_temp:.1f}ºC")
                    with c4:
                        st.write(f"{max_temp:.1f}ºC")
        except Exception as e:
            st.error("Error in displaying weekly forecast: "+str(e))
            
    st.markdown("# Weather Vista ☁️")

    st.sidebar.header(" Weather Vista ☁️")

    city = st.text_input("Enter City Name:","Mumbai")

    weather_api_key = weatherKey
    open_ai_key = openaiKey

    submit = st.button("Get Weather")

    if submit:
        st.markdown("## Weather Updates for "+city+" is:")
        with st.spinner('Fetching weather data...'):
            weather_data = get_weather_data(city,weather_api_key)
            print(weather_data)
            
            
            #Checking if the city is valid
            if weather_data.get("cod") != "404":
                col1,col2 = st.columns(2)
                with col1:
                    st.metric("Temperature 🌡️",f"{weather_data['main']['temp'] - 273.15:.2f}°C")
                    st.metric("Humidity 💧",f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure 😤",f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed 💨",f"{weather_data['wind']['speed']} m/s")
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                #Generating weather description
                # weather_description = generate_weather_description(weather_data,open_ai_key)
                # st.write(weather_description)

                #call function
                forecast_data = get_weekly_forecast(weather_api_key,lat,lon)
                print(forecast_data)
                if forecast_data.get("cod")!="404":
                    display_weekly_forecast(forecast_data)
                else:
                    st.error("Error fetching weekly forecast data")
                    
                #Save the visit data
                usage_data = usage_data._append({'City': city, 'Temperature':weather_data['main']['temp'] - 273.15,'Timestamp': datetime.now()}, ignore_index=True)
                usage_data.to_csv(usage_data_path, index=False)

                
            else:
                #Display error if not found
                st.error("City not found or an error occured")
else:
    st.warning("Please sign in to get the weather info.")
