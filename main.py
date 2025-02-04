import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import plotly.express as px
import folium
from streamlit_folium import folium_static
import numpy as np

# Page Config
st.set_page_config(page_title="🌍 AI-Powered Climate & Trade Simulator", layout="wide")

# 📌 Custom Landing Page Header
st.title("🌍 AI-Powered Climate & Trade Simulator")
st.subheader("An Interactive Tool for Exploring CO₂ Emissions, Trade, and Climate Policies")

st.markdown(
    """
    ### Why This App Matters 🌱💰  
    - Climate change is one of the biggest challenges of our time.  
    - International trade plays a crucial role in global carbon emissions.  
    - AI & data science can help predict emissions trends and shape better policies.  

    **This interactive tool lets you:**  
    ✅ Explore **CO₂ emissions & trade impact** across the world  
    ✅ Simulate **climate policies** with AI-powered suggestions  
    ✅ Play as a policymaker in the **CO₂ Trade Simulator**  
    ✅ Visualize global emissions on an **interactive heatmap**  
    ---
    """
)

# Sidebar - Country Selection
st.sidebar.header("🌎 Select a Country")
selected_country = st.sidebar.selectbox("Choose a Country:", ["USA", "China", "UK", "Germany", "India"])

# Sample Data
data = {
    "USA": {"Emissions": 5100, "Trade Partners": ["China", "Mexico", "Canada"], "Latitude": 37.1, "Longitude": -95.7},
    "China": {"Emissions": 10500, "Trade Partners": ["USA", "EU", "ASEAN"], "Latitude": 35.9, "Longitude": 104.1},
    "UK": {"Emissions": 350, "Trade Partners": ["EU", "USA", "China"], "Latitude": 55.4, "Longitude": -3.4},
    "Germany": {"Emissions": 750, "Trade Partners": ["EU", "China", "USA"], "Latitude": 51.2, "Longitude": 10.4},
    "India": {"Emissions": 2600, "Trade Partners": ["China", "USA", "EU"], "Latitude": 20.6, "Longitude": 78.9}
}

# 📌 AI-Powered Policy Generator
st.sidebar.header("🧠 AI Policy Generator")
policy_goal = st.sidebar.text_input("Describe a policy goal (e.g., 'cut emissions by 20%')")
if st.sidebar.button("Generate AI Policy"):
    policies = [
        "🌱 Implement a national carbon tax",
        "🚗 Provide subsidies for electric vehicles",
        "🏭 Mandate cleaner energy production",
        "💡 Invest in green technology innovation",
        "🌎 Strengthen international climate agreements"
    ]
    st.sidebar.markdown(f"### ✅ AI-Powered Policy Recommendation:")
    st.sidebar.markdown(random.choice(policies))

# 📊 CO₂ Trading Simulator
st.subheader("💰 CO₂ Trading Simulator")
st.markdown("Make trade & emissions decisions. See real-time impact on economy & environment.")

trade_change = st.slider("Change in Trade (+/- %)", -50, 50, 0)
policy_change = st.slider("Emission Reduction Policy Strength (+/- %)", -50, 50, 0)

new_emissions = data[selected_country]["Emissions"] * (1 + trade_change / 100) * (1 - policy_change / 100)
st.metric(label="📉 Projected CO₂ Emissions", value=f"{new_emissions:.2f} million tonnes")

# 📌 CO₂ Heatmap
st.subheader("🔥 Global CO₂ Heatmap")

fig = px.choropleth(pd.DataFrame.from_dict(data, orient="index"),
                    locations=data.keys(),
                    locationmode="country names",
                    color=[d["Emissions"] for d in data.values()],
                    hover_name=data.keys(),
                    title="CO₂ Emissions by Country",
                    color_continuous_scale="Reds")

st.plotly_chart(fig, use_container_width=True)

# 📊 Time Slider for CO₂ Trends (2000–2050)
st.subheader("📈 CO₂ Emissions Over Time")

year_slider = st.slider("Select a Year", 2000, 2050, 2025)
emission_trend = data[selected_country]["Emissions"] * (0.98 ** (2024 - year_slider))
st.metric(label=f"Projected CO₂ Emissions in {year_slider}", value=f"{emission_trend:.2f} million tonnes")

# 🌐 CO₂ Trade Network Graph (Optimized)
st.subheader("🌐 Global CO₂ Trade Network")

G = nx.DiGraph()
for country, details in data.items():
    G.add_node(country)
    for partner in details["Trade Partners"]:
        G.add_edge(country, partner)

fig, ax = plt.subplots(figsize=(8, 5))
pos = nx.spring_layout(G, seed=42, k=0.3)  # Adjusted for better spacing
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, edge_color="gray", font_size=10, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=[selected_country], node_color="red", node_size=3500, ax=ax)
st.pyplot(fig)

# 🌍 Interactive Trade Map
st.subheader("🌎 CO₂ Trade Partners & Emissions Flow")
m = folium.Map(location=[data[selected_country]["Latitude"], data[selected_country]["Longitude"]], zoom_start=4)

for partner in data[selected_country]["Trade Partners"]:
    partner_info = data.get(partner)
    if partner_info:
        folium.Marker(
            [partner_info["Latitude"], partner_info["Longitude"]],
            popup=f"Trade Partner: {partner}",
            icon=folium.Icon(color="green", icon="cloud"),
        ).add_to(m)

folium_static(m)

# 📌 "About the Creator" Section
st.markdown(
    """
    ---
    ## 👩‍💻 About the Creator: Amisha  
    This project was developed by me as part of a research-driven initiative to bring AI into climate policy modeling.  
    Passionate about **international relations, sustainable economics, and technology**, I designed this tool to:  
    - **Visualize global carbon trade dependencies** 🌍  
    - **Help policymakers and researchers** understand emissions trends 📊  
    - **Empower students and citizens** to explore climate solutions 💡  

    🚀 *This project showcases the power of AI & data science in solving global challenges.*
    """
)
