#!/bin/tcsh
#$ -pe omp 1
#$ -l h_rt=4:00:00
#$ -N magduryrsplitmr224
#$ -V

module load python/2.7.5
module load gdal/1.10.0

python prep_year_split_mag_and_dur.py /projectnb/trenders/proj/ltattribution/mr224_band5_greatest/patchfiles_band5_paramset03_greatest_disturbance.csv /projectnb/trenders/proj/david/magnitude_by_year/mr224_band5_greatest/
