import numpy as np
class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.read().strip()
            chunks = [chunk.splitlines() for chunk in lines.split("\n\n")]
            self.ranges = [ list(map(int,c.split('-'))) for c in chunks[0]]
            self.ids = [ int(c) for c in chunks[1]]

    def solve1(self):
        self.res = 0
        for id in self.ids:
            for r in self.ranges:
                if r[0] <= id <= r[1]:
                    self.res += 1
                    break
        print("Result:", self.res)

    def solve2(self):
        self.res = 0
        # merging ranges that are inclusive
        # sort ranges by start
        # then iterate through ranges, merging as needed
        sorted_ranges = sorted(self.ranges, key=lambda x: x[0])
        merged_ranges = []
        for r in sorted_ranges:
            if not merged_ranges:
                merged_ranges.append(r)
            else:
                last = merged_ranges[-1]
                if r[0] <= last[1]:
                    # merge
                    last[1] = max(last[1], r[1])
                else:
                    merged_ranges.append(r)
        # print("Merged ranges:", merged_ranges)
        for range in merged_ranges:
            self.res += range[1] - range[0] + 1
        print("Result 2:", self.res)

if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()


