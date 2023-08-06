import dask
import dask.dataframe as dd
import folium
import streamlit as st
from dask.distributed import Client
from folium.plugins import HeatMap
from streamlit_folium import folium_static

import coiled

# Text in Streamlit
st.header("Coiled and Streamlit")
st.subheader("Analyzing Large Datasets with Coiled and Streamlit")
st.write(
    """
    The computations for this Streamlit app are powered by Coiled, which
    provides on-demand, hosted Dask clusters in the cloud. Change the options
    below to view different visualizations of transportation pickups/dropoffs,
    then let Coiled handle all of the infrastructure and compute.
    """
)

# Interactive widgets in Streamlit
taxi_mode = st.selectbox("Taxi pickup or dropoff?", ("Pickups", "Dropoffs"))
num_passengers = st.slider("Number of passengers", 0, 9, (0, 9))

# Start and connect to Coiled cluster
cluster_state = st.empty()


@st.cache(allow_output_mutation=True)
def get_client():
    cluster_state.write("Starting or connecting to Coiled cluster...")
    cluster = coiled.Cluster(n_workers=5, name="coiled-streamlit")
    client = Client(cluster)
    return client


client = get_client()
if client.status == "closed":
    # In a long-running Streamlit app,
    # the cluster could have shut down from idleness.
    # If so, clear the Streamlit cache to restart it.
    st.caching.clear_cache()
    client = get_client()
cluster_state.write(f"Coiled cluster is up! ({client.dashboard_link})")


# Load data (runs on Coiled)
@st.cache(hash_funcs={dd.DataFrame: dask.base.tokenize})
def load_data():
    return (
        dd.read_parquet(
            "s3://coiled-datasets/nyc-tlc/2019",
            usecols=[
                "passenger_count",
                "pickup_longitude",
                "pickup_latitude",
                "dropoff_longitude",
                "dropoff_latitude",
            ],
            storage_options={"anon": True},
            blocksize="16 MiB",
        )
        .dropna()
        .persist()
    )


df = load_data()

# Filter data based on inputs (runs on Coiled)
with st.spinner("Calculating map data..."):
    map_data = df[
        (df["passenger_count"] >= num_passengers[0])
        & (df["passenger_count"] <= num_passengers[1])
    ]

    if taxi_mode == "Pickups":
        map_data = map_data.iloc[:, [2, 1]]
    elif taxi_mode == "Dropoffs":
        map_data = map_data.iloc[:, [4, 3]]

    map_data.columns = ["lat", "lon"]
    map_data = map_data.loc[~(map_data == 0).all(axis=1)]
    map_data = map_data.head(500)

# Display map in Streamlit
st.subheader("Map of selected rides")
m = folium.Map([40.76, -73.95], tiles="cartodbpositron", zoom_start=12)
HeatMap(map_data).add_to(folium.FeatureGroup(name="Heat Map").add_to(m))
folium_static(m)
