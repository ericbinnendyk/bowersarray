import math

# This is another Bowers Array evaluating program I made for Jonathan Bowers' birthday!
# And like the previous one, I will probably be updating it with new features in the following days,
# so it can run longer and take more shortcuts before it starts decrimenting an incredibly huge number by one each time enter is pressed.
# .ui mi djica lo nu la'o gy. Jonathan Bowers .gy cu se jbedetnunsla

class Bowersarray:
    # self.a: the array itself, as a list
    # self.a_num: which number it is in the evalutaion process

    # initialize a new array
    def __init__(self, input_a, input_a_num = 0):
        self.a = input_a
        self.a_num = input_a_num
        self.canonize()

    def __str__(self):
        string = '{'
        for index, sub in enumerate(self.a):
            if index != 0:
                if len(self.a[index - 1]) == 0:
                    string += '(1) '
                else:
                    string += ' (1) '
            # note: num may actually be a string representing a reference to another array, for example 'A5'
            for index2, num in enumerate(sub):
                if index2 != 0:
                    string += ', '
                string += str(num)
        string += '}'
        return string

    # trim empty rows off the end of array and 1's off the end of rows
    def canonize(self):
        for row in self.a:
            while len(row) > 0 and row[-1] == 1:
                del row[-1]
        while len(self.a) > 0 and self.a[-1] == []:
            del self.a[-1]

    # get element by index. index is a list of coordinates describing position in the row, plane, realm, etc.
    def at_index(self, pos_list):
        # check if index does not refer to element in first plane
        # since the type currently only supports 2D arrays, the result is 1
        if pos_list[2:] != [0] * len(pos_list[2:]):
            return 1
        if len(pos_list) < 2:
            pos_list += [0] * (2 - len(pos_list))
        subarray = self.a
        for i in [1, 0]:
            if pos_list[i] >= len(subarray):
                return 1
            subarray = subarray[pos_list[i]]
        return subarray

    # evaluates the array and (theoretically) returns the final value
    # precondition: array is canonized
    # postcondition: destroys the original array in the process; final array has only two entries
    def eval(self):
        # default prime: evaluate to base
        if self.at_index([1]) == 1:
            self.print_status('= {}'.format(self.at_index([0])))
            raw_input()
            return self.at_index([0])

        # catastrophic rule: 
        while not (len(self.a) == 1 and len(self.a[0]) <= 2):
            self.print_status()
            raw_input()
            self.catastrophic_step()
        # at this point, the array is only two entries
        b = self.at_index([0])
        p = self.at_index([1])
        result = None
        # if the power is less than 10^10000, print its digits
        # if the power is less than 10^10000, return the power as an integer and not a special exponential type
        # otherwise, just return a string describing the exponential expression
        if type(p) == int and p * math.log10(b) < 10000:
            result = b ** p
            print 'A{} = '.format(self.a_num) + self.__str__() + ' = {}^{} = {}'.format(b, p, result)
        else:
            result = str(b) + '^' + str(p)
            print 'A{} = '.format(self.a_num) + self.__str__() + ' = {}^{}'.format(b, p)
        raw_input()
        return result

    # perform the catastrophic step of Bowers array evaluation
    # precondition: self.a has at least one non-1 entry after the first two, is trimmed of excess 1's and empty rows, and has a prime entry unequal to 1 (in other words, catastrophic rule applies)
    # postcondition: self.a is still trimmed of excess 1's and empty rows
    def catastrophic_step(self):
        # find the row index (pilotrow) and the column index (pilotindex) of the pilot
        for pilotrow, sub in enumerate(self.a):
            if pilotrow == 0:
                sub = sub[2:]
            if len(sub) != 0:
                break
            pilotrow += 1

        if pilotrow == 0:
            pilotindex = find_pilot(sub) + 2
        else:
            pilotindex = find_pilot(sub)

        # Make new copy of array a and decrement prime entry (unless prime entry is stored as a very large power instead of an integer)
        new = Bowersarray(copy_list(self.a), self.a_num + 1)
        if type(new.at_index([1])) == int:
            new.a[0][1] -= 1
        new.canonize()

        # decrement pilot of a (this may uncanonize a, but it will be canonized later)
        # again, only if pilot is actually stored as an integer
        if type(self.at_index([pilotindex, pilotrow])) == int:
            self.a[pilotrow][pilotindex] -= 1

        # set the passengers on previous rows equal to the base
        base = self.at_index([0])
        prime = self.at_index([1])
        for i in xrange(0, pilotrow):
            self.a[i] = [base] * prime
        # set all passengers on the same row as the pilot equal to the base
        for i in xrange(pilotindex - 1):
            self.a[pilotrow][i] = base

        if pilotindex > 0:
            # if the copilot exists, make it a reference to the unevaluated array new
            self.a[pilotrow][pilotindex - 1] = 'A{}'.format(new.a_num)
            self.canonize()
            self.print_status()
            raw_input()

            # after evaluating new, set copilot equal to that value
            self.a[pilotrow][pilotindex - 1] = new.eval()
        else:
            self.canonize()

    # print the array and number of array with an optional message after the array
    def print_status(self, msg = ''):
        print 'A{} ='.format(self.a_num), self, msg

def array_string(a, a_num):
    string = '{'
    for index, sub in enumerate(a):
        if index != 0:
            if len(a[index - 1]) == 0:
                string += '(1) '
            else:
                string += ' (1) '
        for index2, num in enumerate(sub):
            if index2 != 0:
                string += ', '
            string += str(num)
    string += '}'
    return string

# finds the index of the first non-1 entry in a list
def find_pilot(a):
    pilotindex = 0
    for num in a:
        if num == 1:
            pilotindex += 1
        else:
            break

    return pilotindex

def copy_list(a):
    b = a[:]
    for index, sub in enumerate(b):
        b[index] = sub[:]

    return b

print "Welcome to Eric's ALL-NEW Array Manager! This program will evaluate Bowers arrays even better than before!"

a = []

print "Your array will be called A0."
row_text = raw_input("Let's get started!\nEnter the first row of A0 (separated by spaces), or press enter to finish: ")

while len(row_text) > 0:
    # entry a single row of the array
    row = map(int, row_text.strip().split(' '))
    if not all([n > 0 for n in row]):
        print "A Bowers array cannot contain numbers less than 1."
        exit()

    # append row to array
    a.append(row)

    row_text = raw_input("Enter the next row of A0 (separated by spaces), or press enter to finish: ")

# Create Bowers array object (automatically internally canonized by removing ones)
arr = Bowersarray(a)

print "Your array is:", arr
print "Now it's time to EVALUATE your array!!! After each step, press enter to go to the next one!"

value = arr.eval()
print "Your array has finished evaluating. Its value is:", value
raw_input()

print "Of course we're happy with the value you got, but it doesn't convey the"
print "true potential of Bowers Exploding Array Function."
print "If you really want to get an inkling of how EXPLOSIVE this function is,"
print "restart the program and try to find an array whose evaluation runs into"
print "a very large number and starts decrementing it by 1, or freezes trying"
print "to finish evaluating an array because it involves exponentiation of"
print "numbers too large to handle."
raw_input()

print "Jonathan Bowers has revolutionized the fields of polytopes and large"
print "numbers, and he is currently working on finding uniform and scaliform"
print "polytopes of dimensions 4 and up. His contributions to mathematical"
print "fields are immeasurable."
