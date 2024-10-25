# **IDENTAM**
<img width="620" alt="Imagen2" src="https://github.com/NMoralesD/IDENTAM/assets/173355210/48db2ba0-bd9b-40eb-8b98-f1c5a34a1f0d">

This repository provides the code for identifying potential Long Terminal Repeat (LTR) retrotransposon (RT) tandem loci.

## INSTALLATION
To obtain the repository from GitHub, use the following command:

```git clone: https://github.com/NMoralesD/IDENTAM```


## REQUIREMENTS
IDENTAM requires the installation of TEsorter. Detailed installation instructions can be found at:
https://github.com/zhangrengang/TEsorter

Additionally, IDENTAM requires bedtools. All the necessary installation information can be found at:
https://bioconda.github.io/recipes/bedtools/README.html

## USAGE
For identifying potential LTR-RT Tandems with IDENTAM we need 3 input files:  
- A transposable element (TE) library with LTRs and internal regions annotated separately
- A reference genome
- A Repeatmasker output 

Then, to run IDENTAM, use the following command:

```sbatch mods/identify_tandems_2modulesv3.sh path/to/reference path/to/TE_library path/to/RepeatMasker_output Distance_between_internal_regions Minimum_internal_region_lenght Minimum_element_lenght Distance_between_LTRs  Maximum_locus_lenght Accession_name```

As shown in the code, several parameters can be modified. The default parameters are listed below:

+ Distance_between_internal_regions (default: 5000 bp): This is the distance, in base pairs, between two internal regions of a TE.
+ Minimum_internal_region_length (default: 500 bp): This is the minimum length, in base pairs, of the internal regions of a TE.
+ Minimum_element_length (default: 1000 bp): This is the minimum length, in base pairs, of a potential LTR-RT tandem.
+ Distance_between_LTRs (default: 15,000 bp): This is the distance, in base pairs, between LTRs in a potential LTR-RT tandem.
+ Maximum_locus_length (default: 40,000 bp): This is the maximum distance, in base pairs, to extend an LTR-RT tandem region if another one is nearby.
+ Accession_name: The species' name. For example, "Nipponbare."

### OUTPUTs
In the results folder, you will find the following files:
+ LTR-RT_TR.tsv: A file containing the genomic positions of potential LTR-RT tandems, the associated family according to TEsorter, as well as information on their completeness and their domains.
+ LTR-RT_related.tsv: A file listing the genomic positions of potential LTR-RT-related tandems, along with the associated superfamily according to TEsorter.

## Methods
IDENTAM identifies potential LTR-RT tandems using two distinct methods:

<img src="https://github.com/NMoralesD/IDENTAM/assets/173355210/07552642-df4f-4e63-a496-d4eed9a679f1" alt="8" style="width:60%; height:auto;">

### METHOD 1 
This method detects two (≤ 5 kb apart) internal LTR-RT regions from the same family. It then checks for the presence of surrounding LTRs and generates a BED file with potential LTR-RT tandems.
### METHOD 2
This method identifies three nearby LTRs from the same family. It then verifies if there are internal LTR-RT regions from the same family located between the LTRs and produces a BED file with potential LTR-RT tandems.









