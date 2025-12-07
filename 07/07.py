import numpy as np
class PSolver():
    def __init__(self):
        pass


    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines_raw = f.readlines()
            lines = [line.strip() for line in lines_raw if line.strip()]
        self.firstshot = lines[0].find('S')
        self.stages = [ list(line) for line in lines ]

    def shoooot(self):
        self.res = 0
        self.beams = [ self.firstshot ] 
        self.realities_beam_cares = { k:1 for k in self.beams }
        for i, stage in enumerate(self.stages[1:-1], 1):
            new_beams = []
            new_realities = {}
            for beam in self.beams:
                if stage[beam] == '.':
                    new_beams.append(beam)
                    new_realities[beam] = new_realities.get(beam,0) + self.realities_beam_cares[beam]

                elif stage[beam] == '^':
                    if beam-1 >= 0:
                        new_beams.append(beam-1)
                        new_realities[beam-1] = new_realities.get(beam-1,0) + self.realities_beam_cares[beam]
                    if beam+1 < len(stage):
                        new_beams.append(beam+1)
                        new_realities[beam+1] = new_realities.get(beam+1,0) + self.realities_beam_cares[beam]
                    self.res += 1
            self.beams = set(new_beams)
            # print(f"After stage {i}, beams at: {self.beams}, splitters used: {self.res}")
            self.realities_beam_cares = new_realities
            # print(f"After stage {i}, beams at: {self.beams}, splitters used: {self.res}, realities: {sum(self.realities_beam_cares.values())}")

    def solve1(self):
        print("Result part 1:", self.res)

    def solve2(self):
        print("Result part 2:", sum(self.realities_beam_cares.values()))



if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.shoooot()
    ps.solve1()
    ps.solve2()
