import ee
ee.Initialize(project='yield-project-2025')
print(ee.Image('NASA/NASADEM_HGT/001').getInfo())
