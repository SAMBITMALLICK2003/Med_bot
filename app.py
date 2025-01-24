# Import required libraries
import streamlit as st
import requests
import json
import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "bd8c93dd-e6e1-4b9f-9a53-18339316c2fb"
FLOW_ID = "14a47627-6974-4a99-a761-fb31bef448fc"
APPLICATION_TOKEN = os.getenv("DATASTAX_API")  # Replace with your actual token
ENDPOINT = "qcd"  # The endpoint name of the flow

TWEAKS = {
    "ChatInput-Y2xdS": {},
    "ChatOutput-spvvP": {},
    "Agent-0NOC9": {},
    "AstraDB-yVi42": {},
    "Prompt-DaInP": {},
    "ParseData-uMT8y": {},
    "File-tUSl2": {},
    "SplitText-A0JuJ": {},
    "File-lHKKK": {},
    "AstraDB-rMJ9L": {},
    "Agent-aDvj9": {},
    "WikipediaAPI-ZMVGp": {},
}

def parse_response(response: dict) -> str:
    try:
        # Navigate the JSON structure to find the "text" field
        return response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError) as e:
        return f"⚠️ Unable to extract the response. Error: {e}"
# Function to run a flow
def run_flow(
    message: str,
    endpoint: str,
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": f"Bearer {application_token}", "Content-Type": "application/json"} if application_token else None

    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit App
def main():
    # App Title and Introduction
    st.title("🔬🤖 Medical AI Agent")
    st.markdown(
        """
        Welcome to the **Medical AI Agent**! 🌟  
        🩺 Ask your questions about medical data or AI analysis, and let our intelligent agent assist you.  
        """
    )

    # Input Section
    st.markdown("### 💬 **Ask Your Query:**")
    user_message = st.text_area(
        "Enter your query below:",
        placeholder="E.g., What are the symptoms of glaucoma?",
        help="Type your medical or AI-related question here.",
    )
    submit_button = st.button("🚀 Submit")

    # Response Section
    if submit_button:
        if not user_message.strip():
            st.error("❌ Please enter a valid query to proceed.")
        else:
            st.info("⏳ Processing your query, please wait...")
            try:
                # Call the run_flow function
                response = run_flow(
                    message=user_message,
                    endpoint=ENDPOINT,
                    tweaks=TWEAKS,
                    application_token=APPLICATION_TOKEN,
                )
                # Extract and display the text response
                extracted_text = parse_response(response)
                st.success("✅ Response Received!")
                st.markdown("### 📜 **Response:**")
                st.write(extracted_text)
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

    # Footer
    st.markdown(
        """
        ---
        Developed with ❤️ by [Your Team Name].  
        For support, contact us at 📧 support@yourcompany.com.  
        """
    )

# Entry point
if __name__ == "__main__":
    main()