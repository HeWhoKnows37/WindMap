# Weatherloo: Wind Direction Visualization

This is my submission for the weatherloo take-home project. It visualizes the 10-meter U and V wind components over a 120-hour window using Streamlit and an interactive Folium map with animated wind particles.

## Running the App

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows (PowerShell)
   .\.venv\Scripts\Activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Task 1: Weather Variable Explanation

**Variables Chosen:** `10m_u_component_of_wind` and `10m_v_component_of_wind`

- **ELI5 Explanation:** Imagine you're standing outside and the wind pushes you. The U-component is how hard the wind pushes you exactly East or West. The V-component is how hard it pushes you exactly North or South. By combining these two directions, we can calculate the overall direction and speed of the wind blowing 10 meters above the ground.
- **Level Type:** These are single-level variables, specifically representing the wind at the surface level (10 meters above the surface), rather than at varying pressure levels higher up in the atmosphere.
- **Common Abbreviations:** These are commonly abbreviated as `u10` and `v10`.

## Task 3: Dataset Understanding

1. **What is the time step of the dataset?**
   The dataset takes a snapshot every 6 hours.

2. **What timezone/time standard does the dataset use?**
   The dataset uses UTC (Coordinated Universal Time).

3. **What do the numbers 1440x721 refer to?**
   This refers to the spatial resolution (grid size) of the dataset. There are 1440 points representing longitudes (covering 360 degrees around the Earth) and 721 points representing latitudes (from pole to pole). Specifically, this means the data has a resolution of 0.25 degrees.

4. **What is zarr?**
   Zarr is a format for the storage of chunked, compressed, N-dimensional arrays. Rather than downloading one massive file, Zarr splits the data into many smaller, compressed chunks that can be accessed in parallel. This is especially useful for cloud storage, allowing us to only load the specific geographical slices and time chunks we actually need for our visualization, without downloading the entire historical dataset.
