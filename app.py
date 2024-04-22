import streamlit as st
import os
import base64
from openai import OpenAI
import json
import httpx
import base64
import streamlit as st
import pickle

httpx_client = httpx.Client(verify=False)


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

import pickle 

file_name = 'api.pickle'

# Open the file in binary read mode and unpickle the data
with open(file_name, 'rb') as file:
    api_key = pickle.load(file)

# Initialize OpenAI client
client = OpenAI(
    api_key=api_key,
    http_client=httpx_client,
)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


def query_openai(image_url):
    """Queries OpenAI with an image URL."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "is this an euro bill? respond in json with key euro_bill which should have value yes or no, and key explanation which provides your explanation. The explanation should be at the level of a 12 year old and a bit funny. If it is non-euro note and you are confident about the currency and the value, try to mention how much the note is worth in euro.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"},
                    },
                ],
            }
        ],
        model="gpt-4-turbo-2024-04-09",
        response_format={"type": "json_object"},
    )
    return chat_completion


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
    response = query_openai(image_url)

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
