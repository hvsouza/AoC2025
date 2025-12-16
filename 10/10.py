import numpy as np
from dataclasses import dataclass
from functools import cache
from cachetools.keys import hashkey

import re
import sys
from scipy.optimize import LinearConstraint
from scipy.optimize import milp

sys.setrecursionlimit(5000)


@dataclass
class Machine:
    target: np.ndarray
    buttons: tuple
    requirements: np.ndarray



class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines =  [ line.strip() for line in f.readlines() if line.strip() ]

        self.machines = []
        for line in lines:
            m = re.match(r"\[([.#]+)\]", line)
            if m is None:
                raise ValueError("Cannot parse line:", line)
            target = np.array([ False if c == '.' else True for c in m.group(1) ])
            m = re.findall(r"\(([\d,]+)\)", line)

            button_mask = np.zeros_like(target, dtype=bool)
            buttons = np.empty( (0, len(target)), dtype=bool )
            for b in m:
                bidx = [int(x) for x in b.split(',')]
                for idx in bidx:
                    button_mask[idx] = True
                buttons = np.vstack( (buttons, button_mask.copy()) )
                button_mask[:] = False
            m = re.search(r"\{([\d,]+)\}", line)
            if m is None:
                raise ValueError("Cannot parse requirements in line:", line)
            # print(m.group(1))
            buttons = tuple( [ tuple(row) for row in buttons ] )
            requirements = np.array([int(x) for x in m.group(1).split(',')] ) 
            self.machines.append( Machine(target=target, buttons=buttons,
                                     requirements=requirements) )

    @cache
    def toggle_light(self, lights_in, button_mask):
        lights = np.array(lights_in)
        button_mask = np.array(button_mask)
        new_state = lights ^ True
        lights[ button_mask ] = new_state[ button_mask ]
        return lights
    
    def plights(self, lights):
        v = ['#' if c else '.' for c in lights ]
        return ''.join(v)
        
    

    def press_buttons(self, original_lights, buttons, skip = -1, past_states_light = tuple()):
        dk = hashkey(original_lights, buttons, skip)
        if dk in self.cached_values:
            # print("Using cached value for:", original_lights, skip)
            return self.cached_values[dk]

        min_pressed = 1e12
        for i, button_mask in enumerate(buttons):
            if skip == -1:
                # self.max_past = 500
                past_states_light = tuple()
            if i == skip:
                continue
            if len(past_states_light) > self.max_past:
                return 200
            lights = tuple(self.toggle_light(original_lights, button_mask))
            if lights in past_states_light:

                continue
            my_past_stages_light = set(past_states_light)
            my_past_stages_light.add(tuple(original_lights))
            # print(self.plights(original_lights), '---', button_mask, '===>', self.plights(lights), ' i = ', i, ' len(past):', len(my_past_stages_light), 'min_pressed:', min_pressed)
            if lights == self.target:
                # print("\t\t\t All lights ON! ", len(my_past_stages_light), " presses.")
                self.max_past = min(self.max_past, len(my_past_stages_light))
                self.cached_values[dk] = 1
                return 1
            min_pressed = min(self.press_buttons(lights, buttons, skip=i, past_states_light=tuple(my_past_stages_light))+1, min_pressed)
        # print(min_pressed)
        
        if min_pressed<self.max_past:
            self.cached_values[dk] = min_pressed
        return min_pressed

    def solve1(self):
        self.res = 0
        for i, machine in enumerate(self.machines):

            # print("Machine target:" , machine.target)
            startingpoint = np.zeros_like(machine.target, dtype=bool)
            self.target = tuple(machine.target)
            self.max_past = 12
            self.cached_values = {}
            self.min_p = self.press_buttons(tuple(startingpoint), machine.buttons, skip = -1, past_states_light=tuple() )

            print(f"Minimum presses for {i} machine:", self.min_p, self.max_past)

            self.res += self.min_p

        print("Result part 1:", self.res)


        
    def solve2(self):
        self.res = 0
        self.cached_values = {}
        for i, machine in enumerate(self.machines):
            startingpoint = np.array([ 0 for _ in machine.requirements ] )
            buttons = np.array( [ np.array(b, dtype=int) for b in machine.buttons ] )
            buttons = tuple([  tuple([int(i) for i, x in enumerate(b) if x ]) for b in buttons ])
            A = np.zeros( (machine.requirements.size, len(buttons)), dtype=int )

            for i in range(machine.requirements.size):
                for j, b in enumerate(buttons):
                    if i in b:
                        A[i,j] = 1
            # print(buttons)
            # for v in A:
            #     print(v)
            # print()
            c = np.array( [ 1 for i in range(len(buttons)) ], dtype=int )
            b_lower = np.array(machine.requirements, dtype=float)
            b_upper = np.full_like(b_lower, b_lower, dtype=float)
            constraints = LinearConstraint(A, b_lower, b_upper)
            integrality = np.ones_like(c)
            res = milp(c=c, constraints=constraints, integrality=integrality)
            counts = np.array(startingpoint)
            for i, b in enumerate(buttons):
                counts[np.array(b)] += int(res.x[i])
            # print(f"Machine {i}: Required presses:", machine.requirements, " Achieved:", counts, "  Total presses:", np.sum(res.x))
            # print(res.x)
            self.res += np.sum(res.x)
                
            

        print("Result part 2:", self.res)

if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()


