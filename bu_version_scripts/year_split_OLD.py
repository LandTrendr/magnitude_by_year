# year_split.py
# prep_year_split_mag_and_dur.py and prep_year_split_attribution.py both currently call this script

# See 'Breaking up output rasters by year and duration' on shared google docs

import os, sys, numpy, gdal, glob
from gdalconst import *
from lthacks.lthacks import *

# Hard code the minimum and maximum output years if necessary
# will only need if different than vertyrs min and max values
minYear = 1984
maxYear = 2012

LAST_UPDATED = "08/26/2015" #by Tara Larrue - added metadata

def inputs():
    # Path of the year and duration .bsq
    yearDurationBSQPath = sys.argv[1]
    # file we're splitting up by year
    inputBSQPath = sys.argv[2]
    # division by duration? Set to either 'True' or 'False'
    divByDur = sys.argv[3]
    inputBandNumber = int(sys.argv[4])
    outpathname = os.path.abspath(sys.argv[5])
    return yearDurationBSQPath, inputBSQPath, divByDur, inputBandNumber, outpathname

# def getYearRange(yearDurationBSQPath):
#     print 'getYearRange'
#     # get the range of years from the vertyrs file for the TSA
#     splitpath = yearDurationBSQPath.split('/')
#     filepath = '/'.join(splitpath[:-2])
#     os.chdir(filepath)
# 
#     splitfile = os.path.basename(yearDurationBSQPath).split('_')
#     paramset = splitfile[4]
#     print paramset
#     filelist = glob.glob('*_{param}_*_vertyrs.bsq'.format(param=paramset))
#     if len(filelist) > 1: 
#         sys.exit("Only one reference file expected in {0}".format(dir))
#     elif len(filelist) == 0:
#         sys.exit("No vertyrs.bsq file found for TSA {0}".format(splitpath[4]))
#     else:
#         fullfilepath = os.path.join(filepath,filelist[0])
#         print fullfilepath
#         vertyrsBSQ = gdal.Open(fullfilepath)
#         for bandInd in range(1,vertyrsBSQ.RasterCount+1):
#             print 'Band Number:', bandInd
#             bandArray = vertyrsBSQ.GetRasterBand(bandInd).ReadAsArray(0,0,vertyrsBSQ.RasterXSize,vertyrsBSQ.RasterYSize)
#             if bandInd == 1: 
#                 minYear = numpy.nanmin(numpy.where(bandArray != 0, bandArray, numpy.nanmax(bandArray)))
#                 maxYear = numpy.nanmax(bandArray)
#             if bandInd > 1:
#                 minYearTest = numpy.nanmin(numpy.where(bandArray != 0, bandArray, numpy.nanmax(bandArray)))
#                 maxYearTest = numpy.nanmax(bandArray)
#                 if minYearTest < minYear: minYear = minYearTest
#                 if maxYearTest > maxYear: maxYear = maxYearTest
#     return minYear, maxYear

def year_split(year, yearRaster, durationRaster, assignRaster, minYear, maxYear, outfile):
    # All inputs are numpy arrays except outfile       
    # loop over years and write out bands
    # locations in the year and duration = 1, others = 0
    yearChanges = numpy.where((yearRaster + durationRaster - 1 >= year) & (year >= yearRaster) & (yearRaster > 0), assignRaster, 0)
    bandIndex = year - minYear + 1
    outband = outfile.GetRasterBand(bandIndex)
    outband.WriteArray(yearChanges)
    #outband.SetDescription("band names", year)
    # want to have each band output as a year
    del yearChanges
    return
    
def choose_outType(assignRaster):
    # Choose data type of output pixels (only integer types right now)
    maxOut = numpy.nanmax(assignRaster)
    if maxOut < 128:
        outType = GDT_Byte
    elif maxOut >= 128 and maxOut < 32768:
        outType = GDT_Int16
    elif maxOut >= 32768 and maxOut < 2147483648:
        outType = GDT_Int32
    elif maxOut >= 2147483648 and max < 9223372036854775808:
        outType = GDT_Int64
    elif maxOut >= 9223372036854775807:
        sys.exit("Output values are too large.")
    #print "Output pixel data type is: ",outType
    return outType

def main():
    yearDurationBSQPath, inputBSQPath, divByDur, inputBandNumber, outpathname = inputs()

    # year is band 1, duration is band 3
    yearDurationBSQ = gdal.Open(yearDurationBSQPath)
    band = yearDurationBSQ.GetRasterBand(1)
    yearRaster = band.ReadAsArray(0,0,yearDurationBSQ.RasterXSize,yearDurationBSQ.RasterYSize)
    band = yearDurationBSQ.GetRasterBand(3)
    durationRaster = band.ReadAsArray(0,0,yearDurationBSQ.RasterXSize,yearDurationBSQ.RasterYSize)

    # load input raster
    inputBSQ = gdal.Open(inputBSQPath)
    band = inputBSQ.GetRasterBand(inputBandNumber)
    if yearDurationBSQ.RasterXSize != inputBSQ.RasterXSize or yearDurationBSQ.RasterYSize != yearDurationBSQ.RasterYSize:
        sys.exit("Raster dimensions are not equal.")
    assignRaster = band.ReadAsArray(0,0,inputBSQ.RasterXSize,inputBSQ.RasterYSize)
    if divByDur == 'True':
        durationRasterOnes = numpy.where(durationRaster == 0, 1, durationRaster)
        # storing this as an int, but should be floats?
        assignRaster = assignRaster/durationRasterOnes

    # first find minimum and maximum values in yearRaster
    # fix these to look up start and end years from respective vertyrs file
    #minYear = #numpy.nanmin(numpy.where(yearRaster != 0, yearRaster, numpy.nanmax(yearRaster)))
    #maxYear = #numpy.nanmax(yearRaster)
    
    # Use getYearRange to get minimum and maximum years for output array
    # can be hard coded at top of file
#     minYear, maxYear = getYearRange(yearDurationBSQPath)
    print "minYear:", minYear
    print "maxYear;", maxYear
    bandRange = maxYear - minYear + 1

    # Get output pixel type
    outType = choose_outType(assignRaster)

    # set up dummy output .bsq and .hdr to fill
    driver = yearDurationBSQ.GetDriver()
    outfile = driver.Create(outpathname,yearDurationBSQ.RasterXSize,yearDurationBSQ.RasterYSize,bandRange,outType)
    outfile.SetGeoTransform(yearDurationBSQ.GetGeoTransform())
    outfile.SetProjection(yearDurationBSQ.GetProjection())
    
    
    # Enter years as wavelength values in the .hdr file
    wavelength_string = "wavelength = {"
    # Loop year_split and add years to wavelength values
    for year in range(minYear,maxYear + 1):
        print "Working on year:", year
        year_split(year, yearRaster, durationRaster, assignRaster, minYear, maxYear, outfile)
        wavelength_string = wavelength_string + " " + str(year) + ","
    outfile = None
    wavelength_string = wavelength_string + "}"
    
    # Edit .hdr file to include years
    f = open(outpathname[:-3] + "hdr",'a')
    f.write("\n")
    f.write("wavelength units = Unknown \n")
    f.write(wavelength_string)
    f.close()

    #write meta.txt file
    desc = "Greatest recovery map, stretched by year, for source of agent aggregation map for mr224."
    this_script = os.path.abspath(__file__)
    createMetadata(sys.argv, outpathname, description=desc, lastCommit=getLastCommit(this_script))

if __name__ == "__main__":
    sys.exit(main())