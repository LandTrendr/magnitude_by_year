'''
segment_split.py

Stretches segment value map (1 value/band per segment) into yearly map.
Does NOT divide values by duration of segment.

Inputs:
-vertyrs_path
-segvals_path [ie. durs, mags, mse..]
-output_path
-meta_desc (opt.)

Output:
- multiband raster with 1 year per band

Usage:
python segment_split.py <vertyrs_path> <segvals_path> <output_path> [meta_desc]
'''
import sys, os, gdal
from gdalconst import *
from lthacks.intersectMask import *

def main(vertyrsPath, segvalsPath, outputPath, meta=None):

	#open vertyrs data
	ds_yrs = gdal.Open(vertyrsPath, GA_ReadOnly)
	numVertices = ds_yrs.RasterCount #vertices bands
	cols = ds_yrs.RasterXSize
	rows = ds_yrs.RasterYSize
	transform = ds_yrs.GetGeoTransform()
	projection = ds_yrs.GetProjection()
	driver = ds_yrs.GetDriver()
	
	#open segvals data
	ds_vals = gdal.Open(segvalsPath, GA_ReadOnly)
	numSegments = ds_vals.RasterCount
	
	#accumulate vertex bands into list
	print "\nAccumulating vertyrs bands..."
	
	allVertices = []
	
	for b in range(1, numVertices+1):
	
		band = ds_yrs.GetRasterBand(b)
		inputData = band.ReadAsArray()
		allVertices.append(inputData)
		
		if b == 1:
			startYear = np.min(inputData[inputData > 0])
			print startYear
		if b == numVertices:
			endYear = np.max(inputData)
			print endYear
		
	del band, inputData, b
	
	#accumulate mse bands into list
	print "\nAccumulating segment value bands..."
	
	allSegments = []
	
	for b in range(1, numSegments+1):
	
		band = ds_vals.GetRasterBand(b)
		inputData = band.ReadAsArray()
		allSegments.append(inputData)
	
	del band, inputData, b
	
	#calculate yearly segment value
	print "\nCalculating yearly segment value..."	
	
	years = range(startYear, endYear+1)
	outBands = [np.zeros((rows, cols)) for i in years]	
		
	for ind,bandData in enumerate(allVertices):
	
		print "\n\tBand: ", ind+1
		
		if ind == 0:
			prevData = bandData
			continue
		else:
			diffData = bandData - prevData #difference in years
		
		for y in years:
			print "\t\tYear: ", y 
			
			#find pixels where current band year is greater than prev band year,
			#current band year is greater or equal to band year to fill,
			#and previous band year is less than or equal to band year to fill
			changePixels = np.where( (diffData > 0) & (bandData >= y) & (prevData <= y) )
			
			#assign pixel values to outbands for changing pixels
			outBands[y-startYear][changePixels] = allSegments[ind-1][changePixels]
			
			del changePixels
			
		prevData = bandData
	
		#3 is integer type; save after each iteration
		saveArrayAsRaster_multiband(outBands, transform, projection, driver, outputPath, 3)
		
	createMetadata(sys.argv, outputPath, description=meta)
	
	
if __name__ == '__main__':
	
	args = sys.argv[1:]
	
	if len(args) != 3 and len(args) != 4:
		errMsg = "Inputs not understood. Usage:\npython segment_split.py {vertyrs_path} \
		{segvals_path} {output_path} [{metadata_desc}]"
		sys.exit(errMsg)
		
	else: 
		sys.exit(main(*args))
			
		
		
		
			
		
		
		
		
		
		
		