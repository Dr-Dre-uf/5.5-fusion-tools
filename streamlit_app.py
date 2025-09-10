import streamlit as st
import threading
import time
import streamlit.components.v1 as components

# Import your Fusion Tools Visualization
from fusion_tools.visualization import Visualization

# Function to run Fusion Tools visualization (Dash under the hood)
def run_fusion():
    vis = Visualization()
    vis.run(port=8050, debug=False, use_reloader=False)

# Start Fusion Tools app in background thread
thread = threading.Thread(target=run_fusion)
thread.daemon = True
thread.start()

# Give the server a moment to start
time.sleep(2)

# Streamlit UI
st.title("Fusion Tools Visualization in Streamlit")
st.write("This is an embedded Fusion Tools app (Dash) inside Streamlit.")

# Embed the Dash app as iframe
components.iframe("http://localhost:8050", height=800, scrolling=True)
