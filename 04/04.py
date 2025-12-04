import numpy as np
class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.readlines()
            lines = np.array([ np.array(list(line.strip())) for line in lines if line.strip()])

        self.data = lines

    def solve1(self):
        self.res = 0
        self.remove_rolls()
        print("Result:", self.res)

    def solve2(self):
        self.res = 0
        while True:
            refres = self.res
            dataprint = self.remove_rolls()
            if self.res == refres:
                print("Result 2:", self.res)
                return
            self.data = dataprint
            

    def remove_rolls(self):
        cross = [ 1, -1, 1j,  -1j ]
        corners = [ 1+1j, 1-1j, -1+1j, -1-1j ]
        tocheck = cross + corners
        self.dataprint = self.data.copy()
        for i, j in np.ndindex(self.data.shape):
            if self.data[i][j] != "@":
                continue
            score = 0
            for dt in tocheck:
                di = dt.real
                dj = int(dt.imag)
                if i + di < 0 or i + di >= self.data.shape[0]:
                    continue
                if j + dj < 0 or j + dj >= self.data.shape[1]:
                    continue
                if self.data[int(i+di)][j+dj] == "@":
                    score += 1
            if score < 4:
                self.res += 1
                self.dataprint[i][j] = 'x'#str(score)

        # for row in self.dataprint:
        #     print(''.join(row))
        return self.dataprint
                    
            


if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    # ps.solve1()
    ps.solve2()
