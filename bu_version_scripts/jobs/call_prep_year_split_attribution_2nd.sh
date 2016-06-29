#!/bin/tcsh
#$ -pe omp 1
#$ -l h_rt=4:00:00
#$ -N attyrsplitmr224
#$ -V

module load python/2.7.5
module load gdal/1.10.0

python prep_year_split_attribution.py /projectnb/trenders/proj/ltattribution/mr224_2nd_fast/patchfiles_nbr_paramset01_second_greatest_fast_disturbance_mmu11_tight.csv /projectnb/trenders/proj/david/mr224_trn1thrutrn3_noNA/mr224_2nd_change_process_trn1thrutrn3_noNA/ /projectnb/trenders/proj/david/magnitude_by_year/mr224_2nd_fast/
