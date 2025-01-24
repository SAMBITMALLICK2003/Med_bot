import streamlit as st
from streamlit_chat import message
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Datastax API configurations
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "bd8c93dd-e6e1-4b9f-9a53-18339316c2fb"
ENDPOINT = "qcd"  # Endpoint name of the flow
APPLICATION_TOKEN = os.getenv("DATASTAX_API")

# Function to parse the response JSON
def parse_response(response: dict) -> str:
    try:
        # Navigate the JSON structure to find the "text" field
        return response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError) as e:
        return f"⚠️ Unable to extract the response. Error: {e}"

# Function to call the DataStax API
def run_flow(message: str, endpoint: str, application_token: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {"input_value": message, "output_type": "chat", "input_type": "chat"}
    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit UI setup
st.set_page_config(page_title="Custom Assistant", page_icon="🤖")
st.subheader("Custom Assistant 🤖")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Your Message:", placeholder="Type something...", key="user_input")

if user_input:
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call the DataStax API
    with st.spinner("Generating response..."):
        raw_response = run_flow(
            message=user_input,
            endpoint=ENDPOINT,
            application_token=APPLICATION_TOKEN
        )
        bot_response = parse_response(raw_response)

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True)
    else:
        message(msg["content"], is_user=False)
