# Input:
# - GIS data
# - Statistics per sensor
# Output:
# - A map that shows sensor locations and click will popup the statistics
#%%
import geopandas
import pandas as pd
import folium
import numpy as np
from plotly import graph_objects as go
from tqdm import tqdm
import os

def draw_sensor_statistics(data_folder, fig_folder):
    # Read the file
    for filename in tqdm(os.listdir(data_folder), "Drawing"):
        data = pd.read_csv(os.path.join(data_folder, filename), index_col=["detid", "date"])
        sensor_id = data.index.get_level_values(0)[0]
        columns = data.columns
        n_plot = len(columns)
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        fig = go.Figure()

        for i in range(len(columns)):
            fig.add_trace(
                go.Scatter(
                    x=data[columns[i]][sensor_id].keys(),
                    y=data[columns[i]][sensor_id].values,
                    name=columns[i],
                    yaxis="y" if i==0 else f"y{i+1}"
                )
            )
        
        fig.update_traces(
            hoverinfo="x+y",
            line={"width": 0.5},
            mode="lines",
            showlegend=False
        )

        layout_dict = dict(
            title_text="Sensor " + sensor_id + " info",
            title_x=0.5,
            title_font_family="Times New Roman",
            title_font_size = 20,
            xaxis=dict(
                tickfont_size=10,
                tickangle = 270,
                # showgrid = True,
                zeroline = True,
                showline = True,
                # showticklabels = True,
                # dtick="D1", #Change the x-axis ticks to be daily
                ),
        )
        
        for i in range(len(columns)):
            layout_dict['yaxis' if i==0 else f'yaxis{i+1}'] = dict(
                anchor="x",
                autorange=True,
                domain=[i/(n_plot+1) + i/(n_plot+1)/n_plot, (i+1)/(n_plot+1) + i/(n_plot+1)/n_plot],
                linecolor=colors[i],
                mirror=True,
                showline=True,
                side="right",
                tickfont={"color": colors[i]},
                tickmode="auto",
                titlefont={"color": colors[i]},
                type="linear",
                title=columns[i],
                zeroline=False
            )
        
        fig.update_layout(layout_dict)

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ]))
        )

        # Save the fig
        fig.write_html(os.path.join(fig_folder, sensor_id + ".html"))

#%%
# Read the gis data
path_to_canton = "./spatial/canton/"
path_to_astra = "./spatial/astra/"
path_to_city = "./spatial/city/"
# path_to_loops = "./spatial/loops"
# Change the crs to EPSG:4326 (lat,long)
canton_gdf = geopandas.read_file(path_to_canton).to_crs("EPSG:4326")
astra_gdf = geopandas.read_file(path_to_astra).to_crs("EPSG:4326")
city_gdf = geopandas.read_file(path_to_city).to_crs("EPSG:4326")
# loops_gdf = geopandas.read_file(path_to_loops).to_crs("EPSG:4326")


# Sensor statistics folder
# canton_sensor_df = pd.read_csv("./preprocessed_data/astra/example.csv", index_col=['detid', 'date'])
# astra_sensor_folder = "./preprocessed_data/astra/per_day"
city_sensor_folder = "./preprocessed_data/city/per_day/"
city_sensor_fig_folder = "./figs/city/per_day/"

#%%
# Draw a figure for each sensor
# For canton

# For astra

# For city
draw_sensor_statistics(city_sensor_folder, city_sensor_fig_folder)

#%%
# Set the map 
canton_geo_list = np.array([[point.xy[1][0], point.xy[0][0]] for point in canton_gdf['geometry']])
astra_geo_list = np.array([[point.xy[1][0], point.xy[0][0]] for point in astra_gdf['geometry']])
city_geo_list = np.array([[point.xy[1][0], point.xy[0][0]] for point in city_gdf['geometry']])
# loops_geo_list = np.array([[point.xy[1][0], point.xy[0][0]] for point in loops_gdf['geometry']])

start_location = np.mean(canton_geo_list, axis=0).tolist()
map = folium.Map(location=start_location, tiles="OpenStreetMap", zoom_start=10)


# Creat markers for sensors on the map
canton_sensors = folium.FeatureGroup(name="canton_sensors")
astra_sensors = folium.FeatureGroup(name="astra_sensors", show=False)
city_sensors = folium.FeatureGroup(name="city_sensors", show=False)
# loops_sensors = folium.FeatureGroup(name="loops_sensors")

for index, row in tqdm(city_gdf.iterrows(), desc="Adding to map"):
    html="""
    <iframe src=\"""" + city_sensor_fig_folder + row['detid'] + ".html" + """\"width="1200" height="800"  frameborder="0">    
    """
    popup = folium.Popup(folium.Html(html, script=True))
    folium.CircleMarker(location=city_geo_list[index], radius=5, color="crimson", fill=True, popup=popup).add_to(city_sensors)

for sensor_position in canton_geo_list:
    folium.CircleMarker(location=sensor_position, radius=5, color="#3388ff", fill=True).add_to(canton_sensors)

for sensor_position in astra_geo_list:
    folium.CircleMarker(location=sensor_position, radius=5, color="orange", fill=True).add_to(astra_sensors)

# for sensor_position in canton_geo_list:
#     folium.Marker(location=sensor_position, icon=folium.Icon(color="blue")).add_to(loops_sensors)

canton_sensors.add_to(map)
astra_sensors.add_to(map)
city_sensors.add_to(map)
# loops_sensors.add_to(map)

folium.LayerControl().add_to(map)
map.save('visualization.html')

# %%
