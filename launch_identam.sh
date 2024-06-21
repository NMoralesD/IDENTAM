#!/bin/bash -l
#SBATCH --job-name="iden_tands"
#SBATCH --ntasks=1
#SBATCH --mem=40G
#SBATCH --cpus-per-task=1
#IRGSP.fa.out.gff
# #SCRIPT: Identify tandems
# #Author: M-D,N

#Parameters to define
reference="/path/to/reference.fa";
library="/path/to/library.fa";
repeatmasker_result="/path/to/RepeatMasker/file.gff";
distance_between_ints="5000";
minimum_int_length="500";
minimum_element_length="1000";
distance_between_ltrs="15000";
locus_length="40000";
accession="Accession_name"


sbatch mods/identify_tandems_2modulesv3.sh "$reference" "$library" "$repeatmasker_result" "$distance_between_ints" "$minimum_int_length" "$minimum_element_length" "$distance_between_ltrs" "$locus_length" "$accession"