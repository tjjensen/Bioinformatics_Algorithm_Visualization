
class SeqAlign():
    DIRECTION_MAP = {0 : 'zero', 1 : 'diag', 2 : 'up', 3: 'left'}
    SCORE_MAP = {'A':0, 'C':1, 'G':2, 'T':3, '-':4}

    def __init__(self, seq1, seq2, scores, alphabet, is_local=False):
        self.seq1 = seq1
        self.seq2 = seq2
        self.scores = scores
        self.score_map = dict([(value, idx) for idx, value in enumerate(alphabet)])
        self.is_local = is_local
        self.S = [[None for i in range(len(self.seq1)+1)] for i in range(len(self.seq2)+1)]
        self.S[0][0] = 0.0
        self.D = [[[] for i in range(len(self.seq1)+1)] for i in range(len(self.seq2)+1)]
        self.D[0][0] = None

    def proceedForward(self):
        j = None
        for i, row in enumerate(self.S):
            try:
                j = row.index(None)
                break
            except ValueError:
                continue
        if j is None:
            return False
        values = []
        if self.is_local:
            values.append(0)
        else:
            values.append(None)
        if i>0 and j>0:
            values.append(self.S[i-1][j-1] + self.scores[self.score_map[self.seq1[j-1]]][self.score_map[self.seq2[i-1]]])
        else:
            values.append(None)
        if i>0:
            values.append(self.S[i-1][j] + self.scores[self.score_map[self.seq1[j-1]]][self.score_map['-']])
        else:
            values.append(None)
        if j>0:
            values.append(self.S[i][j-1] + self.scores[self.score_map['-']][self.score_map[self.seq2[i-1]]])
        else:
            values.append(None)
        max_value = max(values)
        self.S[i][j] = max_value
        max_indices = [idx for idx, value in enumerate(values) if value == max_value]
        for max_index in max_indices:
            self.D[i][j].append(SeqAlign.DIRECTION_MAP[max_index])
        return True

    def proceedBackward(self):
        j = None
        for i, row in enumerate(self.S):
            try:
                j = row.index(None)
                break
            except ValueError:
                continue
        if j is None:
            self.S[-1][-1] = None
            self.D[-1][-1] = list()
            return True
        elif i==0 and j==1:
            return False
        else:
            if j==0:
                i= i-1
                j = -1
            else:
                j = j-1
            self.S[i][j]=None
            self.D[i][j]= list()
            return True

    def finish(self):
        while self.proceedForward():
            continue
        return True

    def restart(self):
        self.S = [[None for i in range(len(self.seq1)+1)] for i in range(len(self.seq2)+1)]
        self.S[0][0] = 0.0
        self.D = [[[] for i in range(len(self.seq1)+1)] for i in range(len(self.seq2)+1)]
        self.D[0][0] = None
        return True

if __name__ == '__main__':
    scores = [[2,-1,-1,-1,-1],[-1,2,-1,-1,-1],[-1,-1,2,-1,-1],[-1,-1,-1,2,-1],[-1,-1,-1,-1,-10]]
    seq1 = 'ACACACTA'
    seq2 = 'AGCACACA'
    S, D = seq_init(seq1, seq2)
    print S
    print D
    S, D = seq_forward(seq1, seq2, S, D, scores, True)
    print S
    print D
    while True:
        S, D = seq_forward(seq1, seq2, S, D, scores, True)
        for row in S:
            print row
        print ''
        print ''
        for row in  D:
            print row
