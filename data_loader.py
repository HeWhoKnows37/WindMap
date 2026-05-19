import xarray as xr
import numpy as np
import streamlit as st

@st.cache_data
def load_and_process_data():
    """
    Connects to GCP Zarr, selects 120h of data, subsamples, 
    and prepares it for Leaflet-velocity.
    """
    # Use anonymous connection for public bucket
    url = "gs://gcp-public-data-arco-era5/ar/1959-2022-6h-1440x721.zarr"
    
    import gcsfs
    fs = gcsfs.GCSFileSystem(token='anon')
    mapper = fs.get_mapper(url)
    
    # We use xarray to open the zarr store. lazy loading
    ds = xr.open_zarr(mapper, consolidated=True)
    
    # Pick a start date, e.g., 2021-12-01 00:00:00 to 2021-12-05 18:00:00 (120 hours)
    start_date = '2021-12-01T00:00:00'
    end_date = '2021-12-05T18:00:00' 
    
    # Select our variables and time slice
    ds_slice = ds[['10m_u_component_of_wind', '10m_v_component_of_wind']].sel(
        time=slice(start_date, end_date)
    )
    
    # Subsample data: 1440x721 is over 1M points.
    # Taking every 8th point gives ~16k points, which the browser can animate smoothly.
    step = 8
    ds_sub = ds_slice.isel(longitude=slice(None, None, step), latitude=slice(None, None, step))
    
    # Load this subset into memory
    ds_sub = ds_sub.load()
    
    lats = ds_sub.latitude.values
    lons = ds_sub.longitude.values
    times = ds_sub.time.values
    
    # Determine intervals
    dx = abs(lons[1] - lons[0]) if len(lons) > 1 else 1.0
    dy = abs(lats[1] - lats[0]) if len(lats) > 1 else 1.0
    
    formatted_data = {}
    time_strings = [str(t)[:19] for t in times]
    
    for i, t_str in enumerate(time_strings):
        u_data = ds_sub['10m_u_component_of_wind'].isel(time=i).values
        v_data = ds_sub['10m_v_component_of_wind'].isel(time=i).values
        
        # Leaflet-velocity requires flat lists
        u_flat = np.nan_to_num(u_data).flatten().tolist()
        v_flat = np.nan_to_num(v_data).flatten().tolist()
        
        # leaflet-velocity format
        velocity_js = [
            {
                "header": {
                    "parameterUnit": "m.s-1",
                    "parameterNumber": 2,
                    "parameterNumberName": "U-component_of_wind",
                    "parameterCategory": 2,
                    "nx": len(lons),
                    "ny": len(lats),
                    "la1": float(lats[0]),
                    "la2": float(lats[-1]),
                    "lo1": float(lons[0]),
                    "lo2": float(lons[-1]),
                    "dx": float(dx),
                    "dy": float(dy)
                },
                "data": u_flat
            },
            {
                "header": {
                    "parameterUnit": "m.s-1",
                    "parameterNumber": 3,
                    "parameterNumberName": "V-component_of_wind",
                    "parameterCategory": 2,
                    "nx": len(lons),
                    "ny": len(lats),
                    "la1": float(lats[0]),
                    "la2": float(lats[-1]),
                    "lo1": float(lons[0]),
                    "lo2": float(lons[-1]),
                    "dx": float(dx),
                    "dy": float(dy)
                },
                "data": v_flat
            }
        ]
        
        formatted_data[t_str] = velocity_js
        
    return time_strings, formatted_data
