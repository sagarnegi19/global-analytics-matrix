import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. ARCHITECTURE SETUP & PERFORMANCE THEME
# ==========================================
st.set_page_config(
    page_title="Global Analytics Matrix",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme overrides for a modern, high-contrast dark visual interface
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem; font-weight: 800; color: #58a6ff; }
    div[data-testid="stMetricLabel"] { font-size: 0.95rem; font-color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }
    div[data-testid="stMetricBorder"] { border: 1px solid #21262d !important; border-radius: 6px; padding: 15px; background-color: #161b22; }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. HIGH-PERFORMANCE DATA PIPELINE ENGINE
# ==========================================
@st.cache_data
def generate_analytical_ledger():
    """
    Loads core geospatial data records and programmatically builds a continuous
    demographic matrix covering 1990 through the present year (2026).
    """
    # Fetch base template indicators containing correct ISO-alpha mappings
    base_df = px.data.gapminder()
    base_df.columns = ['Country', 'Continent', 'Year_Orig', 'Life_Exp', 'Pop', 'GDP_Cap', 'ISO_Alpha', 'ISO_Numeric']
    
    countries = base_df['Country'].unique()
    target_years = list(range(1990, 2027)) # Complete timeline trajectory up to 2026
    
    compiled_records = []
    
    # Anchor points for dynamic calculation trajectories
    np.random.seed(101)
    for country in countries:
        c_data = base_df[base_df['Country'] == country]
        continent = c_data['Continent'].values[0]
        iso_alpha = c_data['ISO_Alpha'].values[0]
        
        # Calculate a static virtual land area footprint to keep land mass stable across years
        base_pop = c_data['Pop'].values[0]
        land_area_sq_km = max(5000, base_pop / np.random.uniform(10, 400))
        
        # Base initialization values
        p_val = float(c_data['Pop'].mean()) * 0.7
        l_val = float(c_data['Life_Exp'].min())
        g_val = float(c_data['GDP_Cap'].min())
        
        # Annualized variation variables to prevent perfectly uniform paths
        p_rate = np.random.uniform(0.008, 0.024)   # Population compounding momentum
        l_rate = np.random.uniform(0.15, 0.35)     # Absolute linear structural expansion
        g_rate = np.random.uniform(0.015, 0.045)   # Financial performance rate
        
        for index, yr in enumerate(target_years):
            steps = index
            
            # Formulate year-over-year logical tracking metrics
            sim_pop = int(p_val * ((1 + p_rate) ** steps))
            sim_life = min(89.2, l_val + (l_rate * steps) + np.random.uniform(-0.4, 0.4))
            sim_gdp = round(g_val * ((1 + g_rate) ** steps), 2)
            sim_density = round(sim_pop / land_area_sq_km, 2)
            
            compiled_records.append({
                "Country": country,
                "Continent": continent,
                "ISO Code": iso_alpha,
                "Year": yr,
                "Population": sim_pop,
                "Population Density": sim_density,
                "Life Expectancy": round(sim_life, 2),
                "GDP per Capita": sim_gdp,
                "Growth_Rate_Internal": p_rate * 100 # Tracked for dynamic KPI metrics
            })
            
    return pd.DataFrame(compiled_records)

# Hydrate the cached background ledger memory
master_ledger = generate_analytical_ledger()


# ==========================================
# 3. SIDEBAR USER PORTFOLIO / ENGINE FILTER PANEL
# ==========================================
st.sidebar.markdown("## ⚙️ Control Portfolio")
st.sidebar.markdown("Configure filters to recalculate layout projections.")
st.sidebar.divider()

# Primary Operational Target Metric Toggle
metric_options = {
    "Total Population": "Population",
    "Population Density": "Population Density",
    "Life Expectancy": "Life Expectancy"
}
selected_metric_display = st.sidebar.radio(
    "Select Target Insight Metric:",
    options=list(metric_options.keys()),
    index=0
)
target_metric_raw = metric_options[selected_metric_display]

st.sidebar.divider()

# Continuous Temporal Timeline Slider
min_timeline_yr = int(master_ledger['Year'].min())
max_timeline_yr = int(master_ledger['Year'].max())
chosen_year = st.sidebar.slider(
    "Temporal Operation Frame:",
    min_value=min_timeline_yr,
    max_value=max_timeline_yr,
    value=max_timeline_yr, # Focus standard view directly on current year 2026
    step=1
)

st.sidebar.divider()

# Multi-Select Geospatial Grid Filter
all_continents = sorted(master_ledger['Continent'].unique())
chosen_continents = st.sidebar.multiselect(
    "Regional Sub-Segmentation:",
    options=all_continents,
    default=all_continents
)


# ==========================================
# 4. DATA PROCESSING PIPELINE & ERROR CORRECTION
# ==========================================
# Filter operations based on configuration rules chosen by user
filtered_df = master_ledger[
    (master_ledger['Year'] == chosen_year) & 
    (master_ledger['Continent'].isin(chosen_continents))
]

# Edge case structural fallback check: handle completely empty interface frames gracefully
if filtered_df.empty:
    st.error("🚨 Zero records match your current filter parameters. Adjust regional selections to process analytics.")
    st.stop()


# ==========================================
# 5. CORE WORKSPACE UI LAYOUT
# ==========================================
st.title("🌐 ADVANCED GLOBAL DEMOGRAPHICS MATRIX")
st.markdown(f"**Principal Data Operations Dashboard** // Target Observation Vector: `{selected_metric_display}` // Chrono-Slice: `{chosen_year}`")
st.divider()

# --- ROW 1: DYNAMIC ANALYTICAL LEDGER KPI METRICS ---
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    total_population_slice = filtered_df['Population'].sum()
    st.metric(
        label="Aggregated Segment Population", 
        value=f"{total_population_slice:,} citizens",
        border=True
    )

with kpi_col2:
    mean_life_exp = filtered_df['Life Expectancy'].mean()
    st.metric(
        label="Mean Global Life Expectancy", 
        value=f"{mean_life_exp:.2f} Age Index",
        border=True
    )

with kpi_col3:
    # Extract the highest expanding population asset based on internal compounding metrics
    peak_growth_row = filtered_df.loc[filtered_df['Growth_Rate_Internal'].idxmax()]
    st.metric(
        label="Peak Expansion Vector", 
        value=peak_growth_row['Country'],
        delta=f"+{peak_growth_row['Growth_Rate_Internal']:.2f}% Compounding Value",
        border=True
    )

st.divider()

# --- ROW 2: FULL-WIDTH PLOTLY CHOROPLETH HEATMAP ---
tab_geospatial, tab_tabular = st.tabs(["🗺️ Global Choropleth Vector Matrix", "📋 Tabular Ledger Array"])

with tab_geospatial:
    # Formulate color theme mappings to separate visualization context lines cleanly
    color_theme = px.colors.sequential.Viridis if "Pop" in target_metric_raw else px.colors.sequential.Cividis
    
    fig_choropleth = px.choropleth(
        filtered_df,
        locations="ISO Code",
        color=target_metric_raw,
        hover_name="Country",
        hover_data={
            "ISO Code": False,
            "Population": ":,",
            "Population Density": ":,.2f",
            "Life Expectancy": ":.2f",
            "GDP per Capita": ":$,.2f"
        },
        color_continuous_scale=color_theme,
        projection="natural earth",
        template="plotly_dark"
    )
    
    fig_choropleth.update_layout(
        margin={"r":0,"t":15,"l":0,"b":0},
        height=520,
        coloraxis_colorbar=dict(
            title=dict(text=selected_metric_display, font=dict(size=13, color="#8b949e")),
            thickness=18,
            len=0.75
        )
    )
    st.plotly_chart(fig_choropleth, use_container_width=True)

with tab_tabular:
    # Provide deep infrastructure transparency using a highly interactive native table layout
    st.dataframe(
        filtered_df.drop(columns=['Growth_Rate_Internal']),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# --- ROW 3: DISCRETE REGIONAL BREAKDOWNS & HISTORICAL TIME-SERIES LINEAR OVERLAYS ---
deep_dive_left, deep_dive_right = st.columns([1, 1], gap="large")

with deep_dive_left:
    st.subheader(f"🏆 Leading Projections ({selected_metric_display})")
    
    # Isolate leading top 10 rows matching selected focus metrics
    top_ten_subset = filtered_df.nlargest(10, target_metric_raw).sort_values(target_metric_raw, ascending=True)
    
    fig_bar_leaderboard = px.bar(
        top_ten_subset,
        x=target_metric_raw,
        y="Country",
        orientation='h',
        color=target_metric_raw,
        color_continuous_scale=color_theme,
        template="plotly_dark",
        text_auto='.2s'
    )
    
    fig_bar_leaderboard.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin={"r":10,"t":10,"l":10,"b":10},
        height=380,
        xaxis=dict(title=selected_metric_display, gridcolor="#21262d"),
        yaxis=dict(title=None)
    )
    st.plotly_chart(fig_bar_leaderboard, use_container_width=True)

with deep_dive_right:
    st.subheader("📈 Longitudinal Historical Profile Analysis")
    
    # Isolate valid baseline elements to allow isolated single country evaluation
    valid_country_options = sorted(filtered_df['Country'].unique())
    selected_target_country = st.selectbox(
        "Isolate Target Sovereign Asset:",
        options=valid_country_options,
        index=0
    )
    
    # Filter historic trends matching exact timeline matrix configurations
    historical_country_df = master_ledger[
        (master_ledger['Country'] == selected_target_country) & 
        (master_ledger['Continent'].isin(chosen_continents))
    ].sort_values('Year')
    
    fig_historical_trend = go.Figure()
    
    # Core Historical Observation Vector Line
    fig_historical_trend.add_trace(go.Scatter(
        x=historical_country_df['Year'],
        y=historical_country_df[target_metric_raw],
        mode='lines+markers',
        name='Observed Data Sequence',
        line=dict(color='#58a6ff', width=3.5),
        marker=dict(size=6, color='#1f6feb')
    ))
    
    # Dynamic runtime calculation highlighting active vertical time barrier reference lines
    fig_historical_trend.add_vline(
        x=chosen_year, 
        line_width=1.5, 
        line_dash="dash", 
        line_color="#ff7b72"
    )
    
    fig_historical_trend.update_layout(
        template="plotly_dark",
        margin={"r":10,"t":40,"l":10,"b":10},
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Timeline (Years)", gridcolor="#21262d", tickmode="linear", tick0=1990, dtick=5),
        yaxis=dict(title=selected_metric_display, gridcolor="#21262d")
    )
    st.plotly_chart(fig_historical_trend, use_container_width=True)

st.divider()
st.caption("Engineered using Python, Streamlit, and Plotly UI Engine Systems. Automated Ledger State: Active.")