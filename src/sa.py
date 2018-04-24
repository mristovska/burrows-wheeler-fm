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