#!/bin/bash -l

# #DATA TO INTRODUCE.- PART I 
reference=$1
library=$2
repeatmasker=$3
distance_between_ints=$4
minimum_int_length=$5
minimum_element_length=$6
distance_between_ltrs=$7
locus_length=$8
accession=$9

# #Identify consensuses length
cat $library | seqkit fx2tab --length | awk -F "\t" '{print $1"#"$4}' | tr '#' '\t' | awk '{print $1"#"$3}' > cons_lengths.txt 

# #Save IDs
grep '>' $library | tr '/' '\t' | tr '#' '\t' | cut -f1 | sed 's/>//g' > ids.txt

# #TE length from repeatmasker file #File with RM. hit length
grep -w -f ids.txt $repeatmasker | tr ':' '\t' | sed 's/ID=//g' | sed 's:"::g' | awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$11"#"$5-$4}' | tr ' ' '\t' > genome.lengths.gff

# #Get rid of "-int" sufix in previous result
sed 's/-int//g' genome.lengths.gff > sed.genome.lengths.gff

# #Obtain TEs #Filter gff by length #Compare hit length with consensus length and print only full elements
python3 mods/filter70len_1.py cons_lengths.txt sed.genome.lengths.gff > genome_full_length.gff   

# #Getting read of extra \n
perl -pe 's/EDTA\n/EDTA\t/' genome_full_length.gff  > genome_full_length_no_n.txt

# #PART 1.- INTs 70%
# #Filter INTs from the result output
grep "INT" genome_full_length_no_n.txt > INT_genome_full_length.gff

# #Check if at least 2 internal copies of a TE are close to each other
python3 mods/intclose2_kb_2.py INT_genome_full_length.gff $distance_between_ints > INT_pairs.gff 

# #Sort for chr + eliminate extra ".0"
cat INT_pairs.gff  | tail -n +2 | sort -k1,1 -k2,2n | sed 's/\b\.0\b//g' > sorted_INT_pairs.gff 

# #Check if the TEs are from the same family 
python3 mods/familyINT_3.py sorted_INT_pairs.gff  > INT_TE_pairs_same_family.gff

# #Search for LTRs between the 2 internal copies 
python3 mods/ltr_matcher_4.py sed.genome.lengths.gff INT_TE_pairs_same_family.gff INT_result_full_tandems.gff $distance_between_ints

# #Identify tandem locus
python3 mods/identify_locus_5.py INT_result_full_tandems.gff INT_result_full_tandems_locus.gff f1_locus.gff $locus_length

#Filter by INT length
python3 mods/filter_INTv3_6.py f1_locus.gff filtered_final_1_locus.gff $minimum_int_length

#Bed file
python3 mods/gff2bed.py filtered_final_1_locus.gff f1_regions.bed $accession

#Filter by total length of the LTR-RT sequence
python3 mods/filter_complete_length.py f1_regions.bed f1_filtered_regions.bed $minimum_element_length

#Extract region
bedtools getfasta -fi $reference -bed f1_filtered_regions.bed -name -fo f1_regions.fa

#Filter by TEsorter
TEsorter f1_regions.fa -db rexdb-plant 

# #PART 2.- LTRs 70%
# #Obtain tandem TEs with at least 3 LTRs from the same family and 2 internal copies (no minimum length needed for internal copies, just for LTRs)
# #Filter LTRs from the result output
grep "LTR" genome_full_length_no_n.txt > LTR.genome_full_length.gff

# #Sort file
sort -t$'\t' -k1,1 -k4,4n LTR.genome_full_length.gff > sorted.LTR.genome_full_length.gff

# #Check if at least 3 LTR copies from the same family are close to each other
python3 mods/ltrclose2_7.py sorted.LTR.genome_full_length.gff $distance_between_ltrs > LTR_triplets.gff

# #Check if the LTRs are from the same family 
python3 mods/familyLTR_8.py LTR_triplets.gff > LTR_TE_triplets_same_family.gff

# #Sort for looking by chr + eliminate extra ".0"
cat LTR_TE_triplets_same_family.gff | sort -k1,1 -k2,2n | sed 's/\b\.0\b//g' > sorted_LTR_TE_triplets_same_family.gff

# #Search for INTs between every LTR 
python3 mods/int_matcher_9.py sed.genome.lengths.gff sorted_LTR_TE_triplets_same_family.gff LTR_result_full_tandems.gff

#Filter INTs of different families
python3 mods/familyINT_10.py LTR_result_full_tandems.gff filtered_INT_LTR_result_full_tandems.gff

# #Identify tandem locus
python3 mods/identify_locus_5.py filtered_INT_LTR_result_full_tandems.gff LTR_result_full_tandems_locus.gff final_2_locus.gff $locus_length

# #Filter by INT length
python3 mods/filter_INTv3_6.py final_2_locus.gff filtered_final_2_locus.gff $minimum_int_length

# #Bed file
python3 mods/gff2bed.py filtered_final_2_locus.gff  f2_regions.bed $accession

# #Filter by length of the LTR-RT tandem element
python3 mods/filter_complete_length.py f2_regions.bed f2_filtered_regions.bed $minimum_element_length

# #Extract region
bedtools getfasta -fi $reference -bed f2_filtered_regions.bed -name -fo f2_regions.fa

# #Filter by TEsorter
TEsorter f2_regions.fa -db rexdb-plant 

# #Classify TEs according to output #Concatenate
cat f1_regions.fa.rexdb-plant.cls.tsv f2_regions.fa.rexdb-plant.cls.tsv > final_regions.tsv

# #Filter - just uniq lines
cat final_regions.tsv | sort | uniq | tail -n +2 > uniq_final_regions.tsv

# #If end position is duplicated in two rows, erase one
python3 mods/check_end.py uniq_final_regions.tsv all.regions.tsv

# #Classification
cat all.regions.tsv | grep -v "none" | grep -v "Superfamily"> LTR-RT_TR.tsv
cat all.regions.tsv | grep "none" > LTR-RT_related.tsv

# #Divide results
mkdir temp;
mv cons_lengths.txt  temp/cons_lengths.txt 
mv ids.txt temp/ids.txt
mv genome.lengths.gff temp/genome.lengths.gff
mv sed.genome.lengths.gff temp/sed.genome.lengths.gff
mv genome_full_length.gff  temp/genome_full_length.gff 
mv genome_full_length_no_n.txt temp/genome_full_length_no_n.txt
mv INT_genome_full_length.gff temp/INT_genome_full_length.gff
mv INT_pairs.gff temp/INT_pairs.gff 
mv INT_TE_pairs_same_family.gff temp/INT_TE_pairs_same_family.gff
mv INT_result_full_tandems.gff temp/INT_result_full_tandems.gff
mv f1_locus.gff temp/f1_locus.gff
mv INT_result_full_tandems_locus.gff temp/INT_result_full_tandems_locus.gff
mv LTR.genome_full_length.gff temp/LTR.genome_full_length.gff
mv sorted.LTR.genome_full_length.gff temp/sorted.LTR.genome_full_length.gff
mv LTR_triplets.gff temp/LTR_triplets.gff
mv LTR_TE_triplets_same_family.gff  temp/LTR_TE_triplets_same_family.gff 
mv sorted_LTR_TE_triplets_same_family.gff temp/sorted_LTR_TE_triplets_same_family.gff
mv LTR_result_full_tandems.gff  temp/LTR_result_full_tandems.gff 
mv filtered_INT_LTR_result_full_tandems.gff temp/filtered_INT_LTR_result_full_tandems.gff
mv LTR_result_full_tandems_locus.gff temp/LTR_result_full_tandems_locus.gff
mv final_2_locus.gff temp/final_2_locus.gff
mv f1_filtered_regions.bed temp/f1_filtered_regions.bed
mv f2_filtered_regions.bed temp/f2_filtered_regions.bed
mv final_regions.tsv temp/final_regions.tsv
mv f2_regions.bed temp/f2_regions.bed
mv f1_regions.bed temp/f1_regions.bed
mv uniq_final_regions.tsv temp/uniq_final_regions.tsv
mv sorted_INT_pairs.gff temp/sorted_INT_pairs.gff

mkdir results;
mv all.regions.tsv results/all.regions.tsv
mv LTR-RT_TR.tsv results/LTR-RT_TR.tsv
mv LTR-RT_related.tsv results/LTR-RT_related.tsv
mv filtered_final_1_locus.gff results/filtered_final_1_locus.gff
mv filtered_final_2_locus.gff results/filtered_final_2_locus.gff 
mv f1_regions.fa.rexdb-plant.cls.lib results/f1_regions.fa.rexdb-plant.cls.lib
mv f1_regions.fa.rexdb-plant.cls.pep results/1_regions.fa.rexdb-plant.cls.pep
mv f1_regions.fa.rexdb-plant.cls.tsv  results/f1_regions.fa.rexdb-plant.cls.tsv
mv f1_regions.fa.rexdb-plant.dom.faa  results/f1_regions.fa.rexdb-plant.dom.faa
mv f1_regions.fa.rexdb-plant.dom.gff3 results/f1_regions.fa.rexdb-plant.dom.gff3
mv f1_regions.fa.rexdb-plant.dom.tsv  results/f1_regions.fa.rexdb-plant.dom.tsv
mv f1_regions.fa.rexdb-plant.domtbl  results/f1_regions.fa.rexdb-plant.domtbl
mv f2_regions.fa  results/f2_regions.fa
mv f1_regions.fa results/f1_regions.fa
mv f2_regions.fa.rexdb-plant.cls.lib  results/f2_regions.fa.rexdb-plant.cls.lib
mv f2_regions.fa.rexdb-plant.cls.pep  results/f2_regions.fa.rexdb-plant.cls.pep
mv f2_regions.fa.rexdb-plant.cls.tsv  results/f2_regions.fa.rexdb-plant.cls.tsv
mv f2_regions.fa.rexdb-plant.dom.faa  results/f2_regions.fa.rexdb-plant.dom.faa
mv f2_regions.fa.rexdb-plant.dom.gff3  results/f2_regions.fa.rexdb-plant.dom.gff3
mv f2_regions.fa.rexdb-plant.dom.tsv  results/f2_regions.fa.rexdb-plant.dom.tsv
mv f2_regions.fa.rexdb-plant.domtbl  results/f2_regions.fa.rexdb-plant.domtbl

