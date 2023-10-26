import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from utils import *
import geopandas as gpd
import json

"""
Utilities for simplifying drawing, using plotly
"""

def draw_bar_plot(legends, x, y, layout_dict=dict(), trace_dict=dict(), icolor=None):
    """Draw a bar plot. You can pass multiple x's and y's such that they appear on the same graph. If 
    you want to draw for single x and y, remember also to use []brackets to embrace them.
    
    Args:
    - names: list of strings. legends
    - x: list of list. bin names
    - y: list of list. bin values
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config
    - icolor: list of integers. color index, if None, use default color scheme

    Returns:
    - Plotly figure
    """
    # Draw figure with random color
    colors = px.colors.qualitative.T10.copy() + px.colors.qualitative.G10.copy() + px.colors.qualitative.D3.copy() + px.colors.qualitative.Bold.copy()
    fig = go.Figure()
    for i in range(len(legends)):
        if icolor == None:
            marker_color = colors[i]
            colors.remove(marker_color)
        else:
            marker_color = colors[icolor[i]]
        fig.add_trace(
            go.Bar(
                name = legends[i],
                x = x[i],
                y = y[i],
                marker_color = marker_color
            )
        )
    
    # Basic config
    fig.update_layout(
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_traces(
        hoverinfo = "x+y"
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_bar_plot_with_slider(legends, x, y, layout_dict=dict(), trace_dict=dict(), icolor=None):
    """Draw a bar plot with slider that changes the data to show

    Args:
    - names: list. legend
    - x: list of list. bin names
    - y: list of list. bin values
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config
    - icolor: list of integers. color index, if None, use default color scheme

    Returns:
    - Plotly figure
    """
    # Draw figure with random color
    colors = px.colors.qualitative.T10.copy() + px.colors.qualitative.G10.copy() + px.colors.qualitative.D3.copy() + px.colors.qualitative.Bold.copy()
    
    fig = go.Figure()
    for i in range(len(legends)):
        if icolor == None:
            marker_color = colors[i]
            colors.remove(marker_color)
        else:
            marker_color = colors[icolor[i]]
        fig.add_trace(
            go.Bar(
                name = legends[i],
                x = x[i],
                y = y[i],
                marker_color = marker_color
            )
        )

    # Set sliders
    steps = []
    for i, legend in enumerate(legends):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(legends)}],
            label=legend
        )
        step["args"][0]["visible"][i] = True  
        steps.append(step)

    sliders = [dict(
        active=1,
        steps=steps
    )]

    # Basic config
    fig.update_layout(
        sliders = sliders,
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_traces(
        hoverinfo = "x+y"
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_layout(layout_dict)

    return fig


def draw_line_plot(legends, x, y, layout_dict=dict(), trace_dict=dict(), icolor=None):
    """Draw a line plot. You can pass multiple x's and y's such that they appear on the same graph. If 
    you want to draw for single x and y, remember also to use []brackets to embrace them.
    
    Args:
    - names: list. legend
    - x: list of list. 
    - y: list of list. 
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config
    - icolor: list of integers. color index, if None, use default color scheme

    Returns:
    - Plotly figure
    """
    # Draw figure with random color
    colors = px.colors.qualitative.T10.copy() + px.colors.qualitative.G10.copy() + px.colors.qualitative.D3.copy() + px.colors.qualitative.Bold.copy()
    fig = go.Figure()
    for i in range(len(legends)):
        if icolor == None:
            marker_color = colors[i]
            colors.remove(marker_color)
        else:
            marker_color = colors[icolor[i]]
        fig.add_trace(
            go.Scatter(
                name = legends[i],
                x = x[i],
                y = y[i],
                marker_color = marker_color
            )
        )
    
    # Basic config
    fig.update_layout(
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_traces(
        hoverinfo = "x+y",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_bubble_map(legend, lat, lon, z, layout_dict=dict(), mapbox_dict=dict(), trace_dict=dict()):
    """Draw a density map
    
    Args:
    - legend: string, legend
    - lat: list, latitude
    - lon: list. longititude
    - z: list, value of each point
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config

    Returns:
    - Plotly figure
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scattermapbox(
            name = legend,
            lat = lat,
            lon = lon,
            marker = dict(
                size = 13,
                color = z,
                showscale = True,
                colorscale = "Portland"
            ),
        )
    )

    # Basic config
    fig.update_layout(
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_mapboxes(
        center = dict(lat=47.384065708143886, lon=8.530691620597517), # Center of Zurich is used here, change it for your own case
        zoom = 12,
        style = "open-street-map",
    )
    fig.update_traces(
        hoverinfo = "all",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_mapboxes(mapbox_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_density_map(legend, lat, lon, z, layout_dict=dict(), mapbox_dict=dict(), trace_dict=dict()):
    """Draw a density map
    
    Args:
    - legend: string, legend
    - lat: list, latitude
    - lon: list. longititude
    - z: list, value of each point
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config

    Returns:
    - Plotly figure
    """
    fig = go.Figure()
    fig.add_trace(
        go.Densitymapbox(
            name = legend,
            lat = lat,
            lon = lon,
            z = z,
            radius = 10,
            opacity = 0.9,
            colorscale= "Portland"
        )
    )

    # Basic config
    fig.update_layout(
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_mapboxes(
        center = dict(lat=47.384065708143886, lon=8.530691620597517), # Center of Zurich is used here, change it for your own case
        zoom = 12,
        style = "open-street-map",
    )
    fig.update_traces(
        hoverinfo = "all",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_mapboxes(mapbox_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_density_map_with_slider(legends, lat, lon, z, layout_dict=dict(), mapbox_dict=dict(), trace_dict=dict()):
    """Draw a scatter geo map with a slide that changes the data to show
    
    Args:
    - legend: list of string, legend
    - lat: list of list, latitude
    - lon: list of list, longititude
    - z: list of list, value of each point
    - layout_dict: dictionary for updating default layout
    - trace_dict: dictionary for updating defauce trace config

    Returns:
    - Plotly figure
    """
    fig = go.Figure()
    for i in range(len(legends)):
        fig.add_trace(
            go.Densitymapbox(
                name = legends[i],
                lat = lat[i],
                lon = lon[i],
                z = z[i],
                radius = 10,
                opacity = 0.9,
                colorscale= "Portland"
            )
        )

    # Set sliders
    steps = []
    for i, legend in enumerate(legends):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(legends)}],
            label=legend
        )
        step["args"][0]["visible"][i] = True  
        steps.append(step)

    sliders = [dict(
        active=1,
        steps=steps
    )]

    # Basic config
    fig.update_layout(
        sliders = sliders,
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_mapboxes(
        center = dict(lat=47.384065708143886, lon=8.530691620597517), # Center of Zurich is used here, change it for your own case
        zoom = 12,
        style = "open-street-map",
    )
    fig.update_traces(
        hoverinfo = "all",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_mapboxes(mapbox_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_choropleth_map(legend, gdf, z, layout_dict=dict(), mapbox_dict=dict(), trace_dict=dict()):
    """Draw a choropleth map
    Note that the geo dataframe must contain a coloum named "id"

    Args:
    - gdf: geopandas dataframe
    - z: list, value of each geometry primitive
    - gdf: geo dataframe containing polygons
    - layout_dict: dictionary for updating default layout
    - mapbox_dict: dictionary for updating default mapbox config
    - trace_dict: dictionary for updating defauce trace config

    Returns:
    - Plotly figure
    """
    fig = go.Figure()
    geojson = json.loads(gdf.to_json())
    fig.add_trace(
        go.Choroplethmapbox(
            name=legend,
            featureidkey="properties.id",
            geojson=geojson,
            locations=gdf['id'].astype(str),
            z=z,
            marker_opacity=0.5, 
            marker_line_width=0.3,
            colorscale="Portland"
        )
    )

    # Basic config
    fig.update_mapboxes(
        center = dict(lat=47.384065708143886, lon=8.530691620597517), # Center of Zurich is used here, change it for your own case
        zoom = 12,
        style = "carto-positron"
    )
    fig.update_traces(
        hoverinfo = "all",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_mapboxes(mapbox_dict)
    fig.update_layout(layout_dict)    

    return fig

def draw_choropleth_with_slider(legends, gdf, z, layout_dict=dict(), mapbox_dict=dict(), trace_dict=dict()):
    """Draw a choropleth map with a slider that changes the data to show
    Note that the geo dataframe must contain a coloum named "id"
    
    Args:
    - legends: list of string, legend
    - gdf: geo dataframe containing polygons
    - z: list of list, value of each point
    - layout_dict: dictionary for updating default layout
    - mapbox_dict: dictionary for updating default mapbox config
    - trace_dict: dictionary for updating defauce trace config

    Returns:
    - Plotly figure
    """
    fig = go.Figure()
    geojson = json.loads(gdf.to_json())

    for i in range(len(legends)):
        fig.add_trace(
            go.Choroplethmapbox(
                name=legends[i],
                featureidkey="properties.id",
                geojson=geojson,
                locations=gdf['id'].astype(str),
                z=z[i],
                marker_opacity=0.5, 
                marker_line_width=0.3,
                colorscale="Portland"
            )
        )

    # Set sliders
    steps = []
    for i, legend in enumerate(legends):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(legends)}],
            label=legend
        )
        step["args"][0]["visible"][i] = True  
        steps.append(step)

    sliders = [dict(
        active=1,
        steps=steps
    )]

    # Basic config
    fig.update_layout(
        sliders = sliders,
        showlegend = True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_mapboxes(
        center = dict(lat=47.384065708143886, lon=8.530691620597517),
        zoom = 12,
        style = "carto-positron"
    )
    fig.update_traces(
        hoverinfo = "all",
    )

    # Custom config
    fig.update_traces(trace_dict)
    fig.update_mapboxes(mapbox_dict)
    fig.update_layout(layout_dict)

    return fig

def draw_scatter_3d(x, y, z, color, layout_dict=dict(), trace_dict=dict()):
    fig = px.scatter_3d(x=x, y=y, z=z, color=color)

    fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=0, xanchor="center", x=0.5),
            scene_camera=dict(up=dict(x=0, y=0, z=1), 
                                center=dict(x=0, y=0, z=-0.1),
                                eye=dict(x=1.5, y=-1.4, z=0.5)),
                                margin=dict(l=0, r=0, b=0, t=0),
            scene = dict(xaxis=dict(backgroundcolor='white',
                                    color='black',
                                    gridcolor='#f0f0f0',
                                    title_font=dict(size=10),
                                    tickfont=dict(size=10),
                                    ),
                        yaxis=dict(backgroundcolor='white',
                                    color='black',
                                    gridcolor='#f0f0f0',
                                    title_font=dict(size=10),
                                    tickfont=dict(size=10),
                                    ),
                        zaxis=dict(backgroundcolor='lightgrey',
                                    color='black', 
                                    gridcolor='#f0f0f0',
                                    title_font=dict(size=10),
                                    tickfont=dict(size=10),
                                    )))
    fig.update(layout_dict)
    fig.update(trace_dict)
    return fig

if __name__ == "__main__":
    """
    Test code below
    """
    id_path = "./preprocessed_data/city/city_id.csv"
    data_path = "./preprocessed_data/city"
    id = list(pd.read_csv(id_path)["detid"])
    weekend_df_dict = read_from_ids(id, "weekend", data_path)
    weekend_df_list = list(weekend_df_dict.values())
    weekend_agg_df = query(weekend_df_list, datetime(2018,1,1), datetime(2019,1,1), "month")

    # names = ["2018", "2019", "2020"]
    # x = [[i for i in range(1,13)]] * 3
    # y = [query(weekend_df_list, datetime(2018,1,1), datetime(2019,1,1), "month")["occ"], query(weekend_df_list, datetime(2019,1,1), datetime(2020,1,1), "month")["occ"], query(weekend_df_list, datetime(2020,1,1), datetime(2021,1,1), "month")["occ"]]
    # layout = dict(
    #     title = dict(
    #         text = "Average Weekend Traffic Occupancy in Zurich City for Months"
    #     ),
    #     xaxis_title = "Month",
    #     yaxis_title = "Occupancy"
    # )
    # fig = draw_line_plot(names, x, y, layout)
    # fig.write_html("test2.html")

    geo_sensor_path = "./spatial/loop_update_city/"
    geo_district_path =  "./spatial/districts/"

    city_gdf = gpd.read_file(geo_sensor_path).to_crs("EPSG:4326")
    city_geo_list = np.array([[point.xy[1][0], point.xy[0][0]] for point in city_gdf['geometry']])

    city_gdf_indexed = city_gdf.set_index("detid")
    lat = []
    lon = []
    sensor_data_list = []
    for detid in tqdm(city_gdf["detid"], desc="Collecting data for every sensor"):
        if detid in list(weekend_df_dict.keys()):
            sensor_data_list.append(query([weekend_df_dict[detid]], datetime(2018,1,1), datetime(2018,2,1), "month")["occ"])
            lat.append(city_gdf_indexed.loc[detid]["geometry"].xy[1][0])
            lon.append(city_gdf_indexed.loc[detid]["geometry"].xy[0][0])
    
    sensor_data_df = pd.concat(sensor_data_list, axis = 1).fillna(0)
    z = sensor_data_df.to_numpy()[0] * 10
    fig = draw_density_map("test", lat, lon, z)
    fig.write_html("test3.html")

    # district_gdf = gpd.read_file(geo_district_path).to_crs("EPSG:4326")
    # district_gdf['bezeichnun'] = district_gdf['bezeichnun'].apply(lambda x: x.replace(' ', '_'))
    # district_gdf.rename(columns={'bezeichnun': 'Kreis', 'objid': 'id'}, inplace=True)
    # district_gdf.to_file("district.json", driver="GeoJSON")
    # fig = draw_choropleth_map("test", district_gdf, np.random.rand(len(district_gdf.index)))
    # fig.write_html("test4.html")