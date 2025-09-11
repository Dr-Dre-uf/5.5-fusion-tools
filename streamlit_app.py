import os
import threading
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

from fusion_tools.visualization.components import Visualization
from fusion_tools.database.database import fusionDB


def main():
    st.write("------ Creating Visualization App ------")
    st.write("App start time:", datetime.now())

    # --- Database setup ---
    try:
        db_url = "sqlite:///fusion.db"
        db = fusionDB(db_url)
        st.write("✅ Database initialized:", db_url)
    except Exception as e:
        st.error(f"❌ Database initialization failed: {e}")
        return

    # --- Image asset ---
    image_path = os.path.abspath("assets/breast_US.png")
    if not os.path.exists(image_path):
        st.error(f"❌ Image not found: {image_path}")
        return
    else:
        st.write("✅ Image found:", image_path)

    # --- Visualization ---
    try:
        vis = Visualization(
            local_slides=[image_path],
            database=db,
            components=[],
            app_options={"title": "FUSION Streamlit", "port": 8050, "host": "0.0.0.0"}
        )

        st.write("✅ Visualization created successfully")

        # Run the Dash app in a background thread
        def run_dash():
            vis.run()

        thread = threading.Thread(target=run_dash, daemon=True)
        thread.start()

        # Render inside Streamlit with iframe
        components.iframe("http://localhost:8050", height=800, scrolling=True)

    except Exception as e:
        st.error(f"❌ Visualization failed: {e}")


if __name__ == "__main__":
    main()
