"""Компонент карти"""
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from visualization.config.settings import MAP_CONFIG
from visualization.utils.scoring import get_status, get_gradient_by_value, get_color_by_value
from visualization.utils.icons import icon


def get_metric_value(location, metric_name):
    if metric_name in location:
        return location[metric_name]
    elif 'normalized' in location and metric_name in location['normalized']:
        return location['normalized'][metric_name]
    else:
        return 0.0


def create_popup_html(location, rank):
    score = location.get('score', 0)
    restaurants_val = get_metric_value(location, 'restaurants')
    subway_val = get_metric_value(location, 'subway')
    borough_val = get_metric_value(location, 'borough_quality')

    score_gradient = get_gradient_by_value(score, 1)

    restaurants_color, _ = get_color_by_value(restaurants_val)
    subway_color, _ = get_color_by_value(subway_val)
    borough_color, _ = get_color_by_value(borough_val)

    return f"""
        <style>
            .leaflet-popup-content-wrapper {{
                background: #0a0a0a !important;
                border: 1px solid #2d2d2d !important;
                border-radius: 16px !important;
                padding: 0 !important;
            }}
            .leaflet-popup-tip {{
                background: #0a0a0a !important;
            }}
            .leaflet-popup-content {{
                margin: 0 !important;
                width: 260px !important;
            }}
        </style>
        <div style="font-family: 'Inter', sans-serif; background: #0a0a0a; 
                    color: white; padding: 16px; border-radius: 16px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%); 
                            border-radius: 8px; display: flex; align-items: center; justify-content: center; 
                            border: 1px solid #3d3d3d;">
                    <i class="fas fa-map-marker-alt" style="color: #05e07e; font-size: 14px;"></i>
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">
                        {location.get('name', 'Unknown')}
                    </h4>
                    <p style="margin: 2px 0 0 0; color: #6b7280; font-size: 0.75rem;">#{rank}</p>
                </div>
            </div>
            
            <div style="background: {score_gradient}; padding: 12px; 
                        border-radius: 10px; text-align: center; margin: 10px 0; 
                        box-shadow: 0 4px 16px rgba(5, 224, 126, 0.3);">
                <div style="font-size: 2rem; font-weight: 900; color: #000;">
                    {score:.2f}
                </div>
                <div style="font-size: 0.65rem; color: #000; opacity: 0.7; font-weight: 600; 
                            text-transform: uppercase; letter-spacing: 0.05em;">
                    з 1.00
                </div>
            </div>
            
            <div style="margin-top: 12px;">
                <div style="background: #0f0f0f; padding: 10px; border-radius: 6px; border: 1px solid #1a1a1a; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <i class="fas {icon('restaurants')}" style="color: #6b7280; font-size: 12px;"></i>
                        <span style="color: #9ca3af; font-size: 0.75rem;">Ресторани</span>
                    </div>
                    <span style="color: {restaurants_color}; font-weight: 700; font-size: 0.95rem;">{restaurants_val:.2f}</span>
                </div>
                
                <div style="background: #0f0f0f; padding: 10px; border-radius: 6px; border: 1px solid #1a1a1a; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <i class="fas {icon('subway')}" style="color: #6b7280; font-size: 12px;"></i>
                        <span style="color: #9ca3af; font-size: 0.75rem;">Метро</span>
                    </div>
                    <span style="color: {subway_color}; font-weight: 700; font-size: 0.95rem;">{subway_val:.2f}</span>
                </div>
                
                <div style="background: #0f0f0f; padding: 10px; border-radius: 6px; border: 1px solid #1a1a1a;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <i class="fas fa-city" style="color: #6b7280; font-size: 12px;"></i>
                        <span style="color: #9ca3af; font-size: 0.75rem;">Якість району</span>
                    </div>
                    <span style="color: {borough_color}; font-weight: 700; font-size: 0.95rem;">{borough_val:.2f}</span>
                </div>
            </div>
        </div>
    """


def render_map(locations, top_n=20, show_clusters=True, center=None, zoom=None):
    map_center = center if center else MAP_CONFIG['center']
    map_zoom = zoom if zoom is not None else MAP_CONFIG['zoom']

    map_obj = folium.Map(
        location=map_center,
        zoom_start=map_zoom,
        tiles=MAP_CONFIG['tile'],
        prefer_canvas=True
    )

    top_locations = locations[:top_n]
    other_locations = locations[top_n:]

    for i, loc in enumerate(top_locations):
        status = get_status(loc.get('score', 0))

        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=folium.Popup(create_popup_html(loc, i + 1), max_width=280),
            icon=folium.Icon(
                color=status['color'],
                icon=status['icon'].replace('fa-', ''),
                prefix='fa'
            )
        ).add_to(map_obj)

    if show_clusters and len(other_locations) > 0:
        marker_cluster = MarkerCluster(
            name='Інші локації',
            overlay=True,
            control=True,
            options={
                'maxClusterRadius': 50,
                'spiderfyOnMaxZoom': True,
                'showCoverageOnHover': False,
                'zoomToBoundsOnClick': True
            }
        ).add_to(map_obj)

        for i, loc in enumerate(other_locations):
            status = get_status(loc.get('score', 0))

            folium.Marker(
                location=[loc['lat'], loc['lon']],
                popup=folium.Popup(
                    create_popup_html(loc, top_n + i + 1),
                    max_width=280
                ),
                icon=folium.Icon(
                    color=status['color'],
                    icon='circle',
                    prefix='fa'
                )
            ).add_to(marker_cluster)

    if show_clusters:
        folium.LayerControl().add_to(map_obj)

    map_data = st_folium(
        map_obj,
        width=None,
        height=600,
        returned_objects=["bounds", "center", "zoom"]
    )

    return map_data