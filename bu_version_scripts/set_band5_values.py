# set_band5_values

# See 'Breaking up output rasters by year and duration' on shared google docs

import os, sys, csv

patchfilesPath = '/projectnb/trenders/proj/ltattribution/mr224_band5_greatest/patchfiles_band5_paramset03_greatest_disturbance.csv'
band = '1'
setValue = '20'
outputPathDir = '/projectnb/trenders/proj/david/magnitude_by_year/mr224_band5_greatest/setvalue_allyears/'

patchfiles = list(csv.reader(open(patchfilesPath,'rb')))
for row in patchfiles[2:]:
    print row[0]
    inputBSQPath = row[1]
    fileOut = inputBSQPath.split('/')[-1][:-4] + '_setValue' + setValue +'.bsq'
    outputPath = os.path.join(outputPathDir,fileOut)
    print outputPath
    os.system('python set_pixels_to_value.py {0} {1} {2} {3}'.format(inputBSQPath, band, setValue, outputPath))
