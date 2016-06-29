'''
vertvals_split.py

Stretches vertex value map (1 value/band per vertex) into yearly map.

Inputs:
-vertyrs_path
-vertvals_path [ie. vertvals, durs, mags..]
-divide_bool [True/False - divide by duration?]
-output_path
-metadata_desc (opt.)

Output:
-map with 1 band per year representing vertvals

Usage: 
python vertvals_split.py <vertyrs_path> <vertvals_path> <divide_bool> <output_path> [metadata_desc]
'''
import sys, os, gdal
import numpy as np
from gdalconst import *
from lthacks.intersectMask import *


def interpolateBands(years, listOfBands):
	
	numbands = len(listOfBands)
	bandshape = listOfBands[0].shape
	newbands = [np.zeros(bandshape) for i in numbands]
	
	matrix = np.array(listOfBands)
	
	toFill = np.where(matrix[:,1000,1000] != 0)
	
	for b,band in enumerate(listOfBands):
	
		year = years[b]
		
		if (b == 0):
			
			x1 = np.zeros(bandshape)
			x1 = year
			
			y1 = band
			
			newbands = listOfBands
			
			continue
			
		else:
			
			nonzeros = np.where(band != 0)	
			
			y2 = y1
			y2[nonzeros] = band[nonzeros] #non-zero pixel values of current band/year
			x2 = x1
			x2[nonzeros] = years[b] #year is filled out where non-zero pixel values are
			
			slope = (y2[nonzeros] - y1[nonzeros]) / (x2[nonzeros] - x1[nonzeros])
			b = y2[nonzeros] - (slope[nonzeros] * x2[nonzeros])
			
			minYear = np.min(x1) + 1
			maxYear = np.max(x2)
			yearsToFill = range(minYear, maxYear)
			
			for fillYear in yearsToFill:
				
				fillBand = years.index(fillYear)
				
				fillVal = slope*fillYear + b
				
				newbands[fillBand][nonzeros] = fillVal
				
			y1 = y2
			x1 = x2
			

	return newbands


def main(vertyrsPath, vertvalsPath, divideBool, outputPath, metaDesc=None):

	#determine if slope needs to be calculated
	if type(divideBool) is str:
		if ("t" in divideBool.lower()) or ("1" in divideBool):
			divide = True
		else:
			divide = False
	else:
		divide = bool(divideBool)
		 
	#open vertyrs data
	ds_yrs = gdal.Open(vertyrsPath, GA_ReadOnly)
	numVertices = ds_yrs.RasterCount #vertices bands
	cols = ds_yrs.RasterXSize
	rows = ds_yrs.RasterYSize
	transform = ds_yrs.GetGeoTransform()
	projection = ds_yrs.GetProjection()
	driver = ds_yrs.GetDriver()
	
	#open vertvals data
	ds_vals = gdal.Open(vertvalsPath, GA_ReadOnly)
	
	#accumulate vertex bands into list
	print "\nAccumulating vertyrs/vertvals bands..."
	
	allYears = []
	allVals = []
	for b in range(1, numVertices+1):
	
		band_yrs = ds_yrs.GetRasterBand(b)
		data_yrs = band_yrs.ReadAsArray()
		allYears.append(data_yrs)
		
		band_vals = ds_vals.GetRasterBand(b)
		data_vals = band_vals.ReadAsArray()
		allVals.append(data_vals)
		
	del band_yrs, band_vals, data_yrs, data_vals, b
	
	startYear = np.min(allYears[0][allYears[0] != 0])
	endYear = np.max(allYears[1])
	years = range(startYear, endYear+1)

	#calculate year MSE	
	print "\nCalculating yearly values..."	
	
	outBands = [np.zeros((rows, cols)) for i in years]	
		
	for ind,currYears in enumerate(allYears):
	
		print "\n\tVertex: ", ind+1
		
		if not divide:
			if ind == 0:
				prevYears = currYears
				continue
			else:
				diffData = currYears - prevYears
		
		for y in years:
			print "\t\tYear: ", y 

			if not divide:
				#assign pixel values to outbands for changing pixels
				changePixels = np.where( (diffData > 0) & (currYears >= y) & (prevYears <= y) )
				outBands[y-startYear][changePixels] = allVals[ind-1][changePixels]
				
			else:
			
				changePixels = np.where(currYears == y)
				outBands[y-startYear][changePixels] = allVals[ind][changePixels]
				
				outBands = interpolateBands(outBands)
				
		prevYears = currYears
	
		#3 is integer type; save after each iteration
		saveArrayAsRaster_multiband(outBands, transform, projection, driver, outputPath, 3)
		
	createMetadata(sys.argv, outputPath, description=metaDesc)
	
	
if __name__ == '__main__':
	args = sys.argv

	inputs = args[1:]
	
	if (len(inputs) < 4) or (len(inputs) > 5):
	
		err = "\nInputs not understood. Proper usage:\npython vertvals_split.py \
 		{vertyrs_path} {vertvals_path} {divide_bool} {output_path} [{metadata_description}]"
 		sys.exit(err)
 		
 	else:
 	
		sys.exit(main(*inputs))
	

	