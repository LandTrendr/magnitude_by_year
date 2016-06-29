'''
mse_split.py

Usage: mse_split.py {vertyrs_path} {mse_path} {output_path}

'''

import sys, os, gdal
from gdalconst import *
from lthacks.intersectMask import *

YEARS = range(1984,2013)

def main(vertyrsPath, msePath, outputPath):

	#open vertyrs data
	ds_yrs = gdal.Open(vertyrsPath, GA_ReadOnly)
	numVertices = ds_yrs.RasterCount #vertices bands
	cols = ds_yrs.RasterXSize
	rows = ds_yrs.RasterYSize
	transform = ds_yrs.GetGeoTransform()
	projection = ds_yrs.GetProjection()
	driver = ds_yrs.GetDriver()
	
	#open mse data
	ds_mse = gdal.Open(msePath, GA_ReadOnly)
	numSegments = ds_mse.RasterCount
	
	#accumulate vertex bands into list
	print "\nAccumulating vertyrs bands..."
	
	allVertices = []
	
	for b in range(1, numVertices+1):
	
		band = ds_yrs.GetRasterBand(b)
		inputData = band.ReadAsArray()
		allVertices.append(inputData)
		
	del band, inputData, b
	
	#accumulate mse bands into list
	print "\nAccumulating mse bands..."
	
	allMSE = []
	
	for b in range(1, numSegments+1):
	
		band = ds_mse.GetRasterBand(b)
		inputData = band.ReadAsArray()
		allMSE.append(inputData)
	
	del band, inputData, b
	
	
	#calculate year MSE	
	print "\nCalculating yearly mse..."	
	
	outBands = [np.zeros((rows, cols)) for i in YEARS]	
		
	for ind,bandData in enumerate(allVertices):
	
		print "\n\tBand: ", ind+1
		
		if ind == 0:
			prevData = bandData
			continue
		else:
			diffData = bandData - prevData
		
		for y in YEARS:
			print "\t\tYear: ", y 
		
			#pixels where current band year is greater than prev band year
			#changePixels = (diffData > 0) 
			
			#pixels where additionally current band year is greater than band to fill 
			#changePixels = np.logical_and(changePixels, (bandData >= y))
			
			#pixels where additionally previous band year is less than or equal to band to fill
			#changePixels = np.logical_and(changePixels, (prevData <= y))
			
			changePixels = np.where( (diffData > 0) & (bandData >= y) & (prevData <= y) )
			
			#assign pixel values to outbands for changing pixels
			outBands[y-1984][changePixels] = allMSE[ind-1][changePixels]
			
		prevData = bandData
	
		#3 is integer type; save after each iteration
		saveArrayAsRaster_multiband(outBands, transform, projection, driver, outputPath, 3)
		
	createMetadata(sys.argv, outputPath, description="Yearly mse.")
	
	
if __name__ == '__main__':
	args = sys.argv
	sys.exit(main(args[1], args[2], args[3]))
			