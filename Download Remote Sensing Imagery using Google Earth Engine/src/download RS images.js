// LOAD NAIP DATA FOR THE SELECTED YEAR (2016) AND REGION OF INTEREST (ROI)
// PLEASE 
var naip = ee.ImageCollection('USDA/NAIP/DOQQ')
              .filterDate('2016-01-01', '2016-12-31') //Collect 2016 NAIP image
              .filterBounds(ROI)
              .mosaic()
              .clip(ROI); 

// CLIPPING NAIP IMAGERY BY GIVEN ROI
var ROI2016 = naip.clip(ROI);
var title = 'ROI2016'; //output image name

// MAPPING NAIP IMAGERY
Map.addLayer(ROI2016, {}, title);

// EXPORT CLIPPED IMAGE TO GOOGLE DRIVE
Export.image.toDrive({
  image: ROI2016,
  scale: 0.6, //0.6m spatial resolution
  maxPixels: 100000000000, //Specify higher maxPixels value if you intend to export a large area,
  region: ROI,
  folder: 'output', 
  description: title
});