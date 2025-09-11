import os
import tempfile
import threading
import streamlit as st
from fusion_tools.visualization.components import Visualization
from fusion_tools.database.database import fusionDB

# --------------------------
# Ensure database works
# --------------------------
db_path = os.path.join(tempfile.gettempdir(), "fusion.db")
db_url = f"sqlite:///{db_path}"

# Initialize fusionDB directly
try:
    db = fusionDB(db_url)
except Exception as e:
    st.error(f"❌ fusionDB failed to initialize: {e}")
    st.stop()

# --------------------------
# Initialize Visualization
# --------------------------
try:
    vis = Visualization()
    vis.database = db  # attach our initialized DB
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
st.info("Dash app is running on port **8050**. Embed or proxy as needed.")
