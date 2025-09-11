# streamlit_app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
from PIL import Image, ImageDraw
import numpy as np
import os
from skimage import data
import imageio

st.set_page_config(page_title="Interactive Medical Image Annotation", layout="wide")
st.title("Interactive Medical Image Annotation")

# Ensure temp folder exists
os.makedirs("temp", exist_ok=True)

# --- Prepare default sample image if none uploaded ---
default_image_path = os.path.join("temp", "sample.png")
if not os.path.exists(default_image_path):
    sample = data.coins()  # guaranteed sample image from skimage
    imageio.imwrite(default_image_path, sample)

# --- Sidebar: upload and selection ---
st.sidebar.header("Images")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more images (PNG/JPG). If none uploaded, a sample image will be used.",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Save uploaded files to temp and build list of choices
image_choices = []
if uploaded_files:
    for up in uploaded_files:
        path = os.path.join("temp", up.name)
        with open(path, "wb") as f:
            f.write(up.getbuffer())
        image_choices.append(path)
else:
    # fallback sample
    image_choices.append(default_image_path)

# Let user choose which image to work on
selected_path = st.sidebar.selectbox("Select image", image_choices, format_func=lambda p: os.path.basename(p))

# Load selected image
try:
    base_img = Image.open(selected_path).convert("RGB")
except Exception as e:
    st.error(f"Could not open image: {e}")
    st.stop()

w, h = base_img.size  # note: PIL returns (width, height)

# Display a small preview
st.subheader(f"Selected: {os.path.basename(selected_path)}")
st.image(base_img, caption=os.path.basename(selected_path), width=480)

# --- Build folium map with ImageOverlay ---
# Use Simple CRS so coordinates map directly to image pixel space.
m = folium.Map(location=[h/2, w/2], zoom_start=0, tiles=None, crs="Simple")

# Bounds: top-left (0,0) to bottom-right (height, width)
# For ImageOverlay, bounds are [[y_min, x_min], [y_max, x_max]]
bounds = [[0, 0], [h, w]]

folium.raster_layers.ImageOverlay(
    image=selected_path,
    bounds=bounds,
    opacity=1.0,
    interactive=True,
    cross_origin=False,
    zindex=1
).add_to(m)

m.fit_bounds(bounds)

# Add Draw controls
draw = Draw(
    export=False,
    filename="annotations.geojson",
    position="topleft",
    draw_options={
        "polyline": True,
        "polygon": True,
        "circle": True,
        "rectangle": True,
        "marker": True,
        "circlemarker": False,
    },
    edit_options={"edit": True}
)
draw.add_to(m)

st.write("Draw on the image below (use toolbar at top-left). When you finish drawing, the shapes are rendered on the image below.")
map_result = st_folium(m, width=900, height=650, returned_objects=["all_drawings"])

# --- Render drawn shapes back on the image ---
drawings = None
if map_result:
    drawings = map_result.get("all_drawings") or map_result.get("drawn_features") or None

if drawings:
    # Create a copy of the base image to draw on
    annotated = base_img.copy()
    drawer = ImageDraw.Draw(annotated)

    # drawings is expected to be a list of GeoJSON Feature objects
    # Each feature: {"type":"Feature", "properties":..., "geometry":{"type":..., "coordinates":...}}
    for feat in drawings:
        geom = feat.get("geometry", {})
        if not geom:
            continue
        gtype = geom.get("type")
        coords = geom.get("coordinates")

        # Handle polygons or multipolygons (rectangle, polygon)
        if gtype == "Polygon":
            # coords: [ [ [x, y], [x, y], ... ] ]  (first ring)
            try:
                ring = coords[0]
                poly = [(int(x), int(y)) for x, y in ring]
                drawer.polygon(poly, outline="red")
            except Exception:
                pass

        elif gtype == "MultiPolygon":
            try:
                for poly_coords in coords:
                    ring = poly_coords[0]
                    poly = [(int(x), int(y)) for x, y in ring]
                    drawer.polygon(poly, outline="red")
            except Exception:
                pass

        elif gtype == "Point":
            try:
                x, y = coords
                x, y = int(x), int(y)
                r = max(3, int(min(w, h) * 0.005))
                drawer.ellipse((x - r, y - r, x + r, y + r), outline="blue")
            except Exception:
                pass

        elif gtype == "LineString":
            try:
                line = [(int(x), int(y)) for x, y in coords]
                drawer.line(line, fill="green", width=3)
            except Exception:
                pass

        else:
            # Some Draw plugins export circles/rectangles as a Polygon; many shapes will be caught by Polygon case.
            # If coordinates look like a bbox (4 pts), draw polygon anyway.
            try:
                # fallback attempt: if coords is a list of points
                if isinstance(coords, list) and len(coords) > 1 and isinstance(coords[0], (list, tuple)):
                    points = [(int(x), int(y)) for x, y in coords[0]] if isinstance(coords[0][0], (list, tuple)) else [(int(x), int(y)) for x, y in coords]
                    if len(points) >= 2:
                        drawer.polygon(points, outline="red")
            except Exception:
                pass

    # Show annotated image
    st.subheader("Annotated image")
    st.image(annotated, caption="Annotated image", width=900)
else:
    st.info("No drawings available. Use drawing tools (top-left) to add shapes. After drawing, refresh or click elsewhere to see rendered annotations appear here.")
