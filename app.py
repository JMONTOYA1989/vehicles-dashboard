import streamlit as st
import pandas as pd
import plotly.express as px

# Título principal
st.title("🚗 Vehicle Sales Dashboard")

st.markdown("""
This interactive dashboard allows you to explore vehicle listings data.
Use the filters on the sidebar to customize the analysis.
""")

# Cargar datos
df = pd.read_csv("vehicles_us.csv")

# Sidebar filters
st.sidebar.header("Filters")

price_range = st.sidebar.slider(
    "Select Price Range",
    int(df["price"].min()),
    int(df["price"].max()),
    (int(df["price"].min()), int(df["price"].max()))
)

odometer_range = st.sidebar.slider(
    "Select Odometer Range",
    int(df["odometer"].min()),
    int(df["odometer"].max()),
    (int(df["odometer"].min()), int(df["odometer"].max()))
)

vehicle_type = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
)

# Filtrar datos
filtered_df = df[
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1]) &
    (df["odometer"] >= odometer_range[0]) &
    (df["odometer"] <= odometer_range[1]) &
    (df["type"].isin(vehicle_type))
]

# Métricas principales
st.subheader("Key Metrics")

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Listings", len(filtered_df))
    col2.metric("Average Price", f"${int(filtered_df['price'].mean())}")
    col3.metric("Average Odometer", f"{int(filtered_df['odometer'].mean())} miles")

# Histograma
if st.checkbox("Show Price Distribution"):
    fig_hist = px.histogram(filtered_df, x="price", title="Price Distribution")
    st.plotly_chart(fig_hist)

# Scatter Plot
if st.checkbox("Show Price vs Odometer"):
    fig_scatter = px.scatter(
        filtered_df,
        x="odometer",
        y="price",
        title="Price vs Odometer",
        opacity=0.5
    )
    st.plotly_chart(fig_scatter)

if st.checkbox("Show Vehicle Type Distribution"):
    fig_type = px.histogram(filtered_df, x="type", title="Vehicle Type Distribution")
    st.plotly_chart(fig_type)

# Mostrar tabla
if st.checkbox("Show Data Table"):
    st.dataframe(
        filtered_df.sort_values(by="price", ascending=False),
        use_container_width=True
    )