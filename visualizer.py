# visualizer.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from config import ORIGINS, MAP_STYLES, PRODUCT_COLORS, CO2_FACTORS, PRODUCT_VESSEL_MAPPING


def create_emissions_factor_chart():
    """
    Creates a horizontal bar chart comparing the carbon intensity
    of different products/ship types.
    """
    # 1. Prepare Data
    data = []
    for product, factor in CO2_FACTORS.items():
        data.append({
            "Product": product,
            "Ship Type": PRODUCT_VESSEL_MAPPING.get(product, "Unknown"),
            "Factor": factor * 1000, # Convert to grams for display legibility
            "Factor_Raw": factor,
            "Color": PRODUCT_COLORS.get(product, "#94a3b8")
        })

    df_factors = pd.DataFrame(data)
    df_factors = df_factors.sort_values(by="Factor_Raw", ascending=True)

    # 2. Create Chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_factors["Product"],
        x=df_factors["Factor_Raw"],
        orientation='h',
        marker=dict(color=df_factors["Color"], opacity=0.8, line=dict(width=1, color='white')),
        text=df_factors["Ship Type"],
        textposition='auto',
        hovertemplate=(
            "<b>%{y}</b><br>" +
            "Ship: %{text}<br>" +
            "Factor: %{x:.5f} kg CO₂/t-km<extra></extra>"
        )
    ))

    # 3. Styling
    fig.update_layout(
        title="LOGISTICS CARBON INTENSITY BY PRODUCT",
        xaxis_title="kg CO₂e per Ton-Km",
        yaxis_title="",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94a3b8", size=11),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showgrid=True, gridcolor='#334155', zeroline=False),
        yaxis=dict(showgrid=False)
    )

    return fig


def create_route_map(route_results, map_style="Dark", show_all_routes=False, show_animation=False):
    fig = go.Figure()
    legend_products_seen = set()

    # 1. DRAW ROUTES
    for item in route_results:
        if item.get('volume_kg', 0) > 0:
            route_coords = item.get('route_coords', [])
            if not route_coords: continue

            route_array = np.array(route_coords)
            product_name = item.get('product_group', item.get('product', 'Unknown'))
            line_color = PRODUCT_COLORS.get(product_name, '#FFFFFF')

            show_legend = False
            if product_name not in legend_products_seen:
                show_legend = True
                legend_products_seen.add(product_name)

            fig.add_trace(go.Scattergeo(
                lon=route_array[:, 0], lat=route_array[:, 1],
                mode='lines',
                line=dict(width=1.5, color=line_color),
                name=product_name, legendgroup=product_name, showlegend=show_legend,
                hovertemplate=f"<b>Route:</b> {product_name}<br><b>To:</b> {item['dest_name']}<extra></extra>",
                opacity=0.7
            ))

            fig.add_trace(go.Scattergeo(
                lon=[item['dest_coords'][0]], lat=[item['dest_coords'][1]],
                mode='markers',
                marker=dict(size=4, color=line_color, symbol='square'),
                hovertemplate=f"<b>Destination:</b> {item['dest_name']}<br><b>Volume:</b> {item['volume_tons']:,.0f} tons<extra></extra>",
                showlegend=False
            ))

    # 2. DRAW ORIGINS
    added_origin_legend = False
    for name, coords in ORIGINS.items():
        fig.add_trace(go.Scattergeo(
            lon=[coords[0]], lat=[coords[1]],
            mode='markers',
            marker=dict(size=6, color='white', symbol='circle-dot'),
            name="Origin Hub", showlegend=not added_origin_legend, legendgroup="Origins",
            hovertemplate=f"<b>Origin Hub:</b> {name}<extra></extra>"
        ))
        added_origin_legend = True

    # 3. LAYOUT
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=550,
        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',
        geo=dict(
            projection_type="natural earth",
            showland=True, showocean=True, showcountries=True,
            landcolor='#1e293b',
            countrycolor='#334155',
            oceancolor='#0f172a',
            coastlinewidth=0.5,
            center={"lat": 10, "lon": 10},
            projection_scale=1.1,
            bgcolor='#0f172a'
        ),
        showlegend=True,
        legend=dict(
            orientation="v", yanchor="bottom", y=0.05, xanchor="left", x=0.02,
            bgcolor="rgba(0,0,0,0.5)", font=dict(color="white", size=10)
        )
    )
    return fig


def create_sankey_diagram(chart_data):
    if not chart_data: return None
    origins = list(set([d['Origin'] for d in chart_data]))
    destinations = list(set([d['Destination'].split('(')[0] for d in chart_data]))
    all_nodes = origins + destinations
    node_map = {name: i for i, name in enumerate(all_nodes)}
    sources, targets, values, colors = [], [], [], []
    for d in chart_data:
        sources.append(node_map[d['Origin']])
        targets.append(node_map[d['Destination'].split('(')[0]])
        values.append(d['Export Volume (tons)'])
        colors.append(PRODUCT_COLORS.get(d.get('product_group', 'Unknown'), '#3b82f6'))

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=15, line=dict(color="black", width=0.5), label=all_nodes, color="#94a3b8"),
        link=dict(source=sources, target=targets, value=values, color=colors)
    )])
    fig.update_layout(font=dict(size=10, color="#94a3b8"), height=350, paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=10, r=10, t=20, b=10))
    return fig


def create_heatmap(chart_data):
    if not chart_data: return None
    df = pd.DataFrame(chart_data)
    df['ShortDest'] = df['Destination'].apply(lambda x: x.split('(')[0])
    df['Intensity'] = df['CO₂ Emissions (tons)'] / df['Export Volume (tons)']
    if 'product_group' in df.columns:
        pivot = df.pivot_table(index='ShortDest', columns='product_group', values='Intensity', fill_value=0)
    else:
        pivot = df.pivot_table(index='ShortDest', values='Intensity', fill_value=0)
    fig = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale='Magma'))
    fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8", size=10),
                      margin=dict(l=10, r=10, t=20, b=10))
    return fig


def create_bubble_radar(chart_data):
    if not chart_data: return None
    fig = go.Figure()
    for d in chart_data:
        color = PRODUCT_COLORS.get(d.get('product_group', 'Unknown'), '#3b82f6')
        fig.add_trace(go.Scatter(
            x=[d['Distance (NM)']], y=[d['Export Volume (tons)']],
            mode='markers',
            marker=dict(size=d['CO₂ Emissions (tons)'] / max(x['CO₂ Emissions (tons)'] for x in chart_data) * 40 + 5,
                        color=color, opacity=0.7, line=dict(width=0.5, color='white')),
            name=d['Destination'].split('(')[0],
            hovertemplate=f"<b>{d['Destination']}</b><br>Vol: {d['Export Volume (tons)']:,.0f}t<br>CO2: {d['CO₂ Emissions (tons)']:,.0f}t<extra></extra>"
        ))
    fig.update_layout(
        xaxis=dict(title="DISTANCE (NM)", gridcolor='#334155', tickfont=dict(size=10)),
        yaxis=dict(title="VOLUME (TONS)", gridcolor='#334155', tickfont=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8", size=10),
        height=350, showlegend=False, margin=dict(l=10, r=10, t=20, b=10)
    )
    return fig