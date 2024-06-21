
import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py cons_lengths_file gff_length_file")
    sys.exit(1)

#Open files 
cons_lengths_file = sys.argv[1]
gff_length_file = sys.argv[2]

#open files
cons_length = open(cons_lengths_file, 'r')
gff_length = open(gff_length_file, 'r')

#read file
loop=gff_length.readlines()

for line in cons_length.readlines():
	line=line.strip()
	line=line.split('#')
	cons_name=line[0]				#+"#"+line[1]
	cons_length_var=float(line[1])
	#print(cons_name+'\t'+str(cons_length))
	for elto in loop:
		elto=elto.strip()
		export=elto.split('\t')
		elto2=elto.split('\t')[8]
		attr=elto2.split('#')
		hit_name=attr[0]				#+"#"+attr[1]
		hit_length_var=float(attr[1])
		#print(hit_length)
		if str(cons_name) == str(hit_name):
			#print(cons_name+" "+hit_name+" "+str(cons_length_var)+" "+str(hit_length_var))
			ratio=hit_length_var/cons_length_var
			#print(hit_length)
			#print(cons_length)
			#print(ratio)
			if ratio > 0.70 and ratio < 1.1:
				#print(cons_name+"\t"+hit_name+"\t"+str(cons_length)+"\t"+str(hit_length))
				print(export[0]+'\t'+export[1]+'\t'+export[2]+'\t'+export[3]+'\t'+export[4]+'\t'+export[5]+'\t'+export[6]+'\t'+export[7]+'\tID='+str(attr[0])+';Method=EDTA')
				print(cons_name+" "+hit_name+" "+str(cons_length_var)+" "+str(hit_length_var))
				#print(cons_name+"\t"+hit_name+"#"+str(hit_length))

#close files
cons_length.close()
gff_length.close()