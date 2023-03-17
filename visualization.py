# Input:
# - GIS data
# - Statistics per sensor
# Output:
# - A map that shows sensor locations and click will popup the statistics

import geopandas
import pandas as pd
import folium
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm


# Read the gis data
path_to_canton = "./spatial/canton"
path_to_astra = "./spatial/astra/"
path_to_dav = "./spatial/city/"
# path_to_loops = "./spatial/loops"
# Change the crs to EPSG:4326 (lat,long)
canton_gdf = geopandas.read_file(path_to_canton).to_crs("EPSG:4326")
astra_gdf = geopandas.read_file(path_to_astra).to_crs("EPSG:4326")
city_gdf = geopandas.read_file(path_to_dav).to_crs("EPSG:4326")
# loops_gdf = geopandas.read_file(path_to_loops).to_crs("EPSG:4326")


# Read the sensor statistics
# canton_sensor_df = pd.read_csv("./preprocessed_data/astra/example.csv", index_col=['sensor_id', 'date'])
astra_sensor_df = pd.read_csv("./preprocessed_data/astra/example.csv", index_col=['sensor_id', 'date'])

# Draw a figure for each sensor
# For canton
for sensor_id in tqdm(astra_gdf['detid']):
    fig=make_subplots(specs=[[{"secondary_y":True}]])

    # Draw #cars per day per sensor
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=astra_sensor_df['count'][2].keys(),
            y=astra_sensor_df['count'][2].values,
            name="#Cars per day",
            hoverinfo='none'                 #Hide the hoverinfo
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis (left)

    
    # fig.add_trace(                           #Add the second chart (line chart) to the figure
    #     go.Scatter(
    #     x=sensor_df[1]['date'],
    #     y=sensor_df[1]['count']/2,
    #     name="test",
    #     mode='lines',
    #     # text=sensor_df['text'],               
    #     # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
    #     line = dict(color='firebrick', width=3)#Specify the color of the line
    #      ),
    #     secondary_y=True)                   #The line chart uses the secondary y-axis (right)

    fig.update_layout(
                hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light gray
                title_text="Sensor info", #Add a chart title
                title_font_family="Times New Roman",
                title_font_size = 20,
                title_font_color="darkblue", #Specify font color of the title
                title_x=0.5, #Specify the title position
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        showticklabels = True,
                        dtick="D1", #Change the x-axis ticks to be monthly
                        tickformat="%y-%b-%d"
                        ),
                #  legend = dict(orientation = 'h', xanchor = "center", x = 0.72, y= 1), #Adjust legend position
                yaxis_title='#Cars',
                #  yaxis2_title=''
                )

    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="7d", step="day", stepmode="backward"),
            # dict(count=1, label="1m", step="month", stepmode="todate"),
            # dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ]))
    )

    fig.write_html("./figs/astra/"+sensor_id+".html")

# For astra

# For city

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

for index, row in astra_gdf.iterrows():
    html="""
    <iframe src=\"""" + "./figs/astra/" + row['detid'] + ".html" + """\"width="850" height="400"  frameborder="0">    
    """
    popup = folium.Popup(folium.Html(html, script=True))
    folium.CircleMarker(location=astra_geo_list[index], radius=5, color="crimson", fill=True, popup=popup).add_to(astra_sensors)

for sensor_position in canton_geo_list:
    folium.CircleMarker(location=sensor_position, radius=5, color="#3388ff", fill=True).add_to(canton_sensors)

for sensor_position in canton_geo_list:
    folium.CircleMarker(location=sensor_position, radius=5, color="pink", fill=True).add_to(city_sensors)

# for sensor_position in canton_geo_list:
#     folium.Marker(location=sensor_position, icon=folium.Icon(color="blue")).add_to(loops_sensors)

canton_sensors.add_to(map)
astra_sensors.add_to(map)
city_sensors.add_to(map)
# loops_sensors.add_to(map)

folium.LayerControl().add_to(map)
map.save('visualization.html')