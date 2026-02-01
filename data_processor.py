"""
Data processing utilities for Airbnb Analytics Dashboard.
Handles data cleaning, transformation, and validation.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


# Room type mapping (integer to descriptive string)
ROOM_TYPE_MAP = {
    1: 'Private Room',
    2: 'Entire Home/Apt',
    3: 'Shared Room',
    4: 'Hotel Room'
}

# City coordinates for geographic visualization
CITY_COORDINATES = {
    'Toronto': {'lat': 43.6532, 'lon': -79.3832},
    'NewYork': {'lat': 40.7128, 'lon': -74.0060},
    'Amsterdam': {'lat': 52.3676, 'lon': 4.9041},
    'Berlin': {'lat': 52.5200, 'lon': 13.4050},
    'Dublin': {'lat': 53.3498, 'lon': -6.2603},
    'Hongkong': {'lat': 22.3193, 'lon': 114.1694},
    'Munich': {'lat': 48.1351, 'lon': 11.5820},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198},
    'Sydney': {'lat': -33.8688, 'lon': 151.2093},
    'Tokyo': {'lat': 35.6762, 'lon': 139.6503}
}

# Area color scheme
AREA_COLORS = {
    'North America': '#06b6d4',  # Teal (Guest accent)
    'Europe': '#f97316',         # Coral/Orange (Host accent)
    'Asia': '#a855f7',           # Purple (Highlight)
    'Oceania': '#fbbf24'         # Gold/Yellow (Australia - distinct from teal)
}

# Correct city-to-area mapping (fixes incorrect data in source)
CORRECT_CITY_AREA = {
    'Toronto': 'North America',
    'NewYork': 'North America',
    'Amsterdam': 'Europe',
    'Berlin': 'Europe',
    'Dublin': 'Europe',
    'Munich': 'Europe',
    'Hongkong': 'Asia',
    'Singapore': 'Asia',
    'Sydney': 'Oceania',  # Sydney is in Australia/Oceania
    'Tokyo': 'Asia'
}


def convert_european_decimal(value: str) -> float:
    """
    Convert European-style decimal notation (comma as decimal separator) to float.
    Handles values like "6,81" -> 6.81 or "0,9" -> 0.9
    """
    if pd.isna(value) or value == '' or value == 0:
        return np.nan
    
    if isinstance(value, (int, float)):
        return float(value)
    
    try:
        # Replace comma with period for decimal conversion
        cleaned = str(value).strip().replace(',', '.')
        return float(cleaned)
    except (ValueError, AttributeError):
        return np.nan


def clean_price(value) -> float:
    """
    Clean price values - removes currency symbols and converts to float.
    Handles values like "250" or "$250" or "1,250"
    """
    if pd.isna(value) or value == '':
        return np.nan
    
    if isinstance(value, (int, float)):
        return float(value)
    
    try:
        # Remove currency symbols, spaces, and thousands separators
        cleaned = str(value).strip()
        cleaned = cleaned.replace('$', '').replace('€', '').replace('£', '')
        cleaned = cleaned.replace(' ', '')
        # Handle both comma as thousands separator and as decimal
        if ',' in cleaned and '.' not in cleaned:
            # Check if it's a thousands separator or decimal
            parts = cleaned.split(',')
            if len(parts[-1]) == 2:  # Likely decimal
                cleaned = cleaned.replace(',', '.')
            else:  # Likely thousands separator
                cleaned = cleaned.replace(',', '')
        return float(cleaned)
    except (ValueError, AttributeError):
        return np.nan


def clean_host_since(value) -> Optional[int]:
    """
    Clean host_since values - ensures valid integer day counts.
    """
    if pd.isna(value) or value == '':
        return np.nan
    
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return np.nan


def load_and_clean_data(filepath: str) -> Tuple[pd.DataFrame, dict]:
    """
    Load and clean the Airbnb dataset.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Tuple of (cleaned DataFrame, stats dictionary)
    """
    # Load data
    df = pd.read_csv(filepath)
    
    # Store original count for stats
    original_count = len(df)
    
    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # ============ Data Cleaning ============
    
    # 1. Clean price column
    df['price_clean'] = df['price'].apply(clean_price)
    
    # 2. Clean bathrooms (European decimal format)
    df['bathrooms_clean'] = df['bathrooms'].apply(convert_european_decimal)
    
    # 3. Clean consumer rating (European decimal format)
    df['consumer_clean'] = df['consumer'].apply(convert_european_decimal)
    
    # 4. Clean host response rate (European decimal format - already 0-1)
    df['host_response_rate_clean'] = df['host response rate'].apply(convert_european_decimal)
    
    # 5. Clean host acceptance rate (European decimal format - already 0-1)
    df['host_acceptance_rate_clean'] = df['host acceptance rate'].apply(convert_european_decimal)
    
    # 6. Decode room_type from integers to strings
    df['room_type_decoded'] = df['room_type'].map(ROOM_TYPE_MAP)
    # Fill any unmapped values with 'Unknown'
    df['room_type_decoded'] = df['room_type_decoded'].fillna('Unknown')
    
    # 7. Calculate revenue estimate
    df['revenue_estimate'] = df['price_clean'] * df['sales']
    
    # 8. Clean host_since
    df['host_since_clean'] = df['host since'].apply(clean_host_since)
    
    # 9. Add city coordinates
    df['city_lat'] = df['city'].map(lambda x: CITY_COORDINATES.get(x, {}).get('lat', np.nan))
    df['city_lon'] = df['city'].map(lambda x: CITY_COORDINATES.get(x, {}).get('lon', np.nan))
    
    # 10. Clean host certification (convert to boolean)
    df['host_certified'] = df['host Certification'].fillna(0).astype(bool)
    
    # 11. Clean guest favourite (convert to boolean)
    df['guest_favourite'] = df['guest favourite'].fillna(0).astype(bool)
    
    # 12. CORRECT AREA ASSIGNMENTS (fixes incorrect region data)
    # Apply correct city-to-area mapping
    df['area'] = df['city'].map(CORRECT_CITY_AREA).fillna(df['area'])
    
    # 13. Clean numeric columns
    numeric_cols = ['accommodates', 'bedrooms', 'beds', 'total reviewers number', 'sales']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 13. Fill missing values for key metrics
    df['bedrooms'] = df['bedrooms'].fillna(0)
    df['bathrooms_clean'] = df['bathrooms_clean'].fillna(1)
    df['beds'] = df['beds'].fillna(1)
    
    # ============ Calculate Statistics ============
    stats = {
        'total_listings': len(df),
        'original_count': original_count,
        'cities': df['city'].nunique(),
        'areas': df['area'].nunique(),
        'unique_cities': sorted(df['city'].unique().tolist()),
        'unique_areas': sorted(df['area'].unique().tolist()),
        'unique_room_types': sorted(df['room_type_decoded'].unique().tolist()),
        'avg_price': df['price_clean'].mean(),
        'avg_rating': df['consumer_clean'].mean(),
        'total_hosts': df['host_id'].nunique(),
        'date_range': {
            'min': df['host_since_clean'].min(),
            'max': df['host_since_clean'].max()
        },
        'price_range': {
            'min': df['price_clean'].min(),
            'max': df['price_clean'].max()
        },
        'rating_range': {
            'min': df['consumer_clean'].min(),
            'max': df['consumer_clean'].max()
        }
    }
    
    return df, stats


def filter_data(df: pd.DataFrame, 
                cities: list = None,
                areas: list = None,
                room_types: list = None,
                price_range: tuple = None,
                min_reviews: int = 0,
                min_rating: float = 0,
                guest_favourites_only: bool = False,
                certified_hosts_only: bool = False) -> pd.DataFrame:
    """
    Filter the dataset based on multiple criteria.
    
    Args:
        df: The cleaned DataFrame
        cities: List of cities to include
        areas: List of areas to include
        room_types: List of room types to include
        price_range: Tuple of (min_price, max_price)
        min_reviews: Minimum number of reviews
        min_rating: Minimum consumer rating
        guest_favourites_only: Only include guest favourites
        certified_hosts_only: Only include certified hosts
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    # Apply city filter
    if cities and len(cities) > 0:
        filtered = filtered[filtered['city'].isin(cities)]
    
    # Apply area filter
    if areas and len(areas) > 0:
        filtered = filtered[filtered['area'].isin(areas)]
    
    # Apply room type filter
    if room_types and len(room_types) > 0:
        filtered = filtered[filtered['room_type_decoded'].isin(room_types)]
    
    # Apply price range filter
    if price_range:
        filtered = filtered[
            (filtered['price_clean'] >= price_range[0]) & 
            (filtered['price_clean'] <= price_range[1])
        ]
    
    # Apply minimum reviews filter
    if min_reviews > 0:
        filtered = filtered[filtered['total reviewers number'] >= min_reviews]
    
    # Apply minimum rating filter
    if min_rating > 0:
        filtered = filtered[filtered['consumer_clean'] >= min_rating]
    
    # Apply guest favourites filter
    if guest_favourites_only:
        filtered = filtered[filtered['guest_favourite'] == True]
    
    # Apply certified hosts filter
    if certified_hosts_only:
        filtered = filtered[filtered['host_certified'] == True]
    
    return filtered


def calculate_guest_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate guest-focused metrics from the dataset.
    """
    return {
        'total_properties': len(df),
        'avg_price': df['price_clean'].mean() if len(df) > 0 else 0,
        'avg_rating': df['consumer_clean'].mean() if len(df) > 0 else 0,
        'pct_favourites': (df['guest_favourite'].sum() / len(df) * 100) if len(df) > 0 else 0,
        'most_popular_city': df.groupby('city').size().idxmax() if len(df) > 0 else 'N/A',
        'best_value_city': df.groupby('city').apply(
            lambda x: x['consumer_clean'].mean() / x['price_clean'].mean() if x['price_clean'].mean() > 0 else 0
        ).idxmax() if len(df) > 0 else 'N/A'
    }


def calculate_host_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate host-focused metrics from the dataset.
    """
    return {
        'total_revenue': df['revenue_estimate'].sum() if len(df) > 0 else 0,
        'avg_occupancy': (df['sales'].mean() / 365 * 100) if len(df) > 0 else 0,
        'total_hosts': df['host_id'].nunique() if len(df) > 0 else 0,
        'avg_listings_per_host': df.groupby('host_id').size().mean() if len(df) > 0 else 0,
        'pct_certified': (df['host_certified'].sum() / len(df) * 100) if len(df) > 0 else 0,
        'best_city': df.groupby('city')['revenue_estimate'].sum().idxmax() if len(df) > 0 else 'N/A'
    }


def get_city_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get aggregated statistics per city.
    """
    return df.groupby('city').agg({
        'price_clean': 'mean',
        'consumer_clean': 'mean',
        'total reviewers number': 'sum',
        'bedrooms': 'mean',
        'bathrooms_clean': 'mean',
        'guest_favourite': 'mean',
        'revenue_estimate': 'sum',
        'sales': 'mean',
        'id': 'count'
    }).rename(columns={
        'price_clean': 'avg_price',
        'consumer_clean': 'avg_rating',
        'total reviewers number': 'total_reviews',
        'bedrooms': 'avg_bedrooms',
        'bathrooms_clean': 'avg_bathrooms',
        'guest_favourite': 'pct_guest_favourite',
        'revenue_estimate': 'total_revenue',
        'sales': 'avg_sales',
        'id': 'listing_count'
    }).reset_index()


def get_area_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get aggregated statistics per area.
    """
    return df.groupby('area').agg({
        'price_clean': 'mean',
        'consumer_clean': 'mean',
        'revenue_estimate': 'sum',
        'sales': 'sum',
        'id': 'count'
    }).rename(columns={
        'price_clean': 'avg_price',
        'consumer_clean': 'avg_rating',
        'revenue_estimate': 'total_revenue',
        'sales': 'total_sales',
        'id': 'listing_count'
    }).reset_index()
