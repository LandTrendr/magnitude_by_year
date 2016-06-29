# set_pixels_to_value.py

# See 'Breaking up output rasters by year and duration' on shared google docs

# set all pixels of a given raster that are > 0 to an integer value

import os, sys, numpy, gdal
from gdalconst import *

inputBSQPath = sys.argv[1]
bandNumber = int(sys.argv[2])
setValue = int(sys.argv[3])
outpath = sys.argv[4]

inputBSQ = gdal.Open(inputBSQPath)
raster = inputBSQ.GetRasterBand(bandNumber).ReadAsArray(0,0,inputBSQ.RasterXSize,inputBSQ.RasterYSize)
outRaster = numpy.where(raster > 0, setValue, 0)

driver = inputBSQ.GetDriver()
outfile = driver.Create(outpath,inputBSQ.RasterXSize,inputBSQ.RasterYSize,1,GDT_Byte)
outfile.SetGeoTransform(inputBSQ.GetGeoTransform())
outfile.SetProjection(inputBSQ.GetProjection())
outfile.GetRasterBand(1).WriteArray(outRaster)
outfile = None