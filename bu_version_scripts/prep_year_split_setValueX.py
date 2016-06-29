# prep_year_split_setValueX.py

# See 'Breaking up output rasters by year and duration' on shared google docs

# before running:
# module load python/2.7.5
# module load gdal/1.10.0

# calls year_split.py
# will separate unknown attribution = X calls by year and duration

# python prep_year_split_setValueX.py /projectnb/trenders/proj/ltattribution/mr224_band5_greatest/patchfiles_band5_paramset03_greatest_disturbance.csv /projectnb/trenders/proj/david/magnitude_by_year/mr224_band5_greatest/setvalue_allyears/ /projectnb/trenders/proj/david/magnitude_by_year/mr224_band5_greatest/ 20
# details of inputs below

import os, sys, csv, glob
# path of patchfile...csv for filenames in modeling region
file = sys.argv[1]
# directory of attributed rasters, created using predictRF_noprior_batch.R
inputdir = sys.argv[2]
# directory of outputs
outdir = sys.argv[3]
# value of setValue
X = sys.argv[4]
patchfiles = list(csv.reader(open(file,"rb")))

os.chdir(inputdir)
Xstring = "*setValue" + X + ".bsq"
attributionList = glob.glob(Xstring)
for i in range(2,len(patchfiles)):
    print "    Scene: " + patchfiles[i][0]
    # remove patchid from file name and just append .bsq if necessary (not for wetness and band5)
    name_split = patchfiles[i][1].split("_")
    if name_split[-1] == 'patchid.bsq':
        yearDurationBSQPath = "_".join(name_split[:-1]) + ".bsq"
    else:
        yearDurationBSQPath = patchfiles[i][1]
    # find correct attribution raster
    for item in attributionList:
        if patchfiles[i][0] == item.split("_")[3]: attributionRasterPath = item
    inputBSQPath = os.path.join(inputdir,attributionRasterPath)
    # for attribution
    divByDur = 'False'
    inputBandNumber = '1'
    pathsub = attributionRasterPath[:-4] + "ByYear.bsq"
    outpathname = os.path.join(outdir,pathsub)
    print "    "
    print "Output: " + outpathname
    os.system("python /projectnb/trenders/proj/david/magnitude_by_year/year_split.py {0} {1} {2} {3} {4}".format(yearDurationBSQPath,inputBSQPath,divByDur,inputBandNumber,outpathname))
