import sys
import time
import psutil, os 
from itertools import groupby
from operator import itemgetter
from io import StringIO


def suffix_array_basic(s):
    """Given string s returns suffix array SA(s) 
       Time complexity O(n^2LogN)"""
    suffices = sorted([(s[i:], i) for i in range(0, len(s))])
    return [x[1] for x in suffices]



def suffix_array_fast(text, _step=32):
    """Analyze all common strings in the text.

    Short substrings of the length _step a are first pre-sorted. The are the 
    results repeatedly merged so that the garanteed number of compared
    characters bytes is doubled in every iteration until all substrings are
    sorted exactly.

    Arguments:
        text:  The text to be analyzed.
        _step: Is only for optimization and testing. 
    Return value:      [list]
      (sa)
        sa:  Suffix array                
    >>> suffix_array(text='banana')
    [5, 3, 1, 0, 4, 2]

    Explanation: 'a' < 'ana' < 'anana' < 'banana' < 'na' < 'nana'
    """
    tx = text
    size = len(tx)
    step = min(max(_step, 1), len(tx))
    sa = list(range(len(tx)))
    sa.sort(key=lambda i: tx[i:i + step])
    grpstart = size * [False] + [True]  # a boolean map for iteration speedup.
    # It helps to skip yet resolved values. The last value True is a sentinel.
    rsa = size * [None]
    stgrp, igrp = '', 0
    for i, pos in enumerate(sa):
        st = tx[pos:pos + step]
        if st != stgrp:
            grpstart[igrp] = (igrp < i - 1)
            stgrp = st
            igrp = i
        rsa[pos] = igrp
        sa[i] = pos
    grpstart[igrp] = (igrp < size - 1 or size == 0)
    while grpstart.index(True) < size:
        # assert step <= size
        nextgr = grpstart.index(True)
        while nextgr < size:
            igrp = nextgr
            nextgr = grpstart.index(True, igrp + 1)
            glist = []
            for ig in range(igrp, nextgr):
                pos = sa[ig]
                if rsa[pos] != igrp:
                    break
                newgr = rsa[pos + step] if pos + step < size else -1
                glist.append((newgr, pos))
            glist.sort()
            for ig, g in groupby(glist, key=itemgetter(0)):
                g = [x[1] for x in g]
                sa[igrp:igrp + len(g)] = g
                grpstart[igrp] = (len(g) > 1)
                for pos in g:
                    rsa[pos] = igrp
                igrp += len(g)
        step *= 2
    del grpstart
    return sa


def bwt(s, sa):
    """Given string s returns BWT(s), using suffix array"""
    bw = []
    for idx in sa:
        if idx == 0:
            bw.append("$")
        else:
            bw.append(s[idx - 1])
    return "".join(bw)


def parse_fasta(fh):
    fa = {}
    current_short_name = None
    # Part 1: compile list of lines per sequence
    for ln in fh:
        if ln[0] == '>':
            # new name line; remember current sequence's short name
            long_name = ln[1:].rstrip()
            current_short_name = long_name.split()[0]
            fa[current_short_name] = []
        else:
            # append nucleotides to current sequence
            fa[current_short_name].append(ln.rstrip())
    # Part 2: join lists into strings
    for short_name, nuc_list in fa.items():
        # join this sequence's lines into one long string
        fa[short_name] = ''.join(nuc_list)
    return fa


class Checkpoints:
    def __init__(self, bwt, step):
        """
        Creates checkpoints matrix.
        There is entry for each character, and each value in dict is list of number of occurences
        of that character. 
        Trick is to not store every element of the list but store only on positions divisible by step.
        """
        self.checkpoints = {}
        self.step = step
        tally = {}
        for c in bwt:
            if c not in tally:
                tally[c] = 0
                self.checkpoints[c] = []
        for i in range(len(bwt)):
            tally[bwt[i]] += 1
            if i % step == 0:
                for k in tally.keys():
                    self.checkpoints[k].append(tally[k])
    
    def rank(self, bwt, c, row):
        """Returns number of occurences of c before row (inclusive)"""
        if c not in self.checkpoints or row < 0:
            return 0
        cnt, i = 0, row
        while i % self.step != 0:
            if bwt[i] == c:
                cnt += 1
            i -= 1
        return cnt + self.checkpoints[c][i // self.step]


class FMIndex:
    def cut_suffix_array(self, full_sa, sa_step):
        """Sizes down suffix array taking every sa_step-th element, the rest are removed"""
        res_sa = {}
        for i in range(len(full_sa)):
            if full_sa[i] % sa_step == 0:
                res_sa[i] = full_sa[i]
        return res_sa
    
    def calc_first_col(self, bwt):
        """
        Returns first column of BWT matrix.
        It is enough to keep only number of characters less than current, because it is sorted column.
        """
        cnts = {}
        for c in bwt:
            cnts[c] = cnts.get(c, 0) + 1
        ret = {}
        total = 0
        for c, cnt in sorted(cnts.items()):
            ret[c] = total
            total += cnt
        return ret
    
    def __init__(self, T, suffix_array, cp_step, sa_step):
        if T[-1] != '$':
            T += '$'
        full_sa = suffix_array(T)
        self.bwt = bwt(T, full_sa)
        self.sa = self.cut_suffix_array(full_sa, sa_step)
        self.cps = Checkpoints(self.bwt, cp_step)
        self.first_col = self.calc_first_col(self.bwt)
        
    def count(self, c):
        """Return number of characters less than c"""
        if c not in self.first_col:
            for cc in sorted(self.first_col.keys()):
                if c < cc: 
                    return self.first_col[cc]
            return self.first_col[cc]
        else:
            return self.first_col[c]
        
    def interval(self, p):
        """Returns inclusive interval of BWM rows where p is prefix"""
        l, r = 0, len(self.bwt) - 1
        for i in range(len(p) - 1, -1, -1): #start from last character and go backwards
            l = self.cps.rank(self.bwt, p[i], l - 1) + self.count(p[i])
            r = self.cps.rank(self.bwt, p[i], r) + self.count(p[i]) - 1
            if r < l:
                break
        return l, r + 1
    
    def get_offset(self, r):
        """Given row in matrix returns its real offset in text"""
        steps = 0
        while r not in self.sa:
            c = self.bwt[r]
            r = self.cps.rank(self.bwt, c, r - 1) + self.count(c)
            steps += 1
        return self.sa[r] + steps
    
    def find_occurences(self, p):
        """Returns all occurences of pattern p"""
        l, r = self.interval(p)
        return [self.get_offset(i) for i in range(l, r)]


def search_text(text, pattern, cut_size, suffix_array):
    start = time.time()
    i = 0
    n = 1
    total = 0
    cut_size = min(cut_size, len(text))
    occ = []
    while i < len(text):
        part = text[i : i + cut_size] + "$"
        start_i = time.time()
        fm_index = FMIndex(part, suffix_array_fast, 32, 32)
        occ_i = fm_index.find_occurences(pattern)
        occ_i = [x + i for x in occ_i]
        occ += occ_i
        end_i = time.time()
        total += len(occ_i)
        #print ("Cut no. " + str(n) + ", elapsed_time = " + str(end_i - start_i) + ", found " + str(len(occ_i)) + " matches")
        n += 1
        i += cut_size - (len(pattern) - 1)
    end = time.time()
    print ('Total time consumed while searching: ' + str(end - start) + 's', 'Total matches: '  + str(total))
    return occ


parsed_fa = {}
file_name1 = 'cfa_ref_CanFam3.1_chr1.fa'
file_name2 = '42345_ref_DPV01_chrUn.fa'
text = ""
with open(file_name1) as f:
    parsed_fa = parse_fasta(StringIO(f.read()))
    for k, d in parsed_fa.items():
        text += d
print('Total length of input text sequence = {}'.format(len(text)))

search_text(text, 'ATGATG', 10**4, suffix_array_fast)

process = psutil.Process(os.getpid()) 
mem = process.memory_info().rss / 1024 / 1024 
print("Used this much memory: " + str(mem) + ' Mb')