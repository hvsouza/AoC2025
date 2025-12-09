import numpy as np

class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        self.data = np.loadtxt('input.dat', dtype=int, delimiter=',')
        self.data = self.data.tolist() # better print..
        
        self.vertical_walls = []
        self.horizontal_walls = []
        datacycle = self.data + [self.data[0]]
        for i , (x, y) in enumerate(datacycle[:-1]):
            if datacycle[i+1][0] == x:
                # vertical line
                xwall = x
                y1 = min(y, datacycle[i+1][1])
                y2 = max(y, datacycle[i+1][1])
                self.vertical_walls.append( (xwall, y1, y2) )
            elif datacycle[i+1][1] == y:
                # horizontal line
                ywall = y
                x1 = min(x, datacycle[i+1][0])
                x2 = max(x, datacycle[i+1][0])
                self.horizontal_walls.append( (ywall, x1, x2) )
        # print("Vertical walls:", self.vertical_walls)
        # print("Horizontal walls:", self.horizontal_walls)

    def solve1(self):
        self.res = 0
        for i, (x, y) in enumerate(self.data):
            for j, (xx, yy) in enumerate(self.data[i+1:]):
                area = (abs(x - xx) + 1) * (abs(y - yy)+1)
                if area > self.res:
                    self.res = area
        print("Result part 1:", self.res)

    def solve2(self):
        self.res = 0
        for i, (x, y) in enumerate(self.data):
            for j, (xx, yy) in enumerate(self.data[i+1:]):
                area = (abs(x - xx) + 1) * (abs(y - yy)+1)
                bigger_x = max(x, xx)
                smaller_x = min(x, xx)
                bigger_y = max(y, yy)
                smaller_y = min(y, yy)

                # if (smaller_x, smaller_y) == (7,1) and (bigger_x, bigger_y) == (9,5):
                #     pass
                # else:
                #     continue
                square_is_valid = self.check_square(smaller_x, smaller_y, bigger_x, bigger_y)
                # print(f"{x, y} {xx, yy} form square: ({smaller_x}, {smaller_y}) -> ({bigger_x}, {bigger_y}) with area {area} Valid: {square_is_valid}")
                if not square_is_valid:
                    continue

                if area > self.res:
                    self.res = area
        print("Result part 2:", self.res)


    def check_square(self, smaller_x, smaller_y, bigger_x, bigger_y):
        
        # there should be no vertical or horizontal walls inside the square
        for vwall in self.vertical_walls:
            xwall, ys, yb = vwall
            if smaller_x < xwall < bigger_x:
                # print(vwall, smaller_y, bigger_y)
                # if ys <= smaller_y <= yb or ys <= bigger_y <= yb:
                if bigger_y > ys and smaller_y < yb:
                    # print("bingo... vertical")
                    return False
        for hwall in self.horizontal_walls:
            ywall, xs, xb = hwall
            if smaller_y < ywall < bigger_y:
                # print(hwall, smaller_x, bigger_x)
                if bigger_x > xs and smaller_x < xb:
                    # print("bingo... horizontal")
                    return False

                # if xs <= smaller_x < xb or xs <= bigger_x <= xb:
                #     return False

        return True

        
            
            
            




if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()




