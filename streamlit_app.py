import os
import tempfile
import threading
import streamlit as st
import streamlit.components.v1 as components
from fusion_tools.visualization.components import Visualization
from fusion_tools.database.database import fusionDB

# --------------------------
# Database setup
# --------------------------
db_path = os.path.join(tempfile.gettempdir(), "fusion.db")
db_url = f"sqlite:///{db_path}"

try:
    db = fusionDB(db_url)
except Exception as e:
    st.error(f"❌ fusionDB failed to initialize: {e}")
    st.stop()

# --------------------------
# Visualization setup
# --------------------------
try:
    vis = Visualization()
    vis.database = db

    # ✅ Add your assets folder
    assets_folder = os.path.abspath("assets")
    if os.path.exists(assets_folder):
        vis.assets_folder = assets_folder
    else:
        st.warning(f"⚠️ Assets folder not found at {assets_folder}")

except Exception as e:
    st.error(f"❌ Visualization failed to initialize: {e}")
    st.stop()

# --------------------------
# Run Dash app in background
# --------------------------
def run_dash():
    try:
        vis.viewer_app.run(
            host="0.0.0.0",
            port=8050,
            debug=False,
            use_reloader=False
        )
    except Exception as e:
        st.error(f"❌ Dash server error: {e}")

thread = threading.Thread(target=run_dash, daemon=True)
thread.start()

# --------------------------
# Streamlit UI
# --------------------------
st.markdown("### Fusion Tools Visualization")
st.info("Dash app is running below, embedded in an iframe.")

# ✅ Embed Dash app inside Streamlit
components.iframe("http://localhost:8050", height=800, scrolling=True)
