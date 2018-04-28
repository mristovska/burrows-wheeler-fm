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

#testing
test = 'banana'
cps_1 = Checkpoints(test, 1)
cps_2 = Checkpoints(test, 2)
ranks_1 = [cps_1.rank(test, 'a', i) for i in range(len(test))]
ranks_2 = [cps_2.rank(test, 'a', i) for i in range(len(test))]
print (ranks_1)
assert ranks_1 == [0, 1, 1, 2, 2, 3]
assert ranks_1 == ranks_2