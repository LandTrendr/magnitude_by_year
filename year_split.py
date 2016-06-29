'''
Year Split.
Produces yearly stacks from change label maps or patch maps with 1 year band & 1 value band 
& 1 dur band, if applicable.

Usage:
  year_split.py <yearmap> <yearband> <magmap> <magband> <startyear> <endyear> <output> [--durmap=<dm>] [--durband=<db>] [--dividebydur=<div>] [--meta=<m>]
  year_split.py -h | --help
  
Options:
  -h --help         		Show this screen.
  --durmap=<dm>         	Path to raster containing duration band.
  --durband=<db>			Band of durmap that contains the duration of patches.
  --dividebydur=<div>       Divide magnitude by duration to determine yearly mag? [default: False].
  --meta=<m>				Additional notes for meta.txt file.
'''

import os, sys, gdal, glob, docopt
import numpy as np
from gdalconst import *
import lthacks.intersectMask as imask
from lthacks.lthacks import *
    
def year_split(year, yearRaster, durationRaster, assignRaster):
    # All inputs are numpy arrays except outfile       
    # loop over years and write out bands
    # locations in the year and duration = 1, others = 0
    yearChanges = np.where((yearRaster + durationRaster - 1 >= year) & (year >= yearRaster) 
    & (yearRaster > 0), assignRaster, 0)

    return yearChanges

def main(args):
    
    #accumulate all input maps
    allmaps = [args['<yearmap>'], args['<magmap>']]
    if args['--durmap']: 
    	allmaps.append(args['--durmap'])
    
    #find common bounds between input maps
    common_size, common_transform, projection, driver = imask.findLeastCommonBoundaries(allmaps)
    cols = int(common_size[0])
    rows = int(common_size[1])
    (midx, midy) = imask.transformToCenter(common_transform, cols, rows)
    
    #load year data
    year_ds = gdal.Open(args['<yearmap>'])
    year_transform = year_ds.GetGeoTransform()
    year_data = extract_kernel(year_ds, midx, midy, cols, rows, args['<yearband>'], 
    year_transform)
    del year_ds, year_transform
    
    #load magnitude data
    mag_ds = gdal.Open(args['<magmap>'])
    mag_transform = mag_ds.GetGeoTransform()
    mag_data = extract_kernel(mag_ds, midx, midy, cols, rows, args['<magband>'], 
    mag_transform)
    mag_band = mag_ds.GetRasterBand(args['<magband>'])
    nodata = mag_band.GetNoDataValue()
    outType = mag_band.DataType
    del mag_ds, mag_band, mag_transform
    
    #load duration data
    if args['--durmap']:
    	dur_ds = gdal.Open(args['--durmap'])
    	dur_transform = dur_ds.GetGeoTransform()
    	dur_data = extract_kernel(dur_ds, midx, midy, cols, rows, args['--durband'], 
    	dur_transform)
    	del dur_ds, dur_transform
    	
    else:
		dur_data = np.zeros((rows, cols))
		dur_data = 1
    	
    if args['--dividebydur']:
    	durationRasterOnes = np.where(dur_data==0, 1, dur_data)
    	mag_data = mag_data/durationRasterOnes

    #get year range
    bandRange = args['<endyear>'] - args['<startyear>'] + 1
    
    # Enter years as wavelength values in the .hdr file
    wavelength_string = "wavelength = {"
    
    # Loop year_split and add years to wavelength values
    years = range(args['<startyear>'], args['<endyear>'] + 1)
    outbands = []
    for year in years:
    
        print "Working on year:", year

        outband = year_split(year, year_data, dur_data, mag_data)
        outbands.append(outband)
        wavelength_string = wavelength_string + " " + str(year) + ","

    wavelength_string = wavelength_string + "}"
    
    #save all yearly bands
    imask.saveArrayAsRaster_multiband(outbands, common_transform, projection, driver, 
    args['<output>'], outType, nodata=nodata)
    
    # Edit .hdr file to include years
    f = open(args['<output>'][:-3] + "hdr",'a')
    f.write("\n")
    f.write("wavelength units = Unknown \n")
    f.write(wavelength_string)
    f.close()

    #write meta.txt file
    this_script = os.path.abspath(__file__)
    createMetadata(sys.argv, args['<output>'], description=args['--meta'], 
    lastCommit=getLastCommit(this_script))

if __name__ == '__main__':

    try:
        #parse arguments, use file docstring as parameter definition
		args = docopt.docopt(__doc__)
		
		#format args
		int_args = ['<yearband>', '<magband>', '<startyear>', '<endyear>', '--durband']
		for i in int_args:
			if args[i]:
				args[i] = int(args[i])
		
		if 'f' in args['--dividebydur'].lower():
			args['--dividebydur'] = False
		elif 't' in args['--dividebydur'].lower():
			args['--dividebydur'] = True
		else:
			sys.exit('--dividebydur argument not understood. Please enter True or False')	

		#call main function
		main(args)

    #handle invalid options
    except docopt.DocoptExit as e:
        print e.message
	