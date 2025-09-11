import streamlit as st
import threading
import time
import socket

from fusion_tools.visualization.components import Visualization


# -------------------------------
# Utility: find a free port
# -------------------------------
def get_free_port(default=8050):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 0))
    port = s.getsockname()[1]
    s.close()
    return port or default


# -------------------------------
# Initialize Visualization safely
# -------------------------------
try:
    vis = Visualization()  # minimal init
    vis.add_assets_folder("assets")  # register all assets inside ./assets
except Exception as e:
    st.error(f"❌ Visualization failed to initialize: {e}")
    vis = None

# -------------------------------
# Run Dash viewer in background
# -------------------------------
def run_dash(port):
    if vis is not None:
        try:
            vis.viewer_app.run(host="0.0.0.0", port=port, debug=False)
        except Exception as e:
            print(f"⚠️ Dash server error: {e}")

port = get_free_port()

if vis is not None:
    thread = threading.Thread(target=run_dash, args=(port,), daemon=True)
    thread.start()
    time.sleep(1)  # give Dash server time to start

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🖼 Fusion Tools Visualization")

if vis is not None:
    st.components.v1.iframe(f"http://localhost:{port}", height=800)
else:
    st.warning("⚠️ Visualization not available.")
