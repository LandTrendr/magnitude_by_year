# prep_year_split_attribution.py

# See 'Breaking up output rasters by year and duration' on shared google docs

# before running:
# module load python/2.7.5
# module load gdal/1.10.0

# calls year_split.py
# will separate attribution calls by year and duration

# python prep_year_split_attribution.py /projectnb/trenders/proj/ltattribution/mr224_fast/patchfiles_nbr_paramset01_greatest_fast_disturbance_mmu11_tight.csv /projectnb/trenders/proj/david/mr224_trn1thrutrn3_noNA/mr224_change_process_trn1thrutrn3_noNA/ /projectnb/trenders/proj/david/magnitude_by_year/test/
# details of inputs below

import os, sys, csv, glob
# path of patchfile...csv for filenames in modeling region
file = sys.argv[1]
# directory of attributed rasters, created using predictRF_noprior_batch.R
inputdir = sys.argv[2]
# directory of outputs
outdir = sys.argv[3]
patchfiles = list(csv.reader(open(file,"rb")))

os.chdir(inputdir)
attributionList = glob.glob("*votes_top_detail.bsq")
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
    pathsub = attributionRasterPath[:-4] + "_by_year.bsq"
    outpathname = os.path.join(outdir,pathsub)
    print "    Attribution"
    print "Output: " + outpathname
    os.system("python /projectnb/trenders/proj/david/magnitude_by_year/year_split.py {0} {1} {2} {3} {4}".format(yearDurationBSQPath,inputBSQPath,divByDur,inputBandNumber,outpathname))