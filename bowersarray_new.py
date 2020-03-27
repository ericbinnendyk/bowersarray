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

    # evaluates the array and (theoretically) returns the final value
    # precondition: array is canonized
    # postcondition: destroys the original array in the process; final array has only two entries
    def eval(self):
        # empty array: return 1
        if len(self.a) == 0:
            self.print_status('= %d' % 1)
            raw_input()
            return 1

        # default prime: evaluate to base
        if len(self.a[0]) < 2 or self.a[0][1] == 1:
            self.print_status('= %d' % self.a[0][0])
            raw_input()
            return self.a[0][0]

        # catastrophic rule: 
        while len(self.a) > 1 or len(self.a[0]) > 2:
            self.print_status()
            raw_input()
            self.catastrophic_step()
        # at this point, the array is only two entries
        print 'A%d = ' % self.a_num + self.__str__() + ' = %d^%d' % (self.a[0][0], self.a[0][1])
        raw_input()
        return self.a[0][0] ** self.a[0][1]

    # perform the catastrophic step of Bowers array evaluation
    # precondition: self.a has at least one non-1 entry after the first two, is trimmed of excess 1's and empty rows, and has a prime entry unequal to 1 (in other words, catastrophic rule applies)
    # postcondition: self.a is still trimmed of excess 1's and empty rows
    def catastrophic_step(self):
        # find the row index (index) and the column index (pilotindex) of the pilot
        for index, sub in enumerate(self.a):
            if index == 0:
                sub = sub[2:]
            if len(sub) != 0:
                break
            index += 1

        if index == 0:
            pilotindex = find_pilot(sub) + 2
        else:
            pilotindex = find_pilot(sub)

        # Make new copy of array a and decrement prime entry
        new = Bowersarray(copy_list(self.a), self.a_num + 1)
        new.a[0][1] -= 1
        new.canonize()

        # decrement pilot of a (this may uncanonize a, but it will be canonized later)
        self.a[index][pilotindex] -= 1

        # set the passengers on previous rows equal to the base
        base = self.a[0][0]
        prime = self.a[0][1]
        for i in xrange(0, index):
            self.a[i] = [base] * prime
        # set all passengers on the same row as the pilot equal to the base
        for i in xrange(pilotindex - 1):
            self.a[index][i] = self.a[0][0]

        if pilotindex > 0:
            # if the copilot exists, make it a reference to the unevaluated array new
            self.a[index][pilotindex - 1] = 'A%d' % new.a_num
            self.canonize()
            self.print_status()
            raw_input()

            # after evaluating new, set copilot equal to that value
            self.a[index][pilotindex - 1] = new.eval()
        else:
            self.canonize()

    # print the array and number of array with an optional message after the array
    def print_status(self, msg = ''):
        print 'A%d =' % self.a_num, self, msg

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
sub = []

entry = int(raw_input("Let's get started!\nEnter the first member of your array, A0\n(or 0 to go to the next row, or a non-positive number to finish): "))

while entry >= 0:
    # entry a single row of the array
    while entry > 0:
        sub.append(entry)
        entry = int(raw_input("Enter the next member of A0, 0 to go to the next row, or a non-positive number to finish: "))

    # append row to array
    a.append(sub)
    if entry < 0:
        break

    sub = []
    entry = int(raw_input("Enter the next member of A0, 0 to go to the next row, or a non-positive number to finish: "))

arr = Bowersarray(a)
arr.canonize()

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

print "I would like to wish a happy 47th birthday to Jonathan Bowers. He has"
print "revolutionized the fields of polytopes and large numbers, and he is now"
print "working on searching regiments of dimensions 6 and up. His contributions"
print "to mathematical fields are immeasurable."
