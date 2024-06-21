import sys


if len(sys.argv) != 3:
    print("Usage: python script_name.py sorted.LTR.genome_full_length.gff $distance_between_ltrs")
    sys.exit(1)

full_length = sys.argv[1]
number = sys.argv[2]

#open file
ltr_file = open(full_length, 'r')

#State elements
elements = []
    #read file
for line in ltr_file.readlines():
    fields = line.strip().split('\t')
    element_id2=fields[9]
    element_id=element_id2.split(' ')[0]
    element_start=float(fields[3])
    element_end=float(fields[4])
    element_chr=str(fields[0])
    element_consen_size=element_id2.split(' ')[2]
    element_TE_size=element_id2.split(' ')[3]
    element ={
        'chr':element_chr,
        'start':element_start,
        'end':element_end,
        'id':element_id,
        'con_size':element_consen_size,
        'te_size':element_TE_size
    }
    elements.append(element)
    #print(element)


def are_close(element1, element2, element3, distance_threshold):
   return(
        element1['chr'] == element2['chr'] == element3['chr'] and
        (element2['start'] - element1['end']) <= float(distance_threshold) and
        (element3['start'] - element2['end']) <= float(distance_threshold)
    )



def find_close_elements(elements, distance_threshold):
    close_triplets = []
    for i in range(len(elements)-2):
        element1 = elements[i]
        element2 = elements[i + 1]
        element3 = elements[i + 2]
        if are_close (element1, element2, element3, distance_threshold): 
            close_triplets.append((element1, element2, element3))
    return close_triplets; 

close_3_te = find_close_elements(elements, number)

if close_3_te:
    print("Elementos cercanos a "+str(number)+"pb")
    for triplet in close_3_te:
        print(f"{triplet[0]['chr']}\t{triplet[0]['start']}\t{triplet[0]['end']}\t{triplet[0]['id']}\t{triplet[0]['con_size']}\t{triplet[0]['te_size']} y " f"{triplet[1]['chr']}\t{triplet[1]['start']}\t{triplet[1]['end']}\t{triplet[1]['id']}\t{triplet[1]['con_size']}\t{triplet[1]['te_size']} y " f"{triplet[2]['chr']}\t{triplet[2]['start']}\t{triplet[2]['end']}\t{triplet[2]['id']}\t{triplet[2]['con_size']}\t{triplet[2]['te_size']}")
else:
    print("No se encontraron elementos transposponibles cercanos a " +str(number)+ "pb")



#close files
ltr_file.close()
