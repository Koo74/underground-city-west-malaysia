"""
Advanced GeoAI Agent - West Malaysia Underground City Site Selection v3.0
========================================================================
CYBERPUNK EDITION: Futuristic UI + OSM Up-to-Date + INSTANT Results
PHASE 2-5: Infrastructure Planning, Cost Analysis, Construction AI, Public Engagement

FOCUSED ON: UNDERGROUND CITY SITE SELECTION IN PENINSULAR (WEST) MALAYSIA 🏙️

NEW:
- ✅ USGS Earthquake API — real seismic data
- ✅ OneGeology WMS — geological map layer + text summary
- ✅ Simple OpenStreetMap / Satellite toggle
- ✅ FIXED: "Critical" count in summary now correctly counts only Critical-priority actions
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MiniMap, MousePosition, Draw, HeatMap
from folium import raster_layers
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from functools import wraps
import requests
from pathlib import Path
import sqlite3
import pickle
import math
import threading
import queue
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CYBERPUNK STYLING
# ============================================================================

CYBERPUNK_CSS = """
<style>
    :root {
        --neon-cyan: #00f0ff;
        --neon-pink: #ff2d95;
        --neon-purple: #b026ff;
        --neon-green: #39ff14;
        --neon-yellow: #ffe84d;
    }
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a1f 100%); }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.3);
        letter-spacing: 4px; animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 40px rgba(0, 240, 255, 0.3); }
        50% { text-shadow: 0 0 60px rgba(0, 240, 255, 0.6), 0 0 80px rgba(176, 38, 255, 0.3); }
    }
    .subtitle {
        font-family: 'Courier New', monospace; color: #00f0ff;
        font-size: 1.2rem; letter-spacing: 8px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .phase-badge {
        display: inline-block; padding: 4px 15px; border-radius: 20px;
        font-family: 'Courier New', monospace; font-size: 0.7rem;
        letter-spacing: 2px; text-transform: uppercase; font-weight: bold;
        margin: 0 5px; border: 1px solid;
    }
    .phase-badge-2 { color: #00f0ff; border-color: #00f0ff; background: rgba(0,240,255,0.05); }
    .phase-badge-3 { color: #39ff14; border-color: #39ff14; background: rgba(57,255,20,0.05); }
    .phase-badge-4 { color: #ffe84d; border-color: #ffe84d; background: rgba(255,232,77,0.05); }
    .phase-badge-5 { color: #ff2d95; border-color: #ff2d95; background: rgba(255,45,149,0.05); }
    .css-1d391kg, .css-1633s9g {
        background: rgba(10, 10, 20, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    .css-1d391kg p, .css-1633s9g p,
    .css-1d391kg label, .css-1633s9g label,
    .css-1d391kg div, .css-1633s9g div,
    .css-1d391kg span, .css-1633s9g span {
        color: #ffffff !important; font-weight: 400 !important;
    }
    .recommendation-container {
        background: rgba(15, 15, 35, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px; padding: 20px; margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
    }
    .recommendation-container:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }
    .recommendation-title {
        color: #00f0ff; font-family: 'Courier New', monospace;
        font-size: 1.2rem; font-weight: bold; letter-spacing: 2px;
        margin-bottom: 10px; text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    .recommendation-item {
        color: #ffffff; font-family: 'Courier New', monospace;
        font-size: 0.9rem; padding: 6px 0;
        border-bottom: 1px solid rgba(0, 240, 255, 0.05);
        line-height: 1.6;
    }
    .recommendation-item:last-child { border-bottom: none; }
    .recommendation-item .icon { margin-right: 8px; }
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(176, 38, 255, 0.15)) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important; text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px);
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.3), rgba(176, 38, 255, 0.3)) !important;
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3) !important;
        transform: scale(1.02); color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(176, 38, 255, 0.25)) !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }
    [data-testid="metric-container"] {
        background: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 10px; padding: 15px; backdrop-filter: blur(5px);
    }
    [data-testid="metric-container"] label {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px; font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] div {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    .dataframe {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    .dataframe th {
        color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.1) !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px; font-weight: bold !important; font-size: 0.9rem !important;
    }
    .dataframe td {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderHeader {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important; color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px; font-weight: bold !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.1) !important;
        border-top: none !important;
    }
    .streamlit-expanderContent p, .streamlit-expanderContent div,
    .streamlit-expanderContent li, .streamlit-expanderContent span {
        color: #ffffff !important;
    }
    .stAlert {
        background: rgba(15, 15, 35, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    .stAlert p, .stAlert div, .stAlert li, .stAlert span { color: #ffffff !important; }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px; text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00f0ff !important;
        border-bottom: 2px solid #00f0ff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        font-weight: bold !important;
    }
    .cyber-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00f0ff, #b026ff, #ff2d95, transparent);
        margin: 20px 0; opacity: 0.5;
    }
    .stMarkdown p, .stMarkdown li {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        line-height: 1.6 !important;
    }
    .stMarkdown h1 { color: #00f0ff !important; }
    .stMarkdown h2 { color: #b026ff !important; }
    .stMarkdown h3 { color: #ff2d95 !important; }
    .stMarkdown h4 { color: #39ff14 !important; }
    .folium-map {
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.05);
    }
    .stRadio label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }
    .stRadio [role="radiogroup"] { gap: 8px; }
</style>

<div class="scanlines"></div>
<div class="vignette"></div>
"""

# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

def generate_recommendation_strategy(result_data: Dict) -> Dict:
    score = result_data.get('suitability_percentage', 0)
    details = result_data.get('details', {})
    elevation_m = result_data.get('elevation_m', 0)
    flood_risk = result_data.get('flood_risk', 'Unknown')
    population_density = result_data.get('population_density', 0)
    coastal_distance = result_data.get('coastal_distance_km', 0)
    bedrock_depth = result_data.get('bedrock_depth_m', 50)
    water_table = result_data.get('water_table_depth_m', 10)
    seismic_risk = result_data.get('seismic_risk', 'Low')

    recommendations = {
        'immediate_actions': [],
        'short_term_actions': [],
        'long_term_actions': [],
        'investment_required': 'Low',
        'overall_feasibility': 'High',
        'risk_level': 'Low',
        'timeline_summary': {}
    }

    def add_action(bucket, text, priority, cost):
        recommendations[bucket].append({
            'text': text, 'priority': priority, 'cost': cost
        })

    if elevation_m < 20:
        add_action('immediate_actions',
            '🚨 CRITICAL: Low elevation (<20m). Flood risk is high for underground structures. Consider extensive waterproofing.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif elevation_m < 50:
        add_action('short_term_actions',
            '🌊 Moderate elevation (20-50m). Need flood defenses and drainage for underground construction.',
            'High', '💸💸💸')
        recommendations['investment_required'] = 'Moderate'
    elif elevation_m < 200:
        add_action('immediate_actions',
            '✅ Good elevation (50-200m). Minimal flood risk for underground structures.',
            'Low', '💸')
    elif elevation_m < 500:
        add_action('short_term_actions',
            '⛰️ High elevation (200-500m). Good for underground city - natural protection from surface flooding.',
            'Medium', '💸💸')
    else:
        add_action('short_term_actions',
            '🏔️ Very high elevation (500m+). Excellent for underground city - stable foundation.',
            'Low', '💸💸')

    if bedrock_depth < 20:
        add_action('immediate_actions',
            '🪨 SHALLOW BEDROCK (0-20m). Excellent for underground excavation. Minimal rock removal.',
            'Low', '💸')
    elif bedrock_depth < 50:
        add_action('immediate_actions',
            '🪨 GOOD BEDROCK DEPTH (20-50m). Suitable for underground city construction.',
            'Low', '💸💸')
    elif bedrock_depth < 100:
        add_action('short_term_actions',
            '🪨 DEEP BEDROCK (50-100m). Significant excavation required. Consider advanced tunneling methods.',
            'Medium', '💸💸💸')
    else:
        add_action('long_term_actions',
            '🪨 VERY DEEP BEDROCK (100m+). Major excavation project. Long construction timeline.',
            'High', '💸💸💸💸')

    if water_table < 10:
        add_action('immediate_actions',
            '💧 SHALLOW WATER TABLE (0-10m). Groundwater issues expected. Need robust dewatering systems.',
            'Critical', '💸💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Very High'
    elif water_table < 30:
        add_action('short_term_actions',
            '💧 MODERATE WATER TABLE (10-30m). Standard dewatering and waterproofing needed.',
            'High', '💸💸💸')
        if recommendations['investment_required'] == 'Low':
            recommendations['investment_required'] = 'Moderate'
    else:
        add_action('immediate_actions',
            '💧 DEEP WATER TABLE (30m+). Excellent for underground construction. Minimal groundwater issues.',
            'Low', '💸')

    if population_density > 5:
        add_action('immediate_actions',
            '🏙️ HIGH POPULATION DENSITY (5+ people/km²). Land acquisition costs high. Consider underground city near existing infrastructure.',
            'High', '💸💸💸💸')
    elif population_density > 2:
        add_action('short_term_actions',
            '🏘️ MODERATE POPULATION (2-5 people/km²). Balanced approach - underground city can serve surrounding communities.',
            'Medium', '💸💸💸')
    else:
        add_action('immediate_actions',
            '✅ VERY LOW POPULATION (<2 people/km²). Ideal for underground city development. Abundant space.',
            'Low', '💸')

    if seismic_risk == 'High':
        add_action('immediate_actions',
            '🌋 HIGH SEISMIC RISK! Underground structures must be earthquake-resistant. Special engineering required.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif seismic_risk == 'Moderate':
        add_action('short_term_actions',
            '🌋 MODERATE SEISMIC RISK. Design underground city with seismic resilience.',
            'High', '💸💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'High'
    else:
        add_action('immediate_actions',
            '✅ LOW SEISMIC RISK. Safe for underground city construction.',
            'Low', '💸')

    if coastal_distance < 5:
        add_action('immediate_actions',
            '🌊 COASTAL PROXIMITY (0-5km). Accessible for construction materials. Consider tsunami protection for underground city.',
            'High', '💸💸💸')
    elif coastal_distance < 30:
        add_action('short_term_actions',
            '🚢 NEAR COAST (5-30km). Good access for materials. Balanced location.',
            'Medium', '💸💸')
    else:
        add_action('long_term_actions',
            '🚛 INLAND (30+km). Better protection from sea-level rise. May require dedicated transport infrastructure.',
            'Low', '💸💸')

    land_details = details.get('land_availability', {}).get('value', {})
    if isinstance(land_details, dict):
        forest = land_details.get('forest_areas', 0)
        developed = land_details.get('developed_areas', 0)
        if forest > 20 and developed < 5:
            add_action('immediate_actions',
                '🌳 ABUNDANT LAND (20+ forest areas). Excellent for underground city development.',
                'Low', '💸')
        elif forest > 10 and developed < 10:
            add_action('short_term_actions',
                '🌿 GOOD LAND AVAILABILITY. Sufficient space for underground city footprint.',
                'Medium', '💸💸')
        else:
            add_action('immediate_actions',
                '🏗️ LIMITED LAND. Need to acquire additional land for underground city infrastructure.',
                'High', '💸💸💸💸')

    if flood_risk == 'High':
        add_action('immediate_actions',
            '🌊 HIGH FLOOD RISK! Underground city must have extensive flood protection systems.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif flood_risk == 'Moderate':
        add_action('short_term_actions',
            '🌊 MODERATE FLOOD RISK. Standard flood protection for underground structures.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'

    infra_details = details.get('infrastructure_access', {}).get('value', {})
    if isinstance(infra_details, dict):
        if infra_details.get('airports', 0) == 0:
            add_action('short_term_actions',
                '✈️ No airport nearby. Build airstrip for personnel transport.',
                'High', '💸💸💸')
        if infra_details.get('major_roads', 0) == 0:
            add_action('short_term_actions',
                '🛣️ No major roads. Build access roads for construction equipment.',
                'High', '💸💸💸')
        if infra_details.get('ports', 0) == 0:
            add_action('long_term_actions',
                '🚢 No port. Consider building a small port for heavy equipment delivery.',
                'Medium', '💸💸💸💸')
        if infra_details.get('power_facilities', 0) == 0:
            add_action('long_term_actions',
                '⚡ No power infrastructure. Build power plant or connect to grid.',
                'High', '💸💸💸💸')

    # Count only REAL Critical actions (not all immediate actions)
    critical_count = sum(1 for a in recommendations['immediate_actions'] if a['priority'] == 'Critical')
    high_count = sum(1 for a in recommendations['short_term_actions'] if a['priority'] == 'High')
    total_actions = (len(recommendations['immediate_actions']) +
                     len(recommendations['short_term_actions']) +
                     len(recommendations['long_term_actions']))

    if score >= 80:
        score_band, score_emoji = 'Excellent', '✅'
    elif score >= 65:
        score_band, score_emoji = 'Good', '👍'
    elif score >= 50:
        score_band, score_emoji = 'Moderate', '👌'
    elif score >= 35:
        score_band, score_emoji = 'Limited', '⚠️'
    else:
        score_band, score_emoji = 'Poor', '❌'

    if critical_count >= 3:
        feasibility = '❌ Poor - Major critical issues must be resolved before development'
        risk_level = 'Very High'
    elif critical_count == 2:
        feasibility = '⚠️ Limited - Multiple critical issues require resolution'
        risk_level = 'High'
    elif critical_count == 1:
        feasibility = '👌 Moderate - One critical issue requires resolution'
        risk_level = 'High'
    elif high_count >= 2:
        feasibility = '👌 Moderate - Several high-priority preparations required'
        risk_level = 'Medium'
    else:
        feasibility = f'{score_emoji} {score_band} - ' + {
            'Excellent': 'Highly suitable for underground city development',
            'Good': 'Suitable with minor site preparation',
            'Moderate': 'Significant investment required',
            'Limited': 'Major investment required',
            'Poor': 'Not recommended for underground city development',
        }[score_band]
        risk_level = {
            'Excellent': 'Low', 'Good': 'Low',
            'Moderate': 'Medium', 'Limited': 'High', 'Poor': 'Very High',
        }[score_band]

    recommendations['overall_feasibility'] = feasibility
    recommendations['risk_level'] = risk_level
    recommendations['critical_action_count'] = critical_count
    recommendations['high_action_count'] = high_count
    recommendations['total_action_count'] = total_actions
    recommendations['timeline_summary'] = {
        'immediate': f"{len(recommendations['immediate_actions'])} actions (0-6 months)",
        'short_term': f"{len(recommendations['short_term_actions'])} actions (6-18 months)",
        'long_term': f"{len(recommendations['long_term_actions'])} actions (18-36 months)"
    }
    return recommendations

# ============================================================================
# CACHE
# ============================================================================

class APICache:
    def __init__(self, cache_dir: str = "west_malaysia_underground_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    def _get_cache_key(self, url, params):
        return hashlib.md5((url + json.dumps(params, sort_keys=True)).encode()).hexdigest()
    def get(self, url, params):
        cf = self.cache_dir / f"{self._get_cache_key(url, params)}.json"
        if cf.exists():
            mt = datetime.fromtimestamp(cf.stat().st_mtime)
            if datetime.now() - mt < self.ttl:
                try:
                    with open(cf, 'r') as f: return json.load(f)
                except: return None
        return None
    def set(self, url, params, data):
        cf = self.cache_dir / f"{self._get_cache_key(url, params)}.json"
        try:
            with open(cf, 'w') as f: json.dump(data, f)
        except: pass
    def clear(self):
        for f in self.cache_dir.glob("*.json"): f.unlink()
    def get_stats(self):
        return {'total_cached': len(list(self.cache_dir.glob("*.json"))), 'cache_dir': str(self.cache_dir)}

api_cache = APICache()

# ============================================================================
# LOCATION DATA - COMPLETE WEST MALAYSIA
# ============================================================================

WEST_MALAYSIA_LOCATIONS = {
    'Kangar (Perlis)': (6.4414, 100.1986),
    'Arau (Perlis)': (6.4297, 100.2703),
    'Padang Besar (Perlis)': (6.6601, 100.3244),
    'Kuala Perlis (Perlis)': (6.4000, 100.1300),
    'Chuping (Perlis)': (6.5000, 100.2600),
    'Wang Kelian (Perlis)': (6.6800, 100.1700),
    'Beseri (Perlis)': (6.4700, 100.2200),
    'Simpang Empat (Perlis)': (6.4600, 100.2100),
    'Alor Setar (Kedah)': (6.1248, 100.3678),
    'Sungai Petani (Kedah)': (5.6470, 100.4877),
    'Kulim (Kedah)': (5.3649, 100.5600),
    'Langkawi (Kedah)': (6.3500, 99.8000),
    'Kuah (Langkawi)': (6.3265, 99.8430),
    'Pantai Cenang (Langkawi)': (6.2930, 99.7250),
    'Teluk Ewa (Langkawi)': (6.4000, 99.9000),
    'Datai Bay (Langkawi)': (6.4700, 99.6800),
    'Baling (Kedah)': (5.6800, 100.9200),
    'Sik (Kedah)': (5.8200, 100.7400),
    'Pendang (Kedah)': (6.0000, 100.4700),
    'Jitra (Kedah)': (6.2683, 100.4225),
    'Yan (Kedah)': (5.8000, 100.3700),
    'Gurun (Kedah)': (5.8200, 100.4700),
    'Bedong (Kedah)': (5.7300, 100.5200),
    'Kuala Nerang (Kedah)': (6.1500, 100.6000),
    'George Town (Penang)': (5.4141, 100.3288),
    'Bayan Lepas (Penang)': (5.2950, 100.2700),
    'Batu Ferringhi (Penang)': (5.4750, 100.2400),
    'Balik Pulau (Penang)': (5.3500, 100.2300),
    'Butterworth (Penang)': (5.3990, 100.3630),
    'Bukit Mertajam (Penang)': (5.3630, 100.4670),
    'Nibong Tebal (Penang)': (5.1700, 100.4800),
    'Teluk Bahang (Penang)': (5.4600, 100.2100),
    'Gertak Sanggul (Penang)': (5.2700, 100.2000),
    'Batu Maung (Penang)': (5.2800, 100.2900),
    'Teluk Kumbar (Penang)': (5.2900, 100.2400),
    'Pulau Betong (Penang)': (5.3300, 100.2000),
    'Ipoh (Perak)': (4.5975, 101.0901),
    'Taiping (Perak)': (4.8500, 100.7333),
    'Teluk Intan (Perak)': (4.0259, 101.0214),
    'Kuala Kangsar (Perak)': (4.7700, 100.9400),
    'Lumut (Perak)': (4.2300, 100.6300),
    'Pangkor Island (Perak)': (4.2200, 100.5600),
    'Sitiawan (Perak)': (4.2200, 100.7000),
    'Batu Gajah (Perak)': (4.4700, 101.0400),
    'Kampar (Perak)': (4.3100, 101.1500),
    'Tapah (Perak)': (4.2000, 101.2600),
    'Tanjung Malim (Perak)': (3.6800, 101.5200),
    'Gerik (Perak)': (5.4300, 101.1300),
    'Lenggong (Perak)': (5.1000, 100.9700),
    'Pengkalan Hulu (Perak)': (5.7000, 100.9900),
    'Segari (Perak)': (4.2800, 100.6000),
    'Pantai Remis (Perak)': (4.4500, 100.6300),
    'Gopeng (Perak)': (4.4300, 101.1600),
    'Shah Alam (Selangor)': (3.0733, 101.5185),
    'Petaling Jaya (Selangor)': (3.1073, 101.6067),
    'Subang Jaya (Selangor)': (3.0567, 101.5850),
    'Klang (Selangor)': (3.0333, 101.4500),
    'Port Klang (Selangor)': (3.0000, 101.4000),
    'Kuala Selangor (Selangor)': (3.3500, 101.2500),
    'Kuala Kubu Bharu (Selangor)': (3.5600, 101.6400),
    'Rawang (Selangor)': (3.3200, 101.5800),
    'Sepang (Selangor)': (2.7000, 101.7500),
    'Banting (Selangor)': (2.8100, 101.5000),
    'Morib (Selangor)': (2.7500, 101.4400),
    'Tanjung Sepat (Selangor)': (2.6600, 101.5600),
    'Sekinchan (Selangor)': (3.5100, 101.1000),
    'Sabak Bernam (Selangor)': (3.7700, 100.9800),
    'Kajang (Selangor)': (2.9900, 101.7900),
    'Bangi (Selangor)': (2.9500, 101.7800),
    'Putrajaya (FT)': (2.9264, 101.6964),
    'Cyberjaya (Selangor)': (2.9200, 101.6500),
    'Puchong (Selangor)': (3.0000, 101.6200),
    'Batang Kali (Selangor)': (3.4700, 101.6500),
    'Carey Island (Selangor)': (2.8700, 101.3800),
    'Pulau Ketam (Selangor)': (3.0200, 101.2500),
    'Pulau Carey (Selangor)': (2.8800, 101.3500),
    'Pulau Indah (Selangor)': (2.9800, 101.3200),
    'Kuala Langat (Selangor)': (2.8500, 101.4500),
    'Kuala Lumpur City Centre': (3.1390, 101.6869),
    'KLCC (KL)': (3.1578, 101.7120),
    'Bukit Bintang (KL)': (3.1450, 101.7100),
    'Cheras (KL)': (3.0800, 101.7300),
    'Kepong (KL)': (3.2100, 101.6400),
    'Sungai Besi (KL)': (3.0600, 101.7000),
    'Batu Caves (Selangor)': (3.2379, 101.6840),
    'Seremban (N. Sembilan)': (2.7297, 101.9381),
    'Port Dickson (N. Sembilan)': (2.5228, 101.7967),
    'Nilai (N. Sembilan)': (2.8200, 101.8000),
    'Bahau (N. Sembilan)': (2.8000, 102.4000),
    'Tampin (N. Sembilan)': (2.4700, 102.2300),
    'Kuala Pilah (N. Sembilan)': (2.7400, 102.2500),
    'Rembau (N. Sembilan)': (2.5900, 102.0900),
    'Gemas (N. Sembilan)': (2.5800, 102.6100),
    'Lukut (N. Sembilan)': (2.5800, 101.8300),
    'Tanjung Tuan (N. Sembilan)': (2.4000, 101.8500),
    'Blue Lagoon (N. Sembilan)': (2.4800, 101.8300),
    'Linggi (N. Sembilan)': (2.4800, 102.0000),
    'Kuala Klawang (N. Sembilan)': (2.8200, 102.0400),
    'Melaka City (Melaka)': (2.1896, 102.2501),
    'Ayer Keroh (Melaka)': (2.2700, 102.2900),
    'Alor Gajah (Melaka)': (2.3800, 102.2100),
    'Jasin (Melaka)': (2.3100, 102.4300),
    'Masjid Tanah (Melaka)': (2.3500, 102.1100),
    'Merlimau (Melaka)': (2.1400, 102.4300),
    'Tanjung Kling (Melaka)': (2.2200, 102.1600),
    'Tanjung Bidara (Melaka)': (2.2800, 102.0900),
    'Pengkalan Balak (Melaka)': (2.3200, 102.0800),
    'Kuala Sungai Baru (Melaka)': (2.3500, 102.0400),
    'Johor Bahru (Johor)': (1.4927, 103.7414),
    'Iskandar Puteri (Johor)': (1.4300, 103.6300),
    'Kulai (Johor)': (1.6600, 103.6000),
    'Skudai (Johor)': (1.5400, 103.6700),
    'Senai (Johor)': (1.6200, 103.6600),
    'Pasir Gudang (Johor)': (1.4700, 103.9000),
    'Pengerang (Johor)': (1.3600, 104.1700),
    'Kota Tinggi (Johor)': (1.7300, 103.9000),
    'Mersing (Johor)': (2.4300, 103.8300),
    'Batu Pahat (Johor)': (1.8500, 102.9300),
    'Muar (Johor)': (2.0500, 102.5700),
    'Segamat (Johor)': (2.5100, 102.8100),
    'Kluang (Johor)': (2.0300, 103.3200),
    'Pontian (Johor)': (1.4800, 103.3800),
    'Desaru (Johor)': (1.5500, 104.2600),
    'Endau (Johor)': (2.6500, 103.6200),
    'Pulau Aur (Johor)': (2.4500, 104.5200),
    'Pulau Pemanggil (Johor)': (2.5800, 104.3300),
    'Pulau Sibu (Johor)': (2.2000, 104.1000),
    'Pulau Tinggi (Johor)': (2.3000, 104.1200),
    'Pulau Rawa (Johor)': (2.5300, 103.9700),
    'Pulau Kukup (Johor)': (1.3100, 103.4200),
    'Tanjung Piai (Johor)': (1.2700, 103.5100),
    'Labis (Johor)': (2.3800, 103.0200),
    'Yong Peng (Johor)': (2.0100, 103.0600),
    'Ayer Hitam (Johor)': (1.9200, 103.1800),
    'Kota Bharu (Kelantan)': (6.1256, 102.2386),
    'Kubang Kerian (Kelantan)': (6.1000, 102.2800),
    'Pasir Puteh (Kelantan)': (5.8300, 102.4000),
    'Pasir Mas (Kelantan)': (6.0500, 102.1400),
    'Tumpat (Kelantan)': (6.2000, 102.1700),
    'Bachok (Kelantan)': (6.0700, 102.4000),
    'Tanah Merah (Kelantan)': (5.8000, 102.1500),
    'Machang (Kelantan)': (5.7700, 102.2100),
    'Kuala Krai (Kelantan)': (5.5300, 102.2000),
    'Gua Musang (Kelantan)': (4.8800, 101.9600),
    'Jeli (Kelantan)': (5.7000, 101.8400),
    'Tok Bali (Kelantan)': (5.8200, 102.4500),
    'Pantai Cahaya Bulan (Kelantan)': (6.1300, 102.2900),
    'Kuala Terengganu (Terengganu)': (5.3303, 103.1408),
    'Kuala Nerus (Terengganu)': (5.3800, 103.0800),
    'Kemaman (Terengganu)': (4.2300, 103.4200),
    'Chukai (Terengganu)': (4.2200, 103.4200),
    'Kerteh (Terengganu)': (4.5200, 103.4500),
    'Paka (Terengganu)': (4.6400, 103.4400),
    'Dungun (Terengganu)': (4.7700, 103.4200),
    'Marang (Terengganu)': (5.2000, 103.2100),
    'Kuala Berang (Terengganu)': (5.0700, 102.9500),
    'Jerteh (Terengganu)': (5.7400, 102.5100),
    'Besut (Terengganu)': (5.7300, 102.5600),
    'Setiu (Terengganu)': (5.5800, 102.8000),
    'Kuala Besut (Terengganu)': (5.8300, 102.5600),
    'Pulau Perhentian (Terengganu)': (5.9100, 102.7400),
    'Pulau Redang (Terengganu)': (5.7800, 103.0000),
    'Pulau Kapas (Terengganu)': (5.2200, 103.2600),
    'Pulau Tenggol (Terengganu)': (4.8000, 103.6800),
    'Pulau Lang Tengah (Terengganu)': (5.7800, 102.8900),
    'Kijal (Terengganu)': (4.3600, 103.5000),
    'Kuantan (Pahang)': (3.8077, 103.3260),
    'Pekan (Pahang)': (3.4900, 103.3900),
    'Temerloh (Pahang)': (3.4500, 102.4200),
    'Bentong (Pahang)': (3.5200, 101.9100),
    'Raub (Pahang)': (3.7900, 101.8600),
    'Kuala Lipis (Pahang)': (4.1800, 102.0500),
    'Jerantut (Pahang)': (3.9400, 102.3600),
    'Mentakab (Pahang)': (3.4900, 102.3500),
    'Cameron Highlands (Pahang)': (4.4700, 101.3800),
    'Genting Highlands (Pahang)': (3.4200, 101.7900),
    'Fraser\'s Hill (Pahang)': (3.7100, 101.7400),
    'Tioman Island (Pahang)': (2.7900, 104.1700),
    'Cherating (Pahang)': (4.1300, 103.3900),
    'Balok (Pahang)': (3.9500, 103.3700),
    'Beserah (Pahang)': (3.8800, 103.3600),
    'Sungai Lembing (Pahang)': (3.9200, 103.0300),
    'Gambang (Pahang)': (3.7100, 103.0900),
    'Maran (Pahang)': (3.5800, 102.7700),
    'Kuala Rompin (Pahang)': (2.8200, 103.4800),
    'Nenasi (Pahang)': (2.9900, 103.4900),
    'Gebeng (Pahang)': (3.9600, 103.3700),
    'Bukit Ibam (Pahang)': (3.3000, 102.8500),
    'Lanchang (Pahang)': (3.5000, 102.2000),
    'Janda Baik (Pahang)': (3.3200, 101.8800),
}

WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES = {
    'Cameron Highlands (Pahang)': (4.4700, 101.3800),
    'Fraser\'s Hill (Pahang)': (3.7100, 101.7400),
    'Genting Highlands (Pahang)': (3.4200, 101.7900),
    'Bukit Tinggi (Pahang)': (3.4000, 101.8200),
    'Janda Baik (Pahang)': (3.3200, 101.8800),
    'Kuala Lipis (Pahang)': (4.1800, 102.0500),
    'Jerantut (Pahang)': (3.9400, 102.3600),
    'Sungai Lembing (Pahang)': (3.9200, 103.0300),
    'Bukit Ibam (Pahang)': (3.3000, 102.8500),
    'Lanchang (Pahang)': (3.5000, 102.2000),
    'Maran (Pahang)': (3.5800, 102.7700),
    'Gopeng (Perak)': (4.4300, 101.1600),
    'Gerik (Perak)': (5.4300, 101.1300),
    'Lenggong (Perak)': (5.1000, 100.9700),
    'Pengkalan Hulu (Perak)': (5.7000, 100.9900),
    'Kuala Kangsar (Perak)': (4.7700, 100.9400),
    'Tapah (Perak)': (4.2000, 101.2600),
    'Kampar (Perak)': (4.3100, 101.1500),
    'Gua Musang (Kelantan)': (4.8800, 101.9600),
    'Kuala Krai (Kelantan)': (5.5300, 102.2000),
    'Dabong (Kelantan)': (5.3800, 102.0100),
    'Jeli (Kelantan)': (5.7000, 101.8400),
    'Batang Kali (Selangor)': (3.4700, 101.6500),
    'Kuala Kubu Bharu (Selangor)': (3.5600, 101.6400),
    'Pulau Carey (Selangor)': (2.8800, 101.3500),
    'Pulau Ketam (Selangor)': (3.0200, 101.2500),
    'Kuala Klawang (N. Sembilan)': (2.8200, 102.0400),
    'Bahau (N. Sembilan)': (2.8000, 102.4000),
    'Gemas (N. Sembilan)': (2.5800, 102.6100),
    'Labis (Johor)': (2.3800, 103.0200),
    'Segamat (Johor)': (2.5100, 102.8100),
    'Yong Peng (Johor)': (2.0100, 103.0600),
    'Ayer Hitam (Johor)': (1.9200, 103.1800),
    'Kluang Rural (Johor)': (2.0300, 103.3200),
    'Pulau Aur (Johor)': (2.4500, 104.5200),
    'Pulau Pemanggil (Johor)': (2.5800, 104.3300),
    'Pulau Tioman (Pahang)': (2.7900, 104.1700),
    'Baling (Kedah)': (5.6800, 100.9200),
    'Sik (Kedah)': (5.8200, 100.7400),
    'Pendang (Kedah)': (6.0000, 100.4700),
    'Wang Kelian (Perlis)': (6.6800, 100.1700),
    'Padang Besar (Perlis)': (6.6601, 100.3244),
    'Kuala Berang (Terengganu)': (5.0700, 102.9500),
    'Setiu (Terengganu)': (5.5800, 102.8000),
    'Pulau Tenggol (Terengganu)': (4.8000, 103.6800),
    'Pulau Redang (Terengganu)': (5.7800, 103.0000),
    'Pulau Perhentian (Terengganu)': (5.9100, 102.7400),
    'Pulau Kapas (Terengganu)': (5.2200, 103.2600),
    'Pulau Lang Tengah (Terengganu)': (5.7800, 102.8900),
}

STATIC_AIRPORTS = {
    'Langkawi International': (6.3297, 99.7287),
    'Sultan Abdul Halim (Alor Setar)': (6.1897, 100.3982),
    'Kangar Airport': (6.4500, 100.2000),
    'Penang International': (5.2972, 100.2768),
    'Butterworth Air Base': (5.4000, 100.3700),
    'Sultan Azlan Shah (Ipoh)': (4.5679, 101.0920),
    'Taiping Airport': (4.8667, 100.7167),
    'Pulau Pangkor Airstrip': (4.2200, 100.5500),
    'Lumut RMAF Base': (4.2300, 100.6200),
    'Sultan Abdul Aziz Shah (Subang)': (3.1306, 101.5493),
    'KLIA (Sepang)': (2.7456, 101.7099),
    'KLIA2 (Sepang)': (2.7430, 101.6860),
    'Melaka International': (2.2633, 102.2517),
    'Senai International (JB)': (1.6411, 103.6696),
    'Batu Pahat Airport': (1.8500, 102.9300),
    'Mersing Airport': (2.4300, 103.8300),
    'Sultan Ahmad Shah (Kuantan)': (3.7753, 103.2090),
    'Tioman Airport': (2.8183, 104.1600),
    'Sultan Mahmud (K. Terengganu)': (5.3825, 103.1033),
    'Kerteh Airport': (4.5200, 103.4500),
    'Sultan Ismail Petra (Kota Bharu)': (6.1664, 102.2924),
    'Tok Bali Airstrip': (5.8200, 102.4500),
    'Gua Musang Airstrip': (4.8800, 101.9600),
}

STATIC_SETTLEMENTS = {
    'Kangar': {'coords': (6.4414, 100.1986), 'population': 50000},
    'Arau': {'coords': (6.4297, 100.2703), 'population': 30000},
    'Alor Setar': {'coords': (6.1248, 100.3678), 'population': 400000},
    'Sungai Petani': {'coords': (5.6470, 100.4877), 'population': 300000},
    'Kulim': {'coords': (5.3649, 100.5600), 'population': 150000},
    'Langkawi': {'coords': (6.3500, 99.8000), 'population': 90000},
    'Baling': {'coords': (5.6800, 100.9200), 'population': 30000},
    'George Town': {'coords': (5.4141, 100.3288), 'population': 700000},
    'Butterworth': {'coords': (5.3990, 100.3630), 'population': 200000},
    'Bukit Mertajam': {'coords': (5.3630, 100.4670), 'population': 200000},
    'Bayan Lepas': {'coords': (5.2950, 100.2700), 'population': 150000},
    'Ipoh': {'coords': (4.5975, 101.0901), 'population': 750000},
    'Taiping': {'coords': (4.8500, 100.7333), 'population': 200000},
    'Teluk Intan': {'coords': (4.0259, 101.0214), 'population': 100000},
    'Kuala Kangsar': {'coords': (4.7700, 100.9400), 'population': 50000},
    'Lumut': {'coords': (4.2300, 100.6300), 'population': 40000},
    'Sitiawan': {'coords': (4.2200, 100.7000), 'population': 150000},
    'Shah Alam': {'coords': (3.0733, 101.5185), 'population': 700000},
    'Petaling Jaya': {'coords': (3.1073, 101.6067), 'population': 800000},
    'Subang Jaya': {'coords': (3.0567, 101.5850), 'population': 700000},
    'Klang': {'coords': (3.0333, 101.4500), 'population': 900000},
    'Kuala Lumpur': {'coords': (3.1390, 101.6869), 'population': 1800000},
    'Putrajaya': {'coords': (2.9264, 101.6964), 'population': 100000},
    'Cyberjaya': {'coords': (2.9200, 101.6500), 'population': 100000},
    'Sepang': {'coords': (2.7000, 101.7500), 'population': 90000},
    'Kajang': {'coords': (2.9900, 101.7900), 'population': 300000},
    'Bangi': {'coords': (2.9500, 101.7800), 'population': 200000},
    'Kuala Selangor': {'coords': (3.3500, 101.2500), 'population': 40000},
    'Kuala Kubu Bharu': {'coords': (3.5600, 101.6400), 'population': 30000},
    'Rawang': {'coords': (3.3200, 101.5800), 'population': 200000},
    'Banting': {'coords': (2.8100, 101.5000), 'population': 40000},
    'Sekinchan': {'coords': (3.5100, 101.1000), 'population': 15000},
    'Sabak Bernam': {'coords': (3.7700, 100.9800), 'population': 30000},
    'Seremban': {'coords': (2.7297, 101.9381), 'population': 500000},
    'Port Dickson': {'coords': (2.5228, 101.7967), 'population': 100000},
    'Nilai': {'coords': (2.8200, 101.8000), 'population': 100000},
    'Bahau': {'coords': (2.8000, 102.4000), 'population': 30000},
    'Tampin': {'coords': (2.4700, 102.2300), 'population': 30000},
    'Kuala Pilah': {'coords': (2.7400, 102.2500), 'population': 20000},
    'Melaka City': {'coords': (2.1896, 102.2501), 'population': 500000},
    'Ayer Keroh': {'coords': (2.2700, 102.2900), 'population': 60000},
    'Alor Gajah': {'coords': (2.3800, 102.2100), 'population': 40000},
    'Jasin': {'coords': (2.3100, 102.4300), 'population': 30000},
    'Johor Bahru': {'coords': (1.4927, 103.7414), 'population': 1500000},
    'Iskandar Puteri': {'coords': (1.4300, 103.6300), 'population': 500000},
    'Kulai': {'coords': (1.6600, 103.6000), 'population': 200000},
    'Pasir Gudang': {'coords': (1.4700, 103.9000), 'population': 200000},
    'Pengerang': {'coords': (1.3600, 104.1700), 'population': 30000},
    'Kota Tinggi': {'coords': (1.7300, 103.9000), 'population': 50000},
    'Mersing': {'coords': (2.4300, 103.8300), 'population': 30000},
    'Batu Pahat': {'coords': (1.8500, 102.9300), 'population': 300000},
    'Muar': {'coords': (2.0500, 102.5700), 'population': 200000},
    'Segamat': {'coords': (2.5100, 102.8100), 'population': 80000},
    'Kluang': {'coords': (2.0300, 103.3200), 'population': 150000},
    'Pontian': {'coords': (1.4800, 103.3800), 'population': 50000},
    'Desaru': {'coords': (1.5500, 104.2600), 'population': 15000},
    'Kota Bharu': {'coords': (6.1256, 102.2386), 'population': 500000},
    'Kubang Kerian': {'coords': (6.1000, 102.2800), 'population': 50000},
    'Pasir Puteh': {'coords': (5.8300, 102.4000), 'population': 30000},
    'Pasir Mas': {'coords': (6.0500, 102.1400), 'population': 40000},
    'Tumpat': {'coords': (6.2000, 102.1700), 'population': 30000},
    'Bachok': {'coords': (6.0700, 102.4000), 'population': 20000},
    'Kuala Krai': {'coords': (5.5300, 102.2000), 'population': 20000},
    'Gua Musang': {'coords': (4.8800, 101.9600), 'population': 15000},
    'Kuala Terengganu': {'coords': (5.3303, 103.1408), 'population': 400000},
    'Kemaman': {'coords': (4.2300, 103.4200), 'population': 60000},
    'Chukai': {'coords': (4.2200, 103.4200), 'population': 40000},
    'Kerteh': {'coords': (4.5200, 103.4500), 'population': 20000},
    'Paka': {'coords': (4.6400, 103.4400), 'population': 15000},
    'Dungun': {'coords': (4.7700, 103.4200), 'population': 40000},
    'Marang': {'coords': (5.2000, 103.2100), 'population': 20000},
    'Kuala Berang': {'coords': (5.0700, 102.9500), 'population': 15000},
    'Jerteh': {'coords': (5.7400, 102.5100), 'population': 30000},
    'Besut': {'coords': (5.7300, 102.5600), 'population': 25000},
    'Setiu': {'coords': (5.5800, 102.8000), 'population': 15000},
    'Kuantan': {'coords': (3.8077, 103.3260), 'population': 600000},
    'Pekan': {'coords': (3.4900, 103.3900), 'population': 50000},
    'Temerloh': {'coords': (3.4500, 102.4200), 'population': 100000},
    'Bentong': {'coords': (3.5200, 101.9100), 'population': 60000},
    'Raub': {'coords': (3.7900, 101.8600), 'population': 50000},
    'Kuala Lipis': {'coords': (4.1800, 102.0500), 'population': 20000},
    'Jerantut': {'coords': (3.9400, 102.3600), 'population': 30000},
    'Mentakab': {'coords': (3.4900, 102.3500), 'population': 40000},
    'Cameron Highlands': {'coords': (4.4700, 101.3800), 'population': 40000},
    'Genting Highlands': {'coords': (3.4200, 101.7900), 'population': 30000},
    'Kuala Rompin': {'coords': (2.8200, 103.4800), 'population': 20000},
    'Cherating': {'coords': (4.1300, 103.3900), 'population': 10000},
    'Balok': {'coords': (3.9500, 103.3700), 'population': 15000},
    'Gambang': {'coords': (3.7100, 103.0900), 'population': 20000},
    'Maran': {'coords': (3.5800, 102.7700), 'population': 15000},
}

UNDERGROUND_CITY_TAGS = {
    'hospital': [('amenity', 'hospital'), ('amenity', 'clinic')],
    'airport': [('aeroway', 'aerodrome'), ('aeroway', 'airport'), ('aeroway', 'heliport')],
    'port': [('harbour', 'yes'), ('amenity', 'ferry_terminal'), ('waterway', 'port')],
    'power_plant': [('power', 'plant'), ('power', 'substation'), ('power', 'generator')],
    'road': [('highway', 'motorway'), ('highway', 'trunk'), ('highway', 'primary')],
    'railway': [('railway', 'rail'), ('railway', 'station')],
    'telecom': [('telecom', 'tower'), ('telecom', 'exchange'), ('man_made', 'tower')],
    'population_center': [('place', 'city'), ('place', 'town'), ('place', 'village')],
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Location:
    lat: float
    lon: float
    name: str = ""
    properties: Dict = field(default_factory=dict)

@dataclass
class AnalysisStep:
    step_number: int
    name: str
    description: str
    status: str = "pending"
    result: Any = None
    execution_time: float = 0.0
    reasoning: str = ""

@dataclass
class AnalysisResult:
    query: str
    steps: List[AnalysisStep] = field(default_factory=list)
    final_result: Any = None
    total_time: float = 0.0
    timestamp: str = ""
    success: bool = False

@dataclass
class MemoryEntry:
    query: str
    query_embedding: List[float] = field(default_factory=list)
    result_summary: str = ""
    success: bool = False
    execution_time: float = 0.0
    timestamp: str = ""
    parameters_used: Dict = field(default_factory=dict)

# ============================================================================
# MEMORY REPOSITORY
# ============================================================================

class MemoryRepository:
    def __init__(self, db_path: str = "west_malaysia_underground_city_memory.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL, query_hash TEXT NOT NULL,
                result_summary TEXT, success INTEGER, execution_time REAL,
                parameters TEXT, timestamp TEXT, embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL, parameter_name TEXT NOT NULL,
                optimal_value TEXT, success_rate REAL,
                usage_count INTEGER DEFAULT 1, last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_analysis(self, entry: MemoryEntry):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query_hash = hashlib.md5(entry.query.lower().encode()).hexdigest()
        cursor.execute("""
            INSERT INTO analysis_memory
            (query, query_hash, result_summary, success, execution_time, parameters, timestamp, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (entry.query, query_hash, entry.result_summary,
              1 if entry.success else 0, entry.execution_time,
              json.dumps(entry.parameters_used), entry.timestamp,
              pickle.dumps(entry.query_embedding)))
        conn.commit()
        conn.close()

    def get_all_analyses(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        results = [{
            'query': row[1], 'result_summary': row[3],
            'success': bool(row[4]), 'execution_time': row[5],
            'parameters': json.loads(row[6]) if row[6] else {},
            'timestamp': row[7]
        } for row in rows]
        conn.close()
        return results

    def find_similar_analyses(self, query: str, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        if not query or not query.strip():
            conn.close(); return []
        keywords = query.lower().split()
        results = []
        for row in rows:
            stored_query = row[1].lower()
            match_score = sum(1 for kw in keywords if kw in stored_query)
            if match_score > 0:
                results.append({
                    'query': row[1], 'result_summary': row[3],
                    'success': bool(row[4]), 'execution_time': row[5],
                    'parameters': json.loads(row[6]) if row[6] else {},
                    'timestamp': row[7], 'match_score': match_score
                })
        conn.close()
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:limit]

    def get_learned_parameter(self, analysis_type: str, parameter_name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT optimal_value FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ?
            ORDER BY success_rate DESC LIMIT 1
        """, (analysis_type, parameter_name))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def update_learned_parameter(self, analysis_type: str, parameter_name: str,
                                  value: str, success: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, success_rate, usage_count FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ? AND optimal_value = ?
        """, (analysis_type, parameter_name, value))
        row = cursor.fetchone()
        if row:
            new_count = row[2] + 1
            new_rate = ((row[1] * row[2]) + (1 if success else 0)) / new_count
            cursor.execute("""
                UPDATE learned_parameters
                SET success_rate = ?, usage_count = ?, last_updated = ?
                WHERE id = ?
            """, (new_rate, new_count, datetime.now().isoformat(), row[0]))
        else:
            cursor.execute("""
                INSERT INTO learned_parameters
                (analysis_type, parameter_name, optimal_value, success_rate, usage_count, last_updated)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (analysis_type, parameter_name, value,
                  1.0 if success else 0.0, datetime.now().isoformat()))
        conn.commit(); conn.close()

    def get_analysis_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_memory")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM analysis_memory WHERE success = 1")
        successful = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(execution_time) FROM analysis_memory")
        avg_time = cursor.fetchone()[0] or 0
        conn.close()
        return {
            'total_analyses': total, 'successful_analyses': successful,
            'success_rate': successful / total if total > 0 else 0,
            'avg_execution_time': avg_time
        }

# ============================================================================
# ANALYSIS STRATEGY
# ============================================================================

class AnalysisStrategy(ABC):
    @abstractmethod
    def analyse(self, location: Location, params: Dict) -> Dict: pass
    @abstractmethod
    def get_name(self) -> str: pass


class UndergroundCitySuitabilityStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Underground City Suitability Analysis (HYBRID + USGS + OneGeology)"

    def _get_elevation_quick(self, location: Location) -> tuple:
        try:
            url = f"https://api.open-elevation.com/api/v1/lookup?locations={location.lat},{location.lon}"
            r = requests.get(url, timeout=3)
            elev = r.json()['results'][0]['elevation']
            if 100 <= elev <= 500: return 5.0, elev, 'Live Elevation API - Optimal underground elevation'
            elif 50 <= elev < 100: return 4.5, elev, 'Live Elevation API - Good underground elevation'
            elif 500 < elev <= 1000: return 4.0, elev, 'Live Elevation API - High elevation, stable'
            elif 20 <= elev < 50: return 3.5, elev, 'Live Elevation API - Moderate elevation'
            elif 0 <= elev < 20: return 2.0, elev, 'Live Elevation API - Low elevation, flood risk'
            else: return 3.0, elev, 'Live Elevation API - Very high elevation'
        except Exception:
            lat, lon = location.lat, location.lon
            if 3.3 < lat < 4.7 and 101.3 < lon < 101.9:
                return 4.5, 1200, 'Fallback: Titiwangsa highlands - excellent underground site'
            elif lat > 4.5 and 101.5 < lon < 102.5:
                return 3.5, 250, 'Fallback: Kelantan interior - moderate site'
            elif 3.5 < lat < 4.6 and 101.9 < lon < 102.8:
                return 3.5, 300, 'Fallback: Pahang interior - moderate site'
            elif lat < 2.5 and 102.5 < lon < 103.8:
                return 3.0, 80, 'Fallback: Johor interior'
            else:
                return 3.0, 30, 'Fallback: Coastal lowland'

    def _estimate_bedrock_depth(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if 3.3 < lat < 4.7 and 101.3 < lon < 101.9:
            return 5.0, 8, 'Geographic: Titiwangsa Range - shallow bedrock'
        elif 5.5 < lat < 6.5 and 100.3 < lon < 101.0:
            return 4.5, 15, 'Geographic: Kedah interior - shallow bedrock'
        elif 4.5 < lat < 5.5 and 100.9 < lon < 101.5:
            return 4.5, 12, 'Geographic: Perak interior - limestone geology'
        elif 4.5 < lat < 6.0 and 101.5 < lon < 102.5:
            return 4.5, 20, 'Geographic: Kelantan/Pahang highlands - good bedrock'
        elif 3.5 < lat < 4.5 and 101.9 < lon < 103.0:
            return 4.0, 25, 'Geographic: Pahang interior - moderate bedrock'
        elif lat < 2.5 and 102.5 < lon < 104.0:
            return 4.0, 30, 'Geographic: Johor interior - moderate bedrock'
        else:
            return 3.0, 50, 'Geographic: Coastal lowland - deeper bedrock'

    def _estimate_water_table(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if 3.3 < lat < 4.7 and 101.3 < lon < 101.9:
            return 5.0, 60, 'Geographic: Titiwangsa highlands - deep water table'
        elif 5.5 < lat < 6.5 and 100.3 < lon < 101.0:
            return 4.5, 45, 'Geographic: Kedah interior - deep water table'
        elif 4.5 < lat < 5.5 and 100.9 < lon < 101.5:
            return 4.5, 50, 'Geographic: Perak interior - deep water table'
        elif 4.5 < lat < 6.0 and 101.5 < lon < 102.5:
            return 4.5, 50, 'Geographic: Kelantan/Pahang highlands - deep water table'
        elif 3.5 < lat < 4.5 and 101.9 < lon < 103.0:
            return 4.0, 40, 'Geographic: Pahang interior - deep water table'
        elif lat < 2.5 and 102.5 < lon < 104.0:
            return 4.0, 40, 'Geographic: Johor interior - deep water table'
        else:
            return 2.5, 10, 'Geographic: Coastal lowland - shallow water table'

    def _get_seismic_usgs(self, location: Location) -> Optional[Dict]:
        try:
            url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
            params = {
                "format": "geojson",
                "latitude": location.lat,
                "longitude": location.lon,
                "maxradiuskm": 200,
                "starttime": "1975-01-01",
                "minmagnitude": 3.0,
                "orderby": "magnitude",
            }
            r = requests.get(url, params=params, timeout=8)
            data = r.json()
            features = data.get('features', [])
            magnitudes = [f['properties']['mag'] for f in features if f['properties'].get('mag') is not None]
            count = len(magnitudes)
            max_mag = max(magnitudes) if magnitudes else 0.0
            return {
                'count': count,
                'max_magnitude': round(max_mag, 2),
                'source': 'USGS Earthquake API (Live)',
                'radius_km': 200,
                'period': '1975-present',
            }
        except Exception:
            return None

    def _estimate_seismic_risk(self, location: Location) -> tuple:
        usgs = self._get_seismic_usgs(location)
        if usgs is not None:
            count = usgs['count']
            max_mag = usgs['max_magnitude']
            if count == 0:
                score, risk = 5.0, 'Low'
                note = 'USGS: No M3.0+ earthquakes within 200km (1975-present)'
            elif count <= 5 and max_mag < 4.0:
                score, risk = 4.5, 'Low'
                note = f"USGS: {count} minor events, max M{max_mag}"
            elif count <= 20 and max_mag < 4.5:
                score, risk = 4.0, 'Low'
                note = f"USGS: {count} events, max M{max_mag}"
            elif count <= 50 and max_mag < 5.0:
                score, risk = 3.5, 'Moderate'
                note = f"USGS: {count} events, max M{max_mag}"
            elif count <= 100:
                score, risk = 3.0, 'Moderate'
                note = f"USGS: {count} events, max M{max_mag}"
            elif count <= 300 and max_mag < 6.0:
                score, risk = 2.5, 'High'
                note = f"USGS: {count} events, max M{max_mag}"
            else:
                score, risk = 2.0, 'High'
                note = f"USGS: {count} events, max M{max_mag} — active zone"
            return score, risk, note
        else:
            lat, lon = location.lat, location.lon
            if lat > 5.5 and lon < 100.5:
                return 4.5, 'Low', 'Geographic fallback: Northern West Malaysia'
            elif lat > 3.5 and lon > 103.0:
                return 4.0, 'Low', 'Geographic fallback: East Coast'
            elif lat < 2.5 and lon < 103.0:
                return 4.0, 'Moderate', 'Geographic fallback: Southern (near Sumatra fault)'
            else:
                return 4.5, 'Low', 'Geographic fallback: Peninsular Malaysia'

    def _get_onegeology_summary(self, location: Location) -> Optional[Dict]:
        try:
            wms_url = "https://portal.onegeology.org/OneGeologyGlobal/WMS/1.3.0"
            params = {
                "SERVICE": "WMS", "VERSION": "1.3.0", "REQUEST": "GetFeatureInfo",
                "LAYERS": "World_CGMW", "QUERY_LAYERS": "World_CGMW",
                "INFO_FORMAT": "text/plain", "I": 50, "J": 50,
                "WIDTH": 101, "HEIGHT": 101, "CRS": "EPSG:4326",
                "BBOX": f"{location.lat-0.1},{location.lon-0.1},{location.lat+0.1},{location.lon+0.1}",
            }
            r = requests.get(wms_url, params=params, timeout=8)
            if r.status_code != 200:
                return None
            text = r.text.strip()
            if text and "Geology" not in text and len(text) < 5000:
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                summary = lines[0][:120] if lines else 'Regional geology available'
                return {'source': 'OneGeology WMS (Live)', 'summary': summary, 'raw_length': len(text)}
            return None
        except Exception:
            return None

    def _geographic_score_coastal(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if lon > 103.0: return 3.5, 5, 'Geographic: East coast - good for access'
        elif lon > 102.5: return 3.0, 15, 'Geographic: Near east coast - balanced'
        elif lon > 101.5: return 4.0, 40, 'Geographic: Central (inland) - safer from sea-level rise'
        elif lon > 100.5: return 3.5, 25, 'Geographic: Near west coast - balanced'
        else: return 3.0, 10, 'Geographic: West coast (Strait of Malacca)'

    def _geographic_score_population(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            dist = self._haversine(lat, lon, s_lat, s_lon)
            min_dist = min(min_dist, dist)
        if min_dist > 50: return 5.0, 0, 'Geographic: Remote - ideal for underground city'
        elif min_dist > 30: return 4.5, 1, 'Geographic: Rural - good isolation'
        elif min_dist > 20: return 4.0, 2, 'Geographic: Semi-rural - balanced'
        elif min_dist > 10: return 3.0, 5, 'Geographic: Near town - accessible'
        else: return 2.0, 10, 'Geographic: Near city - land expensive'

    def _geographic_score_infrastructure(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, coords in STATIC_AIRPORTS.items():
            d = self._haversine(lat, lon, coords[0], coords[1])
            min_dist = min(min_dist, d)
        details = {
            'airports': 1 if min_dist < 60 else 0,
            'major_roads': 2 if min_dist < 30 else 0,
            'ports': 0, 'power_facilities': 0
        }
        if min_dist < 30: return 4.5, details, 'Geographic: Near airport - good access'
        elif min_dist < 60: return 4.0, details, 'Geographic: Airport nearby - accessible'
        elif min_dist < 100: return 3.0, details, 'Geographic: Some access - moderate'
        else: return 2.5, details, 'Geographic: Remote - access challenges'

    def _geographic_score_land(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            d = self._haversine(lat, lon, data['coords'][0], data['coords'][1])
            min_dist = min(min_dist, d)
        details = {
            'forest_areas': 30 if min_dist > 30 else 10,
            'developed_areas': 2 if min_dist > 30 else 10,
            'agriculture': 5
        }
        if min_dist > 50: return 5.0, details, 'Geographic: Abundant land - perfect'
        elif min_dist > 30: return 4.5, details, 'Geographic: Good land - suitable'
        elif min_dist > 20: return 4.0, details, 'Geographic: Moderate land - enough space'
        elif min_dist > 10: return 3.0, details, 'Geographic: Limited land - constrained'
        else: return 2.0, details, 'Geographic: Scarce land - difficult'

    def _geographic_score_flood(self, elevation_m: float) -> tuple:
        if elevation_m > 200: return 5.0, 'Low'
        elif elevation_m > 100: return 4.5, 'Low'
        elif elevation_m > 50: return 4.0, 'Low'
        elif elevation_m > 20: return 3.0, 'Moderate'
        else: return 1.5, 'High'

    def _geographic_score_geology(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if 3.3 < lat < 4.7 and 101.3 < lon < 101.9:
            return 5.0, 'Geographic: Titiwangsa Range - excellent granite geology'
        elif 4.5 < lat < 5.5 and 100.9 < lon < 101.5:
            return 4.5, 'Geographic: Perak limestone - karst geology'
        elif 4.5 < lat < 6.0 and 101.5 < lon < 102.5:
            return 4.5, 'Geographic: Kelantan limestone - karst caves'
        elif 3.5 < lat < 4.5 and 101.9 < lon < 103.0:
            return 4.0, 'Geographic: Pahang interior - mixed geology'
        elif 5.5 < lat < 6.5 and 100.3 < lon < 101.0:
            return 4.0, 'Geographic: Kedah interior - sedimentary rocks'
        else:
            return 3.5, 'Geographic: Peninsular Malaysia - variable geology'

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(min(1, math.sqrt(a)))

    def _try_osm_in_background(self, location: Location, radius: int) -> Optional[Dict]:
        try:
            url = "https://overpass-api.de/api/interpreter"
            results = {}
            q = f'[out:json][timeout:5];(node["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon});way["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon}););out count;'
            results['airport_count'] = len(requests.post(url, data={'data': q}, timeout=5).json().get('elements', []))
            return results
        except Exception:
            return None

    def analyse(self, location: Location, params: Dict) -> Dict:
        radius = params.get('radius', 10000)
        weights = params.get('weights', {
            'elevation': 0.15, 'bedrock_depth': 0.15, 'water_table_depth': 0.12,
            'seismic_risk': 0.08, 'geology': 0.12, 'population_density': 0.10,
            'coastal_proximity': 0.08, 'infrastructure_access': 0.10,
            'land_availability': 0.05, 'flood_risk': 0.05
        })

        scores, details = {}, {}
        data_source_details = []
        osm_available = False

        elevation_score, elevation_m, elev_source = self._get_elevation_quick(location)
        scores['elevation'] = elevation_score
        details['elevation'] = {'score': elevation_score, 'value': f"{elevation_m:.0f}m",
                                'weight': weights['elevation'], 'source': elev_source}
        data_source_details.append(f"Elevation: {elev_source}")

        bedrock_score, bedrock_m, bedrock_source = self._estimate_bedrock_depth(location)
        scores['bedrock_depth'] = bedrock_score
        details['bedrock_depth'] = {'score': bedrock_score, 'value': f"{bedrock_m:.0f}m",
                                    'weight': weights['bedrock_depth'], 'source': bedrock_source}
        data_source_details.append(f"Bedrock: {bedrock_source}")

        water_score, water_m, water_source = self._estimate_water_table(location)
        scores['water_table_depth'] = water_score
        details['water_table_depth'] = {'score': water_score, 'value': f"{water_m:.0f}m",
                                        'weight': weights['water_table_depth'], 'source': water_source}
        data_source_details.append(f"Water Table: {water_source}")

        seismic_score, seismic_risk, seismic_source = self._estimate_seismic_risk(location)
        scores['seismic_risk'] = seismic_score
        details['seismic_risk'] = {'score': seismic_score, 'value': seismic_risk,
                                   'weight': weights['seismic_risk'], 'source': seismic_source}
        data_source_details.append(f"Seismic: {seismic_source}")

        geology_score, geology_source = self._geographic_score_geology(location)
        scores['geology'] = geology_score
        details['geology'] = {'score': geology_score, 'value': 'Underground construction',
                              'weight': weights['geology'], 'source': geology_source}
        data_source_details.append(f"Geology: {geology_source}")

        onegeo = self._get_onegeology_summary(location)
        if onegeo:
            data_source_details.append(f"🗺️ OneGeology: {onegeo['summary']}")

        pop_score, pop_density, pop_source = self._geographic_score_population(location)
        scores['population_density'] = pop_score
        details['population_density'] = {'score': pop_score, 'value': f"{pop_density:.1f} people/km²",
                                         'weight': weights['population_density'], 'source': pop_source}
        data_source_details.append(f"Population: {pop_source}")

        coastal_score, dist_coast, coastal_source = self._geographic_score_coastal(location)
        scores['coastal_proximity'] = coastal_score
        details['coastal_proximity'] = {'score': coastal_score, 'value': f"{dist_coast:.1f}km",
                                        'weight': weights['coastal_proximity'], 'source': coastal_source}
        data_source_details.append(f"Coastal: {coastal_source}")

        infra_score, infra_details, infra_source = self._geographic_score_infrastructure(location)
        scores['infrastructure_access'] = infra_score
        details['infrastructure_access'] = {'score': infra_score, 'value': infra_details,
                                            'weight': weights['infrastructure_access'], 'source': infra_source}
        data_source_details.append(f"Infrastructure: {infra_source}")

        land_score, land_details, land_source = self._geographic_score_land(location)
        scores['land_availability'] = land_score
        details['land_availability'] = {'score': land_score, 'value': land_details,
                                        'weight': weights['land_availability'], 'source': land_source}
        data_source_details.append(f"Land: {land_source}")

        flood_score, flood_risk = self._geographic_score_flood(elevation_m)
        scores['flood_risk'] = flood_score
        details['flood_risk'] = {'score': flood_score, 'value': flood_risk,
                                 'weight': weights['flood_risk'], 'source': 'From elevation'}

        total_score = sum(scores[k] * weights.get(k, 0) for k in scores if k in weights)
        max_possible = sum(weights.values()) * 5.0
        percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0

        penalty = 0.0
        penalty_reasons = []
        if elevation_m < 20:
            penalty += 12.0
            penalty_reasons.append(f"Very low elevation ({elevation_m:.0f}m): -12%")
        if flood_risk == 'High':
            penalty += 10.0
            penalty_reasons.append("High flood risk: -10%")
        if pop_density > 5:
            penalty += 8.0
            penalty_reasons.append("High population density: -8%")
        if water_m < 10:
            penalty += 15.0
            penalty_reasons.append(f"Shallow water table ({water_m:.0f}m): -15%")
        if seismic_risk == 'High':
            penalty += 12.0
            penalty_reasons.append("High seismic risk: -12%")
        if bedrock_m > 100:
            penalty += 8.0
            penalty_reasons.append("Very deep bedrock: -8%")

        percentage = max(0.0, min(100.0, percentage - penalty))

        if percentage >= 80:
            rating, emoji, rec = 'Excellent', '🏙️', 'Highly suitable for underground city development'
        elif percentage >= 65:
            rating, emoji, rec = 'Good', '👍', 'Suitable with minor site preparation'
        elif percentage >= 50:
            rating, emoji, rec = 'Moderate', '👌', 'Suitable with significant site preparation'
        elif percentage >= 35:
            rating, emoji, rec = 'Limited', '⚠️', 'Marginal - requires major investment'
        else:
            rating, emoji, rec = 'Poor', '❌', 'Not recommended for underground city development'

        try:
            osm_data = self._try_osm_in_background(location, radius)
            if osm_data and any(v > 0 for v in osm_data.values()):
                osm_available = True
                data_source_details.append(f"🌐 OSM Background: {osm_data.get('airport_count', 0)} airports")
        except Exception:
            pass

        return {
            'success': True, 'scores': scores, 'details': details,
            'weighted_score': total_score, 'max_possible_score': max_possible,
            'suitability_percentage': round(percentage, 1),
            'base_percentage': round((total_score / max_possible * 100) if max_possible > 0 else 0, 1),
            'penalty_applied': round(penalty, 1),
            'penalty_reasons': penalty_reasons,
            'rating': rating, 'rating_emoji': emoji, 'recommendation': rec,
            'radius_used': radius,
            'location': f"{location.name or 'West Malaysia location'} ({location.lat:.4f}, {location.lon:.4f})",
            'elevation_m': elevation_m, 'bedrock_depth_m': bedrock_m,
            'water_table_depth_m': water_m, 'seismic_risk': seismic_risk,
            'population_density': pop_density, 'coastal_distance_km': dist_coast,
            'flood_risk': flood_risk,
            'data_source_details': data_source_details,
            'used_osm': osm_available,
            'used_usgs': seismic_source.startswith('USGS'),
            'used_onegeology': onegeo is not None,
            'used_fallback': True, 'from_cache': False,
            'analysis_method': 'HYBRID: Geographic + USGS + OneGeology + OSM'
        }


class ProximityAnalysisStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Proximity Analysis"

    def analyse(self, location: Location, params: Dict) -> Dict:
        amenity_type = params.get('amenity_type', 'hospital')
        radius = params.get('radius', 5000)
        tags = UNDERGROUND_CITY_TAGS.get(amenity_type, [('amenity', amenity_type)])
        parts = []
        for k, v in tags:
            parts.append(f'node["{k}"="{v}"](around:{radius},{location.lat},{location.lon});')
            parts.append(f'way["{k}"="{v}"](around:{radius},{location.lat},{location.lon});')
        query = f"[out:json][timeout:45];({chr(10).join(parts)});out center;"
        try:
            r = requests.post("https://overpass-api.de/api/interpreter",
                              data={'data': query},
                              headers={'User-Agent': 'WMSpaceportGeoAI/1.0'}, timeout=45)
            r.raise_for_status()
            results, seen = [], set()
            for elem in r.json().get('elements', []):
                lat = elem.get('lat') or elem.get('center', {}).get('lat')
                lon = elem.get('lon') or elem.get('center', {}).get('lon')
                if lat and lon:
                    key = f"{round(lat,5)}_{round(lon,5)}"
                    if key not in seen:
                        seen.add(key)
                        tags_d = elem.get('tags', {})
                        results.append({
                            'name': tags_d.get('name', tags_d.get('brand', 'Unknown')),
                            'lat': lat, 'lon': lon, 'type': amenity_type, 'tags': tags_d
                        })
            return {'success': True, 'count': len(results), 'amenities': results,
                    'radius': radius, 'amenity_type': amenity_type,
                    'location': f"West Malaysia ({location.lat:.4f}, {location.lon:.4f})"}
        except Exception as e:
            return {'success': False, 'error': str(e), 'amenities': [],
                    'count': 0, 'radius': radius, 'amenity_type': amenity_type}


class StrategySelector:
    _strategies = {'underground_city': UndergroundCitySuitabilityStrategy,
                   'proximity': ProximityAnalysisStrategy}

    @classmethod
    def get_strategy(cls, t: str) -> AnalysisStrategy:
        c = cls._strategies.get(t)
        if not c: raise ValueError(f"Unknown strategy: {t}")
        return c()

# ============================================================================
# PIPELINE + RATE LIMITER
# ============================================================================

class PipelineStep:
    def __init__(self, name, processor, description=""):
        self.name = name; self.processor = processor
        self.description = description; self.execution_time = 0.0; self.result = None

class Pipeline:
    def __init__(self, name):
        self.name = name; self.steps = []; self.results = {}
        self.execution_log = []
    def add_step(self, s): self.steps.append(s); return self
    def execute(self, initial_data, progress_callback=None):
        current = initial_data.copy()
        total = len(self.steps)
        for i, step in enumerate(self.steps):
            a = AnalysisStep(step_number=i+1, name=step.name,
                             description=step.description, status="running")
            if progress_callback: progress_callback(i/total, f"Running: {step.name}")
            t0 = time.time()
            try:
                step.result = step.processor(current)
                current.update(step.result)
                self.results[step.name] = step.result
                step.execution_time = time.time() - t0
                a.status = "completed"; a.result = step.result
                a.execution_time = step.execution_time
                a.reasoning = f"Successfully processed {step.name}"
            except Exception as e:
                step.execution_time = time.time() - t0
                a.status = "failed"; a.reasoning = f"Error: {e}"
                self.execution_log.append(a); raise
            self.execution_log.append(a)
        if progress_callback: progress_callback(1.0, "Complete")
        return current

class RateLimiter:
    def __init__(self, calls_per_second=0.5):
        self.calls_per_second = calls_per_second; self.last_call = 0
    def wait(self):
        now = time.time()
        delta = now - self.last_call
        min_i = 1.0 / self.calls_per_second
        if delta < min_i: time.sleep(min_i - delta)
        self.last_call = time.time()

# ============================================================================
# AGENT
# ============================================================================

class WestMalaysiaUndergroundCityGeoAIAgent:
    def __init__(self):
        self.memory_repo = MemoryRepository()
        self.rate_limiter = RateLimiter(0.5)
        self.short_term_memory = {}
        self.current_analysis = None

    def reason_about_query(self, query: str) -> tuple:
        steps = [{'step': 'Understanding Query',
                  'reasoning': f"Analysing underground city request: '{query}'",
                  'action': 'parse_intent'}]
        similar = self.memory_repo.find_similar_analyses(query, 3)
        if similar:
            steps.append({'step': 'Memory Recall',
                          'reasoning': f"Found {len(similar)} similar past analyses.",
                          'action': 'apply_learned_parameters'})
        analysis_type = 'underground_city'
        steps.append({'step': 'Strategy Selection',
                      'reasoning': 'Using Underground City Suitability strategy.',
                      'action': 'use_underground_city_strategy'})
        lr = self.memory_repo.get_learned_parameter(analysis_type, 'radius')
        if lr:
            steps.append({'step': 'Parameter Optimisation',
                          'reasoning': f"Using learned radius {lr}m.",
                          'action': 'apply_learned_radius', 'value': lr})
        else:
            steps.append({'step': 'Parameter Selection',
                          'reasoning': 'Using default radius 10000m.',
                          'action': 'use_default_radius', 'value': '10000'})
        steps.append({'step': 'Execution Planning',
                      'reasoning': f'Will execute {analysis_type} analysis.',
                      'action': 'prepare_execution'})
        return steps, analysis_type

    def execute_analysis(self, location, query, params, progress_callback=None):
        t0 = time.time()
        result = AnalysisResult(query=query, timestamp=datetime.now().isoformat())
        reasoning, atype = self.reason_about_query(query)
        for i, si in enumerate(reasoning):
            result.steps.append(AnalysisStep(step_number=i+1, name=si['step'],
                                             description=si['reasoning'],
                                             status='completed', reasoning=si['reasoning']))
        if progress_callback: progress_callback(0.3, "Executing hybrid analysis...")
        try:
            strategy = StrategySelector.get_strategy(atype)
            self.rate_limiter.wait()
            ar = strategy.analyse(location, params)
            ar['from_cache'] = False
            if ar.get('success'):
                result.steps.append(AnalysisStep(
                    step_number=len(result.steps)+1, name="Data Source Validation",
                    description=f"Method: {ar.get('analysis_method','HYBRID')}",
                    status='completed',
                    reasoning=f"USGS={ar.get('used_usgs')}, OneGeology={ar.get('used_onegeology')}, OSM={ar.get('used_osm')}"))
            result.steps.append(AnalysisStep(
                step_number=len(result.steps)+1,
                name=f"Execute {strategy.get_name()}",
                description=f"Running {atype} on {location.name or 'location'}",
                status='completed' if ar.get('success') else 'failed',
                result=ar, reasoning=f"Returned {len(str(ar))} bytes"))
            result.final_result = ar
            result.success = ar.get('success', False)
        except Exception as e:
            result.steps.append(AnalysisStep(
                step_number=len(result.steps)+1, name="Analysis Execution",
                description="Executing spatial analysis", status='failed',
                reasoning=f"Error: {e}"))
            result.success = False
        if progress_callback: progress_callback(0.8, "Storing in memory...")
        result.total_time = time.time() - t0
        self.memory_repo.store_analysis(MemoryEntry(
            query=query,
            result_summary=str(result.final_result)[:500] if result.final_result else "",
            success=result.success, execution_time=result.total_time,
            timestamp=result.timestamp, parameters_used=params))
        if result.success:
            self.memory_repo.update_learned_parameter(
                atype, 'radius', str(params.get('radius', 10000)), True)
        self.short_term_memory['last_analysis'] = result
        self.short_term_memory['last_location'] = location
        if progress_callback: progress_callback(1.0, "Complete")
        return result

# ============================================================================
# PHASE 2-5 MODULES
# ============================================================================

@dataclass
class InfrastructurePlan:
    site_name: str
    cost_breakdown: Dict
    transport_network: Dict
    utility_systems: Dict
    timeline: Dict
    total_cost: float
    timeline_years: int

class CostEstimator:
    COST_FACTORS = {
        'excavation': {'hard_rock': 2000, 'soft_rock': 1200, 'soil': 500},
        'construction': {'basic': 3000, 'mid': 5000, 'luxury': 8000},
        'infrastructure': {'water': 500, 'power': 800, 'ventilation': 1200, 'transport': 1500, 'telecom': 400},
        'finishing': {'basic': 1500, 'mid': 3000, 'luxury': 5000}
    }
    def estimate(self, site_data: Dict, size_sqm: int = 1000000) -> Dict:
        elevation = site_data.get('elevation_m', 100)
        geology_score = site_data.get('scores', {}).get('geology', 3)
        if elevation > 500 and geology_score > 4:
            rock_type = 'hard_rock'
        elif elevation > 200:
            rock_type = 'soft_rock'
        else:
            rock_type = 'soil'
        excavation_cost = self.COST_FACTORS['excavation'][rock_type] * size_sqm
        construction_cost = self.COST_FACTORS['construction']['mid'] * size_sqm * 0.4
        infrastructure_cost = sum(self.COST_FACTORS['infrastructure'].values()) * size_sqm * 0.2
        finishing_cost = self.COST_FACTORS['finishing']['mid'] * size_sqm * 0.3
        bedrock_depth = site_data.get('bedrock_depth_m', 30)
        if bedrock_depth < 20: excavation_cost *= 0.7
        elif bedrock_depth > 80: excavation_cost *= 1.3
        water_table = site_data.get('water_table_depth_m', 30)
        if water_table < 15: infrastructure_cost *= 1.4
        total = excavation_cost + construction_cost + infrastructure_cost + finishing_cost
        return {
            'total_cost_rm': total, 'total_cost_billions': total / 1_000_000_000,
            'excavation': excavation_cost, 'construction': construction_cost,
            'infrastructure': infrastructure_cost, 'finishing': finishing_cost,
            'per_sqm_cost': total / size_sqm, 'size_sqm': size_sqm,
            'rock_type': rock_type,
            'breakdown': {
                'Excavation': excavation_cost / total * 100,
                'Construction': construction_cost / total * 100,
                'Infrastructure': infrastructure_cost / total * 100,
                'Finishing': finishing_cost / total * 100
            }
        }

class TransportPlanner:
    def plan_transport(self, site_data: Dict, population: int = 50000) -> Dict:
        if population > 100000:
            transport_type, network_length = 'metro', population * 0.002
        elif population > 50000:
            transport_type, network_length = 'light_rail', population * 0.0015
        else:
            transport_type, network_length = 'automated_pod', population * 0.001
        depth = site_data.get('elevation_m', 100)
        elevators = 8 if depth > 200 else 5 if depth > 100 else 3
        return {
            'primary_transport': transport_type,
            'network_length_km': network_length,
            'elevators': elevators,
            'stations': max(10, int(population / 5000)),
            'estimated_cost': network_length * 50_000_000,
            'environmental_impact': 'Low',
            'access_points': 4 + elevators,
            'emergency_exits': int(population / 10000)
        }

class UtilityDesigner:
    def design_utilities(self, site_data: Dict, population: int = 50000) -> Dict:
        water_needed = population * 150
        power_needed = population * 5
        air_needed = population * 10
        return {
            'water': {'daily_need_liters': water_needed, 'storage_capacity': water_needed * 3,
                      'recycling_rate': 95, 'source': 'Rainwater + Groundwater'},
            'power': {'peak_demand_mw': power_needed / 1000, 'storage_mwh': power_needed * 12 / 1000,
                      'sources': ['Geothermal 60%', 'Solar 30%', 'Grid 10%'], 'redundancy': 3},
            'ventilation': {'airflow_m3h': air_needed, 'heat_exchange_efficiency': 85,
                            'co2_scrubbers': True, 'oxygen_generation': True},
            'waste': {'recycling_rate': 90, 'composting': True, 'zero_discharge': True}
        }

class ConstructionSimulator:
    def simulate_construction(self, site_data: Dict, plan: Dict) -> Dict:
        size_sqm = 1000000
        depth = site_data.get('elevation_m', 100)
        phases = {
            'site_preparation': {'duration_months': 6, 'tasks': ['Surveying', 'Access roads', 'Surface facilities'], 'cost_percentage': 5},
            'excavation': {'duration_months': max(12, depth / 10), 'tasks': ['Tunnel boring', 'Rock removal', 'Shoring'], 'cost_percentage': 25},
            'structural': {'duration_months': max(18, size_sqm / 50000), 'tasks': ['Concrete work', 'Steel structures', 'Waterproofing'], 'cost_percentage': 30},
            'systems_installation': {'duration_months': 12, 'tasks': ['Ventilation', 'Power', 'Water', 'Communication'], 'cost_percentage': 20},
            'finishing': {'duration_months': 12, 'tasks': ['Lighting', 'Interior', 'Furnishing'], 'cost_percentage': 15},
            'testing': {'duration_months': 6, 'tasks': ['Systems testing', 'Safety checks', 'Commissioning'], 'cost_percentage': 5}
        }
        total_months = sum(p['duration_months'] for p in phases.values())
        return {
            'phases': phases, 'total_months': total_months, 'total_years': total_months / 12,
            'daily_progress': 100 / total_months / 30,
            'critical_path': ['excavation', 'structural', 'systems_installation'],
            'completion_probability': min(95, 100 - (1 / max(depth, 1) * 10)),
            'risk_factors': ['Geological unexpected conditions',
                             'Water ingress' if depth < 50 else 'Minimal',
                             'Equipment failures']
        }

class ResourceOptimizer:
    def optimize_resources(self, site_data: Dict, construction_plan: Dict) -> Dict:
        size_sqm = 1000000
        return {
            'materials': {
                'concrete': {'amount_m3': size_sqm * 0.3, 'unit': 'm³', 'cost_per_unit': 250, 'suppliers': ['Local', 'Regional']},
                'steel': {'amount_tonnes': size_sqm * 0.05, 'unit': 'tonnes', 'cost_per_unit': 3000, 'suppliers': ['Regional', 'Import']},
                'tunnel_segments': {'amount': int(size_sqm / 100), 'unit': 'segments', 'cost_per_unit': 15000, 'suppliers': ['Specialized']}
            },
            'labor': {'engineers': int(size_sqm / 10000), 'workers': int(size_sqm / 1000), 'specialists': int(size_sqm / 5000)},
            'equipment': {'tbm': 3, 'excavators': 10, 'cranes': 5, 'ventilation_systems': 20},
            'optimization_score': 85, 'waste_reduction': 15, 'cost_savings_percentage': 12
        }

class ProgressMonitor:
    def monitor_progress(self, site_data: Dict, timeline: Dict) -> Dict:
        total_months = 48
        return {
            'current_progress': 30,
            'monthly_progress': 100 / total_months,
            'status': 'On Track',
            'milestones': [
                {'name': 'Site Survey Complete', 'month': 2, 'status': 'Completed'},
                {'name': 'Excavation Start', 'month': 4, 'status': 'Completed'},
                {'name': 'First Chamber', 'month': 12, 'status': 'In Progress'},
                {'name': 'Structural Complete', 'month': 24, 'status': 'Pending'},
                {'name': 'Systems Installation', 'month': 36, 'status': 'Pending'},
                {'name': 'Commissioning', 'month': 48, 'status': 'Pending'}
            ]
        }

class VRWalkthroughGenerator:
    def generate_walkthrough(self, site_data: Dict, plan: Dict) -> Dict:
        return {
            'scenes': [
                {'name': 'Main Entrance', 'description': 'Welcome to the underground city', 'features': ['Elevators', 'Security', 'Information Center']},
                {'name': 'City Center', 'description': 'The heart of the underground city', 'features': ['Shopping', 'Parks', 'Restaurants']},
                {'name': 'Residential Zone', 'description': 'Modern underground apartments', 'features': ['Homes', 'Schools', 'Healthcare']},
                {'name': 'Transit Hub', 'description': 'Automated transport network', 'features': ['Trains', 'Pods', 'Accessible Design']},
                {'name': 'Agricultural Center', 'description': 'Hydroponic vertical farming', 'features': ['Fresh produce', 'Sustainable']}
            ],
            'vr_ready': True, 'estimated_size_mb': 200,
            'platforms': ['Oculus', 'HTC Vive', 'WebVR'],
            'interactive_elements': 25
        }

class PublicConsultation:
    def create_consultation(self, site_data: Dict) -> Dict:
        return {
            'survey_questions': [
                {'question': 'Do you support underground city development?', 'options': ['Yes', 'No', 'Need more information']},
                {'question': 'What features are most important?', 'options': ['Housing', 'Jobs', 'Parks', 'Transportation', 'Education']},
                {'question': 'Would you consider living underground?', 'options': ['Yes', 'Maybe', 'No', 'Need to see it']},
                {'question': 'Environmental concerns?', 'options': ['Forest preservation', 'Water usage', 'Energy', 'Wildlife']}
            ],
            'community_events': ['Town halls', 'Virtual tours', 'Information sessions', 'School programs', 'Open houses'],
            'feedback_channels': ['Web portal', 'Mobile app', 'Physical center', 'Social media', 'Email newsletter']
        }

class EducationSystem:
    def create_education_material(self, site_data: Dict) -> Dict:
        return {
            'modules': [
                {'title': 'Understanding Underground Living', 'topics': ['History', 'Benefits', 'Future'], 'target_audience': 'General Public', 'duration_hours': 2},
                {'title': 'Underground City Systems', 'topics': ['Life support', 'Energy', 'Water', 'Waste'], 'target_audience': 'Students', 'duration_hours': 4},
                {'title': 'Construction Technology', 'topics': ['Tunneling', 'Safety', 'Materials', 'Innovation'], 'target_audience': 'Engineers', 'duration_hours': 8},
                {'title': 'Sustainability Underground', 'topics': ['Green design', 'Climate resilience', 'Biodiversity'], 'target_audience': 'All ages', 'duration_hours': 3}
            ],
            'formats': ['Video', 'Interactive', 'Workshops', 'Online courses']
        }

class TourismPlanner:
    def plan_tourism(self, site_data: Dict) -> Dict:
        return {
            'attractions': [
                {'name': 'World\'s Largest Underground City', 'type': 'Landmark', 'visitors_per_year': 500000},
                {'name': 'Cave Cathedral', 'type': 'Natural Wonder', 'visitors_per_year': 300000},
                {'name': 'Underground Gardens', 'type': 'Eco-tourism', 'visitors_per_year': 200000},
                {'name': 'Transport Experience', 'type': 'Technology', 'visitors_per_year': 150000}
            ],
            'facilities': {'hotels': 3, 'restaurants': 15, 'museums': 2, 'visitor_centers': 2, 'shops': 20},
            'estimated_annual_revenue': 50_000_000,
            'jobs_created': 1000, 'sustainability_score': 95
        }

class MultiCountrySupport:
    COUNTRIES = {
        'Malaysia': {'currency': 'RM', 'regulations': 'MS1234:2024', 'labor_cost_factor': 1.0, 'material_cost_factor': 1.0},
        'Singapore': {'currency': 'SGD', 'regulations': 'SS EN 1997', 'labor_cost_factor': 2.5, 'material_cost_factor': 1.8},
        'China': {'currency': 'CNY', 'regulations': 'GB 50838', 'labor_cost_factor': 0.7, 'material_cost_factor': 0.8},
        'Japan': {'currency': 'JPY', 'regulations': 'JIS A 8319', 'labor_cost_factor': 2.2, 'material_cost_factor': 1.5}
    }
    def adapt_site_analysis(self, site_data: Dict, country: str) -> Dict:
        country_data = self.COUNTRIES.get(country, self.COUNTRIES['Malaysia'])
        adapted = site_data.copy()
        if 'cost_estimates' in adapted:
            adapted['cost_estimates']['total_cost'] *= country_data['labor_cost_factor']
            adapted['cost_estimates']['material_cost'] *= country_data['material_cost_factor']
        adapted['country'] = country
        adapted['regulations'] = country_data['regulations']
        adapted['currency'] = country_data['currency']
        return adapted

class MarsAdaptation:
    def adapt_for_mars(self, site_data: Dict) -> Dict:
        return {
            'mars_adaptation': {
                'pressure_vessels': True, 'radiation_shielding': '5m regolith cover',
                'atmosphere': 'Earth-like (O2 + N2)', 'temperature': '0°C stable',
                'gravity': '0.38g adjustment', 'day_night_cycle': '24h 37m simulation',
                'water_source': 'Subsurface ice mining', 'power_source': 'Nuclear + Solar',
                'food_production': 'Hydroponics + Algae', 'transport': 'Pressurized rovers',
                'construction_materials': 'Regolith-based concrete', 'life_support': '100% closed loop'
            },
            'similarities': {
                'underground_construction': '90% transferable', 'life_support': '95% transferable',
                'energy_systems': '85% transferable', 'water_recycling': '95% transferable',
                'food_production': '90% transferable'
            },
            'timeline': {
                'design': '2026-2030', 'prototype': '2030-2035',
                'mars_ready': '2035-2040', 'first_colony': '2040-2050'
            }
        }

class ClimateCrisisModule:
    def assess_climate_resilience(self, site_data: Dict) -> Dict:
        elevation = site_data.get('elevation_m', 100)
        sea_level_rise = {'2030': 0.2, '2050': 0.5, '2100': 1.5}
        return {
            'elevation_safety': elevation > 50,
            'flood_protection_needed': elevation < 50,
            'sea_level_rise_projection': sea_level_rise,
            'temperature_stability': 'Excellent (underground)',
            'extreme_weather_protection': 'Complete (underground)',
            'energy_resilience': 'Self-sufficient 95%',
            'water_resilience': 'Self-sufficient 100%',
            'food_resilience': 'Self-sufficient 90%',
            'overall_resilience_score': min(95, 80 + (elevation / 50)),
            'climate_refuge_capacity': 100000 if elevation > 50 else 0
        }

class AISwarm:
    def __init__(self):
        self.agents = []
    def create_swarm(self, num_agents: int = 5) -> Dict:
        agent_roles = ['Site Surveyor', 'Geological Analyst', 'Infrastructure Planner',
                       'Construction Manager', 'Public Relations']
        self.agents = []
        for i in range(min(num_agents, len(agent_roles))):
            self.agents.append({
                'id': f'Agent_{i+1}', 'role': agent_roles[i], 'status': 'Active',
                'specialty': f'Underground city {agent_roles[i].lower()}',
                'capabilities': ['AI vision', 'NLP', 'Predictive modeling']
            })
        return {'agents': self.agents, 'coordination_level': 'High',
                'redundancy': 3, 'self_healing': True, 'learning_rate': 0.95}

class EnhancedUndergroundCityDeveloper:
    def __init__(self):
        self.cost_estimator = CostEstimator()
        self.transport_planner = TransportPlanner()
        self.utility_designer = UtilityDesigner()
        self.construction_simulator = ConstructionSimulator()
        self.resource_optimizer = ResourceOptimizer()
        self.progress_monitor = ProgressMonitor()
        self.vr_generator = VRWalkthroughGenerator()
        self.public_consultation = PublicConsultation()
        self.education_system = EducationSystem()
        self.tourism_planner = TourismPlanner()
        self.multi_country = MultiCountrySupport()
        self.mars_adaptation = MarsAdaptation()
        self.climate_module = ClimateCrisisModule()
        self.ai_swarm = AISwarm()
    def develop_complete_city(self, site_data: Dict, population: int = 50000) -> Dict:
        return {
            'phase_1_site_selection': {'site_data': site_data,
                                       'suitability_score': site_data.get('suitability_percentage', 0)},
            'phase_2_infrastructure': {
                'cost_estimate': self.cost_estimator.estimate(site_data),
                'transport_plan': self.transport_planner.plan_transport(site_data, population),
                'utility_plan': self.utility_designer.design_utilities(site_data, population)
            },
            'phase_3_construction': {
                'simulation': self.construction_simulator.simulate_construction(site_data, {}),
                'resource_optimization': self.resource_optimizer.optimize_resources(site_data, {}),
                'progress_plan': self.progress_monitor.monitor_progress(site_data, {})
            },
            'phase_4_public': {
                'vr_walkthrough': self.vr_generator.generate_walkthrough(site_data, {}),
                'consultation': self.public_consultation.create_consultation(site_data),
                'education': self.education_system.create_education_material(site_data),
                'tourism': self.tourism_planner.plan_tourism(site_data)
            },
            'phase_5_global': {
                'mars_adaptation': self.mars_adaptation.adapt_for_mars(site_data),
                'climate_resilience': self.climate_module.assess_climate_resilience(site_data),
                'ai_swarm': self.ai_swarm.create_swarm()
            }
        }

# ============================================================================
# UI FUNCTIONS
# ============================================================================

def init_session_state():
    if 'agent' not in st.session_state:
        st.session_state.agent = WestMalaysiaUndergroundCityGeoAIAgent()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = Location(
            lat=4.4700, lon=101.3800, name="Cameron Highlands (Pahang)")
    if 'reasoning_log' not in st.session_state:
        st.session_state.reasoning_log = []
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    if 'basemap_choice' not in st.session_state:
        st.session_state.basemap_choice = "OpenStreetMap"
    if 'show_radius_circle' not in st.session_state:
        st.session_state.show_radius_circle = True
    if 'show_heatmap' not in st.session_state:
        st.session_state.show_heatmap = False
    if 'show_onegeology' not in st.session_state:
        st.session_state.show_onegeology = False
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'candidate_scores' not in st.session_state:
        st.session_state.candidate_scores = {}
    if 'phase_view' not in st.session_state:
        st.session_state.phase_view = 'all'


def get_tiles_for_basemap(basemap_choice: str) -> str:
    if basemap_choice == "Satellite":
        return "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    return "OpenStreetMap"


def render_region_selector():
    regions = {
        '🌏 All West Malaysia': 'all',
        '🏝️ Northern (Perlis, Kedah, Penang, Perak)': 'north',
        '🏙️ Central (Selangor, KL, Putrajaya, N. Sembilan)': 'central',
        '🌴 Southern (Melaka, Johor)': 'south',
        '🌊 East Coast (Kelantan, Terengganu, Pahang)': 'east',
        '🏙️ Underground City Candidates': 'candidates'
    }
    sel = st.selectbox("Select Region", options=list(regions.keys()), index=0)
    rk = regions[sel]
    north = ['Perlis', 'Kedah', 'Penang', 'Perak']
    central = ['Selangor', 'Kuala Lumpur', 'Putrajaya', 'Negeri Sembilan']
    south = ['Melaka', 'Johor']
    east = ['Kelantan', 'Terengganu', 'Pahang']
    if rk == 'all':
        locs = WEST_MALAYSIA_LOCATIONS
        st.info(f"🌏 Showing {len(locs)} locations across West Malaysia")
    elif rk == 'candidates':
        locs = WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES
        st.info(f"🏙️ Showing {len(locs)} underground city candidate sites")
    else:
        sl = {'north': north, 'central': central, 'south': south, 'east': east}[rk]
        locs = {k: v for k, v in WEST_MALAYSIA_LOCATIONS.items()
                if any(f"({s})" in k for s in sl)}
        st.info(f"📍 Showing {len(locs)} locations in {sel}")
    return locs, rk


def render_phase_selector():
    st.markdown("""
    <div style="display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap;">
        <span class="phase-badge phase-badge-2">🔧 PHASE 2: INFRASTRUCTURE</span>
        <span class="phase-badge phase-badge-3">🏗️ PHASE 3: CONSTRUCTION AI</span>
        <span class="phase-badge phase-badge-4">👥 PHASE 4: PUBLIC ENGAGEMENT</span>
        <span class="phase-badge phase-badge-5">🌍 PHASE 5: GLOBAL EXPANSION</span>
    </div>
    """, unsafe_allow_html=True)
    phases = {
        'Phase 2: Infrastructure Planning': 'phase2',
        'Phase 3: Construction AI': 'phase3',
        'Phase 4: Public Engagement': 'phase4',
        'Phase 5: Global Expansion': 'phase5',
        '🎯 All Phases (Complete Plan)': 'all'
    }
    selected_phase = st.selectbox("Select Development Phase", options=list(phases.keys()), index=4)
    return phases[selected_phase]


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.2rem; font-family: 'Courier New', monospace; 
                 background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 font-weight: 900; letter-spacing: 3px;">UNDERGROUND</div>
            <div style="color: #00f0ff; font-size: 0.75rem; font-family: 'Courier New', monospace;
                 letter-spacing: 4px; text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);">
                WEST MALAYSIA</div>
            <div class="cyber-divider"></div>
        </div>
        """, unsafe_allow_html=True)
        cache_stats = api_cache.get_stats()
        st.markdown(f"""
        <div style="color: #a0a0c0; font-family: 'Courier New', monospace; font-size: 0.7rem; 
             letter-spacing: 1px; text-align: center; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; padding: 4px 8px; margin-bottom: 10px;">
            ⚡ CACHE: {cache_stats['total_cached']} RESPONSES
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚡ LOCATION SELECTOR</div>""", unsafe_allow_html=True)
        locations, region = render_region_selector()
        quick = st.selectbox("Select Location", list(locations.keys()), index=0)
        if st.button("⚡ GO TO LOCATION", use_container_width=True):
            coords = locations[quick]
            st.session_state.selected_location = Location(lat=coords[0], lon=coords[1], name=quick)
            st.rerun()
        st.caption("Or click on the map to select any location")
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🗺️ MAP SETTINGS</div>""", unsafe_allow_html=True)

        basemap_choice = st.radio(
            "Map Style",
            options=["🗺️ OpenStreetMap", "🛰️ Satellite"],
            index=0 if st.session_state.basemap_choice == "OpenStreetMap" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        if "Satellite" in basemap_choice:
            st.session_state.basemap_choice = "Satellite"
        else:
            st.session_state.basemap_choice = "OpenStreetMap"

        st.session_state.show_radius_circle = st.checkbox("Show Search Radius", value=True)
        st.session_state.show_onegeology = st.checkbox("🗺️ Show OneGeology Layer", value=False,
                                                       help="Overlay the global geological map (World CGMW)")
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚙️ ANALYSIS PARAMETERS</div>""", unsafe_allow_html=True)
        radius = st.slider("Assessment Radius (m)", 2000, 20000, 10000, 1000)
        st.divider()
        if st.button("🔄 COMPARE ALL", use_container_width=True):
            st.session_state.comparison_mode = True
            st.rerun()
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("Results cleared!"); st.rerun()
        if st.button("🗑️ CLEAR CACHE", use_container_width=True):
            api_cache.clear(); st.success("Cache cleared!"); st.rerun()
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace; 
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🧠 AGENT MEMORY</div>""", unsafe_allow_html=True)
        stats = st.session_state.agent.memory_repo.get_analysis_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
                 border-radius: 4px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
                     letter-spacing: 1px;">ANALYSES</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 1.2rem; 
                     font-weight: bold;">{stats['total_analyses']}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
                 border-radius: 4px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
                     letter-spacing: 1px;">SUCCESS RATE</div>
                <div style="color: #39ff14; font-family: 'Courier New', monospace; font-size: 1.2rem; 
                     font-weight: bold;">{stats['success_rate']*100:.0f}%</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 8px; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; margin-top: 8px;">
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
                 letter-spacing: 1px;">AVG EXECUTION</div>
            <div style="color: #b026ff; font-family: 'Courier New', monospace; font-size: 1.2rem; 
                 font-weight: bold;">{stats['avg_execution_time']:.2f}s</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
            Path("west_malaysia_underground_city_memory.db").unlink(missing_ok=True)
            st.session_state.agent = WestMalaysiaUndergroundCityGeoAIAgent()
            st.session_state.analysis_history = []
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("All memory cleared!"); st.rerun()
        return {'radius': radius}


def render_map(params: Dict):
    st.subheader("🗺️ West Malaysia Underground City Site Map")
    center = [4.2, 102.0]
    location_name = "West Malaysia"
    if st.session_state.selected_location:
        center = [st.session_state.selected_location.lat, st.session_state.selected_location.lon]
        location_name = st.session_state.selected_location.name or "West Malaysia Location"

    basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
    tiles_url = get_tiles_for_basemap(basemap_choice)

    try:
        if basemap_choice == "Satellite":
            m = folium.Map(location=center, zoom_start=7,
                           tiles=tiles_url, attr='Esri World Imagery')
        else:
            m = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    except Exception:
        m = folium.Map(location=center, zoom_start=7)

    if st.session_state.get('show_onegeology', False):
        try:
            onegeo_layer = folium.WmsTileLayer(
                url="https://portal.onegeology.org/OneGeologyGlobal/WMS/1.3.0",
                name="OneGeology Bedrock",
                layers="World_CGMW",
                fmt="image/png",
                transparent=True,
                opacity=0.55,
                version="1.3.0",
            )
            onegeo_layer.add_to(m)
            folium.LayerControl(position='topright').add_to(m)
        except Exception:
            pass

    if st.session_state.selected_location:
        marker_color = 'red'
        result_data = st.session_state.get('current_results', None)
        if result_data and 'suitability_percentage' in result_data:
            pct = result_data['suitability_percentage']
            if pct >= 80: marker_color = 'green'
            elif pct >= 65: marker_color = 'lightgreen'
            elif pct >= 50: marker_color = 'orange'
            elif pct >= 35: marker_color = 'lightred'
            else: marker_color = 'red'
        folium.Marker(
            center,
            popup=f"<b>🏙️ {location_name}</b><br>Lat: {center[0]:.6f}<br>Lon: {center[1]:.6f}",
            tooltip="🏙️ Candidate Site - Click for details",
            icon=folium.Icon(color=marker_color, icon='home', prefix='fa')
        ).add_to(m)
        if st.session_state.get('show_radius_circle', True):
            radius = params.get('radius', 10000)
            folium.Circle(center, radius=radius, color='#2ecc71', fill=True,
                          fillColor='#2ecc71', fillOpacity=0.1, weight=2,
                          tooltip=f"Assessment radius: {radius}m").add_to(m)
    try:
        Fullscreen(position='topleft').add_to(m)
        MiniMap(toggle_display=True, position='bottomright').add_to(m)
        MousePosition(position='bottomleft', prefix='West MY Coords: ').add_to(m)
    except Exception:
        pass
    map_data = st_folium(m, width=None, height=500, use_container_width=True)
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        new_location = Location(lat=clicked_lat, lon=clicked_lon, name="West Malaysia Location")
        if st.session_state.selected_location is None or \
           abs(st.session_state.selected_location.lat - clicked_lat) > 0.0001 or \
           abs(st.session_state.selected_location.lon - clicked_lon) > 0.0001:
            st.session_state.selected_location = new_location
            st.rerun()


def render_query_interface(params: Dict):
    st.subheader("💬 Natural Language Query")
    with st.expander("💡 Example Underground City Queries", expanded=False):
        st.markdown("""
        **🏙️ Underground City Site Selection:**
        - "Find the best location for an underground city in West Malaysia"
        - "Which site has the best geology for underground construction?"
        - "Evaluate this site for subterranean city development"
        - "Compare all candidate sites for underground city"

        **🪨 Site Suitability:**
        - "Assess bedrock depth at this location"
        - "What's the water table level here?"
        - "Check seismic risk and geology"
        - "Is this area suitable for underground city development?"
        """)
    query = st.text_area("Describe what you want to analyse for underground city site selection:",
                         placeholder="e.g., Find the best location for an underground city in West Malaysia",
                         height=100)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyse_btn = st.button("🏙️ ANALYSE SITE", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🧹 CLEAR", use_container_width=True)
    if clear_btn:
        st.session_state.current_results = None
        st.session_state.reasoning_log = []
        st.rerun()
    if analyse_btn and st.session_state.selected_location:
        with st.spinner("🧠 HYBRID: INSTANT + USGS + OneGeology + OSM..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            def update_progress(progress, status):
                progress_bar.progress(progress)
                status_text.text(status)
            result = st.session_state.agent.execute_analysis(
                st.session_state.selected_location,
                query if query else "Evaluate this site for underground city development",
                params, progress_callback=update_progress)
            st.session_state.analysis_history.append(result)
            st.session_state.reasoning_log = result.steps
            st.session_state.current_results = result.final_result
            progress_bar.empty(); status_text.empty()
            if result.success:
                st.success(f"✅ Analysis complete in {result.total_time:.2f}s"); st.rerun()
            else:
                st.error("❌ Analysis failed. Check reasoning log.")
    elif analyse_btn and not st.session_state.selected_location:
        st.warning("Please select a location in West Malaysia first!")


def render_reasoning_log():
    st.subheader("🧠 Agent Reasoning (Chain of Thought)")
    if not st.session_state.reasoning_log:
        st.info("Run an underground city site analysis to see the agent's reasoning.")
        return
    for step in st.session_state.reasoning_log:
        icon = "✅" if step.status == "completed" else "❌" if step.status == "failed" else "⏳"
        with st.expander(f"{icon} Step {step.step_number}: {step.name}", expanded=True):
            st.write(f"**Reasoning:** {step.reasoning}")
            if step.execution_time > 0:
                st.write(f"**Execution Time:** {step.execution_time:.3f}s")
            if step.result and step.name.startswith("Execute"):
                st.json(step.result)


def render_results():
    st.subheader("🏙️ Underground City Site Analysis Results")
    if not st.session_state.analysis_history:
        st.info("No analysis results yet.")
        return
    lr = st.session_state.analysis_history[-1]
    if not lr.final_result:
        st.warning("No results available."); return
    rd = lr.final_result
    if not rd.get('success', False):
        st.error(f"Analysis failed: {rd.get('error', 'Unknown error')}"); return

    if 'suitability_percentage' in rd:
        usgs_badge = "🛰️ USGS Live" if rd.get('used_usgs') else "🌐 OSM"
        onegeo_badge = "🗺️ OneGeology Live" if rd.get('used_onegeology') else "📍 Geographic"
        st.success(f"🌐 **HYBRID** · {usgs_badge} · {onegeo_badge}")

        if rd.get('penalty_applied', 0) > 0:
            with st.expander(f"⚠️ Score Penalty Applied: -{rd['penalty_applied']}%"):
                st.write(f"**Base score:** {rd.get('base_percentage', 0)}%")
                st.write(f"**Penalty:** -{rd['penalty_applied']}%")
                st.write("**Reasons:**")
                for r in rd.get('penalty_reasons', []):
                    st.warning(r)
                st.write(f"**Final score:** {rd['suitability_percentage']}%")

        if 'data_source_details' in rd:
            with st.expander("📊 Data Sources Used"):
                for d in rd['data_source_details']:
                    if '🌐' in d: st.success(f"🌐 {d}")
                    elif 'USGS' in d: st.success(f"🛰️ {d}")
                    elif 'OneGeology' in d: st.success(f"🗺️ {d}")
                    elif 'Geographic' in d: st.info(f"📍 {d}")
                    elif 'Fallback' in d: st.warning(f"⚠️ {d}")
                    else: st.success(f"✅ {d}")

        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.metric("🏙️ Underground City Suitability", f"{rd['suitability_percentage']}%",
                      delta=f"{rd['rating']} {rd['rating_emoji']}")
            st.caption(rd['recommendation'])
        with c2: st.metric("Elevation", f"{rd.get('elevation_m', 0):.0f}m")
        with c3: st.metric("Bedrock Depth", f"{rd.get('bedrock_depth_m', 0):.0f}m")
        with c4: st.metric("Water Table", f"{rd.get('water_table_depth_m', 0):.0f}m")

        st.write("---")
        st.write("**Detailed Scoring Breakdown:**")
        details = rd.get('details', {}); scores = rd.get('scores', {})
        score_data = []
        for k, d in details.items():
            w = d.get('weight', 0); sc = scores.get(k, 0)
            src = d.get('source', 'Unknown')
            if 'USGS' in src: emoji = '🛰️'
            elif 'Geographic' in src: emoji = '📍'
            elif 'Live' in src: emoji = '✅'
            elif 'Fallback' in src: emoji = '⚠️'
            else: emoji = 'ℹ️'
            display_key = k.replace('_', ' ').title()
            if 'Bedrock' in display_key: display_key = '🪨 ' + display_key
            elif 'Water Table' in display_key: display_key = '💧 ' + display_key
            elif 'Seismic' in display_key: display_key = '🌋 ' + display_key
            elif 'Geology' in display_key: display_key = '🗿 ' + display_key
            score_data.append({
                'Criteria': display_key, 'Score': f"{sc:.1f}/5",
                'Value': d.get('value', 'N/A'), 'Weight': f"{w*100:.0f}%",
                'Weighted': f"{sc*w:.2f}",
                'Source': f"{emoji} {src[:45]}{'...' if len(src) > 45 else ''}"
            })
        st.dataframe(pd.DataFrame(score_data), use_container_width=True, hide_index=True)
        chart = pd.DataFrame([{'Criteria': r['Criteria'], 'Score': float(r['Score'].split('/')[0])}
                              for r in score_data])
        st.bar_chart(chart.set_index('Criteria'))

        st.write("---")
        st.write("**📋 Detailed Recommendation Strategy**")
        recs = generate_recommendation_strategy(rd)
        risk = recs.get('risk_level', 'Unknown')
        risk_color = ('#ff2d95' if risk in ('High', 'Very High')
                      else '#39ff14' if risk == 'Low' else '#ffe84d')
        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">🎯 Overall Feasibility</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; font-size: 1.1rem; padding: 10px;">
                {recs.get('overall_feasibility', 'Assessment not available')}
            </div>
            <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    💰 Investment Required: <span style="color: #00f0ff; font-weight: bold;">{recs.get('investment_required', 'Unknown')}</span></div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    ⚠️ Risk Level: <span style="color: {risk_color}; font-weight: bold;">{risk}</span></div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    🚨 Critical Actions: <span style="color: #ff2d95; font-weight: bold;">{recs.get('critical_action_count', 0)}</span></div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Immediate: <span style="color: #39ff14; font-weight: bold;">{recs['timeline_summary']['immediate']}</span></div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Short-term: <span style="color: #ffe84d; font-weight: bold;">{recs['timeline_summary']['short_term']}</span></div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Long-term: <span style="color: #b026ff; font-weight: bold;">{recs['timeline_summary']['long_term']}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        for bucket, title in [
            ('immediate_actions', '🔴 IMMEDIATE ACTIONS (0-6 Months)'),
            ('short_term_actions', '🟡 SHORT-TERM ACTIONS (6-18 Months)'),
            ('long_term_actions', '🟢 LONG-TERM ACTIONS (18-36 Months)')
        ]:
            if recs[bucket]:
                st.markdown(f"""<div class="recommendation-container">
                    <div class="recommendation-title">{title}</div>""", unsafe_allow_html=True)
                for a in recs[bucket]:
                    st.markdown(f"""
                    <div class="recommendation-item">
                        <span class="icon">{a.get('priority', '')}</span>
                        {a['text']}
                        <span style="float: right; color: #8080a0; font-size: 0.8rem;">{a.get('cost', '')}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ============================================================
        # FIXED: Now uses 'critical_action_count' instead of len(immediate_actions)
        # ============================================================
        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">💰 Investment Summary</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; padding: 10px;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 150px;">
                        <div style="color: #8080a0; font-size: 0.7rem;">TOTAL INVESTMENT</div>
                        <div style="font-size: 1.2rem; font-weight: bold; color: {'#ff2d95' if recs.get('investment_required') == 'Very High' else '#ffe84d' if recs.get('investment_required') == 'Moderate' else '#39ff14'}">
                            {recs.get('investment_required', 'Unknown')}</div>
                    </div>
                    <div style="flex: 2; min-width: 200px;">
                        <div style="color: #8080a0; font-size: 0.7rem;">ACTION ITEMS</div>
                        <div style="font-size: 1rem;">
                            {recs.get('critical_action_count', 0)} Critical • {len(recs['short_term_actions'])} Short-term • {len(recs['long_term_actions'])} Long-term</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_comparison_mode():
    st.subheader("🔄 Site Comparison Dashboard")
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("⬅️ BACK TO SINGLE SITE", key="back_from_comparison", use_container_width=True):
            st.session_state.comparison_mode = False
            st.rerun()
    with st.spinner("Analysing all candidate sites..."):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i, (name, coords) in enumerate(WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES.items()):
            status_text.text(f"Analysing: {name}")
            progress_bar.progress((i + 1) / len(WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES))
            location = Location(lat=coords[0], lon=coords[1], name=name)
            params = {'radius': 10000}
            try:
                strategy = StrategySelector.get_strategy('underground_city')
                result = strategy.analyse(location, params)
                if result.get('success'):
                    results.append({
                        'Site': name, 'Suitability %': result['suitability_percentage'],
                        'Rating': result['rating'], 'Elevation (m)': result.get('elevation_m', 0),
                        'Bedrock (m)': result.get('bedrock_depth_m', 0),
                        'Water Table (m)': result.get('water_table_depth_m', 0),
                        'Seismic Risk': result.get('seismic_risk', 'Unknown'),
                        'Flood Risk': result.get('flood_risk', 'Unknown'),
                        'Method': ('🛰️ USGS + 🗺️ OneGeo' if result.get('used_usgs') and result.get('used_onegeology')
                                   else '🛰️ USGS' if result.get('used_usgs')
                                   else '📍 Geographic'),
                        'Recommendation': result['recommendation'][:50] + '...',
                        'Data': result
                    })
            except Exception as e:
                results.append({
                    'Site': name, 'Suitability %': 0, 'Rating': 'Error',
                    'Elevation (m)': 0, 'Bedrock (m)': 0, 'Water Table (m)': 0,
                    'Seismic Risk': 'Unknown', 'Flood Risk': 'Unknown',
                    'Method': 'Error', 'Recommendation': f"Error: {str(e)[:50]}", 'Data': None
                })
        progress_bar.empty(); status_text.empty()
        if results:
            df = pd.DataFrame(results)
            df_sorted = df.sort_values('Suitability %', ascending=False)
            st.write(f"**📊 Comparison of {len(results)} Candidate Sites**")
            top_site = df_sorted.iloc[0]
            st.success(f"🏙️ **Top Recommended Site: {top_site['Site']}** ({top_site['Suitability %']:.1f}%)")
            st.caption(top_site['Recommendation'])
            display_cols = ['Site', 'Suitability %', 'Rating', 'Elevation (m)', 'Bedrock (m)',
                          'Water Table (m)', 'Seismic Risk', 'Flood Risk', 'Method']
            st.dataframe(df_sorted[display_cols], use_container_width=True, hide_index=True)
            chart_data = df_sorted[['Site', 'Suitability %']].set_index('Site')
            st.bar_chart(chart_data)
            st.session_state.candidate_scores = {row['Site']: row['Suitability %'] for _, row in df.iterrows()}
            st.write("---")
            st.write("**🗺️ Site Map with Suitability Scores**")

            basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
            tiles_url = get_tiles_for_basemap(basemap_choice)
            if basemap_choice == "Satellite":
                m = folium.Map(location=[4.2, 102.0], zoom_start=6,
                               tiles=tiles_url, attr='Esri World Imagery')
            else:
                m = folium.Map(location=[4.2, 102.0], zoom_start=6, tiles="OpenStreetMap")

            for _, row in df.iterrows():
                name = row['Site']; score = row['Suitability %']
                if score >= 80: color = 'green'
                elif score >= 65: color = 'lightgreen'
                elif score >= 50: color = 'orange'
                elif score >= 35: color = 'lightred'
                else: color = 'red'
                coords = WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES.get(name, (0, 0))
                folium.Marker(coords, popup=f"<b>{name}</b><br>Suitability: {score:.1f}%<br>Rating: {row['Rating']}",
                              tooltip=f"{name}: {score:.1f}%",
                              icon=folium.Icon(color=color, icon='home', prefix='fa')).add_to(m)
            try: Fullscreen(position='topleft').add_to(m)
            except Exception: pass
            st_folium(m, width=None, height=400, use_container_width=True)
            selected_site = st.selectbox("Select a site for detailed analysis:", df_sorted['Site'].tolist())
            if selected_site:
                coords = WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES[selected_site]
                st.session_state.selected_location = Location(lat=coords[0], lon=coords[1], name=selected_site)
                st.session_state.comparison_mode = False
                st.rerun()


def render_enhanced_results(complete_plan: Dict):
    st.subheader("🏙️ Complete Underground City Development Plan")
    tabs = st.tabs(["📊 Overview", "💰 Phase 2: Infrastructure", "🏗️ Phase 3: Construction", "👥 Phase 4: Public", "🌍 Phase 5: Global"])
    with tabs[0]:
        site = complete_plan['phase_1_site_selection']['site_data']
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Site Suitability", f"{site.get('suitability_percentage', 0):.1f}%")
        with col2: st.metric("Population Capacity", "50,000+")
        with col3:
            cost = complete_plan['phase_2_infrastructure']['cost_estimate']
            st.metric("Total Cost", f"RM {cost['total_cost_billions']:.1f}B")
        with col4: st.metric("Completion Time", "4-5 years")
        st.info("✅ All phases ready for development. Scroll down for detailed plans.")
    with tabs[1]:
        cost_data = complete_plan['phase_2_infrastructure']['cost_estimate']
        transport_data = complete_plan['phase_2_infrastructure']['transport_plan']
        utility_data = complete_plan['phase_2_infrastructure']['utility_plan']
        st.subheader("💰 Cost Estimation")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Cost", f"RM {cost_data['total_cost_billions']:.2f}B")
        with col2: st.metric("Per SQM Cost", f"RM {cost_data['per_sqm_cost']:,.0f}")
        with col3: st.metric("Rock Type", cost_data['rock_type'].replace('_', ' ').title())
        st.subheader("🚆 Transport Network")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Primary Transport", transport_data['primary_transport'].replace('_', ' ').title())
        with col2: st.metric("Network Length", f"{transport_data['network_length_km']:.1f} km")
        with col3: st.metric("Stations", transport_data['stations'])
        st.subheader("⚡ Utility Systems")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Water", f"{utility_data['water']['daily_need_liters']:,} L/day")
        with col2: st.metric("Power", f"{utility_data['power']['peak_demand_mw']:.1f} MW")
        with col3: st.metric("Ventilation", f"{utility_data['ventilation']['airflow_m3h']:,} m³/h")
    with tabs[2]:
        sim_data = complete_plan['phase_3_construction']['simulation']
        resource_data = complete_plan['phase_3_construction']['resource_optimization']
        st.subheader("🏗️ Construction Timeline")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Duration", f"{sim_data['total_months']:.0f} months")
        with col2: st.metric("Completion Probability", f"{sim_data['completion_probability']:.1f}%")
        with col3: st.metric("Critical Path", " → ".join([s.replace('_', ' ').title() for s in sim_data['critical_path'][:2]]))
        st.subheader("📦 Resource Optimization")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Optimization Score", f"{resource_data['optimization_score']}%")
        with col2: st.metric("Waste Reduction", f"{resource_data['waste_reduction']}%")
        with col3: st.metric("Cost Savings", f"{resource_data['cost_savings_percentage']}%")
    with tabs[3]:
        vr_data = complete_plan['phase_4_public']['vr_walkthrough']
        consult_data = complete_plan['phase_4_public']['consultation']
        tourism_data = complete_plan['phase_4_public']['tourism']
        st.subheader("🕶️ VR Walkthrough")
        for scene in vr_data['scenes']:
            st.write(f"**📍 {scene['name']}**: {scene['description']}")
        st.subheader("🗳️ Public Consultation")
        for i, q in enumerate(consult_data['survey_questions'][:2]):
            st.write(f"**Q{i+1}:** {q['question']}")
        st.subheader("🏨 Tourism")
        col1, col2 = st.columns(2)
        with col1: st.metric("Annual Visitors", f"{sum(a['visitors_per_year'] for a in tourism_data['attractions']):,}")
        with col2: st.metric("Jobs Created", tourism_data['jobs_created'])
    with tabs[4]:
        mars_data = complete_plan['phase_5_global']['mars_adaptation']
        climate_data = complete_plan['phase_5_global']['climate_resilience']
        swarm_data = complete_plan['phase_5_global']['ai_swarm']
        st.subheader("🚀 Mars Adaptation")
        for key, value in list(mars_data['mars_adaptation'].items())[:5]:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        st.subheader("🌍 Climate Resilience")
        col1, col2 = st.columns(2)
        with col1: st.metric("Resilience Score", f"{climate_data['overall_resilience_score']:.0f}%")
        with col2: st.metric("Climate Refuge Capacity", f"{climate_data['climate_refuge_capacity']:,}")
        st.subheader("🧠 AI Swarm")
        for agent in swarm_data['agents']:
            st.write(f"**{agent['role']}**: {agent['specialty']}")


def render_memory_explorer():
    st.subheader("💾 Memory Explorer")
    tab1, tab2 = st.tabs(["Past Analyses", "Learned Parameters"])
    with tab1:
        all_analyses = st.session_state.agent.memory_repo.get_all_analyses(limit=20)
        if all_analyses:
            st.write(f"**{len(all_analyses)} past analyses stored**")
            for entry in all_analyses:
                query_preview = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
                with st.expander(f"{'✅' if entry['success'] else '❌'} {query_preview}"):
                    st.write(f"**Query:** {entry['query']}")
                    st.write(f"**Success:** {'✅ Yes' if entry['success'] else '❌ No'}")
                    st.write(f"**Execution Time:** {entry['execution_time']:.2f}s")
                    st.write(f"**Timestamp:** {entry['timestamp']}")
        else:
            st.info("No past analyses stored yet.")
    with tab2:
        try:
            conn = sqlite3.connect("west_malaysia_underground_city_memory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM learned_parameters ORDER BY success_rate DESC")
            rows = cursor.fetchall(); conn.close()
            if rows:
                st.write(f"**{len(rows)} learned parameters**")
                df = pd.DataFrame(rows, columns=['ID', 'Analysis Type', 'Parameter', 'Value',
                                                 'Success Rate', 'Usage Count', 'Last Updated'])
                st.dataframe(df[['Analysis Type', 'Parameter', 'Value', 'Success Rate', 'Usage Count']],
                             use_container_width=True)
            else:
                st.info("No learned parameters yet.")
        except Exception:
            st.info("No learned parameters yet.")

# ============================================================================
# MAIN
# ============================================================================

def main():
    st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div class="main-title">🏙️ WEST MALAYSIA UNDERGROUND</div>
        <div class="subtitle">PENINSULAR MALAYSIA · CITY SELECTOR v3.1</div>
        <div style="display: flex; justify-content: center; gap: 10px; margin: 10px 0;">
            <span class="phase-badge phase-badge-2">🔧 PHASE 2</span>
            <span class="phase-badge phase-badge-3">🏗️ PHASE 3</span>
            <span class="phase-badge phase-badge-4">👥 PHASE 4</span>
            <span class="phase-badge phase-badge-5">🌍 PHASE 5</span>
        </div>
        <div class="cyber-divider"></div>
        <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem; 
             letter-spacing: 4px; margin-top: 5px;">
            ⚡ HYBRID · 🛰️ USGS LIVE · 🗺️ ONEGEOLOGY LIVE · OSM LIVE · 🛰️ SATELLITE ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)
    init_session_state()
    total_locations = len(WEST_MALAYSIA_LOCATIONS)
    total_candidates = len(WEST_MALAYSIA_UNDERGROUND_CITY_CANDIDATES)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 8px 15px; 
         border: 1px solid rgba(0, 240, 255, 0.1); border-radius: 8px; 
         background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem; 
             letter-spacing: 1px;">📍 LOCATIONS LOADED</span>
        <span style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.8rem; 
             font-weight: bold; letter-spacing: 1px;">{total_locations} (+ {total_candidates} candidates)</span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
             letter-spacing: 1px;">PENINSULAR MALAYSIA</span>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get('comparison_mode', False):
        render_comparison_mode()
        return
    params = render_sidebar()
    selected_phase = render_phase_selector()
    col1, col2 = st.columns([1.5, 1])
    with col1:
        render_map(params)
        render_query_interface(params)
    with col2:
        if st.session_state.selected_location:
            name = st.session_state.selected_location.name or "West Malaysia Location"
            st.markdown(f"""
            <div style="padding: 10px 15px; border: 1px solid rgba(0, 240, 255, 0.15);
                 border-radius: 8px; background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
                     letter-spacing: 1px;">SELECTED LOCATION</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.9rem;">
                    {name}</div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem; 
                     letter-spacing: 1px;">{st.session_state.selected_location.lat:.4f}, {st.session_state.selected_location.lon:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        render_reasoning_log()
    st.divider()
    if st.session_state.current_results:
        result_data = st.session_state.current_results
        col1, col2 = st.columns(2)
        with col1:
            render_results()
        with col2:
            render_memory_explorer()
        if selected_phase == 'all' and 'suitability_percentage' in result_data:
            st.write("---")
            with st.spinner("🧠 Generating complete development plan..."):
                developer = EnhancedUndergroundCityDeveloper()
                complete_plan = developer.develop_complete_city(result_data)
                render_enhanced_results(complete_plan)
    else:
        render_memory_explorer()
    st.markdown("""
    <div class="cyber-divider"></div>
    <div style="text-align: center; padding: 15px 0; color: #333; font-family: 'Courier New', monospace; 
         font-size: 0.6rem; letter-spacing: 2px;">
        <span style="color: #00f0ff;">[</span> 
        WEST MALAYSIA UNDERGROUND CITY SELECTOR v3.1 · USGS + ONEGEOLOGY + SATELLITE ENABLED
        <span style="color: #00f0ff;">]</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()