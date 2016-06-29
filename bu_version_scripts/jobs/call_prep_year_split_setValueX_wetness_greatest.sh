#!/bin/tcsh
#$ -pe omp 1
#$ -l h_rt=4:00:00
#$ -N attyrsplitmr224
#$ -V

module load python/2.7.5
module load gdal/1.10.0

python prep_year_split_setValueX.py /projectnb/trenders/proj/ltattribution/mr224_wetness_greatest/patchfiles_wetness_paramset02_greatest_disturbance.csv /projectnb/trenders/proj/david/magnitude_by_year/mr224_wetness_greatest/setvalue_allyears/ /projectnb/trenders/proj/david/magnitude_by_year/mr224_wetness_greatest/ 19
