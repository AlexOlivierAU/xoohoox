import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import numpy as np
from typing import List, Dict, Any


# Page configuration
st.set_page_config(
    page_title="XooHooX Australian Farm & Producer Tracking",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2E7D32;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .farm-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .farm-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .paddock-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border: 2px solid #4caf50;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .geofence-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .sample-collection {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .info-label {
        font-weight: 600;
        color: #2E7D32;
        margin-right: 0.5rem;
    }
    .info-value {
        color: #424242;
        font-weight: 500;
    }
    .status-active {
        color: #2E7D32;
        font-weight: 600;
        background-color: #C8E6C9;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
    }
    .status-pending {
        color: #F57C00;
        font-weight: 600;
        background-color: #FFE0B2;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
    }
    .status-completed {
        color: #1976D2;
        font-weight: 600;
        background-color: #BBDEFB;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Mock data functions
def get_australian_farms():
    return [
        {
            "farm_id": "FARM_001",
            "name": "Sunshine Citrus Farms",
            "farmer_name": "John Smith",
            "phone": "(03) 5023 1234",
            "email": "john@sunshinecitrus.com.au",
            "latitude": -34.2860,
            "longitude": 142.2630,
            "address": "123 Citrus Grove Rd, Mildura VIC 3500",
            "region": "Victoria",
            "total_paddocks": 8,
            "total_area_hectares": 120,
            "established": "2015",
            "certification": "Organic",
            "last_sample_collection": "2024-04-15"
        },
        {
            "farm_id": "FARM_002", 
            "name": "Golden Apple Orchards",
            "farmer_name": "Sarah Johnson",
            "phone": "(03) 6234 5678",
            "email": "sarah@goldenapple.com.au",
            "latitude": -43.0826,
            "longitude": 147.1277,
            "address": "456 Apple Valley Dr, Hobart TAS 7000",
            "region": "Tasmania",
            "total_paddocks": 12,
            "total_area_hectares": 85,
            "established": "2018",
            "certification": "HACCP",
            "last_sample_collection": "2024-04-14"
        },
        {
            "farm_id": "FARM_003",
            "name": "Tropical Fruit Paradise",
            "farmer_name": "Mike Wilson",
            "phone": "(07) 4031 2345",
            "email": "mike@tropicalfruit.com.au",
            "latitude": -17.1191,
            "longitude": 145.6786,
            "address": "789 Mango Lane, Cairns QLD 4870",
            "region": "Queensland",
            "total_paddocks": 6,
            "total_area_hectares": 65,
            "established": "2020",
            "certification": "GAP",
            "last_sample_collection": "2024-04-13"
        },
        {
            "farm_id": "FARM_004",
            "name": "Riverland Vineyards",
            "farmer_name": "Emma Davis",
            "phone": "(08) 8582 3456",
            "email": "emma@riverland.com.au",
            "latitude": -34.1761,
            "longitude": 140.7472,
            "address": "321 River Rd, Berri SA 5343",
            "region": "South Australia",
            "total_paddocks": 15,
            "total_area_hectares": 200,
            "established": "2012",
            "certification": "Organic",
            "last_sample_collection": "2024-04-12"
        },
        {
            "farm_id": "FARM_005",
            "name": "Western Orchard Co",
            "farmer_name": "David Brown",
            "phone": "(08) 9250 4567",
            "email": "david@westernorchard.com.au",
            "latitude": -31.9522,
            "longitude": 115.8589,
            "address": "654 Orchard Way, Perth WA 6000",
            "region": "Western Australia",
            "total_paddocks": 10,
            "total_area_hectares": 95,
            "established": "2016",
            "certification": "HACCP",
            "last_sample_collection": "2024-04-11"
        }
    ]

def get_mock_paddocks():
    return [
        {
            "paddock_id": "PADDOCK_001",
            "farm_id": "FARM_001",
            "name": "Orange Grove A",
            "fruit_type": "Orange",
            "area_hectares": 15,
            "latitude": -34.2860,
            "longitude": 142.2630,
            "planting_date": "2015-03-15",
            "last_harvest": "2024-04-10",
            "yield_kg": 2500,
            "soil_type": "Sandy Loam",
            "irrigation": "Drip",
            "status": "Active"
        },
        {
            "paddock_id": "PADDOCK_002",
            "farm_id": "FARM_001", 
            "name": "Lemon Grove B",
            "fruit_type": "Lemon",
            "area_hectares": 12,
            "latitude": -34.2960,
            "longitude": 142.2730,
            "planting_date": "2016-08-20",
            "last_harvest": "2024-04-12",
            "yield_kg": 1800,
            "soil_type": "Clay Loam",
            "irrigation": "Sprinkler",
            "status": "Active"
        },
        {
            "paddock_id": "PADDOCK_003",
            "farm_id": "FARM_002",
            "name": "Apple Orchard North",
            "fruit_type": "Apple",
            "area_hectares": 20,
            "latitude": -43.0826,
            "longitude": 147.1277,
            "planting_date": "2018-04-10",
            "last_harvest": "2024-04-08",
            "yield_kg": 3200,
            "soil_type": "Volcanic",
            "irrigation": "Drip",
            "status": "Active"
        },
        {
            "paddock_id": "PADDOCK_004",
            "farm_id": "FARM_003",
            "name": "Mango Plantation East",
            "fruit_type": "Mango",
            "area_hectares": 25,
            "latitude": -17.1191,
            "longitude": 145.6786,
            "planting_date": "2020-11-05",
            "last_harvest": "2024-04-05",
            "yield_kg": 4100,
            "soil_type": "Tropical",
            "irrigation": "Flood",
            "status": "Active"
        },
        {
            "paddock_id": "PADDOCK_005",
            "farm_id": "FARM_004",
            "name": "Grape Vineyard South",
            "fruit_type": "Grape",
            "area_hectares": 30,
            "latitude": -34.1761,
            "longitude": 140.7472,
            "planting_date": "2012-09-15",
            "last_harvest": "2024-04-03",
            "yield_kg": 5500,
            "soil_type": "River Loam",
            "irrigation": "Drip",
            "status": "Active"
        }
    ]

def get_mock_geofences():
    return [
        {
            "geofence_id": "GEO_001",
            "farm_id": "FARM_001",
            "name": "Sample Archive Zone",
            "type": "archive",
            "coordinates": [
                [-34.2860, 142.2630],
                [-34.2860, 142.2730],
                [-34.2960, 142.2730],
                [-34.2960, 142.2630]
            ],
            "radius_meters": 500,
            "status": "active",
            "alerts_enabled": True,
            "description": "Laboratory sample archive storage area"
        },
        {
            "geofence_id": "GEO_002",
            "farm_id": "FARM_002",
            "name": "Laboratory Processing Zone",
            "type": "processing",
            "coordinates": [
                [-43.0826, 147.1277],
                [-43.0826, 147.1377],
                [-43.0926, 147.1377],
                [-43.0926, 147.1277]
            ],
            "radius_meters": 300,
            "status": "active",
            "alerts_enabled": True,
            "description": "Sample processing and analysis area"
        },
        {
            "geofence_id": "GEO_003",
            "farm_id": "FARM_003",
            "name": "Quality Control Zone",
            "type": "quality",
            "coordinates": [
                [-17.1191, 145.6786],
                [-17.1191, 145.6886],
                [-17.1291, 145.6886],
                [-17.1291, 145.6786]
            ],
            "radius_meters": 400,
            "status": "active",
            "alerts_enabled": True,
            "description": "Quality control and testing area"
        }
    ]

def get_mock_harvests():
    return [
        {
            "harvest_id": "HARVEST_001",
            "paddock_id": "PADDOCK_001",
            "farm_id": "FARM_001",
            "batch_id": "BATCH_001",
            "fruit_type": "Orange",
            "harvest_date": "2024-04-10",
            "quantity_kg": 2500,
            "harvest_method": "mechanical",
            "weather_conditions": "Sunny, 25°C",
            "quality_score": 8.5,
            "sample_collected": True,
            "sample_id": "SAMPLE_001",
            "notes": "Excellent quality oranges, ready for laboratory analysis"
        },
        {
            "harvest_id": "HARVEST_002",
            "paddock_id": "PADDOCK_002",
            "farm_id": "FARM_001",
            "batch_id": "BATCH_002",
            "fruit_type": "Lemon",
            "harvest_date": "2024-04-12",
            "quantity_kg": 1800,
            "harvest_method": "manual",
            "weather_conditions": "Partly cloudy, 22°C",
            "quality_score": 8.2,
            "sample_collected": True,
            "sample_id": "SAMPLE_002",
            "notes": "Good quality lemons, suitable for research samples"
        },
        {
            "harvest_id": "HARVEST_003",
            "paddock_id": "PADDOCK_003",
            "farm_id": "FARM_002",
            "batch_id": "BATCH_003",
            "fruit_type": "Apple",
            "harvest_date": "2024-04-08",
            "quantity_kg": 3200,
            "harvest_method": "mechanical",
            "weather_conditions": "Rainy, 18°C",
            "quality_score": 7.8,
            "sample_collected": True,
            "sample_id": "SAMPLE_003",
            "notes": "Apples collected in wet conditions, extra care needed"
        },
        {
            "harvest_id": "HARVEST_004",
            "paddock_id": "PADDOCK_004",
            "farm_id": "FARM_003",
            "batch_id": "BATCH_004",
            "fruit_type": "Mango",
            "harvest_date": "2024-04-05",
            "quantity_kg": 4100,
            "harvest_method": "manual",
            "weather_conditions": "Hot, 32°C",
            "quality_score": 9.1,
            "sample_collected": True,
            "sample_id": "SAMPLE_004",
            "notes": "Premium quality mangoes, perfect for laboratory research"
        },
        {
            "harvest_id": "HARVEST_005",
            "paddock_id": "PADDOCK_005",
            "farm_id": "FARM_004",
            "batch_id": "BATCH_005",
            "fruit_type": "Grape",
            "harvest_date": "2024-04-03",
            "quantity_kg": 5500,
            "harvest_method": "mechanical",
            "weather_conditions": "Mild, 24°C",
            "quality_score": 8.7,
            "sample_collected": True,
            "sample_id": "SAMPLE_005",
            "notes": "Excellent grape harvest, ideal for fermentation research"
        }
    ]

def get_mock_location_tracking():
    return [
        {
            "tracking_id": "TRACK_001",
            "batch_id": "BATCH_001",
            "latitude": -34.2860,
            "longitude": 142.2630,
            "timestamp": "2024-04-15T14:30:00",
            "location_name": "Mildura Farm",
            "status": "Sample collected",
            "source": "GPS"
        },
        {
            "tracking_id": "TRACK_002",
            "batch_id": "BATCH_001",
            "latitude": -36.7578,
            "longitude": 144.2789,
            "timestamp": "2024-04-15T16:45:00",
            "location_name": "Bendigo Transit",
            "status": "In transit to laboratory",
            "source": "GPS"
        },
        {
            "tracking_id": "TRACK_003",
            "batch_id": "BATCH_001",
            "latitude": -37.8136,
            "longitude": 144.9631,
            "timestamp": "2024-04-15T18:20:00",
            "location_name": "Melbourne Laboratory",
            "status": "Delivered to laboratory",
            "source": "GPS"
        },
        {
            "tracking_id": "TRACK_004",
            "batch_id": "BATCH_002",
            "latitude": -34.2960,
            "longitude": 142.2730,
            "timestamp": "2024-04-15T15:15:00",
            "location_name": "Mildura Farm",
            "status": "Sample collected",
            "source": "GPS"
        },
        {
            "tracking_id": "TRACK_005",
            "batch_id": "BATCH_003",
            "latitude": -43.0826,
            "longitude": 147.1277,
            "timestamp": "2024-04-15T13:45:00",
            "location_name": "Hobart Farm",
            "status": "Sample collected",
            "source": "GPS"
        }
    ]

def create_farm_map(farms, paddocks, geofences):
    """Create an interactive farm map"""
    # Center on Australia
    m = folium.Map(
        location=[-25.2744, 133.7751],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add farm markers
    for farm in farms:
        folium.Marker(
            [farm["latitude"], farm["longitude"]],
            popup=f"""
            <div style="min-width: 200px;">
                <h4 style="color: #2E7D32; margin: 0 0 10px 0;">🏡 {farm['name']}</h4>
                <p style="margin: 5px 0;"><strong>👨‍🌾 Producer:</strong> {farm['farmer_name']}</p>
                <p style="margin: 5px 0;"><strong>🌍 Region:</strong> {farm['region']}</p>
                <p style="margin: 5px 0;"><strong>🌱 Production Zones:</strong> {farm['total_paddocks']}</p>
                <p style="margin: 5px 0;"><strong>📏 Total Area:</strong> {farm['total_area_hectares']} ha</p>
                <p style="margin: 5px 0;"><strong>🏆 Certification:</strong> {farm['certification']}</p>
            </div>
            """,
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(m)
    
    # Add paddock markers
    for paddock in paddocks:
        folium.CircleMarker(
            [paddock["latitude"], paddock["longitude"]],
            radius=8,
            popup=f"""
            <div style="min-width: 180px;">
                <h4 style="color: #1976D2; margin: 0 0 10px 0;">🌱 {paddock['name']}</h4>
                <p style="margin: 5px 0;"><strong>🍎 Crop Type:</strong> {paddock['fruit_type']}</p>
                <p style="margin: 5px 0;"><strong>📏 Production Area:</strong> {paddock['area_hectares']} ha</p>
                <p style="margin: 5px 0;"><strong>📊 Harvest Yield:</strong> {paddock['yield_kg']} kg</p>
                <p style="margin: 5px 0;"><strong>📈 Status:</strong> {paddock['status']}</p>
            </div>
            """,
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.7
        ).add_to(m)
    
    # Add geofence polygons
    for geofence in geofences:
        folium.Polygon(
            locations=geofence["coordinates"],
            popup=f"""
            <div style="min-width: 200px;">
                <h4 style="color: #D32F2F; margin: 0 0 10px 0;">🚨 {geofence['name']}</h4>
                <p style="margin: 5px 0;"><strong>🔍 Monitoring Type:</strong> {geofence['type']}</p>
                <p style="margin: 5px 0;"><strong>📊 Status:</strong> {geofence['status']}</p>
                <p style="margin: 5px 0;"><strong>📝 Description:</strong> {geofence['description']}</p>
            </div>
            """,
            color='red',
            weight=2,
            fill=True,
            fillColor='red',
            fillOpacity=0.2
        ).add_to(m)
    
    return m

def main():
    st.markdown('<h1 class="main-header">🌾 XooHooX Australian Farm & Producer Tracking</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 🧭 Navigation")
    page = st.sidebar.selectbox(
        "📋 Choose Dashboard Section",
        ["Farm Overview", "Batch Tracking", "Geofence Alerts", "Sample Collection"]
    )
    
    # Load data
    farms = get_australian_farms()
    paddocks = get_mock_paddocks()
    geofences = get_mock_geofences()
    harvests = get_mock_harvests()
    location_tracking = get_mock_location_tracking()
    
    # Farm selection
    farm_names = [farm["name"] for farm in farms]
    selected_farm = st.sidebar.selectbox("🏡 Select Farm or Producer", ["All Farms"] + farm_names)
    
    if page == "Farm Overview":
        st.markdown('<h2 class="section-header">🏡 Farm & Producer Overview</h2>', unsafe_allow_html=True)
        
        # Metrics with better labels
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_farms = len(farms)
            st.metric("🏭 Active Farms & Producers", total_farms, help="Total number of participating farms and producers")
        
        with col2:
            total_paddocks = len(paddocks)
            st.metric("🌱 Production Zones", total_paddocks, help="Total number of production and collection zones")
        
        with col3:
            total_samples = len(harvests)
            st.metric("🍎 Samples Collected", total_samples, help="Total samples collected from farms")
        
        with col4:
            total_weight = sum(h["quantity_kg"] for h in harvests)
            st.metric("⚖️ Total Sample Weight", f"{total_weight:,} kg", help="Combined weight of all collected samples")
        
        # Interactive map
        st.markdown('<h3 class="section-header">🗺️ Farm & Producer Locations</h3>', unsafe_allow_html=True)
        farm_map = create_farm_map(farms, paddocks, geofences)
        st_folium(farm_map, width=800, height=600)
        
        # Farm details
        st.markdown('<h3 class="section-header">🏡 Farm & Producer Details</h3>', unsafe_allow_html=True)
        
        # Filter farms if selected
        display_farms = farms
        if selected_farm != "All Farms":
            display_farms = [f for f in farms if f["name"] == selected_farm]
        
        for farm in display_farms:
            st.markdown(f"""
            <div class="farm-card">
                <h4 style="color: #2E7D32; margin-bottom: 1rem;">🏡 {farm['name']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p><span class="info-label">👨‍🌾 Primary Contact:</span><br><span class="info-value">{farm['farmer_name']}</span></p>
                        <p><span class="info-label">📞 Phone:</span><br><span class="info-value">{farm['phone']}</span></p>
                        <p><span class="info-label">📧 Email:</span><br><span class="info-value">{farm['email']}</span></p>
                        <p><span class="info-label">📍 Address:</span><br><span class="info-value">{farm['address']}</span></p>
                    </div>
                    <div>
                        <p><span class="info-label">🌍 Region:</span><br><span class="info-value">{farm['region']}</span></p>
                        <p><span class="info-label">🌱 Production Zones:</span><br><span class="info-value">{farm['total_paddocks']} active zones</span></p>
                        <p><span class="info-label">📏 Total Area:</span><br><span class="info-value">{farm['total_area_hectares']} hectares</span></p>
                        <p><span class="info-label">🏆 Certification:</span><br><span class="info-value">{farm['certification']}</span></p>
                        <p><span class="info-label">📅 Last Sample Collection:</span><br><span class="info-value">{farm['last_sample_collection']}</span></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Paddock details
        st.markdown('<h3 class="section-header">🌱 Production Zone Details</h3>', unsafe_allow_html=True)
        
        # Filter paddocks if farm selected
        display_paddocks = paddocks
        if selected_farm != "All Farms":
            farm_id = next(f["farm_id"] for f in farms if f["name"] == selected_farm)
            display_paddocks = [p for p in paddocks if p["farm_id"] == farm_id]
        
        for paddock in display_paddocks:
            # Determine status class
            status_class = "status-active" if "active" in paddock['status'].lower() else "status-pending" if "pending" in paddock['status'].lower() else "status-completed"
            
            st.markdown(f"""
            <div class="paddock-card">
                <h4 style="color: #2E7D32; margin-bottom: 1rem;">🌱 {paddock['name']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <p><span class="info-label">🍎 Crop Type:</span><br><span class="info-value">{paddock['fruit_type']}</span></p>
                        <p><span class="info-label">📏 Production Area:</span><br><span class="info-value">{paddock['area_hectares']} hectares</span></p>
                        <p><span class="info-label">📊 Harvest Yield:</span><br><span class="info-value">{paddock['yield_kg']} kg</span></p>
                        <p><span class="info-label">🌱 Soil Composition:</span><br><span class="info-value">{paddock['soil_type']}</span></p>
                    </div>
                    <div>
                        <p><span class="info-label">💧 Water Management:</span><br><span class="info-value">{paddock['irrigation']}</span></p>
                        <p><span class="info-label">📅 Last Harvest:</span><br><span class="info-value">{paddock['last_harvest']}</span></p>
                        <p><span class="info-label">📈 Production Status:</span><br><span class="{status_class}">{paddock['status']}</span></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "Batch Tracking":
        st.markdown('<h2 class="section-header">📦 Sample Collection Tracking</h2>', unsafe_allow_html=True)
        
        # Batch metrics with better labels
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_batches = len(harvests)
            st.metric("🍎 Total Samples Collected", total_batches, help="Total number of samples collected from farms")
        
        with col2:
            active_batches = len([h for h in harvests if h["sample_collected"]])
            st.metric("🔄 Active Collections", active_batches, help="Samples currently being collected")
        
        with col3:
            avg_quality = sum(h["quality_score"] for h in harvests) / len(harvests)
            st.metric("⭐ Average Quality Score", f"{avg_quality:.1f}/10", help="Average quality rating of all collected samples")
        
        # Batch tracking map
        st.markdown('<h3 class="section-header">📍 Sample Collection Movement</h3>', unsafe_allow_html=True)
        
        # Create tracking map
        tracking_map = folium.Map(
            location=[-25.2744, 133.7751],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add tracking points
        for track in location_tracking:
            folium.Marker(
                [track["latitude"], track["longitude"]],
                popup=f"""
                <b>Batch {track['batch_id']}</b><br>
                Location: {track['location_name']}<br>
                Status: {track['status']}<br>
                Time: {track['timestamp'][:16]}
                """,
                icon=folium.Icon(color='orange', icon='info-sign')
            ).add_to(tracking_map)
        
        st_folium(tracking_map, width=800, height=600)
        
        # Batch details
        st.subheader("📋 Research Batch Details")
        
        # Filter batches if farm selected
        display_harvests = harvests
        if selected_farm != "All Farms":
            farm_id = next(f["farm_id"] for f in farms if f["name"] == selected_farm)
            display_harvests = [h for h in harvests if h["farm_id"] == farm_id]
        
        for harvest in display_harvests:
            st.markdown(f"""
            <div class="sample-collection">
                <h4>🧪 Batch {harvest['batch_id']}</h4>
                <p><strong>Fruit Type:</strong> {harvest['fruit_type']}</p>
                <p><strong>Harvest Date:</strong> {harvest['harvest_date']}</p>
                <p><strong>Quantity:</strong> {harvest['quantity_kg']} kg</p>
                <p><strong>Quality Score:</strong> {harvest['quality_score']}/10</p>
                <p><strong>Sample ID:</strong> {harvest['sample_id']}</p>
                <p><strong>Weather:</strong> {harvest['weather_conditions']}</p>
                <p><strong>Notes:</strong> {harvest['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "Geofence Alerts":
        st.header("🚨 Laboratory Zone Alerts")
        
        # Geofence metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_geofences = len(geofences)
            st.metric("Total Zones", total_geofences)
        
        with col2:
            active_geofences = len([g for g in geofences if g["status"] == "active"])
            st.metric("Active Zones", active_geofences)
        
        with col3:
            alerts_enabled = len([g for g in geofences if g["alerts_enabled"]])
            st.metric("Alerts Enabled", alerts_enabled)
        
        # Geofence map
        st.subheader("🗺️ Laboratory Zone Map")
        
        # Create geofence map
        geofence_map = folium.Map(
            location=[-25.2744, 133.7751],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add geofences
        for geofence in geofences:
            folium.Polygon(
                locations=geofence["coordinates"],
                popup=f"""
                <b>{geofence['name']}</b><br>
                Type: {geofence['type']}<br>
                Status: {geofence['status']}<br>
                Alerts: {'Enabled' if geofence['alerts_enabled'] else 'Disabled'}<br>
                {geofence['description']}
                """,
                color='red',
                weight=3,
                fill=True,
                fillColor='red',
                fillOpacity=0.3
            ).add_to(geofence_map)
        
        st_folium(geofence_map, width=800, height=600)
        
        # Geofence details
        st.subheader("🔍 Laboratory Zone Details")
        
        # Filter geofences if farm selected
        display_geofences = geofences
        if selected_farm != "All Farms":
            farm_id = next(f["farm_id"] for f in farms if f["name"] == selected_farm)
            display_geofences = [g for g in geofences if g["farm_id"] == farm_id]
        
        for geofence in display_geofences:
            st.markdown(f"""
            <div class="geofence-alert">
                <h4>🚨 {geofence['name']}</h4>
                <p><strong>Type:</strong> {geofence['type']}</p>
                <p><strong>Status:</strong> {geofence['status']}</p>
                <p><strong>Alerts:</strong> {'Enabled' if geofence['alerts_enabled'] else 'Disabled'}</p>
                <p><strong>Radius:</strong> {geofence['radius_meters']} meters</p>
                <p><strong>Description:</strong> {geofence['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "Sample Collection":
        st.header("🧪 Research Sample Collection")
        
        # Sample metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_samples = len(harvests)
            st.metric("Total Samples Collected", total_samples)
        
        with col2:
            sample_types = len(set(h["fruit_type"] for h in harvests))
            st.metric("Sample Types", sample_types)
        
        with col3:
            total_weight = sum(h["quantity_kg"] for h in harvests)
            st.metric("Total Weight (kg)", f"{total_weight:,}")
        
        with col4:
            avg_quality = sum(h["quality_score"] for h in harvests) / len(harvests)
            st.metric("Avg Quality Score", f"{avg_quality:.1f}")
        
        # Sample collection charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧪 Research Samples by Fruit Type")
            fruit_counts = pd.DataFrame([
                {"Fruit Type": h["fruit_type"], "Count": 1} for h in harvests
            ]).groupby("Fruit Type").sum().reset_index()
            
            fig = px.pie(
                fruit_counts,
                values="Count",
                names="Fruit Type",
                title="Sample Distribution by Fruit Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🧪 Research Samples by Australian Region")
            region_data = []
            for harvest in harvests:
                farm = next(f for f in farms if f["farm_id"] == harvest["farm_id"])
                region_data.append({
                    "Region": farm["region"],
                    "Weight": harvest["quantity_kg"]
                })
            
            region_df = pd.DataFrame(region_data)
            region_counts = region_df.groupby("Region")["Weight"].sum().reset_index()
            
            fig = px.bar(
                region_counts,
                x="Region",
                y="Weight",
                title="Sample Weight by Australian Region"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Weather conditions chart
        st.subheader("🌤️ Weather Conditions During Sample Collection")
        
        weather_data = {
            "Date": [h["harvest_date"] for h in harvests],
            "Temperature": [25, 22, 18, 32, 24],  # Mock temperatures
            "Conditions": ["Sunny", "Partly cloudy", "Rainy", "Hot", "Mild"]
        }
        
        weather_df = pd.DataFrame(weather_data)
        fig = px.line(
            weather_df,
            x="Date",
            y="Temperature",
            title="Temperature During Sample Collection",
            labels={"Temperature": "Temperature (°C)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent collections
        st.subheader("📋 Recent Collections")
        
        # Filter harvests if farm selected
        display_harvests = harvests
        if selected_farm != "All Farms":
            farm_id = next(f["farm_id"] for f in farms if f["name"] == selected_farm)
            display_harvests = [h for h in harvests if h["farm_id"] == farm_id]
        
        for harvest in display_harvests:
            st.markdown(f"""
            <div class="sample-collection">
                <h4>🧪 Sample {harvest['sample_id']}</h4>
                <p><strong>Batch:</strong> {harvest['batch_id']}</p>
                <p><strong>Fruit Type:</strong> {harvest['fruit_type']}</p>
                <p><strong>Collection Date:</strong> {harvest['harvest_date']}</p>
                <p><strong>Quantity:</strong> {harvest['quantity_kg']} kg</p>
                <p><strong>Quality Score:</strong> {harvest['quality_score']}/10</p>
                <p><strong>Weather Conditions:</strong> {harvest['weather_conditions']}</p>
                <p><strong>Notes:</strong> {harvest['notes']}</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
