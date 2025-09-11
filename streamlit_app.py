import streamlit as st
import threading, time, requests
from fusion_tools.visualization.components import Visualization

# Create Visualization
st.write("------Creating Visualization with 0 rows, 1 columns, and 0 tabs--------")
st.write("----------------- Components in the same row may communicate through callbacks---------")

vis = Visualization()

# Run Dash app in background thread
def run_dash():
    vis.viewer_app.run(
        host="0.0.0.0",
        port=8050,
        debug=False,
        use_reloader=False
    )

thread = threading.Thread(target=run_dash, daemon=True)
thread.start()

# Wait for Dash server to start (retry loop)
dash_url = "http://localhost:8050"
for i in range(20):  # 20 retries max (~10 seconds)
    try:
        r = requests.get(dash_url)
        if r.status_code == 200:
            st.success(f"✅ Dash server is running at {dash_url}")
            break
    except requests.exceptions.ConnectionError:
        time.sleep(0.5)
else:
    st.error("❌ Dash server failed to start.")
    st.stop()

# Embed Dash app in Streamlit
st.markdown(
    f"""
    <iframe src="{dash_url}" width="100%" height="800" style="border:none;"></iframe>
    """,
    unsafe_allow_html=True
)

st.write("app start time:", time.strftime("%Y-%m-%d %H:%M:%S"))
