
def parse_transposon(sentence):
    te = {}
    chr, start, end, type, *_ =  sentence.split("\t")
    te["chr"] = chr
    te["start"] = int(start)
    te["end"] = int(end)
    te["type"] = type
    return te


def test_parse_te():
    sentence = "Chr1	15743458	15747667	Os0039_INT_RIRE3	5791	4209"
    expected = {
        "chr": "Chr1",
        "start": 15743458,
        "end": 15747667,
        "type": "Os0039_INT_RIRE3"
    }
    assert expected == parse_transposon(sentence)


def extract_pair(line):
    l = parse_transposon(line.split(" y ")[0])
    r = parse_transposon(line.split(" y ")[1])
    return (l, r)


def test_extract_pair():
    line = "Chr1	15743458	15747667	Os0039_INT_RIRE3	5791	4209 y Chr1	15747668	15753937	Os0039_INT_RIRE3	5791	6269"
    expected_left = {
        "chr": "Chr1",
        "start": 15743458,
        "end": 15747667,
        "type": "Os0039_INT_RIRE3"
    }
    expected_right = {
        "chr": "Chr1",
        "start": 15747668,
        "end": 15753937,
        "type": "Os0039_INT_RIRE3"
    }

    assert extract_pair(line)[0] == expected_left
    assert extract_pair(line)[1] == expected_right


def parse_transposon_original(sentence):
    te = {}
    chr, program, method, start, end, identity, strand, comment, other =  sentence.split("\t")
    te["chr"] = chr
    te["program"] = program
    te["method"] = method
    te["start"] = int(start)
    te["end"] = int(end)
    te["identity"] = float(identity)
    te["strand"] = strand
    te["comment"] = comment
    te["type"] = other.split('#')[0]
    te["distance"] = int(other.split('#')[1])
    return te


def test_parse_transposon_original():
    sentence = "Chr1	RepeatMasker	similarity	15680318	15686378	6.7	-	.	Os0850_INT#6060"
    expected_transposon = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15680318,
        "end": 15686378,
        "identity": 6.7,
        "strand": "-",
        "comment": ".",
        "type": "Os0850_INT",
        "distance": 6060
    }

    assert parse_transposon_original(sentence) == expected_transposon


def find_te(te,file):
    line_number = 1
    for f in file.readlines():
        new_te = parse_transposon_original(f)
        chr_compare = is_equal_te(te, new_te)
        if chr_compare == True:
            return(line_number, new_te)
        line_number = line_number + 1
    return(None, None)
        


def test_find_te():
    #te = parse_transposon("Chr1	15743458	15747667	Os0039_INT_RIRE3	5791	4209")
    te = parse_transposon("Chr1	15747668	15753937	Os0039_INT_RIRE3	5791	6269")
    path = "/Users/noemiamoralesdiaz/Desktop/Doc/GL_validation/Como_detecta_tandems/repeatmasker/script_try/sed.TG56.fixed.nocontig.lengths.gff"
    file = open(path, "r")
    expected_line_number = 2557
    expected_te = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15747668,
        "end": 15753937,
        "identity": 6.3,
        "strand": "-",
        "comment": ".",
        "type": "Os0039_INT_RIRE3",
        "distance": 6269
    }
    assert find_te(te, file) == (expected_line_number, expected_te)
    file.close()


def is_equal_te(te1,te2):
    checks = ["chr", "start", "end", "type"]
    for check in checks:
        if te1[check] != te2[check]:
            return False
    return True


def test_is_equal_te():
    element1 = {
        "chr": "A",
        "start": 0,
        "end":3,
        "type": "Os"
    }
    element2 = {
        "chr": "B",
        "start": 0,
        "end":3,
        "type": "Os"
    }
    element3 = {
        "chr": "A",
        "start": 0,
        "end":3,
        "type": "Os"
    }
    assert is_equal_te(element1,element2) == False
    assert is_equal_te(element1,element3) == True


def get_te_before(file, line_number, sz):
    left = line_number-sz-1
    right = line_number-1
    if left < 0:
        left = 0
    if right > len(file) - 1:
        right = len(file) - 1
    return file[left:right]


def test_get_te_before():
    file = ["1", "2", "3", "4", "5"]
    line_number = 4
    amount = 2
    expected = ["2", "3"]
    assert get_te_before(file,line_number, amount) == expected


def test_get_te_before_overflow():
    file = ["1", "2", "3", "4", "5"]
    line_number = 2
    amount = 2
    expected = ["1"]
    assert get_te_before(file,line_number, amount) == expected


def get_te_after(file, line_number,size):
    left = line_number
    right = line_number+size
    if right > len(file):
        right = len(file)
    if left ==len(file):
        left = len(file)-1
    return file[left:right]


def test_get_te_after():
    file = ["1", "2", "3", "4", "5"]
    line_number = 3
    amount = 2
    expected = ["4", "5"]
    assert get_te_after(file,line_number,amount) == expected


def test_get_te_after_overflow():
    file = ["1", "2", "3", "4", "5"]
    line_number = 3
    amount = 2
    expected = ["4", "5"]
    assert get_te_after(file,line_number,amount) == expected


def test_get_te_before_original():
    path = "/Users/noemiamoralesdiaz/Desktop/Doc/GL_validation/Como_detecta_tandems/repeatmasker/script_try/sed.TG56.fixed.nocontig.lengths.gff"
    file = open(path, "r")
    line_number = 2556
    amount = 2
    expected = ["Chr1	RepeatMasker	similarity	15738168	15740296	3.7	-	.	Os0039_INT_RIRE3#2128\n",
                "Chr1	RepeatMasker	similarity	15740297	15743457	7.3	-	.	Os0506_LTR#3160\n"]
    assert get_te_before(file.readlines(),line_number, amount) == expected
    file.close()


def get_lines_middle(file, line_before, line_after):
    return file[line_before:(line_after - 1)] 
 

def test_lines_te_middle():
    file = ["1", "2", "3", "4", "5"] 
    line_number_before = 1
    line_number_after = 5
    expected = ["2", "3", "4"]
    assert get_lines_middle(file, line_number_before, line_number_after) == expected


def verify_before(te_before, te_after,number):
    if te_before["start"] < (te_after["start"]-float(number)):
        return False
    return True


def test_verify_before():
    te_before = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15738168,
        "end": 15740296,
        "identity": 3.7	,
        "strand": "-",
        "comment": ".",
        "type": "Os0039_INT_RIRE3",
        "distance": 2128
    }
    te_after = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15743458,
        "end": 15747667,
        "identity": 4.9 ,
        "strand": "-",
        "comment": ".",
        "type": "Os0039_INT_RIRE3",
        "distance": 4209
    }
    number=5000
    expected = True
    assert verify_before (te_before, te_after, number) == expected


def verify_after(te, te_after, number):
    if te_after["start"] > (te["end"]+float(number)):
        return False
    return True


def test_verify_after():
    te = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15738168,
        "end": 15740296,
        "identity": 3.7	,
        "strand": "-",
        "comment": ".",
        "type": "Os0039_INT_RIRE3",
        "distance": 2128
    }
    te_after = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15741296,
        "end": 15747667,
        "identity": 4.9 ,
        "strand": "-",
        "comment": ".",
        "type": "Os0039_INT_RIRE3",
        "distance": 4209
    }
    number=5000
    expected = True
    assert verify_after (te , te_after, number) == expected


def is_LTR(te_before):
    if "LTR" in te_before["type"]:
        return True
    return False


def test_is_LTR():
    te_before = {
        "chr": "Chr1",
        "program": "RepeatMasker",
        "method": "similarity",
        "start": 15740297,
        "end": 15743457,
        "identity": 7.3	,
        "strand": "-",
        "comment": ".",
        "type": "Os0506_LTR",
        "distance": 3160
    }
    expected = True
    assert is_LTR(te_before) == expected


example = {
        "chr": "Chr1",
        "program": "RepeatMasker"
    }


def append2file(file, dictionary):
    out = ""
    for key, _ in dictionary.items():
        out = out + f"{dictionary[key]}\t"
    out = out + f"\n"
    file.write(out)


def write_dictionary(example):
    out = ""
    for key, _ in example.items():
        out = out + f"{example[key]}\t"
    out = out + f"\n"
    return out


def test_write_dictionary(): 
    example = {
        "chr": "Chr1",
        "program": "RepeatMasker"
    }
    expected = "Chr1\tRepeatMasker\t\n"
    assert write_dictionary(example) == expected


def obtain_te_middle(line, file):
    new_te = parse_transposon_original(file.readlines()[line-1])
    return (new_te)
        

def test_obtain_te_middle():
    path = "/Users/noemiamoralesdiaz/Desktop/Doc/GL_validation/Como_detecta_tandems/repeatmasker/script_try/sed.TG56.fixed.nocontig.lengths.gff"
    file = open(path, "r")
    line = 2
    expected = parse_transposon_original("Chr1	RepeatMasker	similarity	58655	59072	15.7	-	.	Os0030_LTR_RIRE2#417\n")
    assert obtain_te_middle(line, file) == expected
    file.close()

def is_any_LTR(var):
    for item in var:
        if "LTR" in item:
            return True
    return False

def test_is_any_LTR():
    variable = ["sentencia sin2\n", "sentencia con LTR\n", "sentencia sin2\n"]
    expected = True
    assert is_any_LTR(variable) == expected
    variable = ["sentencia sin2\n", "sentencia sin2\n"]
    expected = False
    assert is_any_LTR(variable) == expected


import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 mods/ltr_matcher5_4.py sed.genome.lengths.gff INT_TE_pairs_same_family.gff INT_result_full_tandems.gff $distance_between_ints")
        sys.exit(1)

    path = sys.argv[1]
    pairs_same_fam = sys.argv[2]
    result_path = sys.argv[3]
    number = sys.argv[4]


    file_full = open(path, "r")
    file_pairs = open(pairs_same_fam, "r")
    file_result = open(result_path,"w")


    for line in file_pairs.readlines():
        te_left, te_right = extract_pair(line)
        file_full.seek(0)
        line_number_left, new_te_left = find_te(te_left, file_full)
        te_right["type"] == te_right["type"].replace("\n","")
        file_full.seek(0)
        line_number_right, new_te_right = find_te(te_right, file_full)
        if line_number_left > 0 and line_number_right > 0:
            file_full.seek(0)
            te_before = parse_transposon_original(get_te_before(file_full.readlines(),line_number_left,1)[0])
            if is_LTR(te_before) == True: 
                if verify_before(te_before,te_left,number) == True:
                    file_full.seek(0)
                    te_after = parse_transposon_original(get_te_after(file_full.readlines(),line_number_right,1)[0])
                    if is_LTR(te_after) == True: 
                        if verify_after(te_right,te_after,number) == True:
                            file_full.seek(0)
                            middle_lines = get_lines_middle(file_full.readlines(), line_number_left, line_number_right)
                            file_full.seek(0)
                            #print(middle_lines)
                            is_any_LTR_boolean = is_any_LTR(middle_lines)
                            #print(is_any_LTR_boolean)
                            if len(middle_lines) > 0 and is_any_LTR_boolean == True:
                                append2file(file_result,te_before)
                                append2file(file_result,new_te_left)
                                for middle_transposons in middle_lines:
                                    te_middle = parse_transposon_original(middle_transposons)
                                    if te_middle: #and is_LTR(te_middle) == True: #!= None
                                        file_full.seek(0)
                                        append2file(file_result,te_middle)

                                append2file(file_result,new_te_right)
                                append2file(file_result,te_after)
                                file_result.write("**********\n") 
                                print("Data have been written in the result file")
                    
                    
        
    file_full.close()
    file_pairs.close()
    file_result.close()
