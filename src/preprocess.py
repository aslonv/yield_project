import ee
import rasterio
import numpy as np

# Initialize Earth Engine with the project id
ee.Initialize(project='insert-your-project-id')

roi = ee.Geometry.Rectangle([-122.4194, 37.7749, -122.4184, 37.7759])  
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
    return image.updateMask(mask).divide(10000)  

collection = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
    .filterBounds(roi) \
    .filterDate('2025-01-01', '2025-02-27') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .sort('CLOUDY_PIXEL_PERCENTAGE', False) \
    .map(mask_s2_clouds)
image = collection.first().select(['B4', 'B8'])  

ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

task = ee.batch.Export.image.toDrive(
    image=ndvi,
    description='sentinel2_ndvi_harmonized',
    folder='yield_project',
    scale=10,  
    region=roi,
    maxPixels=1e13 
)
task.start()
print("Export task started. Check Google Drive for results.")

def preprocess_local_image(input_path, output_path):
    with rasterio.open(input_path) as src:
        data = src.read()  
        # Atmospheric correction 
        corrected = data * 1.0  # Placeholder, adjust based on your data
        # Align and mask clouds 
        aligned = corrected  # Placeholder, use co-registration as needed
        cloud_mask = np.ones_like(aligned[0])  # Placeholder, implement cloud masking
        processed = aligned * cloud_mask[np.newaxis, :, :]
        profile = src.profile
        profile.update(count=processed.shape[0])
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(processed)
    print(f"Processed image saved to {output_path}")

if __name__ == "__main__":
    preprocess_local_image('data/raw/pre_event.tif', 'data/processed/pre_event_processed.tif')
    preprocess_local_image('data/raw/post_event.tif', 'data/processed/post_event_processed.tif')
