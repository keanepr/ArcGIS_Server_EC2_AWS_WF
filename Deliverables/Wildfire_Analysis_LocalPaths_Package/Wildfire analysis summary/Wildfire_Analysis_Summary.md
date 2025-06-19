
# 🔍 Final Interpretation of Results

## Wildfire Area vs. Distance to Nearest Fire Station – San Diego County (2017)

This analysis explored whether **greater distance from fire stations** correlates with **larger wildfire perimeters**, using fire centroids and projected distances to the closest fire stations in San Diego County.

### 📊 Key Findings:
- A **Pearson correlation coefficient (r) of 0.04** was calculated, with a **p-value of 0.271**.
- This indicates a **very weak** and **statistically insignificant** relationship between fire area and distance to the nearest fire station.
- In practical terms, **fires farther from fire stations did not consistently burn larger areas** in this 2017 dataset.

### 🔎 Additional Observations:
- A majority of fire perimeters were within **500–1000 km projected distances** from stations.
- The most extreme outliers (e.g., **Thomas Fire**) were labeled and suggest that other factors (e.g., wind, terrain, fuel load) may drive fire spread more than station proximity.

---

## 📌 Implications:
- **Emergency response planning** should **not rely solely on geographic distance** from stations as a predictor of fire severity.
- **Other spatial variables** — such as slope, fuel type, wind corridors, and time of ignition — likely have more explanatory power and should be included in a more comprehensive model.
- Nonetheless, this workflow demonstrates a **robust spatial analysis pipeline** combining shapefiles, projections, centroid analysis, and statistical testing in Python.
