def suffix_array(s):
    """Given string s returns suffix array SA(s) 
       Time complexity O(n^2LogN)"""
    suffices = sorted([(s[i:], i) for i in range(0, len(s) + 1)])
    return [x[1] for x in suffices]


class Suffix:
    index = 0
    rank1 = 0
    rank2 = 0


def suffix_array_fast(s):
    """Given string s returns suffix array SA(s) 
       Time complexity O(nLogNLogN)"""
    suffixes = []
    s = s + '$'
    for i in range(len(s)):
        next_suffix = Suffix()
        next_suffix.index = i
        next_suffix.rank1 = ord(s[i]) - ord('a')
        next_suffix.rank2 = ord(s[i + 1]) - ord('a') if (i + 1) < len(s) else -1
        suffixes.append(next_suffix)
        
    suffixes = sorted(suffixes, key = lambda x: (x.rank1, x.rank2))
       
    k = 4
    ind = {}
    while k < 2 * len(s):
        rank = 0
        prev_rank = suffixes[0].rank1
        suffixes[0].rank1 = rank
        ind[suffixes[0].index] = 0
        
        #assign rank1 to each suffix
        for i in range(1, len(s)):
            if (suffixes[i].rank1 == prev_rank and suffixes[i].rank2 == suffixes[i - 1].rank2):
                prev_rank = suffixes[i].rank1
                suffixes[i].rank1 = rank
            else:
                prev_rank = suffixes[i].rank1
                rank += 1
                suffixes[i].rank1 = rank
            ind[suffixes[i].index] = i
        
        #assign rank2 
        for i in range(0, len(s)):
            next_index = suffixes[i].index + k / 2
            suffixes[i].rank2 = suffixes[ind[next_index]].rank1 if next_index < len(s) else -1
        
        suffixes = sorted(suffixes, key = lambda x: (x.rank1, x.rank2))
        k *= 2
    
    result = [suffix.index for suffix in suffixes]
        
    return result


from itertools import groupby
from operator import itemgetter

def suffix_array_new(text, _step=16):
    """Analyze all common strings in the text.

    Short substrings of the length _step a are first pre-sorted. The are the 
    results repeatedly merged so that the garanteed number of compared
    characters bytes is doubled in every iteration until all substrings are
    sorted exactly.

    Arguments:
        text:  The text to be analyzed.
        _step: Is only for optimization and testing. It is the optimal length
               of substrings used for initial pre-sorting. The bigger value is
               faster if there is enough memory. Memory requirements are
               approximately (estimate for 32 bit Python 3.3):
                   len(text) * (29 + (_size + 20 if _size > 2 else 0)) + 1MB

    Return value:      (tuple)
      (sa, rsa, lcp)
        sa:  Suffix array                  for i in range(1, size):
               assert text[sa[i-1]:] < text[sa[i]:]
        rsa: Reverse suffix array          for i in range(size):
               assert rsa[sa[i]] == i
        lcp: Longest common prefix         for i in range(1, size):
               assert text[sa[i-1]:sa[i-1]+lcp[i]] == text[sa[i]:sa[i]+lcp[i]]
               if sa[i-1] + lcp[i] < len(text):
                   assert text[sa[i-1] + lcp[i]] < text[sa[i] + lcp[i]]
    >>> suffix_array(text='banana')
    ([5, 3, 1, 0, 4, 2], [3, 2, 5, 1, 4, 0], [0, 1, 3, 0, 0, 2])

    Explanation: 'a' < 'ana' < 'anana' < 'banana' < 'na' < 'nana'
    The Longest Common String is 'ana': lcp[2] == 3 == len('ana')
    It is between  tx[sa[1]:] == 'ana' < 'anana' == tx[sa[2]:]
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

with open("sa_test.txt") as f:
    s = f.read()
    %timeit suffix_array(s)
    %timeit suffix_array_fast(s)

with open("sa_test.txt") as f:
    s = f.read()
    start = time.time()
    sas = suffix_array(s)
    end = time.time()
    slow = end - start
    start = time.time()
    saf = suffix_array_fast(s)
    end = time.time()
    fast = end - start
    assert sas == saf
    print (str(slow), str(fast))