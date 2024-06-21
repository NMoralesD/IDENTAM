import sys; 

def process_file(file, file_new_1):
    with open(file, "r") as file_f1, open(file_new_1, "w") as file_output:
        end=None
        #bloque=[]
        final=[]

        for line in file_f1.readlines():
            #Get every line
            #bloque.append(line)
            cols=(line.split('\t'))[0].split('-')[1]
            #print(cols)
            if cols: 
                if cols == end: 
                    continue;
                if cols != end:
                    file_output.write(line)
                    end=cols
    #Close files
    file_f1.close()
    file_output.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 check_end.py uniq_final_regions.tsv all.regions.tsv")
        sys.exit(1)

    file = sys.argv[1]
    file_new_1 = sys.argv[2]

    process_file(file, file_new_1)