# Wildfire Analysis: Fire Area vs. Distance to Fire Stations

## Overview
This Jupyter Notebook explores the relationship between wildfire size and proximity to fire stations within San Diego County, California.

**Hypothesis:**  
Wildfires that occur farther from fire stations tend to burn larger areas.

## Dataset Sources
- 🔥 `California_Fire_Perimeters_2017.shp`: Wildfire perimeters (statewide, filtered for San Diego County)
- 🚒 `Fire_Stations_CN.shp`: Location of fire stations across California (used to compute nearest station per fire)

## Files Included
- `Wildfire_Analysis_LocalPaths.ipynb` — The main notebook
- `California_Fire_Perimeters_2017.*` — Shapefile components for wildfire perimeters
- `Fire_Stations_CN.*` — Shapefile components for fire stations

## How to Use
### Step 1: Unzip the package
Extract all contents to a local folder.

### Step 2: Open the Notebook
Using Anaconda Navigator or Jupyter:
- Navigate to the extracted folder
- Launch the notebook: `Wildfire_Analysis_LocalPaths.ipynb`

### Step 3: Run the Analysis
The notebook will:
- Load shapefiles using relative paths
- Calculate distance to nearest fire station
- Plot area vs. distance
- Compute and display Pearson correlation
- Annotate top 5 largest and most distant fire events

## Requirements
This notebook assumes the following Python packages are installed:
- `geopandas`
- `fiona`
- `shapely`
- `matplotlib`
- `seaborn`
- `scipy`
- `pandas`

Install them via Anaconda or pip if missing.

## Output
- 📈 Scatterplot showing fire size vs. distance to nearest station
- 📊 Statistical correlation results
- 🔖 Labeled high-risk fire events

## License
Data sources are public domain (CA Fire, Sangis, OpenTopo). This analysis is shared under MIT License.
