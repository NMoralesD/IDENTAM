import sys; 
def gff2bed(input, output, genome):
    # Open input file
    with open(input, 'r') as input_file:
        lines = input_file.readlines()

    #open output file
    with open(output, 'w') as output_file:
        # Initialize chromosoma + position_start + position_end 
        chr = None
        position_start = None
        position_end = None
        fam_LTR = None
        fam_INT = None
        
        for line in lines:
            #print(line)
            if line.startswith('Chr') and position_start is None:
                # Extract chr + position_start from element 1 
                parts = line.strip().split('\t')
                #print(parts)
                chr = parts[0]
                position_start = parts[3]
                fam_LTR = parts[8]


            elif line.startswith('Chr') and position_start:
                #Replace position_end every time in loop to get the last before asterisks
                parts = line.strip().split('\t')
                position_end = parts[4]
                #print(position_end)
                if 'INT' in parts[8]:
                    fam_INT = parts[8]
            
            elif line.startswith('**********'):
                #End of the block assumed. 
                #Write infor in output file
                if chr is not None and position_start is not None and position_end is not None:
                    resultado = f'{chr}\t{position_start}\t{position_end}\t{genome}\t{fam_LTR};{fam_INT}\n'
                    #print(resultado)
                    output_file.write(resultado)

                # Reinicia las variables para el próximo grupo
                chr = None
                position_start = None
                position_end = None
    #close files
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 test.gff2bed.py filtered_final_1_locus.gff f1_regions.bed genome")
        sys.exit(1)

    file = sys.argv[1]
    file_output = sys.argv[2]
    genome = str(sys.argv[3])

    gff2bed(file, file_output, genome)
