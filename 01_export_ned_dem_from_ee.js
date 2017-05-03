var baseName = 'conus_ned_dem';
var srtmDEM = ee.Image("USGS/NED").resample('bicubic');
var fc = ee.FeatureCollection('ft:1yZQioeTJ7GxiTyis2AWi-EzYvOY42cMC2gRwCtCO');
var affine = [30.0, 0, 15.0, 0, -30.0, 15.0];

for(var i=0; i<=15; i++){
  var chunkInt = i;
  var chunkStr = (chunkInt < 10 ? '0'+chunkInt.toString() : chunkInt.toString());
  var aoi = fc.filter(ee.Filter.eq('id', chunkInt)).geometry();
  var description = baseName+'_chunk_'+chunkStr;
  var box = aoi.bounds(); // get the bounds from the drawn polygon
  Export.image.toDrive({'image': srtmDEM, 'region': box, 'description': description, 'folder': description, 'fileNamePrefix': description, 'crs': 'EPSG:5070', 'crsTransform': affine, 'maxPixels': 1e13});
}
