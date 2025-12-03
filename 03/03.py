import numpy as np
class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]

        self.bateries = lines
            
    def solve1(self):
        res = 0
        for b in self.bateries:
            idxs = [ i for i, _ in enumerate(b)  ]

            bs, idxs = zip(*sorted(zip(b, idxs)))
            bs = list(reversed(bs))
            idxs = list(reversed(idxs))
            firstvalue = '0'
            secondvalue = '0'
            # print('....', b)
            if idxs[0] == len(b)-1 or bs[0] == bs[1]:
                secondvalue = bs[0]
                firstvalue = bs[1]
            else:
                firstvalue = bs[0]
                for i in idxs[1:]:
                    # print(i, idxs[0])
                    if i > idxs[0]:
                        # print(i, bs)
                        secondvalue = b[i]
                        break
            bvalue = int(firstvalue+secondvalue)
            # print("Battery:", b, "First:", firstvalue, "Second:", secondvalue, "BValue:", bvalue)
            res += bvalue


        print("Result:", res)

    def solve(self, n=2):
        res = 0
        res = 0
        for baterie in self.bateries:
            bat_idx = [ i for i, _ in enumerate(baterie)  ]

            baterie_ordered, bat_idx = zip(*sorted(zip(baterie, bat_idx), key=lambda x: (x[0], -x[1]) ))
            baterie_ordered = list(reversed(baterie_ordered))
            bat_idx = list(reversed(bat_idx))
            values = ['0'] * n

            idx_values = 0
            taken = []
            while idx_values < n:
                for bord, idxb in zip(baterie_ordered, bat_idx):
                    if idxb in taken or idxb < max(taken, default=-1):
                        continue
                    if idxb <= len(baterie) - (n - idx_values):
                        values[idx_values] = bord
                        idx_values += 1
                        taken.append(idxb)
                        break

            bvalue = int('' . join(values) )
            res += bvalue

        print("Result:", res)



if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve(n=12)


