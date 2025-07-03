import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data
df = pd.read_csv('train.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Preprocessing
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['City'] = df['City'].str.strip()

# Sidebar Filters
st.sidebar.header("🔍 Optional Filters")
ship_mode = st.sidebar.selectbox("🚚 Ship Mode", ['All'] + sorted(df['Ship Mode'].unique()))
segment = st.sidebar.selectbox("👤 Segment", ['All'] + sorted(df['Segment'].unique()))
region = st.sidebar.selectbox("🌍 Region", ['All'] + sorted(df['Region'].unique()))
customer = st.sidebar.selectbox("🧾 Customer Name", ['All'] + sorted(df['Customer Name'].unique()))

# Apply Filters
filtered_df = df.copy()
if ship_mode != 'All':
    filtered_df = filtered_df[filtered_df['Ship Mode'] == ship_mode]
if segment != 'All':
    filtered_df = filtered_df[filtered_df['Segment'] == segment]
if region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == region]
if customer != 'All':
    filtered_df = filtered_df[filtered_df['Customer Name'] == customer]

# --- KPIs ---
total_sales = filtered_df['Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()
unique_customers = filtered_df['Customer ID'].nunique()
average_order_value = total_sales / total_orders if total_orders != 0 else 0

st.title("📊 Sales Dashboard")
st.subheader("📊 Key Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
rounded_sales = round(total_sales, -2)

kpi1.metric("💰 Total Sales", f"${rounded_sales:,.0f}")
kpi2.metric("📦 Total Orders", f"{total_orders:,}")
kpi3.metric("👥 Unique Customers", f"{unique_customers:,}")
kpi4.metric("🛒 Avg Order Value", f"${average_order_value:,.2f}")

# --- Top Products Table ---
top_products = (
    filtered_df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

st.subheader("📦 Top 5 Products by Sales")
if not top_products.empty:
    st.dataframe(top_products.style.format({"Sales": "${:,.2f}"}), use_container_width=True)
else:
    st.warning("No data found for the selected filters.")

    st.subheader("🏙️ Total Sales by City (in Thousands)")

sales_by_city = (
    filtered_df.groupby('City')['Sales']
    .sum()
    .reset_index()
)
st.subheader("🌍 Total Sales by Region (in Thousands)")

# Group by Region
sales_by_region = (
    filtered_df.groupby('Region')['Sales']
    .sum()
    .reset_index()
)

# Round Sales to nearest thousand
sales_by_region['Sales (K)'] = sales_by_region['Sales'].apply(lambda x: round(x / 1000))

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(sales_by_region['Region'], sales_by_region['Sales (K)'], color='teal')
ax.set_ylabel("Sales (in Thousands)")
ax.set_xlabel("Region")
ax.set_title("Total Sales by Region")
plt.xticks(rotation=0)

# Display in Streamlit
st.pyplot(fig)

