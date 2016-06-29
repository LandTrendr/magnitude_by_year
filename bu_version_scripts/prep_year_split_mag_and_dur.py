# prep_year_split_mag_and_dur.py

# See 'Breaking up output rasters by year and duration' on shared google docs

# before running:
# module load python/2.7.5
# module load gdal/1.10.0

# calls year_split.py
# will separate (magnitude / duration) by year and duration
# as well as duration by year and duration

# example:
# python prep_year_split_mag_and_dur.py /projectnb/trenders/proj/ltattribution/mr224_fast/patchfiles_nbr_paramset01_greatest_fast_disturbance_mmu11_tight.csv /projectnb/trenders/proj/david/magnitude_by_year/test/
# details of inputs below

import os, sys, csv
# path of patchfile...csv for filenames in modeling region
file = sys.argv[1]
# directory of outputs
outdir = sys.argv[2]
patchfiles = list(csv.reader(open(file,"rb")))

#os.system("module load gdal/1.10.0")
for i in range(2,len(patchfiles)):
    print "    Scene: " + patchfiles[i][0]
    name_split = patchfiles[i][1].split("_")
    if name_split[-1] == 'patchid.bsq':
        yearDurationBSQPath = "_".join(name_split[:-1]) + ".bsq"
    else:
        yearDurationBSQPath = patchfiles[i][1]
    inputBSQPath = yearDurationBSQPath
    # for magnitude
    divByDur = 'True'
    inputBandNumber = '2'
    pathsub = yearDurationBSQPath.split("/")[-1][:-4] + "_magnitudeOverDurationByYear.bsq"
    outpathname = os.path.join(outdir,pathsub)
    print "    Magnitude"
    print "Output: " + outpathname
    os.system("python /projectnb/trenders/proj/david/magnitude_by_year/year_split.py {0} {1} {2} {3} {4}".format(yearDurationBSQPath,inputBSQPath,divByDur,inputBandNumber,outpathname))
    
    # for duration - need to figure out why this is returning only 1s and 0s
    divByDur = 'False'
    inputBandNumber = '3'
    pathsub = yearDurationBSQPath.split("/")[-1][:-4] + "_durationByYear.bsq"
    outpathname = os.path.join(outdir,pathsub)
    print "    Duration"
    print "Output: " + outpathname
    os.system("python /projectnb/trenders/proj/david/magnitude_by_year/year_split.py {0} {1} {2} {3} {4}".format(yearDurationBSQPath,inputBSQPath,divByDur,inputBandNumber,outpathname))