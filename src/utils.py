import rasterio
import numpy as np

def load_raster(path):
    """Load a raster file."""
    with rasterio.open(path) as src:
        return src.read(), src.transform, src.crs

def save_raster(data, transform, crs, path):
    """Save a raster file."""
    profile = {
        'driver': 'GTiff',
        'height': data.shape[1],
        'width': data.shape[2],
        'count': data.shape[0],
        'dtype': data.dtype,
        'crs': crs,
        'transform': transform,
    }
    with rasterio.open(path, 'w', **profile) as dst:
        dst.write(data)