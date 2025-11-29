"""UI Application Logic"""
import streamlit as st
from visualization.config.settings import PAGE_CONFIG
from visualization.styles.theme import apply_theme
from visualization.components.header import render_header
from visualization.components.sidebar import render_sidebar
from visualization.components.map_view import render_map
from visualization.components.metrics_cards import render_top_metrics
from visualization.components.location_list import render_location_list
from visualization.components.legend import render_legend
from scripts.score_algorithm import filter_locations, add_normalized_fields
import json
from pathlib import Path
import time


def get_project_root():
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    return project_root


def load_normalized_data():
    project_root = get_project_root()
    normalized_data_path = project_root / 'data' / 'processed' / 'merged_data_normalized.json'

    if normalized_data_path.exists():
        with open(normalized_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    else:
        original_data_path = project_root / 'data' / 'processed' / 'merged_data.json'
        if original_data_path.exists():
            output_dir = project_root / 'data' / 'processed'
            data = add_normalized_fields(str(original_data_path), str(output_dir))
            return data
        else:
            print(f"❌ Файли не знайдено")
            return None


def extract_viewport_from_bounds(bounds):
    if not bounds:
        return None

    try:
        return {
            "ne_lat": bounds['_northEast']['lat'],
            "ne_lng": bounds['_northEast']['lng'],
            "sw_lat": bounds['_southWest']['lat'],
            "sw_lng": bounds['_southWest']['lng']
        }
    except (KeyError, TypeError):
        return None


def viewports_are_different(viewport1, viewport2, threshold=0.001):
    if viewport1 is None or viewport2 is None:
        return True

    for key in ['ne_lat', 'ne_lng', 'sw_lat', 'sw_lng']:
        if abs(viewport1[key] - viewport2[key]) > threshold:
            return True

    return False


def run_ui():
    st.set_page_config(**PAGE_CONFIG)
    apply_theme()

    if 'viewport' not in st.session_state:
        st.session_state.viewport = {
            "ne_lat": 40.917577,
            "ne_lng": -73.700272,
            "sw_lat": 40.477399,
            "sw_lng": -74.259090
        }

    if 'map_center' not in st.session_state:
        st.session_state.map_center = None

    if 'map_zoom' not in st.session_state:
        st.session_state.map_zoom = None

    if 'pending_viewport' not in st.session_state:
        st.session_state.pending_viewport = None

    if 'pending_viewport_timestamp' not in st.session_state:
        st.session_state.pending_viewport_timestamp = None

    if 'previous_weights' not in st.session_state:
        st.session_state.previous_weights = None

    if 'ui_ready' not in st.session_state:
        st.session_state.ui_ready = False

    if not st.session_state.ui_ready:
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; 
                        height: 80vh; flex-direction: column;'>
                <h1 style='color: #05e07e; margin-bottom: 20px;'>🗽 CitySpotter</h1>
            </div>
        """, unsafe_allow_html=True)

        with st.spinner('🔄 Завантаження і підготовка даних...'):
            normalized_data = load_normalized_data()

            if not normalized_data:
                st.error("❌ Немає даних для відображення")
                return

            st.session_state.normalized_data = normalized_data

            default_weights = {
                "restaurants": 0.5,
                "subway": 0.5,
                "borough_quality": 0.1
            }

            st.session_state.previous_weights = default_weights.copy()

            filtered_result = filter_locations(
                normalized_data,
                st.session_state.viewport,
                default_weights,
                min_score=0.0
            )

            locations = filtered_result['locations'][:1000]

            for loc in locations:
                loc['lat'] = loc.get('latitude', loc.get('lat'))
                loc['lon'] = loc.get('longitude', loc.get('lon'))

            st.session_state.cached_locations = locations
            st.session_state.cached_filtered_result = filtered_result

            st.session_state.ui_ready = True

            time.sleep(0.3)

        st.rerun()

    render_header()
    weights = render_sidebar()

    normalized_data = st.session_state.normalized_data
    active_viewport = st.session_state.viewport

    weights_dict = {
        "restaurants": weights['restaurants'],
        "subway": weights['subway'],
        "borough_quality": weights.get('borough_quality', 0.1)
    }

    weights_changed = False
    if st.session_state.previous_weights is not None:
        weights_changed = (weights_dict != st.session_state.previous_weights)

    st.session_state.previous_weights = weights_dict.copy()

    if weights_changed:
        filtered_result = filter_locations(
            normalized_data,
            active_viewport,
            weights_dict,
            min_score=0.0
        )

        locations = filtered_result['locations'][:1000]

        for loc in locations:
            loc['lat'] = loc.get('latitude', loc.get('lat'))
            loc['lon'] = loc.get('longitude', loc.get('lon'))

        st.session_state.cached_locations = locations
        st.session_state.cached_filtered_result = filtered_result

    locations = st.session_state.cached_locations
    filtered_result = st.session_state.cached_filtered_result

    if not locations:
        st.warning("⚠️ Немає локацій у поточному viewport")
        st.info(f"")
        return

    current_time = time.time()
    if st.session_state.pending_viewport and st.session_state.pending_viewport_timestamp:
        time_elapsed = current_time - st.session_state.pending_viewport_timestamp
        time_remaining = max(0, 0.5 - time_elapsed)

        if time_remaining > 0:
            st.info(f"")
            st.rerun()
        else:
            st.session_state.viewport = st.session_state.pending_viewport
            st.session_state.pending_viewport = None
            st.session_state.pending_viewport_timestamp = None

            filtered_result = filter_locations(
                normalized_data,
                st.session_state.viewport,
                weights_dict,
                min_score=0.0
            )

            locations = filtered_result['locations'][:1000]

            for loc in locations:
                loc['lat'] = loc.get('latitude', loc.get('lat'))
                loc['lon'] = loc.get('longitude', loc.get('lon'))

            st.session_state.cached_locations = locations
            st.session_state.cached_filtered_result = filtered_result

            st.rerun()
    else:
        st.success(f"")

    map_data = render_map(
        locations,
        top_n=20,
        show_clusters=True,
        center=st.session_state.map_center,
        zoom=st.session_state.map_zoom
    )

    if map_data:
        if 'center' in map_data and map_data['center']:
            st.session_state.map_center = [
                map_data['center']['lat'],
                map_data['center']['lng']
            ]

        if 'zoom' in map_data and map_data['zoom']:
            st.session_state.map_zoom = map_data['zoom']

    if map_data and 'bounds' in map_data and map_data['bounds']:
        new_viewport = extract_viewport_from_bounds(map_data['bounds'])

        if new_viewport:
            if viewports_are_different(new_viewport, active_viewport):
                if not st.session_state.pending_viewport or \
                   viewports_are_different(new_viewport, st.session_state.pending_viewport):
                    st.session_state.pending_viewport = new_viewport
                    st.session_state.pending_viewport_timestamp = current_time
                    st.rerun()

    if weights_changed:
        st.rerun()

    render_top_metrics(locations)
    st.markdown("<hr>", unsafe_allow_html=True)

    display_limit = min(50, len(locations))
    render_location_list(locations[:display_limit])

    render_legend()