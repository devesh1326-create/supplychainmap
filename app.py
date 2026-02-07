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
st.set_page_config(layout="wide", page_title="BRAZIL STRATEGIC TRADE CENTER", initial_sidebar_state="expanded")

# --- CLEAN CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');

    /* 1. DARK THEME */
    .stApp { background-color: #0f172a; }

    /* 2. CARDS */
    div[data-testid="stMetric"], div.stTabs, div[data-testid="stDataFrame"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* 3. TYPOGRAPHY */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.6rem !important; color: #f8fafc !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.8rem !important; text-transform: uppercase; color: #94a3b8 !important; }

    /* 4. SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }

    /* 5. ALERT BOXES */
    .status-box { padding: 15px; margin-bottom: 20px; border-left: 5px solid; background-color: #1e293b; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; }
    .status-normal { border-color: #10b981; }
    .status-danger { border-color: #ef4444; }
    .status-warn { border-color: #f59e0b; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("### SYSTEM CONTROLS")
st.sidebar.markdown("---")

scenario = st.sidebar.radio(
    "SIMULATION SCENARIO",
    [
        "BUSINESS AS USUAL",
        "THE GREAT CANAL COLLAPSE",  # Suez + Panama
        "ATLANTIC BLOCKADE (GIBRALTAR)",  # Forces Europe traffic South
        "TOTAL PORT BLACKOUT"  # Santos + Tubarao
    ],
    index=0
)

# --- LOGIC ENGINE ---
baseline_restrictions = ['northwest', 'northeast', 'bering']
baseline_origins = ORIGINS.copy()

active_restrictions = ['northwest', 'northeast', 'bering']
active_origins = ORIGINS.copy()

alert_html = '<div class="status-box status-normal">SYSTEM NORMAL: OPTIMAL ROUTING</div>'

if scenario == "THE GREAT CANAL COLLAPSE":
    active_restrictions += ['suez', 'panama', 'babelmandeb']
    alert_html = '<div class="status-box status-danger">GLOBAL CRISIS: SUEZ & PANAMA CLOSED. ROUTES FORCED AROUND CAPES.</div>'

elif scenario == "ATLANTIC BLOCKADE (GIBRALTAR)":
    active_restrictions += ['gibraltar']
    alert_html = '<div class="status-box status-warn">EUROPEAN CRISIS: GIBRALTAR STRAIT CLOSED. NORTHERN ROUTES DIVERTED.</div>'

elif scenario == "TOTAL PORT BLACKOUT":
    if "Santos Port (São Paulo)" in active_origins: del active_origins["Santos Port (São Paulo)"]
    if "Tubarão Port (Vitoria)" in active_origins: del active_origins["Tubarão Port (Vitoria)"]
    alert_html = '<div class="status-box status-danger">CATASTROPHIC FAILURE: SANTOS & TUBARÃO OFFLINE. EXPORT CAPACITY CRITICAL.</div>'

st.sidebar.markdown("---")
product_options = ["All Commodities"] + PRODUCTS
selected_product_view = st.sidebar.selectbox("PRODUCT FILTER", options=product_options)

# --- MAIN PAGE ---
st.title("BRAZIL LOGISTICS IMPACT CENTER")
st.markdown(alert_html, unsafe_allow_html=True)

# --- IMPACT CALCULATION ---
with st.spinner("CALCULATING STRATEGIC IMPACT..."):
    products_to_process = PRODUCTS if selected_product_view == "All Commodities" else [selected_product_view]

    current_routes = []
    current_emissions = []
    curr_co2 = 0
    curr_kg = 0

    # Baseline vars
    base_co2 = 0
    base_kg = 0

    for prod in products_to_process:
        # Run Current Scenario
        r_curr = calculate_routes_for_product(prod, active_restrictions, active_origins)
        e_curr, _, c_co2, c_kg = calculate_total_emissions(r_curr, prod)

        # Run Baseline (Normal) Scenario
        r_base = calculate_routes_for_product(prod, baseline_restrictions, baseline_origins)
        _, _, b_co2, b_kg = calculate_total_emissions(r_base, prod)

        if selected_product_view == "All Commodities":
            for r in r_curr: r['product_group'] = prod
            for e in e_curr: e['product_group'] = prod

        current_routes.extend(r_curr)
        current_emissions.extend(e_curr)
        curr_co2 += c_co2
        curr_kg += c_kg
        base_co2 += b_co2
        base_kg += b_kg

    # --- INTELLIGENT DELTA CALCULATION ---
    # 1. Efficiency Delta (Positive is BAD)
    curr_efficiency = (curr_co2 / curr_kg) if curr_kg > 0 else 0
    base_efficiency = (base_co2 / base_kg) if base_kg > 0 else 0
    eff_diff = curr_efficiency - base_efficiency
    eff_percent = (eff_diff / base_efficiency * 100) if base_efficiency > 0 else 0

    # 2. Volume Delta (Negative is BAD)
    vol_diff = curr_kg - base_kg
    vol_percent = (vol_diff / base_kg * 100) if base_kg > 0 else 0

    # 3. CO2 Total Delta
    co2_diff = curr_co2 - base_co2
    co2_percent = (co2_diff / base_co2 * 100) if base_co2 > 0 else 0

# --- METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "TOTAL CO2 EMISSIONS",
        f"{curr_co2 / 1_000_000:,.1f} M t",
        f"{co2_percent:+.1f}% Impact",
        delta_color="inverse"
    )

with col2:
    st.metric(
        "TRADE VOLUME",
        f"{curr_kg / 1_000_000_000:,.1f} B kg",
        f"{vol_percent:+.1f}% Volume" if abs(vol_percent) > 0.1 else "Stable",
        delta_color="normal"
    )

with col3:
    st.metric(
        "ACTIVE VECTORS",
        f"{len([r for r in current_routes if r.get('volume_kg', 0) > 0])}",
        delta="\xa0",  # Use a non-breaking space character
        delta_color="off"
    )

with col4:
    st.metric(
        "LOGISTICS EFFICIENCY",
        f"{curr_efficiency:.4f} kg/kg",
        f"{eff_percent:+.1f}% Intensity" if abs(eff_percent) > 0.1 else "Stable",
        delta_color="inverse"
    )

# --- MAP ---
st.markdown("### 🗺️ GLOBAL NETWORK MAP")
fig_map = create_route_map(current_routes, "Dark", False, False)
st.plotly_chart(fig_map, use_container_width=True, key=f"map_{scenario}")

# app.py
from config import EMISSIONS_DATA_SOURCE, SOURCE_NAME
from visualizer import create_emissions_factor_chart

# ...  ...

st.markdown("---")
st.markdown("### 📏 METHODOLOGY & DATA SOURCES")

col_method_1, col_method_2 = st.columns([2, 1])

with col_method_1:
    st.markdown("#### CARBON INTENSITY FACTORS")
    st.caption("Comparison of CO₂ emissions per ton-km based on vessel type used for each commodity.")

    # CALL THE NEW VISUALIZER FUNCTION
    fig_factors = create_emissions_factor_chart()
    st.plotly_chart(fig_factors, use_container_width=True)

with col_method_2:
    st.info("ℹ️ **SOURCE DATA**")
    st.markdown(f"""
    **Standard:** {SOURCE_NAME}

    **Link:** [Access Official Data 2024]({EMISSIONS_DATA_SOURCE})

    **Calculation:**
    Emissions = Distance (km) × Weight (tons) × Factor

    *Note: Factors are specific to the vessel class typically used for these commodities (e.g., Capesize for Ore vs. Reefer for Beef).*
    """)
# --- ANALYTICS ---
st.markdown("### 📊 STRATEGIC ANALYSIS")
col_left, col_right = st.columns(2)
valid_data = [d for d in current_emissions if d.get('Export Volume (kg)', 0) > 0]

with col_left:
    tab_flow, tab_matrix = st.tabs(["TRADE FLOW", "CARBON MATRIX"])
    with tab_flow:
        fig_sankey = create_sankey_diagram(valid_data)
        st.plotly_chart(fig_sankey, use_container_width=True)
    with tab_matrix:
        fig_heat = create_heatmap(valid_data)
        st.plotly_chart(fig_heat, use_container_width=True)

with col_right:
    tab_radar, tab_data = st.tabs(["RISK RADAR", "RAW DATA"])
    with tab_radar:
        fig_radar = create_bubble_radar(valid_data)
        st.plotly_chart(fig_radar, use_container_width=True)
    with tab_data:
        df_disp = pd.DataFrame(valid_data)[
            ['Destination', 'Distance (NM)', 'Export Volume (tons)', 'CO₂ Emissions (tons)']]
        st.dataframe(df_disp, use_container_width=True, height=350)


# --- CLEAN CSS ---
st.markdown("""
<style>
    /* ... existing fonts ... */

    /* 2. CARDS */
    div[data-testid="stMetric"], div.stTabs, div[data-testid="stDataFrame"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        min-height: 170px;  /* <--- ADD THIS LINE TO FORCE UNIFORM HEIGHT */
    }

    /* ... rest of css ... */
</style>
""", unsafe_allow_html=True)