import geopandas as gpd
import numpy as np
import rasterio

def quantify_damage(damage_map, field_boundaries_path):
    """Quantify damaged area and severity per field."""
    # Load field boundaries
    fields = gpd.read_file(field_boundaries_path)
    damaged_area = np.sum(damage_map > 0.5) * 100  # Assuming 10m x 10m pixels
    total_area = damage_map.size * 100  # Total area in square meters
    damage_percentage = (damaged_area / total_area) * 100

    # Calculate severity (e.g., based on NDVI deviation)
    severity = np.clip((damage_map - damage_map.min()) / (damage_map.max() - damage_map.min()), 0, 1) * 100
    avg_severity = np.mean(severity[damage_map > 0.5])

    # Per-field statistics
    fields['damage_area'] = 0.0
    fields['severity'] = 0.0
    for idx, field in fields.iterrows():
        field_mask = damage_map[field.geometry.buffer(10).contains(damage_map)]
        fields.loc[idx, 'damage_area'] = np.sum(field_mask > 0.5) * 100
        fields.loc[idx, 'severity'] = np.mean(severity[field_mask > 0.5]) if np.any(field_mask > 0.5) else 0.0

    return damaged_area, damage_percentage, avg_severity, fields

if __name__ == "__main__":
    # Example usage (replace with actual paths)
    damage_map = np.random.rand(100, 100)  # Placeholder damage map
    fields_path = 'data/metadata/fields.geojson'  # Update with your field boundaries
    damaged_area, damage_percentage, avg_severity, fields_df = quantify_damage(damage_map, fields_path)
    print(f"Total damaged area: {damaged_area} m²")
    print(f"Damage percentage: {damage_percentage:.2f}%")
    print(f"Average severity: {avg_severity:.2f}%")
    fields_df.to_file('results/field_damage_stats.geojson')