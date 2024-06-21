import sys
def process_file(input, output, number):
    with open(file, "r") as file_f1, open(file_new_1, "w") as file_output:
        #State reg
        inside = True
        keep = False
        new_block = False
        bloque =[]
        value = 0

        for line in file_f1.readlines():
            #print(line)
            if "**********" in line:
                inside = False
                new_block = True
            
            if inside:
                bloque.append(line)
                columns = line.split('\t')
                if "INT" in columns[8]: 
                    #print(columns[8])
                    reg = float(columns[9])
                    #print(reg)
                    value += reg
                if "LTR" in columns[8]: 
                    #print(value)
                    if value <= float(number) and value != 0:
                        keep = False
                        inside = False
                        bloque = []
                        value = 0
                        continue;
                    if value > float(number): 
                        keep = True; 
                        value = 0;
                        continue;     
      

            if new_block and keep:
                print("Keeping a new block")
                for parts in bloque: 
                    #print(parts)
                    file_output.write(parts)
                file_output.write("**********\n")
                inside = True
                bloque = []
                new_block = False
                value = 0
            
            if new_block and not keep:
                inside = True
                new_block = False
                continue
    #close files
    file_f1.close()
    file_output.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 filter_INT.py f1_locus.gff test.final_1_locus.gff number")
        sys.exit(1)

    file = sys.argv[1]
    file_new_1 = sys.argv[2]
    number = sys.argv[3]

    process_file(file, file_new_1, number)

