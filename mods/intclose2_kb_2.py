#cd /Users/noemiamoralesdiaz/Desktop/Doc/GL_validation/Como_detecta_tandems/repeatmasker/script_try; 

import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py INT_genome_full_length.gff ints_distance")
    sys.exit(1)

full_length = sys.argv[1]
distance = float(sys.argv[2])

#open file
int_file = open(full_length, 'r')
#state elements
elements = []
#read file
for line in int_file.readlines():
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

def are_close(element1, element2, distance_threshold=distance):
   return(
       element1['chr'] == element2['chr'] and 
       abs(element1['end'] - element2['start']) <= distance_threshold
   )

def find_close_elements(elements, distance_threshold=distance):
    close_pairs = []
    for i in range(len(elements)):
        for j in range(i+1, len(elements)):
            if are_close(elements[i], elements[j], distance_threshold):
                close_pairs.append((elements[i], elements[j]))
    return close_pairs

    
close_pairs = find_close_elements(elements, distance_threshold=distance)

if close_pairs:
    print("Elementos transponibles cercanos a menos de " + str(distance) + "pb:")
    for pair in close_pairs:
        print(f"{pair[0]['chr']}\t{pair[0]['start']}\t{pair[0]['end']}\t{pair[0]['id']}\t{pair[0]['con_size']}\t{pair[0]['te_size']} y " f"{pair[1]['chr']}\t{pair[1]['start']}\t{pair[1]['end']}\t{pair[1]['id']}\t{pair[1]['con_size']}\t{pair[1]['te_size']}")
else:
    print("No se encontraron elementos transponibles cercanos a menos de" + str(distance) +"pb.")

#close files
int_file.close()