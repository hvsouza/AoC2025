import numpy as np
import re


class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

        self.connections = {}
        for line in lines:
            tmp = line.split(':')
            key = tmp[0]
            mv = re.findall(r'[A-z]+', tmp[1])
            self.connections[key] = mv


    def make_search(self, searchkey='out', arriekey='you'):
        for key, values in self.connections.items():
            if searchkey in values:
                if key == arriekey:
                    self.paths[searchkey] = 1
                else:
                    if key not in self.paths:
                        self.make_search(key, arriekey=arriekey)
                    self.paths[searchkey] = self.paths.get(searchkey, 0) + self.paths.get(key, 0)


    def solve1(self):
        self.res = 0

        self.paths = {}

        self.make_search(searchkey='out', arriekey='you')
        self.res = self.paths['out']
        print("Result part 1:", self.res)
    


    def solve2(self):
        self.res = 0


        # from out -> dac -> fft -> svr
        self.paths = {}
        self.make_search(searchkey='out', arriekey='dac')
        self.connect1 = self.paths['out']

        self.paths = {}
        self.make_search(searchkey='dac', arriekey='fft')
        self.connect1 *= self.paths['dac']

        self.paths = {}
        self.make_search(searchkey='fft', arriekey='svr')
        self.connect1 *= self.paths['fft']

        # print("-----")
        # from out -> fft -> dac -> svr
        self.paths = {}
        self.make_search(searchkey='out', arriekey='fft')
        self.connect2 = self.paths['out']
        self.paths = {}
        self.make_search(searchkey='fft', arriekey='dac')
        self.connect2 *= self.paths['fft']
        self.paths = {}
        self.make_search(searchkey='dac', arriekey='svr')
        self.connect2 *= self.paths['dac']

        self.res = self.connect1 + self.connect2
        print("Result part 2:", self.res)

if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()

