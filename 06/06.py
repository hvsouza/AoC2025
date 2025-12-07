import numpy as np
class PSolver():
    def __init__(self):
        pass

    def readinput(self, iname='input.dat'):
        with open(iname, 'r') as f:
            lines_raw = f.readlines()

            lines = [line.strip() for line in lines_raw if line.strip()]

            # reading for part1
            self.numbers = np.array( [ np.array([ int(x) for x in line.split()]) for line in lines if line[0].isdigit() ] )
            self.operations = [ line.split() for line in lines if not line[0].isdigit() ][0]
            self.numbers = self.numbers.T  # transpose to match shape


            # reading for par2
            lines = [ line.replace('\n','')[::-1] for line in lines_raw ]
            weird_numbers = lines[:-1]
            weird_operations = lines[-1]
            # print(weird_numbers)
            # print(weird_operations)
            separators = [0]
            for i, wo in enumerate(weird_operations):
                if wo in ["+","*"]:
                    separators.append(i+1)

            
            self.weird_numbers = []
            for i, sep in enumerate(separators[1:]):
                self.weird_numbers.append( [] )
                # print("separator", sep)
                # print('...', weird_numbers[0], '...', weird_numbers[0][separators[i]:sep+1])
                strnumbers = []
                for wn in weird_numbers:
                    # print('...', wn, '...', wn[separators[i]:sep])
                    strnumbers.append( wn[separators[i]:sep] )
                # print('---\n\n')

                strnumbers = np.array(strnumbers)
                # print(strnumbers)
                for j in range(len(strnumbers[0])):
                    number = ''
                    for dig in strnumbers:
                        number += dig[j]
                        # print(dig[j], end='')
                    # print()
                    # print("number:", number)
                    if number.strip():
                        self.weird_numbers[-1].append( int(number) )
            # for wn in self.weird_numbers:
            #     print(len(wn), wn)
            # self.weird_numbers = np.array(self.weird_numbers) # transpose to match shape


    def operate(self, numbers, operations):
        res = 0
        for on, op in zip(numbers, operations):
            opres = 0
            if op == '+':
                opres = np.sum(on)
            elif op == '*':
                opres = np.prod(on)
            else:
                print(f"Unknown operation: {op}")
            # print(f"Operation: {op} on numbers: {numbers}, result: {opres}")
            res += opres
        return res
    
    def solve1(self):
        print("Result:", self.operate(self.numbers, self.operations))
    def solve2(self):
        print("Result:", self.operate(self.weird_numbers, self.operations[::-1]))


if __name__ == "__main__":
    ps = PSolver()
    ps.readinput()
    ps.solve1()
    ps.solve2()

