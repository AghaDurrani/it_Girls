# pylint: disable=missing-module-docstring

import streamlit as st
import pandas as pd
import numpy as np

from streamlit_oauth import OAuth2Component

st.title('Uber pickups in NYC')

# Set environment variables
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://accounts.google.com/o/oauth2/auth"
REVOKE_TOKEN_URL = "https://accounts.google.com/o/oauth2/auth"
CLIENT_ID = "726921588578-gqa9vn25qk4sm8pr1uis5be3v3m9puu5.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://streamlit-template.k8s.aws.tadnet.net"
SCOPE = "userinfo.email"

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.experimental_rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.json(token)
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
        st.experimental_rerun()

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
# pylint: disable=missing-function-docstring
def load_data(nrows):
    # pylint: disable=redefined-outer-name
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # pylint: disable=unnecessary-lambda-assignment
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# pylint: disable=consider-using-f-string
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
