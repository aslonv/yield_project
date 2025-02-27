import rasterio
import numpy as np
from skimage.feature import graycomatrix, graycoprops
import cv2

def calculate_ndvi(nir, red):
    """Calculate NDVI from NIR and Red bands."""
    return (nir - red) / (nir + red + 1e-10) 

def texture_analysis(image):
    """Extract texture features using GLCM."""
    gray = cv2.convertScaleAbs(image) 
    glcm = graycomatrix(gray, [1], [0], 256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0][0]
    return contrast

def extract_features(input_path):
    """Extract NDVI and texture features from a raster file."""
    with rasterio.open(input_path) as src:
        data = src.read()  
        red = data[0]  
        nir = data[1]  
        ndvi = calculate_ndvi(nir, red)
        texture = texture_analysis(nir)  
        return ndvi, texture

if __name__ == "__main__":
    # Example usage
    pre_ndvi, pre_texture = extract_features('data/processed/pre_event_processed.tif')
    post_ndvi, post_texture = extract_features('data/processed/post_event_processed.tif')
    print(f"Pre-event NDVI shape: {pre_ndvi.shape}, Texture: {pre_texture}")
    print(f"Post-event NDVI shape: {post_ndvi.shape}, Texture: {post_texture}")