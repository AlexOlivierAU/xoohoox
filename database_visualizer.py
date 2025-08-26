import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
import psycopg2
from psycopg2.extras import RealDictCursor
import networkx as nx
from collections import defaultdict
import json

# Page configuration
st.set_page_config(
    page_title="XooHooX Distillation Database Visualizer",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    .table-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_database_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="xoohoox",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_database_stats():
    """Get database statistics"""
    conn = get_database_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get table counts
            cur.execute("""
                SELECT COUNT(*) as table_count 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cur.fetchone()['table_count']
            
            # Get field count
            cur.execute("""
                SELECT COUNT(*) as field_count 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
            """)
            field_count = cur.fetchone()['field_count']
            
            # Get enum count
            cur.execute("""
                SELECT COUNT(*) as enum_count 
                FROM pg_type 
                WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public') 
                AND typtype = 'e'
            """)
            enum_count = cur.fetchone()['enum_count']
            
            return {
                'tables': table_count,
                'fields': field_count,
                'enums': enum_count
            }
    except Exception as e:
        st.error(f"Error getting database stats: {e}")
        return None

def get_tables_with_field_counts():
    """Get all tables with their field counts"""
    conn = get_database_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                table_name,
                COUNT(*) as field_count,
                CASE 
                    WHEN table_name LIKE '%batch%' THEN 'Core Production'
                    WHEN table_name LIKE '%result%' THEN 'Process Results'
                    WHEN table_name LIKE '%quality%' OR table_name LIKE '%eval%' THEN 'Quality & Evaluation'
                    WHEN table_name LIKE '%equipment%' OR table_name LIKE '%maintenance%' THEN 'Equipment & Maintenance'
                    WHEN table_name LIKE '%inventory%' THEN 'Inventory & Management'
                    WHEN table_name LIKE '%plan%' OR table_name LIKE '%kinetic%' THEN 'Planning & Kinetics'
                    WHEN table_name LIKE '%log%' THEN 'Logs & Tracking'
                    ELSE 'Other'
                END as category
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            GROUP BY table_name
            ORDER BY field_count DESC
        """
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error getting tables: {e}")
        return pd.DataFrame()

def get_foreign_key_relationships():
    """Get foreign key relationships"""
    conn = get_database_connection()
    if not conn:
        return []
    
    try:
        query = """
            SELECT 
                tc.table_name as source_table,
                kcu.column_name as source_column,
                ccu.table_name as target_table,
                ccu.column_name as target_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu 
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public'
            ORDER BY tc.table_name, kcu.column_name
        """
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error getting relationships: {e}")
        return pd.DataFrame()

def create_interactive_graph():
    """Create interactive network graph"""
    tables_df = get_tables_with_field_counts()
    relationships_df = get_foreign_key_relationships()
    
    if tables_df.empty or relationships_df.empty:
        st.error("No data available for graph visualization")
        return
    
    # Create nodes
    nodes = []
    node_colors = {
        'Core Production': '#FF6B35',
        'Process Results': '#4ECDC4',
        'Quality & Evaluation': '#45B7D1',
        'Equipment & Maintenance': '#96CEB4',
        'Inventory & Management': '#FFEAA7',
        'Planning & Kinetics': '#DDA0DD',
        'Logs & Tracking': '#98D8C8',
        'Other': '#F7DC6F'
    }
    
    for _, row in tables_df.iterrows():
        # Create shorter labels for better readability
        short_label = row['table_name'].replace('_', '\n').replace('batch', 'b').replace('fermentation', 'ferm').replace('transformation', 'trans')
        short_label = short_label.replace('results', 'res').replace('quality', 'qual').replace('equipment', 'equip')
        short_label = short_label.replace('maintenance', 'maint').replace('inventory', 'inv').replace('evaluation', 'eval')
        
        nodes.append(
            Node(
                id=row['table_name'],
                label=short_label,
                size=min(20, max(8, row['field_count'] * 1.5)),  # Smaller size range
                color=node_colors.get(row['category'], '#F7DC6F'),
                title=f"{row['table_name']} - {row['field_count']} fields - {row['category']}",  # Clean title without HTML
                font={'size': 10, 'color': '#333333'}  # Smaller font size
            )
        )
    
    # Create edges
    edges = []
    for _, row in relationships_df.iterrows():
        edges.append(
            Edge(
                source=row['source_table'],
                target=row['target_table'],
                label=f"{row['source_column']} → {row['target_column']}",
                color="#666666",
                width=2
            )
        )
    
    # Graph configuration
    config = Config(
        height=800,
        width=1200,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=True,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': False},  # Hide edge labels for cleaner look
        physics_config={
            'forceAtlas2Based': {
                'gravitationalConstant': -50,
                'centralGravity': 0.01,
                'springLength': 100,
                'springConstant': 0.08,
                'damping': 0.4
            }
        },
        # Prevent navigation on double-click
        interaction={
            'navigationButtons': False,
            'keyboard': False,
            'hover': True,
            'tooltipDelay': 200
        }
    )
    
    return agraph(nodes=nodes, edges=edges, config=config)

def create_plotly_network():
    """Create Plotly network graph"""
    tables_df = get_tables_with_field_counts()
    relationships_df = get_foreign_key_relationships()
    
    if tables_df.empty or relationships_df.empty:
        st.error("No data available for graph visualization")
        return
    
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes
    for _, row in tables_df.iterrows():
        G.add_node(row['table_name'], 
                  field_count=row['field_count'], 
                  category=row['category'])
    
    # Add edges
    for _, row in relationships_df.iterrows():
        G.add_edge(row['source_table'], row['target_table'], 
                  label=f"{row['source_column']} → {row['target_column']}")
    
    # Position nodes using spring layout
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(edge[2].get('label', ''))
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='text',
        mode='lines',
        text=edge_text,
        showlegend=False
    )
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        field_count = G.nodes[node]['field_count']
        category = G.nodes[node]['category']
        
        node_text.append(f"{node}<br>Fields: {field_count}<br>Category: {category}")
        node_sizes.append(min(30, max(10, field_count * 2)))
        
        # Color by category
        color_map = {
            'Core Production': '#FF6B35',
            'Process Results': '#4ECDC4',
            'Quality & Evaluation': '#45B7D1',
            'Equipment & Maintenance': '#96CEB4',
            'Inventory & Management': '#FFEAA7',
            'Planning & Kinetics': '#DDA0DD',
            'Logs & Tracking': '#98D8C8',
            'Other': '#F7DC6F'
        }
        node_colors.append(color_map.get(category, '#F7DC6F'))
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[node.split('_')[0] for node in G.nodes()],  # Short names
        textposition="middle center",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white'),
            showscale=False
        ),
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=dict(
                           text='XooHooX Database Relationships',
                           font=dict(size=16)
                       ),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='white'
                   ))
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🍊 XooHooX Distillation Database Visualizer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Visualization Options")
    viz_type = st.sidebar.selectbox(
        "Choose Visualization Type",
        ["Interactive Network Graph", "Plotly Network Graph", "Table Overview", "Statistics Dashboard"]
    )
    
    # Get database stats
    stats = get_database_stats()
    
    if viz_type == "Statistics Dashboard":
        st.header("📊 Database Statistics")
        
        if stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📋 Tables", stats['tables'])
            
            with col2:
                st.metric("🔢 Fields", stats['fields'])
            
            with col3:
                st.metric("🎯 Enum Types", stats['enums'])
            
            st.success("✅ Database connection successful!")
        else:
            st.error("❌ Unable to connect to database")
    
    elif viz_type == "Table Overview":
        st.header("📋 Database Tables Overview")
        
        tables_df = get_tables_with_field_counts()
        if not tables_df.empty:
            # Category summary
            category_summary = tables_df.groupby('category').agg({
                'table_name': 'count',
                'field_count': 'sum'
            }).rename(columns={'table_name': 'Table Count', 'field_count': 'Total Fields'})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Tables by Category")
                st.dataframe(category_summary, use_container_width=True)
            
            with col2:
                st.subheader("📈 Field Distribution")
                fig = px.pie(tables_df, values='field_count', names='category', 
                           title='Fields by Category')
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table list
            st.subheader("📋 All Tables")
            st.dataframe(tables_df, use_container_width=True)
        else:
            st.error("No table data available")
    
    elif viz_type == "Interactive Network Graph":
        st.header("🔗 Interactive Database Relationships")
        st.info("💡 Drag nodes to rearrange, zoom in/out, and hover for details")
        
        # Create the interactive graph
        create_interactive_graph()
        
        # Add relationship details
        st.subheader("🔗 Foreign Key Relationships")
        relationships_df = get_foreign_key_relationships()
        if not relationships_df.empty:
            st.dataframe(relationships_df, use_container_width=True)
    
    elif viz_type == "Plotly Network Graph":
        st.header("🔗 Plotly Network Graph")
        st.info("💡 Interactive graph with hover details and zoom capabilities")
        
        # Create Plotly network
        fig = create_plotly_network()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🍊 XooHooX Distillation Database Visualizer | 41 Tables | 553 Fields | 14 Enum Types</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
