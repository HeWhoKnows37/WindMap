import streamlit as st
import json
import logging
from data_loader import load_and_process_data

st.set_page_config(page_title="ERA5 Wind Direction", layout="wide")

st.title("Weatherloo: Global Wind Direction (ERA5)")

st.markdown("""
*Please see `README_SOLUTION.md` for answers to Task 1 & Task 3.*
""")

# -----------------
# DATA LOADING
# -----------------
st.write("Loading ERA5 Weather Data (this takes a moment on first load)...")
with st.spinner("Fetching Zarr dataset from GCP... (Downscaled for web performance)"):
    # Load and cache the dataset (120 hour window)
    time_strings, formatted_data = load_and_process_data()

# -----------------
# TASK 2: Plot the variable
# -----------------
st.header("Task 2: Interactive Wind Map")
st.markdown("""
Move the slider **inside the map** to animate the wind vectors over the 120-hour window starting `2021-12-01 00:00:00`.
Use the **magnifying glass** icon on the right side of the map to search for specific locations.
""")

# Render Custom HTML component for leaflet-velocity since folium doesn't natively support it out of the box
# We inject the data right into a temporary HTML frame and provide an embedded JS slider so the map state isn't lost
velocity_data_all_json = json.dumps(formatted_data)
times_json = json.dumps(time_strings)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Wind Map</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    
    <!-- leaflet-velocity -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-velocity@1.6.0/dist/leaflet-velocity.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/leaflet-velocity@1.6.0/dist/leaflet-velocity.min.js"></script>
    
    <!-- leaflet-control-geocoder -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css" />
    <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
    
    <style>
        #map {{ width: 100%; height: 550px; margin: 0; padding: 0; }}
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        #slider-container {{
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
<div id="map"></div>
<div id="slider-container">
    <label for="time-slider"><strong>Time Slice (UTC):</strong> <span id="time-label"></span></label><br>
    <input type="range" id="time-slider" min="0" max="{len(time_strings) - 1}" value="0" style="width: 400px; margin-top: 5px;">
</div>
<script>
    var bounds = [
        [-90, -180], // Southwest coordinates
        [90, 180]    // Northeast coordinates
    ];
    
    var map = L.map('map', {{
        maxBounds: bounds,
        maxBoundsViscosity: 1.0,
        minZoom: 2
    }}).setView([0, 0], 2);
    
    // Add Geocoder search control
    L.Control.geocoder({{
        defaultMarkGeocode: true
    }}).addTo(map);
    
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        subdomains: 'abcd',
        maxZoom: 10,
        noWrap: false
    }}).addTo(map);

    var all_wind_data = {velocity_data_all_json};
    var times = {times_json};

    var velocityLayer = L.velocityLayer({{
        displayValues: true,
        displayOptions: {{
            velocityType: 'Global Wind',
            position: 'bottomleft',
            emptyString: 'No wind data'
        }},
        data: all_wind_data[times[0]],
        maxVelocity: 25,
        velocityScale: 0.01,
        colorScale: ["#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"]
    }});

    velocityLayer.addTo(map);
    
    // UI Updates
    document.getElementById('time-label').innerText = times[0];
    
    document.getElementById('time-slider').addEventListener('input', function(e) {{
        var index = e.target.value;
        var timeStr = times[index];
        document.getElementById('time-label').innerText = timeStr;
        velocityLayer.setData(all_wind_data[timeStr]);
    }});
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=570)

st.divider()

st.caption("Developed with AI")
