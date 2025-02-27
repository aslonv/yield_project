import ee
import rasterio
import numpy as np

# Initialize Earth Engine with your project ID
ee.Initialize(project='yield-project-2025')

# Define your area of interest (replace with your coordinates)
roi = ee.Geometry.Rectangle([-122.4194, 37.7749, -122.4184, 37.7759])  # Example: San Francisco area

# Function to mask clouds in Sentinel-2 Harmonized images
def mask_s2_clouds(image):
    """Masks clouds in a Sentinel-2 Harmonized image using the QA60 band."""
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = (
        qa.bitwiseAnd(cloud_bit_mask)
        .eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )
    return image.updateMask(mask).divide(10000)  # Scale TOA reflectance by 10,000

# Get Sentinel-2 Harmonized imagery
collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
    .filterBounds(roi) \
    .filterDate('2025-01-01', '2025-02-27') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .sort('CLOUDY_PIXEL_PERCENTAGE', False) \
    .map(mask_s2_clouds)
image = collection.first().select(['B4', 'B8'])  # Red (B4), NIR (B8)

# Calculate NDVI (Normalized Difference Vegetation Index)
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

# Export to Google Drive
task = ee.batch.Export.image.toDrive(
    image=ndvi,
    description='sentinel2_ndvi_harmonized',
    folder='yield_project',
    scale=10,  # Sentinel-2 resolution
    region=roi,
    maxPixels=1e13  # Adjust if quota issues occur
)
task.start()
print("Export task started. Check Google Drive for results.")

# Optionally, process local imagery (e.g., your three-panel/2x2 grid images)
def preprocess_local_image(input_path, output_path):
    with rasterio.open(input_path) as src:
        data = src.read()  # Read all bands
        # Example: Atmospheric correction (simplified)
        corrected = data * 1.0  # Placeholder, adjust based on your data
        # Align and mask clouds (example)
        aligned = corrected  # Placeholder, use co-registration as needed
        cloud_mask = np.ones_like(aligned[0])  # Placeholder, implement cloud masking
        processed = aligned * cloud_mask[np.newaxis, :, :]
        # Write to output
        profile = src.profile
        profile.update(count=processed.shape[0])
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(processed)
    print(f"Processed image saved to {output_path}")

if __name__ == "__main__":
    preprocess_local_image('data/raw/pre_event.tif', 'data/processed/pre_event_processed.tif')
    preprocess_local_image('data/raw/post_event.tif', 'data/processed/post_event_processed.tif')