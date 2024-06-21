
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script_name.py LTR_triplets.gff")
    sys.exit(1)

file_pairs = sys.argv[1]

#open file
file = open(file_pairs, 'r')

#state elements
elements = []

for line in file: 
    if " y " in line: 
        element1_str, element2_str, element3_str = line.strip().split(" y ")
        element1=element1_str.split("\t")
        element2=element2_str.split("\t")
        element3=element3_str.split("\t")
        if element1[3] == element2[3] == element3[3]: 
            print(f"{element1[0]}\t{element1[1]}\t{element1[2]}\t{element1[3]}\t{element1[4]}\t{element1[5]} y " f"{element2[0]}\t{element2[1]}\t{element2[2]}\t{element2[3]}\t{element2[4]}\t{element2[5]} y " f"{element3[0]}\t{element3[1]}\t{element3[2]}\t{element3[3]}\t{element3[4]}\t{element3[5]}")


#close files
file.close()