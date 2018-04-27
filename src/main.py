from io import StringIO
from bw import bwt, count_matches, create_tally, first_col
from sa import suffix_array_basic, suffix_array_fast


def search_text(text, pattern, cut_size, suffix_array):
    start = time.time()
    i = 0
    n = 1
    total = 0
    while i < len(text):
        part = text[i : i + cut_size] + "$"
        start_i = time.time()
        b = bwt(part, suffix_array)
        c = count_matches(b, pattern)
        end_i = time.time()
        total += c
        print ("Cut no. " + str(n) + ", elapsed_time = " + str(end_i - start_i) + ", found " + str(c) + " matches")
        n += 1
        i += cut_size - (len(pattern) - 1)
    end = time.time()
    print ('Total time ' + str(end - start) + 's', 'Total matches = '  + str(total))


if __name__ == "__main__":    
    parsed_fa = {}
    file_name1 = 'cfa_ref_CanFam3.1_chr1.fa'
    file_name2 = '42345_ref_DPV01_chrUn.fa'
    text = ""
    with open(file_name1) as f:
        parsed_fa = parse_fasta(StringIO(f.read()))
        for k, d in parsed_fa.items():
            text += d
    print('Total length of input text sequence = {}'.format(len(text)))
    search_text(text, 'ATGATG', 5 * 10**3, suffix_array_fast)