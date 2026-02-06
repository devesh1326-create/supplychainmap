import streamlit as st
import searoute as sr
from geopy.distance import geodesic
from config import DESTINATIONS, CO2_FACTORS, EXPORT_VOLUMES, PRODUCT_ORIGINS


# REMOVED @st.cache_data TO FORCE UPDATES ON SCENARIO CHANGE
def calculate_route_between_points(origin_coords, dest_coords, restrictions):
    """Calculate route between two points with given restrictions."""
    try:
        route_geo = sr.searoute(
            origin_coords,
            dest_coords,
            restrictions=restrictions
        )

        if route_geo and 'geometry' in route_geo:
            route_coords = route_geo['geometry']['coordinates']
            distance_km = route_geo.get('properties', {}).get('length', 0)

            if distance_km <= 0:
                total_km = 0
                for k in range(len(route_coords) - 1):
                    start = (route_coords[k][1], route_coords[k][0])
                    end = (route_coords[k + 1][1], route_coords[k + 1][0])
                    total_km += geodesic(start, end).km
                distance_km = total_km

            dist_nm = distance_km * 0.539957

            return {
                "success": True,
                "distance_nm": dist_nm,
                "distance_km": distance_km,
                "route_coords": route_coords,
                "error": None
            }
        else:
            return {
                "success": False,
                "distance_nm": float('inf'),
                "distance_km": float('inf'),
                "route_coords": [],
                "error": "No route found"
            }
    except Exception as e:
        return {
            "success": False,
            "distance_nm": float('inf'),
            "distance_km": float('inf'),
            "route_coords": [],
            "error": str(e)
        }


def calculate_routes_for_product(selected_product, active_restrictions, active_origins):
    results = []
    product_volumes = EXPORT_VOLUMES.get(selected_product, {})

    # Logic to handle Port Strikes (Origins)
    specialized_ports = PRODUCT_ORIGINS.get(selected_product, list(active_origins.keys()))
    valid_origin_names = [p for p in specialized_ports if p in active_origins]

    for i, (dest_name, dest_coords) in enumerate(DESTINATIONS.items()):
        volume_kg = product_volumes.get(dest_name, 0)

        if volume_kg <= 0:
            continue

        route_options = []

        for org_name in valid_origin_names:
            org_coords = active_origins[org_name]

            route_result = calculate_route_between_points(
                org_coords,
                dest_coords,
                active_restrictions
            )

            route_options.append({
                "origin_name": org_name,
                "origin_coords": org_coords,
                "dest_name": dest_name,
                "dest_coords": dest_coords,
                "success": route_result["success"],
                "distance_nm": route_result["distance_nm"],
                "distance_km": route_result["distance_km"],
                "route_coords": route_result["route_coords"],
                "error": route_result["error"]
            })

        best_route = None
        shortest_distance = float('inf')

        for route in route_options:
            if route["success"] and route["distance_nm"] < shortest_distance:
                shortest_distance = route["distance_nm"]
                best_route = route

        if best_route:
            best_data = {
                **best_route,
                "route_options": route_options,
                "selected": True,
                "volume_kg": volume_kg,
                "volume_tons": volume_kg / 1000,
                "product": selected_product
            }
            results.append(best_data)

    return results


def calculate_total_emissions(route_results, selected_product):
    emission_results = []
    total_product_kg = 0
    total_co2_kg = 0

    avg_co2_per_kg = 0.0
    co2_factor = CO2_FACTORS.get(selected_product, 0.00463)

    for route in route_results:
        if route.get("selected") and route.get("volume_kg", 0) > 0:
            volume_tons = route["volume_tons"]
            total_co2_for_route = route["distance_nm"] * co2_factor * volume_tons

            emission_results.append({
                "Destination": route["dest_name"],
                "Origin": route["origin_name"],
                "Distance (NM)": route["distance_nm"],
                "Export Volume (kg)": route["volume_kg"],
                "Export Volume (tons)": volume_tons,
                "CO₂ Emissions (tons)": total_co2_for_route / 1000
            })

            total_product_kg += route["volume_kg"]
            total_co2_kg += total_co2_for_route

    if total_product_kg > 0:
        avg_co2_per_kg = total_co2_kg / total_product_kg

    return emission_results, avg_co2_per_kg, total_co2_kg, total_product_kg