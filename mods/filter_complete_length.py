import sys; 
def process_length(input, output, number):
    # Open input file
    with open(input, 'r') as input_file:
        lines = input_file.readlines()

    #open output file
    with open(output, 'w') as output_file:
        for line in lines:
            #print(line)
            if line.startswith('Chr'):
                parts = line.strip().split('\t')
                #Substract end - start
                start = float(parts[1])
                #print(start)
                end = float(parts[2])
                #print(end)
                if end - start < float(number): 
                    continue;
                output_file.write(line)
    
    #close files
    input_file.close()
    output_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 mods/filter_complete_length.py f1_regions.bed f1_filtered_regions.bed $minimum_element_length")
        sys.exit(1)

    file = sys.argv[1]
    file_output = sys.argv[2]
    number = sys.argv[3]


    process_length(file, file_output, number)

