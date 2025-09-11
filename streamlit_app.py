import os
import streamlit as st
from fusion_tools.visualization import Visualization

st.title("Fusion Tools Viewer")

# Path to bundled slide
slide_path = "assets/breast_US.png"

if os.path.exists(slide_path):
    vis = Visualization(
        local_slides=[slide_path],
        components=[],  # ✅ empty list = no invalid string refs
        app_options={"jupyter": True}
    )

    # Render Dash inside Streamlit
    st.components.v1.html(vis.viewer_app.index(), height=800, scrolling=True)

else:
    st.error(f"Slide file not found at: {slide_path}")
