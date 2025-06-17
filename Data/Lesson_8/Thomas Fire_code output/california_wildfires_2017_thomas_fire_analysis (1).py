# California wildfires 2017 - Thomas Fire analysis

import arcgis
from arcgis import *
from arcgis.layers import Service

gis = GIS(profile="your_online_profile")

from ipywidgets import *

postfire = Service('https://tiles.arcgis.com/tiles/DO4gTjwJVIJ7O9Ca/arcgis/rest/services/Digital_Globe_Imagery_Dec_11th/MapServer')

def side_by_side(address):
    location = geocode(address)[0]

    satmap1 = gis.map(location)
    satmap1.basemap.basemap = 'satellite'

    satmap2 = gis.map(location)
    satmap2.content.add(postfire)
    
    # Create VBoxes for each map and label
    box1 = VBox([satmap1], layout=Layout(width='50%'))
    box2 = VBox([satmap2], layout=Layout(width='50%'))

    # Place the VBoxes side by side using an HBox
    hbox = HBox([box1, box2])

    # Display the HBox
    display(hbox)

side_by_side('Montclair Dr, Ventura, CA')

side_by_side('801 Seneca St, Ventura, CA 93001')

landsat_item = gis.content.get('d9b466d6a9e647ce8d1dd5fe12eb434b')
landsat = landsat_item.layers[0]
landsat_item

aoi = {'spatialReference': {'latestWkid': 3857, 'wkid': 102100}, 'type': 'extent', 
       'xmax': -13305000, 'xmin': -13315000, 'ymax': 4106000, 'ymin': 4052000}

arcgis.env.analysis_extent = {"xmin":-13337766,"ymin":4061097,"xmax":-13224868,"ymax":4111469,
                              "spatialReference":{"wkid":102100,"latestWkid":3857}}

landsat.extent = aoi

import pandas as pd
from datetime import datetime

selected = landsat.filter_by(where="(Category = 1)",
                             time=[datetime(2017, 11, 15), datetime(2018, 1, 1)],
                             geometry=arcgis.geometry.filters.intersects(aoi))

df = selected.query(out_fields="AcquisitionDate, GroupName, CloudCover, DayOfYear", 
                    order_by_fields="AcquisitionDate").sdf
df['AcquisitionDate'] = pd.to_datetime(df['AcquisitionDate'], unit='ms')
df.tail(5)

prefire = landsat.filter_by('OBJECTID=' + str(df['OBJECTID'][0])) # 2017-11-23 
midfire = landsat.filter_by('OBJECTID=' + str(df['OBJECTID'][1])) # 2017-12-09 

from arcgis.raster.functions import *

apply(midfire, 'Natural Color with DRA')

extract_band(midfire, [6,4,1])

extract_band(prefire, [6,4,1])

nbr_prefire  = band_arithmetic(prefire, "(b5 - b7) / (b5 + b7+1000)")
nbr_postfire = band_arithmetic(midfire, "(b5 - b7) / (b5 + b7+1000)")

nbr_diff = nbr_prefire - nbr_postfire

burnt_areas = colormap(remap(nbr_diff,
                             input_ranges=[0.1,  0.27,  # low severity 
                                           0.27, 0.44,  # medium severity
                                           0.44, 0.66,  # moderate severity
                                           0.66, 1.00], # high severity burn
                             output_values=[1, 2, 3, 4],                    
                             no_data_ranges=[-1, 0.1], astype='u8'), 
                             colormap=[[4, 0xFF, 0xC3, 0], [3, 0xFA, 0x8E, 0], [2, 0xF2, 0x55, 0], [1, 0xE6, 0,    0]])

burnt_areas.draw_graph()

ext = {"xmax": -13246079.10806628, "ymin": 4035733.9433013694, "xmin": -13438700.419344831, "ymax": 4158033.188557592,
       "spatialReference": {"wkid": 102100, "latestWkid": 3857}, "type": "extent"}
pixx = (ext['xmax'] - ext['xmin']) / 1200.0
pixy = (ext['ymax'] - ext['ymin']) / 450.0

res = burnt_areas.compute_histograms(ext, pixel_size={'x':pixx, 'y':pixy})

numpix = 0
histogram = res['histograms'][0]['counts'][1:]
for i in histogram:
    numpix += i

from IPython.display import HTML
sqmarea = numpix * pixx * pixy # in sq. m
acres = 0.00024711 * sqmarea   # in acres

HTML('<h3>Thomas fire has consumed <i>{:,} acres</i>  till {}</h3>.'.format(int(acres), df.iloc[-1]['AcquisitionDate'].date()))

import matplotlib.pyplot as plt
%matplotlib inline

plt.title('Distribution by severity', y=-0.1)
plt.pie(histogram, labels=['Low Severity', 'Medium Severity', 'Moderate Severity', 'High Severity']);
plt.axis('equal');

m = gis.map('Carpinteria, CA')
m

m.content.add([midfire, burnt_areas])

persisted_fire_output = burnt_areas.save()
persisted_fire_output_layer = persisted_fire_output.layers[0]
fire_item = persisted_fire_output_layer.to_features(output_name='ThomasFire_Boundary')

fire_layer = fire_item.layers[0]
fire_layer.filter = 'st_area_sh > 3000000'

fire = gis.content.search('ThomasFire_Boundary', 'Feature Layer')[0]
fire

from arcgis.geoenrichment import enrich
from arcgis.features import SpatialDataFrame, FeatureLayer

sdf = pd.DataFrame.spatial.from_layer(fire.layers[0])

fire_geometry = sdf.iloc[0].SHAPE
sa_filter = geometry.filters.intersects(geometry=fire_geometry, sr=4326)

secondary_roads_layer = FeatureLayer("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Transportation_LargeScale/MapServer/1")
secondary_roads = secondary_roads_layer.query(geometry_filter=sa_filter, out_sr=4326)

local_roads_layer = FeatureLayer("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Transportation_LargeScale/MapServer/2")
local_roads = local_roads_layer.query(geometry_filter=sa_filter, out_sr=4326)

def age_pyramid(df):
    import warnings
    import seaborn as sns
    import matplotlib.pyplot as plt

    %matplotlib inline
    warnings.simplefilter(action='ignore', category=FutureWarning)
    pd.options.mode.chained_assignment = None 
    plt.style.use('ggplot')

    df = df[[x for x in impacted_people.columns if 'MALE' in x or 'FEM' in x]]
    sf = pd.DataFrame(df.sum())
    sf['age'] = sf.index.str.extract('(\d+)').astype('int64')

    f = sf[sf.index.str.startswith('FEM')]
    m = sf[sf.index.str.startswith('MALE')]
    f = f.sort_values(by='age', ascending=False).set_index('age')
    m = m.sort_values(by='age', ascending=False).set_index('age')

    popdf = pd.concat([f, m], axis=1)
    popdf.columns = ['F', 'M']
    popdf['agelabel'] = popdf.index.map(str) + ' - ' + (popdf.index+4).map(str)
    popdf.M = -popdf.M
    
    sns.barplot(x="F", y="agelabel", color="#CC6699", label="Female", data=popdf, edgecolor='none')
    sns.barplot(x="M",  y="agelabel", color="#008AB8", label="Male",   data=popdf,  edgecolor='none')
    plt.ylabel('Age group')
    plt.xlabel('Number of people');
    return plt;

impactmap = gis.map('Carpinteria, CA')
impactmap.basemap.basemap = 'streets-vector'

impactmap

impactmap.content.draw(local_roads)
impactmap.content.draw(secondary_roads)

impacted_people = enrich(sdf, 'Age')
age_pyramid(impacted_people);
