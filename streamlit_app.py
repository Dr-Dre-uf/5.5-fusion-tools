import os
import threading
import streamlit as st
import streamlit.components.v1 as components
from fusion_tools.visualization.components import Visualization
from fusion_tools.database.database import fusionDB, Base

# --------------------------
# Database setup (in-memory for now)
# --------------------------
db_url = "sqlite:///:memory:"
try:
    db = fusionDB(db_url)
except Exception as e:
    st.error(f"❌ fusionDB failed to initialize: {e}")
    st.stop()

# --------------------------
# Helper Functions
# --------------------------
def reset_database():
    try:
        engine = db.engine
        Base.metadata.drop_all(bind=engine)   # drop all tables
        Base.metadata.create_all(bind=engine) # recreate tables
        st.sidebar.success("✅ Database reset successfully.")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to reset DB: {e}")

def reload_assets():
    assets_folder = os.path.abspath("assets")
    if not os.path.exists(assets_folder):
        st.sidebar.warning(f"⚠️ Assets folder not found at {assets_folder}")
        return

    supported_ext = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svs")
    loaded = 0

    for fname in os.listdir(assets_folder):
        fpath = os.path.join(assets_folder, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(supported_ext):
            try:
                vis.local_tile_server.add_new_image(fpath)
                loaded += 1
            except Exception as e:
                st.sidebar.warning(f"⚠️ Could not register {fname}: {e}")

    st.sidebar.success(f"✅ Reloaded {loaded} image(s) into the visualization.")

# --------------------------
# Streamlit Sidebar Controls
# --------------------------
st.sidebar.header("Controls")
if st.sidebar.button("🔄 Reset Database"):
    reset_database()
if st.sidebar.button("🖼 Reload Assets"):
    reload_assets()

# --------------------------
# Visualization setup
# --------------------------
try:
    vis = Visualization()
    vis.database = db

    # Load assets initially
    reload_assets()

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
