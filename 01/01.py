import numpy as np


class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
        self.direction = [ x[0] for x in lines ]
        self.distance = [ int(x[1:]) for x in lines ]
        # print(self.direction)
        # print(self.distance)
            
            # if d > 99:
            #     raise ValueError("Distance too large")

    def solve1(self):
        self.readinput()
        self.point=50
        self.result = 0
        for i, d in enumerate(self.distance):
            if d > 99:
                self.distance[i] = d % 100

        for dir, dist in zip(self.direction, self.distance):
            if dir == "L":
                self.point -= dist
            else:
                self.point += dist
            if self.point > 99:
                self.point = self.point%100
            if self.point < 0:
                self.point = 100 + self.point
            if self.point == 0:
                self.result += 1
            # print("Direction:", dir, "Distance:", dist, "New position:", self.point)
        print("Final position:", self.point, self.result)

    def solve2(self):
        self.readinput()
        self.point=50
        self.result = 0
        self.additions = np.ones_like(self.distance)
        for i, d in enumerate(self.distance):
            if d > 99:
                self.additions[i] = d // 100 #+ 1
                self.distance[i] = d % 100
            else:
                self.additions[i] = 0
        for dir, dist, adds in zip(self.direction, self.distance, self.additions):
            self.notatzero = (self.point != 0)

            if dir == "L":
                self.point -= dist
            else:
                self.point += dist

            self.addpoint = False
            
            if self.point > 99:
                self.point = self.point%100
                self.addpoint = True & self.notatzero

            elif self.point < 0:
                self.point = 100 + self.point
                self.addpoint = True & self.notatzero
            elif self.point == 0:
                self.addpoint = True

            self.result += adds
            if self.addpoint:
                self.result += 1

            # print("Direction:", dir, "Distance:", dist, "New position:", self.point, self.result, adds)
        print("Final position:", self.point, self.result)
        

if __name__ == '__main__':
    solver = PSolver()
    # solver.solve1()
    solver.solve2()

