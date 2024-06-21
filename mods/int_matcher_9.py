def parse_transposon(sentence):
    te = {}
    chr, start, end, type, *_ =  sentence.split("\t")
    te["chr"] = chr
    te["start"] = int(start)
    te["end"] = int(end)
    te["type"] = type
    return te


def test_parse_te():
    sentence = "Chr1    15743458    15747667    Os0039_INT_RIRE3    5791    4209"
    expected = {
        "chr": "Chr1",
        "start": 15743458,
        "end": 15747667,
        "type": "Os0039_INT_RIRE3"
    }
    assert expected == parse_transposon(sentence)


def append2file(file, dictionary):
    out = ""
    for key, _ in dictionary.items():
        out = out + f"{dictionary[key]}\t"
    out = out + f"\n"
    file.write(out)


def get_lines_middle(file, line_before, line_after):
    return file[line_before:(line_after - 1)] 
 

def test_lines_te_middle():
    file = ["1", "2", "3", "4", "5"] 
    line_number_before = 1
    line_number_after = 5
    expected = ["2", "3", "4"]
    assert get_lines_middle(file, line_number_before, line_number_after) == expected


def is_any_INT(var):
    for item in var:
        if "INT" in item:
            return True
    return False

def test_isINT_LTR():
    variable = ["sentencia sin2\n", "sentencia con INT\n", "sentencia sin2\n"]
    expected = True
    assert is_any_INT(variable) == expected
    variable = ["sentencia sin2\n", "sentencia sin2\n"]
    expected = False
    assert is_any_INT(variable) == expected


def extract_triplet(line):
    l = parse_transposon(line.split(" y ")[0])
    m = parse_transposon(line.split(" y ")[1])
    r = parse_transposon(line.split(" y ")[2])
    return (l, m, r)

def test_extract_triplet():
    line = "Chr1    15743458    15747667    Os0039_INT_RIRE3    5791    4209 y Chr1 15747668    15753937    Os0039_INT_RIRE3    5791    6269 y Chr1 15747668    15753937    Os0039_INT_RIRE3    5791    6269"
    expected_left = {
        "chr": "Chr1",
        "start": 15743458,
        "end": 15747667,
        "type": "Os0039_INT_RIRE3"
    }
    expected_middle = {
        "chr": "Chr1",
        "start": 15747668,
        "end": 15753937,
        "type": "Os0039_INT_RIRE3"
    }
    expected_right = {
        "chr": "Chr1",
        "start": 15747668,
        "end": 15753937,
        "type": "Os0039_INT_RIRE3"
    }

    assert extract_triplet(line)[0] == expected_left
    assert extract_triplet(line)[1] == expected_middle
    assert extract_triplet(line)[2] == expected_right

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
    sentence = "Chr1    RepeatMasker    similarity  15680318    15686378    6.7 -   .   Os0850_INT#6060"
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
    #te = parse_transposon("Chr1    15743458    15747667    Os0039_INT_RIRE3    5791    4209")
    te = parse_transposon("Chr1 15747668    15753937    Os0039_INT_RIRE3    5791    6269")
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





import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 4int_matcher.py sed.genome.lengths.gff sorted_LTR_TE_triplets_same_family.gff LTR_result_full_tandems.gff")
        sys.exit(1)

    path = sys.argv[1]
    triplets_same_fam = sys.argv[2]
    result_path = sys.argv[3]

    file_full = open(path, "r")
    file_triplets = open(triplets_same_fam, "r")
    file_result = open(result_path,"w")

    for line in file_triplets.readlines():
        te_left, te_middle, te_right = extract_triplet(line)
        file_full.seek(0)
        line_number_left, new_te_left = find_te(te_left, file_full)
        file_full.seek(0)
        line_number_middle, new_te_middle = find_te(te_middle, file_full)
        te_right["type"] == te_right["type"].replace("\n","")
        file_full.seek(0)
        line_number_right, new_te_right = find_te(te_right, file_full)
        if line_number_left > 0 and line_number_middle > 0 and line_number_right > 0:
            file_full.seek(0)
            middle_lines_1 = get_lines_middle(file_full.readlines(), line_number_left, line_number_middle)
            file_full.seek(0)
            middle_lines_2 = get_lines_middle(file_full.readlines(), line_number_middle, line_number_right)
            file_full.seek(0)
            #print(middle_lines_1)
            #print(middle_lines_2)
            is_any_INT_boolean_1 = is_any_INT(middle_lines_1)
            is_any_INT_boolean_2 = is_any_INT(middle_lines_2)
            if len(middle_lines_1) > 0 and len(middle_lines_2) > 0 and is_any_INT_boolean_1 == True and is_any_INT_boolean_2 == True:
                append2file(file_result,new_te_left)
                
                for middle_transposons_1 in middle_lines_1:
                    te_middle_1 = parse_transposon_original(middle_transposons_1)
                    if te_middle_1:
                        file_full.seek(0)
                        append2file(file_result,te_middle_1)
                
                append2file(file_result,new_te_middle)
                
                for middle_transposons_2 in middle_lines_2:
                    te_middle_2 = parse_transposon_original(middle_transposons_2)
                    if te_middle_2:
                        file_full.seek(0)
                        append2file(file_result,te_middle_2)
                
                append2file(file_result,new_te_right)
                file_result.write("**********\n") 
                print("Data have been written in the result file")

    #Close files
    file_full.close()
    file_triplets.close()
    file_result.close()






















