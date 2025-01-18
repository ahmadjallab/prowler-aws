"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
def LLM_compliance_report(text):
    # Load environment variables from .env file
    load_dotenv()

    # Configure Gemini with API key from .env
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Define the model and configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    prompt = """ You are a security auditor reviewing a text-based compliance report for the 'Gemini' environment. 
            The report is divided into SEC01, SEC02, and SEC03 sections, each containing several checks. 
            Please do the following:
            1. **Summarize the compliance posture** for each section (SEC01, SEC02, SEC03).
            2. **Identify the most critical failures** or risks (especially those marked 'FAILED' or 'CRITICAL').
            3. **Provide recommended remediation steps** and best practices relevant to the issues identified.
            4. **Present an overall compliance status** for Gemini, highlighting any urgent or high-severity issues.
            Use clear, concise language. Tailor the explanation so it's understandable to both technical teams and management.
            **Compliance Report Text**: """
    # Create the generative model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
        prompt
        ),
    )

    # Start a chat session
    chat_session = model.start_chat()

    # Provide the compliance report text


    # Send the compliance report text
    response = chat_session.send_message(text)

    # Print the response
    #print(response.text)

    return response.text
