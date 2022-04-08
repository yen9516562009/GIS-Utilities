// LOAD SPECIFIEC IMAGE COLLECTION FOR THE SELECTED YEAR AND REGION OF INTEREST (ROI) 
var naip = ee.ImageCollection('USDA/NAIP/DOQQ')
              .filterDate('2016-01-01', '2016-12-31') //Collect 2016 NAIP image
              .filterBounds(ROI)
              .mosaic()
              .clip(ROI); 

// CLIPPING NAIP IMAGERY BY ROI
var ROI2016 = naip.clip(ROI);
var title = 'ROI2016'; //output image name

// MAPPING SELECTED IMAGERY
Map.addLayer(ROI2016, {}, title);

// EXPORT CLIPPED IMAGE TO GOOGLE DRIVE
Export.image.toDrive({
  image: ROI2016,
  scale: 0.6, //0.6m spatial resolution
  maxPixels: 100000000000,
  region: ROI,
  folder: 'output', 
  description: title
});
