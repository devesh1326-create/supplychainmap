import streamlit as st
import pandas as pd
from config import PRODUCTS, ORIGINS, PRODUCT_COLORS
from route_calculator import calculate_routes_for_product, calculate_total_emissions
from visualizer import (
    create_route_map,
    create_sankey_diagram,
    create_heatmap,
    create_bubble_radar
)

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="LOGISTICS COMMAND", initial_sidebar_state="expanded")

# --- SVG ICONS (VECTOR ART) ---
ICON_SHIP = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><path d="M2 21h20M4 17l2-9h12l2 9M12 17v4M8 17v4M16 17v4M12 8V3m0 0l-3 3m3-3l3 3"/></svg>"""
ICON_ALERT = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>"""
ICON_CHECK = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>"""
ICON_RADAR = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 2.3 9.4"/></svg>"""

# --- CSS OVERHAUL (TEXTURES & SMALLER FONTS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');

    /* 1. TEXTURE OVERLAYS */
    .stApp {
        background-color: #020617;
        /* Dot Matrix Pattern */
        background-image: radial-gradient(#1e293b 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Scanline effect on containers */
    div[data-testid="stMetric"], div.stTabs, div[data-testid="stDataFrame"] {
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
        border: 1px solid #334155;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    /* 2. TYPOGRAPHY SCALING (FIX BIG TEXT) */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

    /* Force smaller metric numbers */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.8rem !important; /* Reduced from default */
        color: #f8fafc !important;
        text-shadow: 0 0 5px rgba(255,255,255,0.1);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8 !important;
    }

    /* 3. COMPONENT STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0B1120 !important;
        border-right: 1px solid #1e293b;
    }

    /* Custom Alert Boxes (Vector Styled) */
    .tech-alert {
        padding: 12px; margin-bottom: 15px;
        border: 1px solid; border-left-width: 4px;
        background: rgba(0,0,0,0.3);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        display: flex; align-items: center; gap: 10px;
    }
    .alert-red { border-color: #ef4444; color: #fca5a5; box-shadow: 0 0 10px rgba(239,68,68,0.1); }
    .alert-amber { border-color: #f59e0b; color: #fcd34d; box-shadow: 0 0 10px rgba(245,158,11,0.1); }
    .alert-blue { border-color: #3b82f6; color: #93c5fd; box-shadow: 0 0 10px rgba(59,130,246,0.1); }

    /* Tactical Brief Box */
    .tactical-brief {
        margin-top: -10px; margin-bottom: 20px;
        padding: 10px;
        border-top: 1px dashed #334155;
        background: rgba(15, 23, 42, 0.5);
        color: #64748b;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown(f"### {ICON_SHIP} CONTROL DECK", unsafe_allow_html=True)
st.sidebar.markdown("---")

scenario = st.sidebar.radio(
    "SIMULATION PROTOCOL",
    ["BUSINESS AS USUAL", "RED SEA BLOCKADE", "PANAMA DROUGHT", "SANTOS STRIKE"],
    index=0
)

# LOGIC ENGINE
active_restrictions = ['northwest', 'northeast', 'bering']
active_origins = ORIGINS.copy()
alert_html = f'<div class="tech-alert alert-blue">{ICON_CHECK} SYSTEM NORMAL // OPTIMAL FLOW</div>'

if scenario == "RED SEA BLOCKADE":
    active_restrictions += ['suez', 'babalmandab']
    alert_html = f'<div class="tech-alert alert-red">{ICON_ALERT} CRITICAL: SUEZ BLOCKED // REROUTING</div>'
elif scenario == "PANAMA DROUGHT":
    active_restrictions += ['panama']
    alert_html = f'<div class="tech-alert alert-amber">{ICON_RADAR} WARNING: PANAMA CAPACITY LOW</div>'
elif scenario == "SANTOS STRIKE":
    if "Santos Port (São Paulo)" in active_origins:
        del active_origins["Santos Port (São Paulo)"]
    alert_html = f'<div class="tech-alert alert-red">{ICON_ALERT} HAZARD: SANTOS PORT OFFLINE</div>'

# STATUS MONITOR
st.sidebar.markdown("---")
st.sidebar.caption("📡 **TELEMETRY**")
st.sidebar.code(f"MODE: {scenario}\nPORTS: {len(active_origins)} ONLINE\nRESTRICTIONS: {len(active_restrictions)}")

st.sidebar.markdown("---")
product_options = ["All Commodities"] + PRODUCTS
selected_product_view = st.sidebar.selectbox("CARGO MANIFEST", options=product_options)

# --- MAIN PAGE ---
st.title(f"COMMAND CENTER // {selected_product_view.upper()}")
st.markdown(alert_html, unsafe_allow_html=True)

# --- CALCULATION ---
combined_route_results = []
combined_emission_data = []
total_system_co2 = 0
total_system_kg = 0

products_to_process = PRODUCTS if selected_product_view == "All Commodities" else [selected_product_view]

for prod in products_to_process:
    r_results = calculate_routes_for_product(prod, active_restrictions, active_origins)
    e_data, _, p_co2, p_kg = calculate_total_emissions(r_results, prod)

    if selected_product_view == "All Commodities":
        for r in r_results: r['product_group'] = prod
        for e in e_data: e['product_group'] = prod

    combined_route_results.extend(r_results)
    combined_emission_data.extend(e_data)
    total_system_co2 += p_co2
    total_system_kg += p_kg

avg_system_efficiency = (total_system_co2 / total_system_kg) if total_system_kg > 0 else 0

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("NET CO2 IMPACT", f"{total_system_co2 / 1_000_000:,.1f} M t")
with col2: st.metric("EFFICIENCY", f"{avg_system_efficiency:.4f} kg/kg")
with col3:
    active_routes = len([r for r in combined_route_results if r.get('volume_kg', 0) > 0])
    st.metric("ACTIVE VECTORS", f"{active_routes}")
with col4:
    total_vol_b = total_system_kg / 1_000_000_000
    st.metric("TOTAL MASS", f"{total_vol_b:,.1f} B kg")

# --- MAP ---
st.markdown("### 🗺️ GEOSPATIAL NETWORK")
fig_map = create_route_map(combined_route_results, "Dark", False, True)
st.plotly_chart(fig_map, use_container_width=True, key=f"map_{scenario}")
st.markdown("""
<div class="tactical-brief">
    <strong>>> TACTICAL BRIEF:</strong> VISUALIZING REAL-TIME SUPPLY VECTORS. 
    LINES REPRESENT ACTIVE MARITIME ROUTES. 
    COLORS INDICATE COMMODITY TYPE. 
    THICKNESS INDICATES RELATIVE VOLUME.
</div>
""", unsafe_allow_html=True)

# --- INTEL SECTION ---
st.markdown("### STRATEGIC INTELLIGENCE")
col_left, col_right = st.columns(2)
valid_chart_data = [d for d in combined_emission_data if d.get('Export Volume (kg)', 0) > 0]

with col_left:
    tab_flow, tab_matrix = st.tabs(["🌊 FLOW", "🔥 HEATMAP"])

    with tab_flow:
        fig_sankey = create_sankey_diagram(valid_chart_data)
        st.plotly_chart(fig_sankey, use_container_width=True)
        st.markdown(
            """<div class="tactical-brief">>> ANALYSIS: SANKEY DIAGRAM SHOWS MASS TRANSFER FROM ORIGIN HUBS TO DESTINATION MARKETS. WIDTH = VOLUME.</div>""",
            unsafe_allow_html=True)

    with tab_matrix:
        fig_heat = create_heatmap(valid_chart_data)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown(
            """<div class="tactical-brief">>> ANALYSIS: RED ZONES INDICATE HIGH CARBON INTENSITY (CO2 PER TON). TARGET THESE ROUTES FOR OPTIMIZATION.</div>""",
            unsafe_allow_html=True)

with col_right:
    tab_radar, tab_data = st.tabs(["📡 RADAR", "📋 DATA"])

    with tab_radar:
        fig_radar = create_bubble_radar(valid_chart_data)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown(
            """<div class="tactical-brief">>> ANALYSIS: SCATTER PLOT IDENTIFIES EFFICIENCY OUTLIERS. TOP-LEFT QUADRANT = HIGH RISK (SHORT DISTANCE BUT HIGH EMISSION).</div>""",
            unsafe_allow_html=True)

    with tab_data:
        df_disp = pd.DataFrame(valid_chart_data)[
            ['Destination', 'Distance (NM)', 'Export Volume (tons)', 'CO₂ Emissions (tons)']]
        st.dataframe(df_disp, use_container_width=True, height=350)
        st.markdown("""<div class="tactical-brief">>> RAW DATA MANIFEST FOR EXPORT/AUDIT.</div>""",
                    unsafe_allow_html=True)