import numpy as np
import re


class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.read().split('\n\n')

        current = 0
        counterhash = {}
        for jgroup in lines[:6]:
            jgroul = jgroup.strip().split('\n')
            # get current from 0: or 1: line 
            for  junk in jgroul:
                junk = junk.strip()
                m = re.match(r'\d+:', junk)
                if m:
                    current = int(m.group(0)[:-1])
                    if current not in counterhash:
                        counterhash[current] = 0
                        continue
                else:
                    counterhash[current] += junk.count('#')

        self.regions = []
        for line in lines[6].strip().split('\n'):
            mbox = re.match(r"(\d+)x(\d+): ", line)
            area=1
            if mbox:
                area = int(mbox.group(1)) * int(mbox.group(2))
                restofline = line.replace(mbox.group(0), '')
                occupied = 0
                for i, v in enumerate(restofline.split()):
                    occupied += int(v)*9#counterhash.get(i, 0)

                self.regions.append([ area , occupied, area - occupied ])
        self.regions = np.array(self.regions)
            


    def solve1(self):
        self.res = 0

        canstillfit = self.regions[ self.regions[:,2] >= 0 ]
        castillfitareas = sorted(canstillfit, key=lambda x: x[2])
        print("Result part 1:", len(castillfitareas))
        


if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()


