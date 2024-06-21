import sys
def process_file(input, output):
    with open(file, "r") as file_f1, open(file_new_1, "w") as file_output:
        inside = True
        new_block = False
        bloque =[]
        int_families_group1=[]
        int_families_group2=[]
        family1=None
        family2=None
        value=0

        for line in file_f1.readlines():
            #print(line)
            bloque.append(line)
            if inside and not "**********" in line and not new_block:
                columns = line.split('\t')
                #print(columns)
                if "INT" in columns[8]: 
                    if family1: 
                        #print(columns[8])
                        family_new = str(columns[8])
                        if family_new==family1:
                            continue
                        if family_new!=family1:
                            int_families_group1.append(family_new)
                            #print(int_families_group1)

                    if not family1:
                        family1 = str(columns[8])
                        int_families_group1.append(family1)

            if "LTR" in columns[8] and not new_block and family1: 
                #print("Aquí")
                new_block=True

            
            if new_block and not "**********" in line and not "LTR" in line:
                columns = line.split('\t')
                if "INT" in columns[8]: 
                    if family2: 
                        #print(columns[8])
                        family_new2 = str(columns[8])
                        if family_new2==family2:
                            continue

                        #print(value)
                        if family_new2!=family2 and value<2:
                            int_families_group2.append(family_new2)

                    if not family2:
                        family2 = str(columns[8])
                        int_families_group2.append(family2)
            
            if "LTR" in columns[8] and new_block:
                value+=1
                #print(value)
                continue

            if "**********" in line:
                #("Aquí")
                set_int_families_group1=set(int_families_group1)
                set_int_families_group2=set(int_families_group2)
                #print(set_int_families_group1)
                #print(set_int_families_group2)
                if set_int_families_group1.intersection(set_int_families_group2):
                    for parts in bloque: 
                        print("Data have been written in the output file")
                        file_output.write(parts)
                
                family1=None
                family2=None
                new_block=False
                inside=True
                int_families_group1=[]
                int_families_group2=[]
                bloque =[]
                value=0
                continue
    #close files
    file_f1.close()
    file_output.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 familyINT_10.py filtered_final_2_locus.gff  ints_samefam_f2_tandems2.gff")
        sys.exit(1)

    file = sys.argv[1]
    file_new_1 = sys.argv[2]

    process_file(file, file_new_1)
