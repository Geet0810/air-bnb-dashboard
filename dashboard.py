"""
Airbnb Analytics Dashboard - Luxe Dark Theme
A comprehensive analytics platform for Airbnb data visualization.
Built with Streamlit, Plotly, and premium design aesthetics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Import custom utilities
from utils.data_processor import (
    load_and_clean_data, filter_data, 
    calculate_guest_metrics, calculate_host_metrics,
    get_city_stats, get_area_stats,
    ROOM_TYPE_MAP, CITY_COORDINATES, AREA_COLORS
)

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="Airbnb Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS - LUXE DARK THEME ============
CUSTOM_CSS = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #06b6d4 0%, #a855f7 50%, #f97316 100%);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(6, 182, 212, 0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06b6d4, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Host view metrics */
    .host-metric .metric-value {
        background: linear-gradient(135deg, #f97316, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label {
        color: #f8fafc !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.5);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        padding: 12px 24px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #a855f7);
        color: white !important;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Smooth animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 8px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #06b6d4, #a855f7);
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #06b6d4, #a855f7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #0891b2, #9333ea);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============ THEME CONFIGURATION ============
THEME = {
    'bg_primary': '#0f172a',
    'bg_secondary': '#1e293b',
    'guest_accent': '#06b6d4',
    'host_accent': '#f97316',
    'highlight': '#a855f7',
    'text_primary': '#f8fafc',
    'text_secondary': '#cbd5e1',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444'
}

# Plotly theme template
PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': THEME['text_primary'], 'family': 'Inter'},
        'title': {'font': {'size': 18, 'color': THEME['text_primary']}},
        'legend': {'bgcolor': 'rgba(0,0,0,0)', 'font': {'color': THEME['text_secondary']}},
        'xaxis': {'gridcolor': 'rgba(255,255,255,0.1)', 'zerolinecolor': 'rgba(255,255,255,0.1)'},
        'yaxis': {'gridcolor': 'rgba(255,255,255,0.1)', 'zerolinecolor': 'rgba(255,255,255,0.1)'}
    }
}


# ============ DATA LOADING ============
@st.cache_data(show_spinner=True)
def load_data():
    """Load and cache the Airbnb data."""
    try:
        df, stats = load_and_clean_data('/app/data/Airbnb_site_hotel_new.csv')
        return df, stats, None
    except FileNotFoundError:
        # Try alternative path for local development
        try:
            df, stats = load_and_clean_data('data/Airbnb_site_hotel_new.csv')
            return df, stats, None
        except Exception as e:
            return None, None, str(e)
    except Exception as e:
        return None, None, str(e)


# ============ CHART FUNCTIONS - GUEST VIEW ============

def create_radar_chart(df: pd.DataFrame) -> go.Figure:
    """Create radar chart comparing top 5 cities."""
    city_stats = get_city_stats(df)
    top_cities = city_stats.nlargest(5, 'listing_count')
    
    categories = ['Avg Price', 'Avg Rating', 'Total Reviews', 'Avg Bedrooms', 'Avg Bathrooms', 'Guest Favourite %']
    
    fig = go.Figure()
    
    colors = ['#06b6d4', '#f97316', '#a855f7', '#10b981', '#f59e0b']
    
    for idx, (_, row) in enumerate(top_cities.iterrows()):
        # Normalize values for radar chart
        values = [
            row['avg_price'] / city_stats['avg_price'].max() * 100,
            row['avg_rating'] / 7 * 100,  # Rating is 0-7
            row['total_reviews'] / city_stats['total_reviews'].max() * 100,
            row['avg_bedrooms'] / city_stats['avg_bedrooms'].max() * 100,
            row['avg_bathrooms'] / city_stats['avg_bathrooms'].max() * 100,
            row['pct_guest_favourite'] * 100
        ]
        values.append(values[0])  # Close the radar
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=f'rgba{tuple(int(colors[idx][i:i+2], 16) for i in (1, 3, 5)) + (0.2,)}',
            line=dict(color=colors[idx], width=2),
            name=row['city'],
            hovertemplate=f"<b>{row['city']}</b><br>%{{theta}}: %{{r:.1f}}%<extra></extra>"
        ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)'
            )
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(color=THEME['text_secondary'])
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        title=dict(text='🏆 Top 5 Cities Comparison', font=dict(size=18)),
        height=500,
        margin=dict(t=80, b=80)
    )
    
    return fig


def create_contour_plot(df: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart showing average price by city."""
    city_stats = get_city_stats(df)
    
    if len(city_stats) < 1:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data for visualization", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Sort by average price descending
    city_stats = city_stats.sort_values('avg_price', ascending=True)
    
    # Create color gradient based on price
    colors = []
    max_price = city_stats['avg_price'].max()
    min_price = city_stats['avg_price'].min()
    for price in city_stats['avg_price']:
        # Normalize to 0-1 range
        normalized = (price - min_price) / (max_price - min_price) if max_price > min_price else 0.5
        # Interpolate between teal and coral
        if normalized < 0.5:
            colors.append(f'rgba(6, 182, 212, {0.6 + normalized * 0.4})')  # Teal
        else:
            colors.append(f'rgba(249, 115, 22, {0.6 + (normalized - 0.5) * 0.4})')  # Coral
    
    fig = go.Figure()
    
    # Add horizontal bar chart
    fig.add_trace(go.Bar(
        y=city_stats['city'],
        x=city_stats['avg_price'],
        orientation='h',
        marker=dict(
            color=city_stats['avg_price'],
            colorscale=[[0, '#06b6d4'], [0.5, '#a855f7'], [1, '#f97316']],
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        ),
        text=[f"${p:.0f}" for p in city_stats['avg_price']],
        textposition='outside',
        textfont=dict(color=THEME['text_primary'], size=11),
        hovertemplate="<b>%{y}</b><br>Avg Price: $%{x:.0f}<br>Listings: %{customdata:,}<extra></extra>",
        customdata=city_stats['listing_count']
    ))
    
    # Add average line
    avg_price = city_stats['avg_price'].mean()
    fig.add_vline(
        x=avg_price,
        line_dash="dash",
        line_color="#10b981",
        annotation_text=f"Avg: ${avg_price:.0f}",
        annotation_position="top",
        annotation_font_color="#10b981"
    )
    
    fig.update_layout(
        title=dict(text='🏙️ Average Price by City', font=dict(size=18)),
        xaxis=dict(
            title='Average Price ($)',
            gridcolor='rgba(255,255,255,0.1)',
            tickformat='$,.0f'
        ),
        yaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.05)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450,
        margin=dict(l=100, r=60)
    )
    
    return fig




def create_satisfaction_gauge(df: pd.DataFrame) -> go.Figure:
    """Create circular gauge for overall satisfaction score."""
    avg_rating = df['consumer_clean'].mean() if len(df) > 0 else 0
    satisfaction_pct = (avg_rating / 7) * 100  # Convert 0-7 to 0-100%
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=satisfaction_pct,
        number={'suffix': '%', 'font': {'size': 48, 'color': THEME['text_primary']}},
        title={'text': '😊 Overall Satisfaction', 'font': {'size': 18, 'color': THEME['text_primary']}},
        delta={'reference': 80, 'suffix': '%', 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': THEME['text_secondary']},
            'bar': {'color': '#06b6d4', 'thickness': 0.3},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': THEME['highlight'], 'width': 4},
                'thickness': 0.75,
                'value': satisfaction_pct
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=350,
        margin=dict(t=80, b=40)
    )
    
    return fig


def create_stacked_area_chart(df: pd.DataFrame) -> go.Figure:
    """Create stacked area chart for booking trends over time."""
    # Create time periods from host_since
    valid_df = df[df['host_since_clean'].notna()].copy()
    
    if len(valid_df) < 10:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data for visualization", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Create year bins
    valid_df['host_year'] = pd.cut(valid_df['host_since_clean'], bins=10)
    
    # Group by year and room type
    grouped = valid_df.groupby(['host_year', 'room_type_decoded'])['sales'].sum().unstack(fill_value=0)
    
    fig = go.Figure()
    
    colors = {'Private Room': '#06b6d4', 'Entire Home/Apt': '#f97316', 
              'Shared Room': '#a855f7', 'Hotel Room': '#10b981'}
    
    for room_type in grouped.columns:
        fig.add_trace(go.Scatter(
            x=[str(interval) for interval in grouped.index],
            y=grouped[room_type],
            name=room_type,
            mode='lines',
            stackgroup='one',
            fillcolor=f'rgba{tuple(int(colors.get(room_type, "#06b6d4")[i:i+2], 16) for i in (1, 3, 5)) + (0.6,)}',
            line=dict(color=colors.get(room_type, '#06b6d4'), width=2),
            hovertemplate=f"<b>{room_type}</b><br>Period: %{{x}}<br>Sales: %{{y:,.0f}}<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(text='📈 Booking Trends by Room Type', font=dict(size=18)),
        xaxis=dict(
            title='Host Since Period',
            gridcolor='rgba(255,255,255,0.1)',
            tickangle=45
        ),
        yaxis=dict(
            title='Total Sales Volume',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='center',
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450,
        margin=dict(b=100)
    )
    
    return fig


def create_violin_plot(df: pd.DataFrame) -> go.Figure:
    """Create violin plot for price distribution by area."""
    valid_df = df[(df['price_clean'] > 0) & (df['price_clean'] <= 1000)].copy()
    
    fig = go.Figure()
    
    for area in ['North America', 'Europe', 'Asia', 'Oceania']:
        area_data = valid_df[valid_df['area'] == area]['price_clean']
        
        if len(area_data) > 0:
            fig.add_trace(go.Violin(
                y=area_data,
                name=area,
                box_visible=True,
                meanline_visible=True,
                fillcolor=f'rgba{tuple(int(AREA_COLORS.get(area, "#06b6d4")[i:i+2], 16) for i in (1, 3, 5)) + (0.5,)}',
                line_color=AREA_COLORS.get(area, '#06b6d4'),
                opacity=0.8,
                hovertemplate=f"<b>{area}</b><br>Price: $%{{y:.0f}}<extra></extra>"
            ))
    
    fig.update_layout(
        title=dict(text='🎻 Price Distribution by Region', font=dict(size=18)),
        yaxis=dict(
            title='Price ($)',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5
        ),
        height=450
    )
    
    return fig


def create_geographic_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create city performance comparison chart."""
    city_stats = get_city_stats(df)
    
    if len(city_stats) < 1:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data for visualization", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Sort by listing count for better visualization
    city_stats = city_stats.sort_values('listing_count', ascending=False)
    
    fig = go.Figure()
    
    # Add listings bar
    fig.add_trace(go.Bar(
        name='Listings (x100)',
        x=city_stats['city'],
        y=city_stats['listing_count'] / 100,
        marker_color='#06b6d4',
        hovertemplate="<b>%{x}</b><br>Listings: %{customdata:,}<extra></extra>",
        customdata=city_stats['listing_count']
    ))
    
    # Add average rating bar (scaled for visibility)
    fig.add_trace(go.Bar(
        name='Avg Rating (x10)',
        x=city_stats['city'],
        y=city_stats['avg_rating'] * 10,
        marker_color='#a855f7',
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{customdata:.2f}<extra></extra>",
        customdata=city_stats['avg_rating']
    ))
    
    # Add average price bar (scaled)
    fig.add_trace(go.Bar(
        name='Avg Price ($)',
        x=city_stats['city'],
        y=city_stats['avg_price'],
        marker_color='#f97316',
        hovertemplate="<b>%{x}</b><br>Avg Price: $%{y:.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text='🎯 City Performance Comparison', font=dict(size=18)),
        xaxis=dict(
            title='City',
            gridcolor='rgba(255,255,255,0.05)',
            tickangle=45
        ),
        yaxis=dict(
            title='Value (scaled)',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(color=THEME['text_secondary'])
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=500,
        margin=dict(t=80, b=80)
    )
    
    return fig



# ============ CHART FUNCTIONS - HOST VIEW ============

def create_nightingale_chart(df: pd.DataFrame) -> go.Figure:
    """Create Nightingale/Rose chart for revenue by area."""
    area_stats = get_area_stats(df)
    
    fig = go.Figure(go.Barpolar(
        r=area_stats['total_sales'],
        theta=area_stats['area'],
        marker_color=[AREA_COLORS.get(a, '#06b6d4') for a in area_stats['area']],
        marker_line_color='white',
        marker_line_width=2,
        opacity=0.8,
        hovertemplate="<b>%{theta}</b><br>Total Sales: %{r:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text='🌹 Revenue by Region', font=dict(size=18)),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
                tickfont=dict(color=THEME['text_secondary'])
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
                tickfont=dict(color=THEME['text_primary'])
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450
    )
    
    return fig


def create_hexbin_plot(df: pd.DataFrame) -> go.Figure:
    """Create hexagonal binning plot for reviews vs sales."""
    valid_df = df[(df['total reviewers number'] > 0) & (df['sales'] > 0)].copy()
    
    if len(valid_df) < 10:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data for visualization", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = go.Figure(go.Histogram2d(
        x=valid_df['total reviewers number'],
        y=valid_df['sales'],
        colorscale=[[0, '#0f172a'], [0.25, '#06b6d4'], [0.5, '#a855f7'], [0.75, '#f97316'], [1, '#f8fafc']],
        nbinsx=30,
        nbinsy=30,
        hovertemplate="Reviews: %{x}<br>Sales Days: %{y}<br>Count: %{z}<extra></extra>",
        colorbar=dict(
            title=dict(text='Density', font=dict(color=THEME['text_secondary'])),
            tickfont=dict(color=THEME['text_secondary'])
        )
    ))
    
    fig.update_layout(
        title=dict(text='⬡ Reviews vs Sales Correlation', font=dict(size=18)),
        xaxis=dict(
            title='Total Reviews',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title='Sales Days',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450
    )
    
    return fig


def create_circular_treemap(df: pd.DataFrame) -> go.Figure:
    """Create treemap for revenue hierarchy (Area > City > Room Type)."""
    # Aggregate data
    hierarchy = df.groupby(['area', 'city', 'room_type_decoded']).agg({
        'sales': 'sum',
        'price_clean': 'mean'
    }).reset_index()
    
    # Create treemap
    fig = px.treemap(
        hierarchy,
        path=['area', 'city', 'room_type_decoded'],
        values='sales',
        color='price_clean',
        color_continuous_scale=[[0, '#06b6d4'], [0.5, '#a855f7'], [1, '#f97316']],
        hover_data={'price_clean': ':.0f'}
    )
    
    fig.update_traces(
        textfont=dict(color='white'),
        hovertemplate="<b>%{label}</b><br>Sales: %{value:,.0f}<br>Avg Price: $%{color:.0f}<extra></extra>"
    )
    
    fig.update_layout(
        title=dict(text='🌳 Revenue Hierarchy', font=dict(size=18, color=THEME['text_primary'])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        coloraxis_colorbar=dict(
            title=dict(text='Avg Price ($)', font=dict(color=THEME['text_secondary'])),
            tickfont=dict(color=THEME['text_secondary'])
        ),
        height=500
    )
    
    return fig


def create_bump_chart(df: pd.DataFrame) -> go.Figure:
    """Create bump chart for city rankings over time."""
    valid_df = df[df['host_since_clean'].notna()].copy()
    
    if len(valid_df) < 10:
        fig = go.Figure()
        fig.add_annotation(text="Not enough data for visualization", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Create quarters from host_since
    valid_df['period'] = pd.qcut(valid_df['host_since_clean'], q=6, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'], duplicates='drop')
    
    # Calculate rankings
    period_sales = valid_df.groupby(['period', 'city'])['sales'].sum().reset_index()
    period_sales['rank'] = period_sales.groupby('period')['sales'].rank(ascending=False).astype(int)
    
    # Get top 10 cities overall
    top_cities = pd.DataFrame(valid_df.groupby('city')['sales'].sum().nlargest(10).index)['city'].tolist()
    period_sales = period_sales[period_sales['city'].isin(top_cities)]
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3[:len(top_cities)]
    
    for i, city in enumerate(top_cities):
        city_data = period_sales[period_sales['city'] == city].sort_values('period')
        
        fig.add_trace(go.Scatter(
            x=city_data['period'],
            y=city_data['rank'],
            name=city,
            mode='lines+markers',
            line=dict(color=colors[i], width=3),
            marker=dict(size=12, symbol='circle'),
            hovertemplate=f"<b>{city}</b><br>Period: %{{x}}<br>Rank: %{{y}}<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(text='📊 City Rankings Over Time', font=dict(size=18)),
        xaxis=dict(
            title='Time Period',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title='Rank',
            autorange='reversed',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450
    )
    
    return fig


def create_radial_histogram(df: pd.DataFrame) -> go.Figure:
    """Create radial histogram for sales distribution (0-365 days)."""
    valid_df = df[df['sales'] > 0].copy()
    
    # Create 12 monthly bins
    bins = np.linspace(0, 365, 13)
    valid_df['month_bin'] = pd.cut(valid_df['sales'], bins=bins, labels=[f'{i*30}-{(i+1)*30}' for i in range(12)])
    
    bin_counts = valid_df['month_bin'].value_counts().sort_index()
    
    fig = go.Figure(go.Barpolar(
        r=bin_counts.values,
        theta=[f'Day {i*30}' for i in range(12)],
        marker_color='#a855f7',
        marker_line_color='white',
        marker_line_width=1,
        opacity=0.8,
        hovertemplate="<b>%{theta}</b><br>Listings: %{r:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text='🎯 Sales Distribution (Days/Year)', font=dict(size=18)),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
                tickfont=dict(color=THEME['text_secondary'])
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
                tickfont=dict(color=THEME['text_primary'])
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=450
    )
    
    return fig


def create_network_graph(df: pd.DataFrame) -> go.Figure:
    """Create node-link graph for multi-city host connections."""
    # Find hosts with listings in multiple cities
    host_cities = df.groupby('host_id')['city'].apply(set).reset_index()
    multi_city_hosts = host_cities[host_cities['city'].apply(len) > 1]
    
    # Create graph
    G = nx.Graph()
    
    # Add city nodes
    city_counts = df.groupby('city').size().to_dict()
    for city in df['city'].unique():
        G.add_node(city, size=city_counts.get(city, 1), area=df[df['city'] == city]['area'].iloc[0])
    
    # Add edges for shared hosts
    edge_weights = {}
    for _, row in multi_city_hosts.iterrows():
        cities = list(row['city'])
        for i in range(len(cities)):
            for j in range(i+1, len(cities)):
                edge = tuple(sorted([cities[i], cities[j]]))
                edge_weights[edge] = edge_weights.get(edge, 0) + 1
    
    for (city1, city2), weight in edge_weights.items():
        G.add_edge(city1, city2, weight=weight)
    
    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2].get('weight', 1)
        
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.2)', width=min(weight, 5)),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Add nodes
    for node in G.nodes():
        x, y = pos[node]
        size = G.nodes[node]['size']
        area = G.nodes[node]['area']
        color = AREA_COLORS.get(area, '#06b6d4')
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=np.log(size + 1) * 8,
                color=color,
                line=dict(color='white', width=2)
            ),
            text=node,
            textposition='top center',
            textfont=dict(color=THEME['text_primary'], size=10),
            hovertemplate=f"<b>{node}</b><br>Listings: {size}<br>Area: {area}<extra></extra>",
            showlegend=False
        ))
    
    fig.update_layout(
        title=dict(text='🔗 Multi-City Host Network', font=dict(size=18)),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_primary']),
        height=500,
        showlegend=False
    )
    
    return fig


# ============ METRIC DISPLAY FUNCTIONS ============

def display_guest_metrics(metrics: dict):
    """Display guest-focused metrics in a styled grid."""
    cols = st.columns(6)
    
    metric_data = [
        ('🏠', 'Total Properties', f"{metrics['total_properties']:,}"),
        ('💰', 'Avg Price', f"${metrics['avg_price']:.0f}"),
        ('⭐', 'Avg Rating', f"{metrics['avg_rating']:.2f}/7"),
        ('❤️', '% Favourites', f"{metrics['pct_favourites']:.1f}%"),
        ('🏆', 'Most Popular', metrics['most_popular_city']),
        ('💎', 'Best Value', metrics['best_value_city'])
    ]
    
    for col, (icon, label, value) in zip(cols, metric_data):
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def format_large_number(num: float) -> str:
    """Format large numbers with K, M, B suffixes."""
    if num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"${num / 1_000:.1f}K"
    else:
        return f"${num:.0f}"


def display_host_metrics(metrics: dict):
    """Display host-focused metrics in a styled grid."""
    cols = st.columns(6)
    
    # Format the revenue with M/B notation
    formatted_revenue = format_large_number(metrics['total_revenue'])
    
    metric_data = [
        ('💵', 'Total Revenue', formatted_revenue),
        ('📅', 'Avg Occupancy', f"{metrics['avg_occupancy']:.1f}%"),
        ('👥', 'Total Hosts', f"{metrics['total_hosts']:,}"),
        ('🏘️', 'Avg Listings', f"{metrics['avg_listings_per_host']:.1f}"),
        ('✓', '% Certified', f"{metrics['pct_certified']:.1f}%"),
        ('🥇', 'Best City', metrics['best_city'])
    ]
    
    for col, (icon, label, value) in zip(cols, metric_data):
        col.markdown(f"""
        <div class="metric-card host-metric">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)



# ============ MAIN APPLICATION ============

def main():
    """Main application entry point."""
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🏠 Airbnb Analytics Dashboard</h1>
        <p class="dashboard-subtitle">Comprehensive insights across 11 global cities • 86,000+ listings analyzed</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading data...'):
        df, data_stats, error = load_data()
    
    if error:
        st.error(f"""
        ⚠️ **Error Loading Data**
        
        {error}
        
        Please ensure the CSV file is placed in the `data/` folder with the name `Airbnb_site_hotel_new.csv`.
        """)
        return
    
    if df is None or len(df) == 0:
        st.error("No data available. Please check your data file.")
        return
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown("### 🎛️ Filter Controls")
        st.markdown("---")
        
        # Multi-select filters
        selected_cities = st.multiselect(
            "🏙️ Cities",
            options=data_stats['unique_cities'],
            default=data_stats['unique_cities'],
            help="Select one or more cities"
        )
        
        selected_areas = st.multiselect(
            "🌍 Areas",
            options=data_stats['unique_areas'],
            default=data_stats['unique_areas'],
            help="Select one or more regions"
        )
        
        selected_room_types = st.multiselect(
            "🛏️ Room Types",
            options=data_stats['unique_room_types'],
            default=data_stats['unique_room_types'],
            help="Select room types to include"
        )
        
        st.markdown("---")
        
        # Sliders
        price_range = st.slider(
            "💰 Price Range ($)",
            min_value=0,
            max_value=int(data_stats['price_range']['max'] or 1000),
            value=(0, min(500, int(data_stats['price_range']['max'] or 500))),
            step=10
        )
        
        min_reviews = st.slider(
            "📝 Minimum Reviews",
            min_value=0,
            max_value=500,
            value=0,
            step=10
        )
        
        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=0.0,
            max_value=7.0,
            value=0.0,
            step=0.5
        )
        
        st.markdown("---")
        
        # Checkboxes
        guest_favourites_only = st.checkbox("❤️ Guest Favourites Only", value=False)
        certified_hosts_only = st.checkbox("✓ Certified Hosts Only", value=False)
        
        st.markdown("---")
        
        # Stats display
        st.markdown("### 📊 Current Selection")
        
        # Filter data
        filtered_df = filter_data(
            df,
            cities=selected_cities,
            areas=selected_areas,
            room_types=selected_room_types,
            price_range=price_range,
            min_reviews=min_reviews,
            min_rating=min_rating,
            guest_favourites_only=guest_favourites_only,
            certified_hosts_only=certified_hosts_only
        )
        
        st.metric("Listings", f"{len(filtered_df):,}")
        st.metric("Avg Price", f"${filtered_df['price_clean'].mean():.0f}" if len(filtered_df) > 0 else "$0")
        st.metric("Cities", len(filtered_df['city'].unique()) if len(filtered_df) > 0 else 0)
        
        st.markdown("---")
        
        # Download button
        if len(filtered_df) > 0:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name="airbnb_filtered_data.csv",
                mime="text/csv"
            )
    
    # Check if filters result in empty data
    if len(filtered_df) == 0:
        st.warning("No listings match your current filter criteria. Please adjust your filters.")
        return
    
    # ============ MAIN CONTENT - TABS ============
    tab1, tab2 = st.tabs(["🛫 Guest View", "🏠 Host View"])
    
    # ============ GUEST VIEW ============
    with tab1:
        # Metrics
        guest_metrics = calculate_guest_metrics(filtered_df)
        display_guest_metrics(guest_metrics)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts - 2 column grid
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_radar_chart(filtered_df), width="stretch", key="radar")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_contour_plot(filtered_df), width="stretch", key="contour")
                st.markdown('</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_satisfaction_gauge(filtered_df), width="stretch", key="gauge")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_stacked_area_chart(filtered_df), width="stretch", key="stacked")
                st.markdown('</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_violin_plot(filtered_df), width="stretch", key="violin")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col6:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_geographic_heatmap(filtered_df), width="stretch", key="geo")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ============ HOST VIEW ============
    with tab2:
        # Metrics
        host_metrics = calculate_host_metrics(filtered_df)
        display_host_metrics(host_metrics)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts - 2 column grid
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_nightingale_chart(filtered_df), width="stretch", key="nightingale")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_hexbin_plot(filtered_df), width="stretch", key="hexbin")
                st.markdown('</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_circular_treemap(filtered_df), width="stretch", key="treemap")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_bump_chart(filtered_df), width="stretch", key="bump")
                st.markdown('</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_radial_histogram(filtered_df), width="stretch", key="radial")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col6:
            with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(create_network_graph(filtered_df), width="stretch", key="network")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
        <p>🏠 Airbnb Analytics Dashboard • Built with Streamlit & Plotly</p>
        <p>Data: 86,186 listings across 11 cities in 3 regions</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
