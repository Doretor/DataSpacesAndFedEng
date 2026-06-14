import streamlit as st
import pandas as pd
import urllib.parse
from datetime import date, timedelta

st.set_page_config(page_title="EO Flood Data Space", page_icon="🌍", layout="wide")

st.title("🌊 Federated EO Data Space for Flood Monitoring")
st.markdown("An operational hub for Crisis Management Teams to discover, select, and access Earth Observation resources based on the flood phase.")
st.divider()

st.sidebar.header("Operational Targeting")
st.sidebar.markdown("Generate precise access links for specific locations and date ranges.")

target_lat = st.sidebar.number_input("Latitude (e.g., 50.4735):", value=50.4735, format="%.4f")
target_lng = st.sidebar.number_input("Longitude (e.g., 17.3324):", value=17.3324, format="%.4f")
target_zoom = st.sidebar.slider("Zoom Level:", min_value=5, max_value=18, value=12)

st.sidebar.markdown("**Observation Period:**")
col_date1, col_date2 = st.sidebar.columns(2)

with col_date1:
    start_date = st.date_input("Start Date", value=date.today() - timedelta(days=7))
with col_date2:
    end_date = st.date_input("End Date", value=date.today())

if start_date > end_date:
    st.sidebar.error("⚠️ Start date must be before End date.")
    start_date, end_date = end_date, start_date

st.sidebar.divider()
st.sidebar.caption("Select a wider date range (e.g., 7-14 days) to ensure multiple satellite passes are available on the timeline.")

st.subheader("🛰️ Available EO Resources Catalogue")

# --- RESOURCE 1: SENTINEL-1 ---
with st.expander("1. Sentinel-1 (Radar SAR) - Best for: Active Flood & Cloudy Conditions", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Provider:** Copernicus Data Space Ecosystem")
        st.markdown("**Capabilities:** Cloud penetration, night-time operations, reliable flood extent mapping.")
        st.markdown("**Operational Phase:** Response (During Flood)")
    with col2:
        s1_params = {
            "zoom": target_zoom, "lat": target_lat, "lng": target_lng,
            "themeId": "DEFAULT-THEME",
            "datasetId": "S1_CDAS_IW_VVVH",
            "fromTime": f"{start_date}T00:00:00.000Z", 
            "toTime": f"{end_date}T23:59:59.999Z",
	    "dateMode": "MOSAIC"
        }
        s1_link = f"https://browser.dataspace.copernicus.eu/?{urllib.parse.urlencode(s1_params)}"
        st.link_button("Launch Sentinel-1 Viewer", s1_link, type="primary")

# --- RESOURCE 2: SENTINEL-2 ---
with st.expander("2. Sentinel-2 (Optical) - Best for: Post-Flood Damage Assessment"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Provider:** Copernicus Data Space Ecosystem")
        st.markdown("**Capabilities:** High-resolution optical imagery, perfect for vegetation and water boundary index analysis.")
        st.markdown("**Operational Phase:** Recovery (Post-Flood, clear sky required)")
        st.warning("⚠️ Warning: Optical sensors are blind during severe storms. Use Sentinel-1 if cloudy.")
    with col2:
        s2_params = {
	    "zoom": target_zoom, "lat": target_lat, "lng": target_lng,
            "themeId": "DEFAULT-THEME",
            "datasetId": "S2_L2A_CDAS",
            "fromTime": f"{start_date}T00:00:00.000Z",
            "toTime": f"{end_date}T23:59:59.999Z"
	}
        s2_link = f"https://browser.dataspace.copernicus.eu/?{urllib.parse.urlencode(s2_params)}"
        st.link_button("Launch Sentinel-2 Viewer", s2_link, type="primary")

# --- RESOURCE 3: EUMETSAT ---
with st.expander("3. EUMETSAT (Meteosat MSG) - Best for: Weather Tracking & Early Warning"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Provider:** EUMETSAT")
        st.markdown("**Capabilities:** 15-minute temporal resolution, IR cloud top temperature analysis.")
        st.markdown("**Operational Phase:** Early Warning (Pre-Flood)")
        st.info("ℹ️ System Note: EUMETSAT interface restricts deep linking. Operator must manually select the layer upon entry.")
    with col2:
        st.link_button("Access EUMETView Dashboard", "https://view.eumetsat.int/productviewer?v=default")

# --- RESOURCE 4: COPERNICUS EMS ---
with st.expander("4. Copernicus EMS - Best for: Ready-to-use Damage Maps"):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Provider:** Copernicus Emergency Management Service")
        st.markdown("**Capabilities:** On-demand rapid mapping, vector data, infrastructure damage reports.")
        st.markdown("**Operational Phase:** Response & Recovery")
        st.success("Link leads directly to the official Copernicus EMS mapping dashboard.")
    with col2:
        st.link_button("View EMS Mapping Portal", "https://mapping.emergency.copernicus.eu/")

st.divider()
st.caption("Developed by: Filip Pyrek | Faculty of Space Technologies, AGH University of Krakow")
