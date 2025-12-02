class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()][0]
            self.ids_ranges =  lines.split(',')
            self.ids_ranges = [ [int(v) for v in  x.split('-')] for x in self.ids_ranges ]
            
    def solve1(self):
        res = 0
        for id_range in self.ids_ranges:
            start, end = id_range
            for v in range(start, end+1):
                vstr = str(v)
                if vstr[0] == '0':
                    res += 1
                    continue
                if vstr[:len(vstr)//2] == vstr[len(vstr)//2:]:
                    res += v

        print("Result:", res)

    def solve2(self):
        res = 0
        for id_range in self.ids_ranges:
            start, end = id_range
            for v in range(start, end+1):
                vstr = str(v)
                if len(vstr) == 1:
                    continue

                if vstr[0] == '0':
                    # print(vstr, "starts with 0")
                    res += 1
                    continue

                if len(set(vstr)) == 1:
                    # print(vstr, "all same")
                    res += v
                    continue

                options_of_break = [ i for i in range(2, len(vstr)//2+1) if len(vstr) % i == 0 ]

                # print("Checking", vstr, "with options", options_of_break)
                for ob in options_of_break:
                    all_groups = [ vstr[i:i+ob] for i in range(0, len(vstr), ob) ]
                    group_set = set(all_groups)
                    # print("  Trying break of", ob, "gives groups", all_groups, "set", group_set)
                    if len(group_set) == 1:
                        # print(vstr, "break of", ob, vstr[:ob], "repeats")
                        res += v
                        break


        print("Result:", res)



if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    # ps.solve1()
    ps.solve2()


