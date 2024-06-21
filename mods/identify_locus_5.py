import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 identify_locus.py result_full_tandems.gff INT_result_full_tandems_locus.gff final_1_locus.gff $locus_length")
        sys.exit(1)

    file = sys.argv[1]
    file_new_1 = sys.argv[2]
    file_new_3 = sys.argv[3]
    number = sys.argv[4]

    with open(file, "r") as file_full, open(file_new_1, "w") as file_output:
        lines = file_full.readlines()

        #unique set of data
        #unique_lines = set()
        unique_lines = []

        for line in lines: 
            line_strip = line.strip()
            line_parts = line_strip.split("\t")
            #print(line_parts) #Accedo realmente a todas las líneas

            if line_parts not in unique_lines:
                unique_lines.append(line_parts)

        for line_parts in unique_lines: 
            file_output.write("\t".join(line_parts) + "\n")

with open(file_new_1, "r") as input_file, open(file_new_3, "w") as result_output:
    lines = input_file.readlines()
    chr_before = None
    pos_before = None

    for line in lines:
        if line.strip() == "**********":
            continue
        #print(line) #Aquí ya está
        if not line.strip():
            #print(line) #No hace print de nada
            continue  # Ignore
        
        part = line.strip().split("\t")
        
        #print(part) #Aquí ya falta la lína 12
        chromosome = part[0]
        pos = int(part[3])
        if (chr_before is not None and chromosome != chr_before) or (pos_before is not None and pos - pos_before > float(number)): 
            result_output.write("**********\n")

        result_output.write(line)
        chr_before = chromosome
        pos_before = pos
    result_output.write("**********\n")

#close files
file_full.close()
file_output.close()
input_file.close()
result_output.close()














