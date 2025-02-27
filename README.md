# Yield Project

This project develops yield forecasting and damage assessment models for extensive crops using remotely sensed data, specifically targeting wind damage detection and crop health analysis. It leverages Google Earth Engine (GEE), Sentinel-2 imagery, and machine learning techniques.

## Setup

### Prerequisites
- Install WSL (Windows Subsystem for Linux) with Ubuntu.
- Install Miniconda or Anaconda in WSL.

### Environment Setup
1. Create and activate the Conda environment:
   ```bash
   conda create -n yield_project python=3.12
   conda activate yield_project
   ```

2. Install dependencies:
    ```bash
    conda install -c conda-forge gdal rasterio geopandas tensorflow
    pip install scikit-learn opencv-python matplotlib seaborn folium numpy pandas earthengine-api
    ```

## Google Earth Engine
- Register a Google Cloud Project and enable the Earth Engine API.
- Authenticate GEE in WSL:
  ```bash
  python -c "import ee; ee.Authenticate()"
  ```

- Initialize with your project ID:
  ```bash
  python -c "import ee; ee.Initialize(project='project-id')"
  ```

## Directory Structure
```bash
yield_project/
├── data/
│   ├── raw/                  # Satellite imagery 
│   ├── processed/             
│   ├── labels/               
│   └── metadata/             # Field boundaries, weather data
├── notebooks/                # Jupyter notebooks for exploration
├── results/                  # Output maps, statistics, visualizations
├── src/                      # Scripts for preprocessing, modeling, quantification
├── requirements.txt          
├── environment.yml           
└── README.md
```                 

## Usage
1. Add satelite imagery to data/raw/.
2. Run preprocessing:
  ```bash
  python src/preprocess.py
  ```
3. Run modeling:
  ```bash
  python src/modeling.py
  ```
4. Analyze results in notebooks/ or results/.

## Notes
- Adjust roi, dates, and bands in src/preprocess.py based on your imagery.
- Monitor GEE quotas in the Google Cloud Console.

## B.
- Create `environment.yml` at the root of `yield_project/` with:
    ```yaml
    name: yield_project
    channels:
    - conda-forge
    - defaults
    dependencies:
    - python=3.12
    - gdal
    - rasterio
    - geopandas
    - tensorflow
    - scikit-learn
    - opencv-python
    - matplotlib
    - seaborn
    - folium
    - numpy
    - pandas
    - earthengine-api
    - pip
    - pip:
        - earthengine-api  # Ensure the latest version via pip if needed
    ```

- Create the environment:
  ```bash
  conda env create -f environment.yml
  conda activate yield_project
  ```

## C. 
- Create requirements.txt at the root of yield_project/ with:
    ```bash
    earthengine-api
    gdal==3.10.2
    rasterio==1.4.3
    geopandas==1.0.1
    scikit-learn==1.6.1
    tensorflow==2.16.1
    opencv-python==4.11.0
    matplotlib==3.9.2
    seaborn==0.13.2
    folium==0.16.0
    numpy==2.2.3
    pandas==2.2.2
    ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## D.
