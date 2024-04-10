import streamlit as st
import firebase_admin
from firebase_admin import credentials
import json
import requests

# Set the page configuration
st.set_page_config(page_title="All In One GPT", page_icon="🧊")

# Main application function
def app():
    # Set the title of the web page
    st.title('Welcome to :blue[All In One GPT] 🧊')
    
    st.markdown(
        """
        <span style='color:lightblue'>All In One GPT</span> is an innovative web application built on the Streamlit framework, offering a comprehensive and user-friendly interface for interacting with various state-of-the-art GPT (Generative Pre-trained Transformer) models. This project aims to streamline the user experience in exploring and utilizing powerful natural language processing capabilities.
        \n
        """,
        unsafe_allow_html=True
    )
    if 'signedin' not in st.session_state or not st.session_state.signedin:
        st.markdown(
            """
            **Sign-in** **to start using all the features**
            """,unsafe_allow_html=True
        )
    if 'signedin' in st.session_state and st.session_state.signedin:
        st.markdown(
            """
            **Get started by selecting a feature from sidebar on the left 👈**
            """,unsafe_allow_html=True
        )
        
    # Initialize Firebase app
    if not firebase_admin._apps:
        cred = credentials.Certificate("ai-verse-b6ad2-05b515a48912.json")
        firebase_admin.initialize_app(cred)
    
        
    # Function to sign up with email and password
    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyBek5kLX8xgY2mqKyDmuidZEydpGwXoIsk"}, data=payload)
            data = r.json()
            if 'error' in data:
                st.warning(data['error']['message'])
            else:
                return data['email']
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    # Function to sign in with email and password
    def sign_in_with_email_and_password(email, password, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyBek5kLX8xgY2mqKyDmuidZEydpGwXoIsk"}, data=payload)
            data = r.json()
            if 'error' in data:
                st.warning(data['error']['message'])
            else:
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    # Initialize session state variables
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # Function to perform sign in
# Function to perform sign in
    def f():
        with st.spinner("Validating Credentials..."):
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            if userinfo:
                st.session_state.username = userinfo['username']
                st.session_state.useremail = userinfo['email']
                # Set the session state variable to indicate the user is signed in
                st.session_state.signedin = True
                st.session_state.signedout = True
            else:
                st.warning('Login Failed')

    # Function to perform sign out
    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.session_state.email_input = ''
        st.session_state.password_input = ''

    # Render login/signup form if not signed in
    if not st.session_state.signedout:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            with st.spinner("Validating Credintials..."):
                if st.button('Create my account'):
                    user = sign_up_with_email_and_password(email=email, password=password, username=username)
                    if user:
                        st.success('Account created successfully! Please Login using your email and password')
                        st.balloons()
        else:
            if st.button('Login',on_click=f):
                pass

    # Render signout button and user info if signed in
    if 'signedin' in st.session_state and st.session_state.signedin:
        st.sidebar.success(f'Welcome, {st.session_state.username}!') # Show username in sidebar
        st.sidebar.write("") # Add spacing
        st.sidebar.success("Get started by selecting a feature above👆 ")
        st.sidebar.write("")
        st.sidebar.button('Sign out', on_click=t) # Sign out button
    else:
        st.sidebar.empty()

# Run the application
if __name__ == "__main__":
    app()
