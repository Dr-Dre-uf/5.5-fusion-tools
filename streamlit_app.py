import streamlit as st
import streamlit.components.v1 as components

# Set the page to wide mode to better accommodate the iframe
st.set_page_config(layout="wide")

st.title("Embedded FusionPub Application")

# Embed the URL
# You can adjust height and scrolling as needed
components.iframe("https://fusionpub.rc.ufl.edu/#", height=800, scrolling=True)
