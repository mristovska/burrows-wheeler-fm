debug = True


def suffix_array(s):
    """Given string s returns suffix array SA(s)"""
    suffices = sorted([(s[i:], i) for i in range(0, len(s) + 1)])
    if debug:
        print(suffices)
    return map(lambda x: x[1], suffices)


def bwt(s, sa):
    """Given string s returns BWT(s), using suffix array"""
    bw = []
    for idx in sa(s):
        if idx == 0:
            bw.append("$")
        else:
            bw.append(s[idx - 1])
    return "".join(bw)

def first_col(s):
    """Given dict with characters and their counts returns map of first column of BWM"""
    ret = {}
    i = 0
    for c, cnt in sorted(s.items()):
        ret[c] = (i, i + cnt)
        i += cnt
    return ret

def create_tally(bwt):
    """Given bwt string returns tally matrix"""
    #should yet introduce checkpoints
    
    #init
    tally = {}
    cnts = {}
    for c in bwt:
        if c not in cnts:
            cnts[c] = 0
            tally[c] = []
    
    #insertion
    for c in bwt:
        cnts[c] += 1
        for k in cnts:
            tally[k].append(cnts[k])
    
    return tally, cnts


def count_matches(bwt, pat):
    """Given BWT string and pattern returns number of occurencens"""
    tally, cnts = create_tally(bwt)
    first = first_col(cnts)
    if pat[-1] not in first:
        return 0
    l, r = first[pat[-1]]
    i = len(pat) - 2
    while i >= 0 and r > l:
        c = pat[i]
        l = first[c][0] + tally[c][l - 1]
        r = first[c][0] + tally[c][r - 1]
        i -= 1
    return r - l


s = "I am so stupid. I am very stupid."
count_matches(bwt(s), "stupid")

    
    