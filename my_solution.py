from os import stat
import random
import math
from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        # length = self.read_input()
        array_numbers = self.read_input()
        # for i in range(length):
        #     array_numbers.append(random.randint(1,1000))
        step = len(array_numbers) / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(array_numbers[i*step : i*step + step]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(array):
        logArray = []

        for num in array:
            logArray.append(math.log(int(str(num)[::-1])))

        maxNum = logArray[0]
        for num in logArray:
            if num > maxNum:
                max = num
        return max

    @staticmethod
    @expose
    def myreduce(mapped):
        res = mapped[0].value
        for num in mapped:
            if num.value > res:
                res = num.value
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        array = []
        for line in f:
            array.append(int(line))
        f.close()
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'a')
        f.write(str(output))
        f.write('\n')
        f.close()

        f.close()