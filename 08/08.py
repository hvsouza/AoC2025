import numpy as np
from dataclasses import dataclass
from collections import Counter

@dataclass
class jbox:
    x: int
    y: int
    z: int
    id: int
    group: int

class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        data = np.loadtxt('input.dat', dtype=float, delimiter=',')
        self.jboxes = []
        for i, d in enumerate(data):
            self.jboxes.append( jbox(d[0], d[1], d[2], i, -1) )


    def solve(self, part=1):
        self.res = 0
        self.jdistances = {}
        for i, jb in enumerate(self.jboxes):
            jb.group = -1  # reset group
            for jb2 in self.jboxes[i+1:]:
                jdist = np.sqrt( (jb.x - jb2.x)**2 + (jb.y - jb2.y)**2 + (jb.z - jb2.z)**2 )
                self.jdistances[(jb.id, jb2.id)] = jdist

        # print(self.jdistances)
        self.jdistances = dict( sorted(self.jdistances.items(), key=lambda item: item[1]) )

        ngroups = 0
        
        dict_group_jboxes = {}

        pairs = 0

        for (id1, id2), dist in self.jdistances.items():
            jb1 = self.jboxes[id1]
            jb2 = self.jboxes[id2]

            # print(f"Considering jboxes {jb1.id} (group {jb1.group}) and {jb2.id} (group {jb2.group}) with distance {dist:.2f}", end=' ')
            pairs += 1
            if jb1.group == -1 and jb2.group == -1:
                # new group
                ngroups += 1
                jb1.group = ngroups
                jb2.group = ngroups
                dict_group_jboxes[ngroups] = [id1, id2]

            elif jb1.group != -1 and jb2.group == -1:
                jb2.group = jb1.group
                dict_group_jboxes[jb1.group].append(id2)
            elif jb1.group == -1 and jb2.group != -1:
                jb1.group = jb2.group
                dict_group_jboxes[jb2.group].append(id1)
            elif jb1.group != -1 and jb2.group != -1:
                # do nothing, already assigned
                if jb1.group != jb2.group:
                    # get lowest group and assign to both

                    lowgroup = min(jb1.group, jb2.group)
                    oldgroup = max(jb1.group, jb2.group)

                    for jid in dict_group_jboxes[oldgroup]:
                        self.jboxes[jid].group = lowgroup
                        dict_group_jboxes[lowgroup].append(jid)
                    dict_group_jboxes.pop(oldgroup)
                else:
                    continue

            # print(f"=> assigned groups {jb1.group} and {jb2.group} ... pairs: {pairs},  {dict_group_jboxes}")
            if part==1 and pairs >= 1000:
                break
            if part==2:
                if len(dict_group_jboxes) == 1 and len( list(dict_group_jboxes.values())[0] ) == len(self.jboxes):
                    print(f"Result part {part}:", jb1.x * jb2.x)
                    return



        ordered_groups = dict( sorted( dict_group_jboxes.items(), key=lambda item: len(item[1]), reverse=True) )
        self.res = 1
        # print(ordered_groups)
        for lg in list(ordered_groups.values())[:3]:
            self.res *= len(lg)

        print(f"Result part {part}:", self.res)
    def solve1(self):
        self.solve(part=1)
    def solve2(self):
        self.solve(part=2)

if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()


