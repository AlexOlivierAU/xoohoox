import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="XooHooX Logistics & Delivery Tracking",
    page_icon="🚛",
    layout="wide"
)

# Mock data for logistics tracking
MOCK_TRUCKS = [
    {
        "id": "T001",
        "name": "Sample Collection Truck 1",
        "driver": "John Smith",
        "status": "In Transit",
        "current_location": {"lat": -33.8688, "lng": 151.2093},  # Sydney
        "capacity": "500kg",
        "last_update": datetime.now() - timedelta(minutes=15)
    },
    {
        "id": "T002", 
        "name": "Sample Collection Truck 2",
        "driver": "Sarah Johnson",
        "status": "Loading",
        "current_location": {"lat": -37.8136, "lng": 144.9631},  # Melbourne
        "capacity": "500kg",
        "last_update": datetime.now() - timedelta(minutes=5)
    },
    {
        "id": "T003",
        "name": "Sample Collection Truck 3", 
        "driver": "Mike Wilson",
        "status": "Delivered",
        "current_location": {"lat": -31.9505, "lng": 115.8605},  # Perth
        "capacity": "500kg",
        "last_update": datetime.now() - timedelta(hours=2)
    }
]

MOCK_DELIVERIES = [
    {
        "id": "D001",
        "truck_id": "T001",
        "origin": "Hunter Valley Farm",
        "destination": "XooHooX Laboratory",
        "status": "In Transit",
        "samples": [
            {"id": "S001", "type": "Grapes", "weight": "50kg", "farm": "Hunter Valley"},
            {"id": "S002", "type": "Apples", "weight": "30kg", "farm": "Hunter Valley"}
        ],
        "estimated_arrival": datetime.now() + timedelta(hours=3),
        "start_time": datetime.now() - timedelta(hours=1)
    },
    {
        "id": "D002",
        "truck_id": "T002", 
        "origin": "Yarra Valley Farm",
        "destination": "XooHooX Laboratory",
        "status": "Loading",
        "samples": [
            {"id": "S003", "type": "Berries", "weight": "25kg", "farm": "Yarra Valley"},
            {"id": "S004", "type": "Citrus", "weight": "40kg", "farm": "Yarra Valley"}
        ],
        "estimated_arrival": datetime.now() + timedelta(hours=5),
        "start_time": datetime.now() - timedelta(minutes=30)
    },
    {
        "id": "D003",
        "truck_id": "T003",
        "origin": "Margaret River Farm", 
        "destination": "XooHooX Laboratory",
        "status": "Delivered",
        "samples": [
            {"id": "S005", "type": "Grapes", "weight": "60kg", "farm": "Margaret River"},
            {"id": "S006", "type": "Stone Fruit", "weight": "35kg", "farm": "Margaret River"}
        ],
        "estimated_arrival": datetime.now() - timedelta(hours=1),
        "start_time": datetime.now() - timedelta(hours=4)
    }
]

MOCK_WAYPOINTS = [
    {"lat": -33.8688, "lng": 151.2093, "name": "Sydney Hub", "type": "Collection Point"},
    {"lat": -37.8136, "lng": 144.9631, "name": "Melbourne Hub", "type": "Collection Point"},
    {"lat": -31.9505, "lng": 115.8605, "name": "Perth Hub", "type": "Collection Point"},
    {"lat": -34.9285, "lng": 138.6007, "name": "Adelaide Hub", "type": "Collection Point"},
    {"lat": -27.4698, "lng": 153.0251, "name": "Brisbane Hub", "type": "Collection Point"},
    {"lat": -35.2809, "lng": 149.1300, "name": "Canberra Laboratory", "type": "Destination"}
]

def create_logistics_map():
    """Create a map showing trucks, deliveries, and waypoints"""
    # Center on Australia
    m = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add waypoints
    for waypoint in MOCK_WAYPOINTS:
        color = "red" if waypoint["type"] == "Destination" else "blue"
        folium.Marker(
            location=[waypoint["lat"], waypoint["lng"]],
            popup=f"{waypoint['name']}<br>Type: {waypoint['type']}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # Add trucks
    for truck in MOCK_TRUCKS:
        status_colors = {
            "In Transit": "orange",
            "Loading": "yellow", 
            "Delivered": "green"
        }
        
        folium.Marker(
            location=[truck["current_location"]["lat"], truck["current_location"]["lng"]],
            popup=f"Truck {truck['id']}<br>Driver: {truck['driver']}<br>Status: {truck['status']}",
            icon=folium.Icon(color=status_colors.get(truck["status"], "gray"), icon='truck')
        ).add_to(m)
    
    return m

def create_delivery_timeline():
    """Create a timeline of deliveries"""
    timeline_data = []
    
    for delivery in MOCK_DELIVERIES:
        timeline_data.append({
            "Delivery ID": delivery["id"],
            "Origin": delivery["origin"],
            "Destination": delivery["destination"],
            "Status": delivery["status"],
            "Start Time": delivery["start_time"],
            "ETA": delivery["estimated_arrival"],
            "Samples": len(delivery["samples"])
        })
    
    df = pd.DataFrame(timeline_data)
    return df

def main():
    st.title("🚛 XooHooX Sample Collection & Delivery Tracking")
    st.markdown("### Real-time Research Sample Collection and Laboratory Delivery Monitoring")
    
    # Sidebar
    st.sidebar.header("📊 Quick Statistics")
    st.sidebar.metric("🚛 Active Collection Vehicles", len([t for t in MOCK_TRUCKS if t["status"] != "Delivered"]))
    st.sidebar.metric("🔄 Samples In Transit", len([d for d in MOCK_DELIVERIES if d["status"] == "In Transit"]))
    st.sidebar.metric("✅ Delivered Today", len([d for d in MOCK_DELIVERIES if d["status"] == "Delivered"]))
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Live Sample Collection Map")
        logistics_map = create_logistics_map()
        st_folium(logistics_map, width=700, height=500)
    
    with col2:
        st.subheader("📋 Active Sample Deliveries")
        for delivery in MOCK_DELIVERIES:
            if delivery["status"] != "Delivered":
                with st.expander(f"Delivery {delivery['id']} - {delivery['status']}"):
                    st.write(f"**Origin:** {delivery['origin']}")
                    st.write(f"**Destination:** {delivery['destination']}")
                    st.write(f"**ETA:** {delivery['estimated_arrival'].strftime('%H:%M')}")
                    st.write(f"**Samples:** {len(delivery['samples'])}")
                    
                    # Progress bar
                    if delivery["status"] == "In Transit":
                        elapsed = datetime.now() - delivery["start_time"]
                        total_time = delivery["estimated_arrival"] - delivery["start_time"]
                        progress = min(elapsed.total_seconds() / total_time.total_seconds(), 1.0)
                        st.progress(progress)
    
    # Delivery timeline
    st.subheader("📅 Sample Delivery Timeline")
    timeline_df = create_delivery_timeline()
    st.dataframe(timeline_df, use_container_width=True)
    
    # Sample tracking
    st.subheader("🧪 Research Sample Tracking")
    all_samples = []
    for delivery in MOCK_DELIVERIES:
        for sample in delivery["samples"]:
            all_samples.append({
                "Sample ID": sample["id"],
                "Type": sample["type"],
                "Weight": sample["weight"],
                "Farm": sample["farm"],
                "Delivery Status": delivery["status"]
            })
    
    samples_df = pd.DataFrame(all_samples)
    st.dataframe(samples_df, use_container_width=True)
    
    # Truck status
    st.subheader("🚛 Sample Collection Vehicle Status")
    for truck in MOCK_TRUCKS:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**{truck['id']}**")
        with col2:
            st.write(truck["driver"])
        with col3:
            status_color = {
                "In Transit": "🟠",
                "Loading": "🟡", 
                "Delivered": "🟢"
            }
            st.write(f"{status_color.get(truck['status'], '⚪')} {truck['status']}")
        with col4:
            st.write(truck["last_update"].strftime("%H:%M"))

if __name__ == "__main__":
    main()
