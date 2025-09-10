import streamlit as st
import dash
from dash import html
from dash import dcc
from flask import Flask
import threading
import time
import streamlit.components.v1 as components

# Start a simple Dash app in a thread
def run_dash():
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Hello from Dash inside Streamlit"),
        dcc.Graph(
            figure={
                "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar"}],
                "layout": {"title": "Dash Graph"},
            }
        ),
    ])
    app.run_server(port=8050, debug=False, use_reloader=False)

thread = threading.Thread(target=run_dash)
thread.daemon = True
thread.start()

time.sleep(1)  # Give Dash server a moment to start

st.title("Embedding Dash in Streamlit")
components.iframe("http://localhost:8050", height=600)
