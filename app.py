import streamlit as st
import os
import base64
import openai
import traceback
import logging
from openai import OpenAI
#from vl_connect import env
import json
import httpx
import base64
import streamlit as st
import ecb_certifi
#httpx_client = httpx.Client(verify=ecb_certifi.where())


#httpx_client = httpx.Client(verify=False)

import httpx
import ssl


ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1  # Disable TLSv1
ssl_context.options |= ssl.OP_NO_TLSv1_1  # Disable TLSv1.1
ssl_context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK')

# Initialize the HTTPX client with the custom SSL context
httpx_client = httpx.Client(verify=ssl_context)


def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()



def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
    }}
    h1 {{
        color: #FFFFFF; /* Change to your preferred color */
        font-size: 48px; /* Adjust size as needed */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7); /* Shadow effect */
        font-weight: bold; /* Bold font */
        background-color: rgba(0,0,0,0.5); /* Semi-transparent background */
        padding: 10px;
        border-radius: 10px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background("image8.png")


# Initialize OpenAI client
client = OpenAI(api_key="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", http_client = httpx_client)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


import requests
import traceback

import httpx
import json
import traceback

def query_openai(image_url):
    """Queries OpenAI with an image URL and returns the response and any error messages."""
    try:
        # Ensure your OpenAI client is correctly initialized elsewhere in your script with httpx_client passed as http_client
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "is this an euro bill? respond in json with key euro_bill which should have value yes or no, and key explanation which provides your explanation. The explanation should be at the level of a 12 year old and a bit funny",
                        },
                        {
                            "type": "image_url",
                            "image_url": image_url
                        },
                    ],
                }
            ],
            model="gpt-4-turbo-2024-04-09",
            response_format={"type": "json_object"},
        )
        return response, None
    except httpx.HTTPStatusError as e:
        # HTTP status errors are thrown when the response status code indicates an error
        error_details = f"HTTP status error: {e.response.status_code}, message: {str(e)}"
        logging.error("HTTP status error", exc_info=True)
        return None, error_details
    except httpx.RequestError as e:
        # Request errors are thrown when a request fails to send
        error_details = f"Request error: {str(e)}"
        logging.error("Request connection error", exc_info=True)
        return None, error_details
    except Exception as e:
        # Handle general exceptions that could occur, for instance, in parsing responses or other unexpected conditions
        traceback_msg = traceback.format_exc()
        error_details = f"An unexpected error occurred: {str(e)}\n{traceback_msg}"
        logging.error("General exception", exc_info=True)
        return None, error_details





# Streamlit layout
st.markdown(
    "<h1 style='color: #FFFFFF;'>Are you holding a Euro bill?</h1>",
    unsafe_allow_html=True,
)
# st.markdown(
#     "<h2 style='color: #FFFFFF; font-weight: bold;'>Are you holding a Euro bill?</h2>",
#     unsafe_allow_html=True,
# )


img_file_buffer = st.camera_input("Take a photo")


if img_file_buffer is not None:
    encoded_data = base64.b64encode(img_file_buffer.getvalue())
    encoded_string = encoded_data.decode("utf-8")
    image_url = f"data:image/jpeg;base64,{encoded_string}"
    response, error = query_openai(image_url)

    if error:
        st.error(f"Error: {error}")  # Display the error in the UI
    else:
        response_data = json.loads(response.choices[0].message.content)
        euro_bill = response_data.get("euro_bill", "no").lower() == "yes"
        explanation = response_data.get("explanation", "")
        response = "YES EURO BILL :)!" if euro_bill else "NOT A EURO BILL"

        box_color = "#4CAF50" if euro_bill else "#F44336"

        explanation_box = f"""
        <div style="
            border: 1px solid {box_color};
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            background-color: {box_color};
            color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        ">
        <p>{explanation}</p>
        </div>
        """
        response_box = f"""
        <div style="
            border: 1px solid {box_color};
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            background-color: {box_color};
            color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        ">
        <p>AI BOT: {response}</p>
        </div>
        """
        st.markdown(response_box, unsafe_allow_html=True)
        st.markdown(explanation_box, unsafe_allow_html=True)

