import os
import threading
import streamlit as st
import streamlit.components.v1 as components
from fusion_tools.visualization.components import Visualization
from fusion_tools.database.database import fusionDB

# --------------------------
# Database setup
# --------------------------
# Option A: File-based DB in working dir (persistent)
db_path = os.path.abspath("fusion.db")
db_url = f"sqlite:///{db_path}"

# Option B: In-memory DB (non-persistent, safe)
# db_url = "sqlite:///:memory:"

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

    # ✅ Add assets folder
    assets_folder = os.path.abspath("assets")
    if os.path.exists(assets_folder):
        vis.assets_folder = assets_folder
        supported_ext = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svs")

        for fname in os.listdir(assets_folder):
            fpath = os.path.join(assets_folder, fname)
            if os.path.isfile(fpath) and fname.lower().endswith(supported_ext):
                try:
                    vis.local_tile_server.add_new_image(fpath)
                    st.success(f"✅ Registered: {fname}")
                except Exception as e:
                    st.warning(f"⚠️ Could not register {fname}: {e}")
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
components.iframe("http://localhost:8050", height=800, scrolling=True)
