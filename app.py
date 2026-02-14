import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from supabase import create_client, Client
import os
import dotenv

# Page configuration with custom theme
st.set_page_config(
    page_title="Handball Goalkeeper Stats", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inconsolata:wght@400;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-red: #E63946;
        --dark-blue: #1D3557;
        --light-blue: #457B9D;
        --cream: #F1FAEE;
        --accent-yellow: #FFB703;
    }
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #1D3557 0%, #0D1B2A 100%);
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        font-family: 'Bebas Neue', sans-serif !important;
        color: #FFB703 !important;
        font-size: 4rem !important;
        letter-spacing: 4px !important;
        text-transform: uppercase !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 0 !important;
        background: linear-gradient(45deg, #FFB703, #E63946);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        color: #F1FAEE !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
        border-bottom: 3px solid #E63946;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.8rem !important;
        color: #FFB703 !important;
    }
    
    /* Stat boxes */
    [data-testid="stMetricValue"] {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 3rem !important;
        color: #FFB703 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inconsolata', monospace !important;
        font-size: 1rem !important;
        color: #F1FAEE !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    /* Cards and containers */
    .stColumn > div {
        background: rgba(29, 53, 87, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid rgba(255, 183, 3, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.3rem !important;
        letter-spacing: 2px !important;
        background: linear-gradient(135deg, #E63946 0%, #C1121F 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem 2rem !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(230, 57, 70, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(230, 57, 70, 0.6) !important;
    }
    
    /* Form submit button */
    .stForm button[kind="primary"] {
        background: linear-gradient(135deg, #FFB703 0%, #FB8500 100%) !important;
        box-shadow: 0 4px 15px rgba(255, 183, 3, 0.4) !important;
    }
    
    /* Inputs */
    .stSelectbox, .stNumberInput, .stTextInput {
        font-family: 'Inconsolata', monospace !important;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div, .stTextInput > div > div {
        background: rgba(241, 250, 238, 0.1) !important;
        border: 2px solid rgba(69, 123, 157, 0.3) !important;
        border-radius: 8px !important;
        color: #F1FAEE !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(29, 53, 87, 0.3);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid rgba(230, 57, 70, 0.3);
    }
    
    .stRadio label {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px !important;
        color: #F1FAEE !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        font-family: 'Inconsolata', monospace !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Success/Info messages */
    .stSuccess {
        background: rgba(40, 167, 69, 0.3) !important;
        border: 2px solid #28A745 !important;
        border-radius: 10px !important;
        font-family: 'Inconsolata', monospace !important;
        padding: 1rem !important;
        color: #F1FAEE !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3) !important;
    }
    
    .stSuccess > div {
        color: #F1FAEE !important;
    }
    
    .stInfo {
        background: rgba(69, 123, 157, 0.3) !important;
        border: 2px solid #457B9D !important;
        border-radius: 10px !important;
        font-family: 'Inconsolata', monospace !important;
        padding: 1rem !important;
        color: #F1FAEE !important;
        box-shadow: 0 4px 15px rgba(69, 123, 157, 0.3) !important;
    }
    
    .stInfo > div {
        color: #F1FAEE !important;
    }
    
    .stWarning {
        background: rgba(255, 183, 3, 0.3) !important;
        border: 2px solid #FFB703 !important;
        border-radius: 10px !important;
        font-family: 'Inconsolata', monospace !important;
        padding: 1rem !important;
        color: #F1FAEE !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(255, 183, 3, 0.3) !important;
    }
    
    .stWarning > div {
        color: #F1FAEE !important;
    }
    
    /* Dividers */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #E63946, transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #457B9D 0%, #1D3557 100%) !important;
        box-shadow: 0 4px 15px rgba(69, 123, 157, 0.4) !important;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 15px !important;
        overflow: hidden !important;
    }
    
    /* Emoji styling */
    .emoji {
        font-size: 2rem;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
</style>
""", unsafe_allow_html=True)

def env_exists():
    """Check if .env file exists"""
    return os.path.exists(".env")

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"] if not env_exists() else dotenv.get_key(".env", "SUPABASE_URL")
    key = st.secrets["supabase"]["key"] if not env_exists() else dotenv.get_key(".env", "SUPABASE_KEY")
    return create_client(url, key)

try:

    supabase: Client = init_supabase()
except Exception as e:
    st.error("⚠️ Supabase connection failed. Please check your secrets configuration.")
    st.stop()

# Data functions
def load_data(zones=False):
    """Load data from Supabase"""
    try:
        table_name = "shots_bulk" if zones else "shots_detailed"
        response = supabase.table(table_name).select("*").execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            if zones:
                return pd.DataFrame(columns=['id', 'timestamp', 'result', 'shot_origin', 'nshots', 'notes', 'Game', 'player'])
            return pd.DataFrame(columns=['id', 'timestamp', 'goal_area', 'result', 'shot_origin', 'notes', 'Game', 'player', 'nshots'])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def save_shot(data, zones=False):
    """Save a shot to Supabase"""
    try:
        table_name = "shots_bulk" if zones else "shots_detailed"
        response = supabase.table(table_name).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def delete_all_data(zones=False):
    """Delete all data from a table"""
    try:
        table_name = "shots_bulk" if zones else "shots_detailed"
        # Get all IDs first
        response = supabase.table(table_name).select("id").execute()
        if response.data:
            for row in response.data:
                supabase.table(table_name).delete().eq('id', row['id']).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting data: {e}")
        return False

# Header with emoji
st.markdown('<span class="emoji">🥅</span>', unsafe_allow_html=True)
st.title("GOALKEEPER STATISTICS")
st.markdown("### Track Every Save, Analyze Every Shot")
st.markdown("---")

# Main content area
tab1, tab2 = st.tabs(["📊 RECORD SHOTS", "📈 STATISTICS"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("## 🎯 DETAILED SHOT ENTRY")
        st.markdown("*Record shots with goal area information*")
        
        game = st.text_input("Game/Match", "", key='detailed_game')
        
        player = st.text_input("Player Name", "", key='detailed_player')
        
        shot_origin = st.selectbox(
            "Shot Origin",
            ["6m", "9m", "7m (penalty)", "Wing", "Counter Attack", "Unknown"],
            key='detailed_origin'
        )
        
        goal_area = st.selectbox(
            "Goal Area",
            ['Top Left', 'Top Center', 'Top Right',
             'Middle Left', 'Middle Center', 'Middle Right',
             'Lower Left', 'Lower Center', 'Lower Right'],
            key='detailed_area'
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            result = st.radio("Result", ["Save", "Goal"], horizontal=True, key='detailed_result')
        with col_b:
            nr = st.number_input("# Shots", min_value=1, value=1, step=1, key='detailed_nr')
        
        if st.button("➕ ADD SHOT", type="primary", key='add_detailed'):
            new_entry = {
                'timestamp': datetime.now().isoformat(),
                'goal_area': goal_area,
                'result': result,
                'shot_origin': shot_origin,
                'Game': game,
                'player': player,
                'nshots': int(nr)
            }
            
            if save_shot(new_entry, zones=False):
                st.success(f"✅ {int(nr)} shot(s) recorded: {result} in {goal_area} from {shot_origin}")
    
    with col2:
        st.markdown("## 📝 BULK ENTRY")
        st.markdown("*Quick entry without goal area data*")
        
        with st.form("bulk_entry"):
            game_bulk = st.text_input("Game/Match", key='bulk_game')
            
            player_bulk = st.text_input("Player Name", key='bulk_player')
            
            bulk_origin = st.selectbox(
                "Shot Origin",
                ["6m", "9m", "7m (penalty)", "Wing", "Counter Attack"],
                key='bulk_origin'
            )
            
            col_c, col_d = st.columns(2)
            with col_c:
                num_saves = st.number_input("Saves", min_value=0, value=0, step=1)
            with col_d:
                num_goals = st.number_input("Goals", min_value=0, value=0, step=1)
            
            submitted = st.form_submit_button("➕ ADD BULK DATA")
            
            if submitted and (num_saves > 0 or num_goals > 0):
                success = True
                
                if num_saves > 0:
                    new_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'result': 'Save',
                        'shot_origin': bulk_origin,
                        'nshots': int(num_saves),
                        'notes': 'Bulk entry',
                        'Game': game_bulk,
                        'player': player_bulk
                    }
                    success = success and save_shot(new_entry, zones=True)
                
                if num_goals > 0:
                    new_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'result': 'Goal',
                        'shot_origin': bulk_origin,
                        'nshots': int(num_goals),
                        'notes': 'Bulk entry',
                        'Game': game_bulk,
                        'player': player_bulk
                    }
                    success = success and save_shot(new_entry, zones=True)
                
                if success:
                    st.success(f"✅ Added {int(num_saves)} saves and {int(num_goals)} goals from {bulk_origin}!")
with tab2:
    st.markdown("## 📊 PERFORMANCE OVERVIEW")
    
    # Add filters at the top
    st.markdown("### 🔍 FILTERS")
    col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 0.5])

    #Deafult values for df
    df = load_data(zones=False)
    df_bulk = load_data(zones=True)
    
    with col_filter1:
        # Get unique games from both datasets
        games_detailed = df['Game'].unique().tolist() if len(df) > 0 and 'Game' in df.columns else []
        all_games = sorted(list(set(games_detailed)))
        all_games = [g.replace(' ', '') for g in all_games if g.replace(' ', '')]  # Remove empty strings

        game_options = ["All Games"] + all_games
        selected_game = st.selectbox("Filter by Game", game_options, key='game_filter')
    
    with col_filter2:
        # Get unique players from both datasets
        players_detailed = df['player'].unique().tolist() if len(df) > 0 and 'player' in df.columns else []
        all_players = [p.replace(' ', '') for p in players_detailed if p.replace(' ', '')]  # Remove empty strings
        
        player_options = ["All Players"] + all_players
        selected_player = st.selectbox("Filter by Player", player_options, key='player_filter')

    
    with col_filter3:
        if st.button("🔄 RESET FILTERS", key='reset_filters'):
            st.rerun()
    
    # Apply filters
    if selected_game != "All Games":
        df = df[df['Game'] == selected_game] if len(df) > 0 else df
    
    if selected_player != "All Players":
        df = df[df['player'] == selected_player] if len(df) > 0 else df
    
    
    st.markdown("---")
    
    # Calculate totals (after filtering)
    total_detailed = df['nshots'].sum() if len(df) > 0 else 0
    
    saves_detailed = df[df['result'] == 'Save']['nshots'].sum() if len(df) > 0 else 0
    
    goals_detailed = df[df['result'] == 'Goal']['nshots'].sum() if len(df) > 0 else 0
    
    save_pct = (saves_detailed / total_detailed * 100) if total_detailed > 0 else 0
    
    # Big stats display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("TOTAL SHOTS", f"{int(total_detailed)}")
    with col2:
        st.metric("SAVES", f"{int(saves_detailed)}")
    with col3:
        st.metric("GOALS", f"{int(goals_detailed)}")
    with col4:
        st.metric("SAVE %", f"{save_pct:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown("### 🎯 SHOT DISTRIBUTION BY AREA")
        if len(df) > 0:
            expanded_data = []
            for _, row in df.iterrows():
                for _ in range(int(row['nshots'])):
                    expanded_data.append({
                        'goal_area': row['goal_area'],
                        'result': row['result']
                    })
            
            if expanded_data:
                expanded_df = pd.DataFrame(expanded_data)
                zone_counts = expanded_df.groupby(['goal_area', 'result']).size().unstack(fill_value=0)
                
                fig = go.Figure()
                
                colors = {'Save': '#28A745', 'Goal': '#E63946'}
                for result in zone_counts.columns:
                    fig.add_trace(go.Bar(
                        x=zone_counts.index,
                        y=zone_counts[result],
                        name=result,
                        marker_color=colors.get(result, '#457B9D'),
                        text=zone_counts[result],
                        textposition='inside',
                        textfont=dict(size=14, family='Bebas Neue', color='white')
                    ))
                
                fig.update_layout(
                    barmode='stack',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inconsolata', color='#F1FAEE'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    legend=dict(font=dict(family='Bebas Neue', size=14)),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No detailed shot data yet")
    
    with col_chart2:
        st.markdown("### 🎲 SHOT DISTRIBUTION BY ORIGIN")
        
        # Combine both datasets for complete origin stats
        all_origin_data = []
        
        if len(df_bulk) > 0:
            for _, row in df_bulk.iterrows():
                all_origin_data.append({
                    'shot_origin': row['shot_origin'],
                    'result': row['result'],
                    'count': row['nshots']
                })
        
        if all_origin_data:
            origin_df = pd.DataFrame(all_origin_data)
            origin_counts = origin_df.groupby(['shot_origin', 'result'])['count'].sum().unstack(fill_value=0)
            
            fig2 = go.Figure()
            
            colors = {'Save': '#28A745', 'Goal': '#E63946'}
            for result in origin_counts.columns:
                fig2.add_trace(go.Bar(
                    x=origin_counts.index,
                    y=origin_counts[result],
                    name=result,
                    marker_color=colors.get(result, '#457B9D'),
                    text=origin_counts[result],
                    textposition='inside',
                    textfont=dict(size=14, family='Bebas Neue', color='white')
                ))
            
            fig2.update_layout(
                barmode='stack',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inconsolata', color='#F1FAEE'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                legend=dict(font=dict(family='Bebas Neue', size=14)),
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No shot origin data yet")
    
    st.markdown("---")
    
    # Detailed tables
    col_table1, col_table2 = st.columns(2, gap="large")
    
    with col_table1:
        st.markdown("### 📋 BY GOAL AREA")
        if len(df) > 0:
            area_stats = df.groupby(['goal_area', 'result'])['nshots'].sum().unstack(fill_value=0)
            st.dataframe(area_stats, use_container_width=True)
        else:
            st.info("No area data yet")
    
    with col_table2:
        st.markdown("### 📋 BY SHOT ORIGIN")
        if len(df_bulk) > 0:
            if all_origin_data:
                origin_stats = origin_df.groupby(['shot_origin', 'result'])['count'].sum().unstack(fill_value=0)
                st.dataframe(origin_stats, use_container_width=True)
        else:
            st.info("No origin data yet")
