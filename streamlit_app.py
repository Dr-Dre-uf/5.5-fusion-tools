import os
import streamlit as st
from fusion_tools.visualization import Visualization
from fusion_tools.database.database import fusionDB

# --- Database Initialization ---
db_url = f"sqlite:///{os.path.join(os.getcwd(), 'fusion.db')}"
db = fusionDB(db_url=db_url, echo=False)

st.set_page_config(page_title="Fusion Tools Viewer", layout="wide")
st.sidebar.header("Database Status")
st.sidebar.success(f"Connected to Fusion DB at {db_url}")

# --- Main App Title ---
st.title("Fusion Tools Viewer Demo")

# --- Default slide path ---
default_slide = "assets/breast_US.png"
slides = []

if os.path.exists(default_slide):
    slides.append(default_slide)
else:
    st.sidebar.warning("⚠️ Default slide not found at assets/breast_US.png")

# --- Upload slide(s) ---
st.sidebar.header("Upload Your Own Slides")
uploaded_files = st.sidebar.file_uploader(
    "Choose one or more slides", type=["png", "jpg", "tif"], accept_multiple_files=True
)

if uploaded_files:
    os.makedirs(".fusion_assets", exist_ok=True)
    for uploaded in uploaded_files:
        save_path = os.path.join(".fusion_assets", uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.read())
        slides.append(save_path)
    st.sidebar.success(f"✅ Uploaded {len(uploaded_files)} file(s)")

# --- Guard: if no slides available ---
if not slides:
    st.error("No slides available. Please upload a file or place one at assets/breast_US.png")
    st.stop()

# --- Create Visualization with all slides ---
vis = Visualization(
    local_slides=slides,
    components=[
        {"type": "row", "components": ["main_viewer"]},
        {"type": "row", "components": ["annotation_table"]},
    ],
    database=db,
    app_options={"jupyter": True}
)

# --- Embed Viewer ---
st.subheader("Interactive Slide Viewer")
st.components.v1.html(vis.viewer_app.index(), height=800, scrolling=True)
