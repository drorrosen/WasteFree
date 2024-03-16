
import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Assuming OpenAI's client is correctly set up with the API key stored in Streamlit's secrets



st.image('logo.png', width=400)
#st.image('all white.jpg', width=200)

#set_background('fintech_background.png')


st.title("Ad Generator")

with st.sidebar:
    st.title('Ads Generator')

    st.subheader('Client Information')
    #submit the information
    api_key = st.text_input("OpenAI API Key")
    ads_choice = st.selectbox("Select ad category:", ["WasteFree", "Salon"])

    if ads_choice == "Salon":
        st.subheader('Salon Information')
        salon_name = st.text_input("Salon Name", value='Name of Salon')
        #period = st.text_input("Period of Collection", value="Period in years")
        benefits = st.text_input("Environmental Benefits")


    st.session_state['api_key'] = api_key

if st.button('Generate Ad'):

    client = OpenAI(api_key=st.session_state["api_key"])
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"


    st.session_state['ads_choice'] = ads_choice
    if ads_choice == "WasteFree":
        # Fetch website information only once per session to avoid unnecessary requests
        if 'website_information' not in st.session_state:
            response = requests.get('https://wastefreesystems.com.au/')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                st.session_state['website_information'] = text
            else:
                st.error(f"Failed to fetch webpage: HTTP {response.status_code}")
                st.stop()

        prompt = f"Generate 5 creative ads for WasteFree. Audience: both individuals and salons.\nWebsite info:\n{st.session_state['website_information']}. Write it in the style of Mark Cuban, but don't mention him"

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=2048
        )



        response = st.write_stream(stream)
    else:
        salon_info = f"Salon name: {salon_name}, Achievements: {benefits}"
        prompt = f"Generate 5 funny ads for a salon. Focus on the information in the Achivements. Audience: both individuals and salons. Salon info: {salon_info}. Write it in the style of Mark Cuban, but don't mention him."
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=2048
        )

        response = st.write_stream(stream)


