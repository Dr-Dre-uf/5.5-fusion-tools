import os
import streamlit as st
from fusion_tools.visualization import Visualization
from fusion_tools.database.database import fusionDB

# --- Database Initialization ---
# Persistent SQLite database in project root
db_url = f"sqlite:///{os.path.join(os.getcwd(), 'fusion.db')}"
db = fusionDB(db_url=db_url, echo=False)

st.set_page_config(page_title="Fusion Tools Viewer", layout="wide")
st.sidebar.header("Database Status")
st.sidebar.success(f"Connected to Fusion DB at {db_url}")

# --- Main App Title ---
st.title("Fusion Tools Viewer Demo")

# --- Default slide path ---
slide_path = "assets/breast_US.png"

if not os.path.exists(slide_path):
    st.error(f"Default slide not found at path: {slide_path}")
    st.stop()

# --- Create Visualization with bundled slide ---
vis = Visualization(
    local_slides=[slide_path],
    components=[],  # Keep layout simple; customize as needed
    database=db,
    app_options={"jupyter": True}
)

# --- Embed the Viewer in Streamlit ---
st.subheader("Interactive Slide Viewer")
st.components.v1.html(vis.viewer_app.index(), height=800, scrolling=True)

# --- Optional: Save uploaded slide ---
st.sidebar.header("Or Upload Your Own Slide")
uploaded = st.sidebar.file_uploader("", type=["png", "jpg", "tif"])
if uploaded:
    # Save to temp and reload viewer
    temp_path = os.path.join(".fusion_assets", uploaded.name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded.read())
    st.sidebar.success(f"Uploaded to {temp_path}; reload page to view")
