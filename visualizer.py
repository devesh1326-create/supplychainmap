import plotly.graph_objects as go
import numpy as np
import pandas as pd
from config import ORIGINS, MAP_STYLES, PRODUCT_COLORS


def create_route_map(route_results, map_style="Dark", show_all_routes=False, show_animation=False):
    fig = go.Figure()
    legend_products_seen = set()

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
                name=product_name,
                legendgroup=product_name,
                showlegend=show_legend,
                hoverinfo='text',
                text=f"{product_name} -> {item['dest_name']}",
                opacity=0.8
            ))

            fig.add_trace(go.Scattergeo(
                lon=[item['dest_coords'][0]], lat=[item['dest_coords'][1]],
                mode='markers',
                marker=dict(size=3, color=line_color, symbol='square'),  # Smaller markers
                showlegend=False,
                hoverinfo='skip'
            ))

    # Origins
    added_origin_legend = False
    for name, coords in ORIGINS.items():
        fig.add_trace(go.Scattergeo(
            lon=[coords[0]], lat=[coords[1]],
            mode='markers',
            marker=dict(size=5, color='white', symbol='circle'),
            name="Origin Hub",
            hovertext=name,
            showlegend=not added_origin_legend,
            legendgroup="Origins"
        ))
        added_origin_legend = True

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=550,
        paper_bgcolor='#020617',
        plot_bgcolor='#020617',
        geo=dict(
            projection_type="natural earth",
            showland=True, showocean=True, showcountries=True,
            landcolor='#0f172a',
            countrycolor='#1e293b',
            oceancolor='#020617',
            coastlinewidth=0.5,
            center={"lat": 10, "lon": 10},
            projection_scale=1.1,
            bgcolor='#020617'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=0.02,
            xanchor="center", x=0.5,
            bgcolor="rgba(0,0,0,0.5)",
            font=dict(color="white", size=10)  # Smaller font
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
        prod = d.get('product_group', 'Unknown')
        colors.append(PRODUCT_COLORS.get(prod, '#00F0FF'))

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=15,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="#94a3b8"
        ),
        link=dict(
            source=sources, target=targets, value=values, color=colors
        )
    )])

    fig.update_layout(
        font=dict(size=10, color="#94a3b8"),  # Small Tech Font
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=10)
    )
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
        pivot.columns = ['Intensity']

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale='Magma', showscale=True
    ))

    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94a3b8", size=10),
        margin=dict(l=10, r=10, t=20, b=10)
    )
    return fig


def create_bubble_radar(chart_data):
    if not chart_data: return None

    fig = go.Figure()

    for d in chart_data:
        prod = d.get('product_group', 'Unknown')
        color = PRODUCT_COLORS.get(prod, '#00F0FF')

        fig.add_trace(go.Scatter(
            x=[d['Distance (NM)']],
            y=[d['Export Volume (tons)']],
            mode='markers',
            marker=dict(
                size=d['CO₂ Emissions (tons)'] / max(x['CO₂ Emissions (tons)'] for x in chart_data) * 40 + 5,
                color=color, opacity=0.7, line=dict(width=0.5, color='white')
            ),
            name=d['Destination'].split('(')[0],
            text=f"<b>{d['Destination']}</b><br>Vol: {d['Export Volume (tons)']:,.0f}t",
            hoverinfo='text'
        ))

    fig.update_layout(
        xaxis=dict(title="DISTANCE (NM)", gridcolor='#1e293b', tickfont=dict(size=10)),
        yaxis=dict(title="VOLUME (TONS)", gridcolor='#1e293b', tickfont=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#94a3b8", size=10),
        height=350,
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    return fig