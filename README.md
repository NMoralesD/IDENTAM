# **IDENTAM**
<img width="620" alt="Imagen2" src="https://github.com/NMoralesD/IDENTAM/assets/173355210/48db2ba0-bd9b-40eb-8b98-f1c5a34a1f0d">

This repository constains the code for identifying potential LTR-retrotransposons (LTR-RT) tandem loci.

## INSTALLATION
First, to obtain the repository from GitHub:
git clone: ADRESS
cd IDENTAM

## REQUIREMENTS
IDENTAM requires also the installation of TEsorter. 
All the information neccesary for installation can be find in: https://github.com/zhangrengang/TEsorter

## USAGE
For identifying potential LTR-RT Tandems it is neccesary three input files are needed: 
- Transposable Element (TE) library with LTRs and internal regions annotated separately
- Reference genome
- Repeatmasker output

Then, to run IDENTAM we simply type: 

```launch_identam.sh```

Several parameters should be modified in the launch_identam.sh file, as: 
+ Path to the reference file
+ Path to the RepeatMasker output file
+ Name of the accession
+ Maximum distance between internal regions of the TE
+ Minimum length of the internal regions
+ Minimum lenght of the LTR-RT Tandems
+ Maximum distance between LTRs

### OUTPUTs
In the results folder you will find: 
```LTR-RT_TR.tsv  A file with the genomic positions of potential LTR-RT Tandems, as well as the related family according to TEsorter, information about their completeness and their domains.
LTR-RT_related.tsv  A file with the genomic positions of potential LTR-RT related Tandems, as well as the related superfamily family according to TEsorter.```










