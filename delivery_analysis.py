import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Dashboard Configuration ---
st.set_page_config(page_title="Logistics Performance Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

# Main Title
st.title("📦 Logistics & Delivery Performance Dashboard")
st.markdown("Analyzing delivery times, traffic impacts, and route efficiency to optimize logistics operations.")
st.divider()

# --- 2. Load and Clean Data ---
# st.cache_data makes sure the app doesn't reload the CSV every single time you click something
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('amazon_delivery.csv')
        # Clean up column names and whitespace
        df.columns = df.columns.str.strip()
        cols_to_strip = ['Area', 'Traffic', 'Weather', 'Vehicle']
        for col in cols_to_strip:
            if col in df.columns:
                df[col] = df[col].str.strip()
        return df
    except FileNotFoundError:
        st.error("Error: 'amazon_delivery.csv' not found. Please ensure it is in the same folder as this script.")
        return pd.DataFrame()

df = load_data()

# Only run the rest of the app if data loaded successfully
if not df.empty:
    
    # --- Sidebar Metrics ---
    st.sidebar.header("Dataset Overview")
    st.sidebar.metric("Total Deliveries Analyzed", df.shape[0])
    
    # Display raw data toggle
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Delivery Data")
        st.dataframe(df.head(10))

    # --- 3. Data Analysis & Text Reports ---
    st.header("Key Performance Metrics")
    
    # Creating 4 columns for top-level stats
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        avg_time = df['Delivery_Time'].mean()
        st.metric("Avg Delivery Time", f"{avg_time:.1f} min")
        
    with metric_col2:
        worst_traffic = df.groupby('Traffic')['Delivery_Time'].mean().idxmax()
        st.metric("Worst Traffic Condition", worst_traffic)
        
    with metric_col3:
        best_vehicle = df.groupby('Vehicle')['Delivery_Time'].mean().idxmin()
        st.metric("Fastest Vehicle Type", best_vehicle)
        
    with metric_col4:
        avg_rating = df['Agent_Rating'].mean()
        st.metric("Avg Agent Rating", f"{avg_rating:.1f} / 5.0")

    st.divider()

    # --- 4. Visualizations (2x2 Grid) ---
    st.header("Delivery Performance Visualizations")
    
    col1, col2 = st.columns(2)

    # Chart 1: Area Performance
    with col1:
        st.subheader("Average Delivery Time by Area")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='Area', y='Delivery_Time', data=df, hue='Area', palette='viridis', legend=False, ax=ax1)
        ax1.set_ylabel('Delivery Time (minutes)')
        st.pyplot(fig1)

    # Chart 2: Traffic Impact
    with col2:
        st.subheader("Impact of Traffic on Delivery Time")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        order = ['Jam', 'High', 'Medium', 'Low'] if 'Jam' in df['Traffic'].unique() else None
        sns.barplot(x='Traffic', y='Delivery_Time', data=df, hue='Traffic', palette='Reds_r', order=order, legend=False, ax=ax2)
        ax2.set_ylabel('Average Delivery Time (minutes)')
        ax2.set_xlabel('Traffic Condition')
        st.pyplot(fig2)

    # Chart 3: Vehicle Efficiency
    with col1:
        st.subheader("Efficiency: Delivery Time by Vehicle")
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.boxplot(x='Vehicle', y='Delivery_Time', data=df, hue='Vehicle', palette='Set2', legend=False, ax=ax3)
        ax3.set_ylabel('Delivery Time (minutes)')
        st.pyplot(fig3)

    # Chart 4: Agent Rating vs Time
    with col2:
        st.subheader("Agent Rating vs Delivery Time")
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x='Agent_Rating', y='Delivery_Time', data=df, alpha=0.5, color='blue', ax=ax4)
        ax4.set_xlabel('Agent Rating')
        ax4.set_ylabel('Delivery Time (minutes)')
        st.pyplot(fig4)