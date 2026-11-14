# Phuoc Son Landslide Susceptibility Mapping WebGIS (Sentinel-2 GEE & Ensemble ML)

## 1. Purpose & Scope
This repository hosts the interactive **Phuoc Son Landslide Susceptibility System**, an end-to-end WebGIS application for visualizing and querying landslide susceptibility across Phuoc Son District (Quang Nam Province, Vietnam) following the October 28, 2020 extreme rainfall event. The system integrates 10m Sentinel-2 imagery processed on Google Earth Engine (GEE), 12.5m ALOS PALSAR DEM derivatives, daily triggering rainfall, and three machine learning models (**Logistic Regression - LR**, **Random Forest - RF**, and **XGBoost**).

## 2. Architecture & Data Flow
- **Static WebGIS Frontend (`index.html`)**: Built with Leaflet.js, providing 7 thematic GeoTIFF overlays (`DuBao_PhuocLoc_XGBoost`, `NDVI_pre`, `NDVI_post`, `NDVI_diff`, `rainfall`, `slope`, `elevation`), KML landslide inventory polygons (12 landslide zones / 2,033 pixels; 14 non-landslide zones / 2,017 pixels), and dynamic continuous colorbar legends.
- **Serverless Spatial Lookup Engine (`cache/static_bundle.json`)**: Precomputed spatial raster grids and model probability matrices enabling real-time read-only pixel inspection on **GitHub Pages** without requiring a backend Python server.
- **Streamlit Cloud Adapter (`streamlit_app.py`)**: Self-contained Streamlit wrapper for optional one-click deployment on Streamlit Community Cloud (`share.streamlit.io`).

## 3. Usage / Deployment
### Option A: GitHub Pages (Recommended — Direct Fullscreen WebGIS)
1. Push this directory to a public GitHub repository (e.g., `https://github.com/dut2022/SatLoDat-PhuocSon`).
2. Navigate to **Settings → Pages** in your GitHub repository.
3. Under **Build and deployment**, select **Deploy from a branch**, choose branch `main` and folder `/ (root)`, then click **Save**.
4. Your interactive WebGIS will be live at `https://dut2022.github.io/<repo-name>/`.

### Option B: Streamlit Community Cloud
1. Go to `https://share.streamlit.io/` and click **Create app**.
2. Select your GitHub repository, branch `main`, and main file path `streamlit_app.py`.

## 4. Technical Notes, Edge Cases & Gotchas
- **Unified NDVI Color Scale**: Both pre-event (`NDVI_pre`, June–August 2020) and post-event (`NDVI_post`, October 2020–February 2021) layers are clipped strictly to `PhuocSon.shp` and rendered on a unified `[0.00, 1.00]` RdYlGn scale so vegetation loss is directly comparable.
- **Asset Size Optimization**: Raw multi-hundred-megabyte GeoTIFFs are pre-rendered into transparent georeferenced PNG overlays (`cache/*.png`, ~14 MB total) to comply with GitHub's 100 MB file size limit and ensure instant browser loading.
