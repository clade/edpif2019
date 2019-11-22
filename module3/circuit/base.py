from __future__ import division

class BipolarCircuit(object):
    def __add__(self, other):
        return Serial(self, other)
    
    def __or__(self, other):
        return Parallel(self, other)
    
    def impedance(self):
        raise Exception('you should implement impedance for {self.__class__.__name__}'.format(self=self))
        
    def admittance(self, freq):
        return 1/self.impedance(freq)

    def new_method(self):
	print('Hello')	

class Combination(BipolarCircuit):
    def __init__(self, *list_of_circuit):
        self.list_of_circuit = list_of_circuit
        self.simplify()
         
    def __repr__(self):
        args = ', '.join([repr(item) for item in self.list_of_circuit])
        return '{self.__class__.__name__}({args})'.format(self=self, args=args)
    
    def simplify(self):
        new_list = []
        for elm in self.list_of_circuit:
            if isinstance(elm, self.__class__):
                new_list.extend(elm.list_of_circuit)
            else:
                new_list.append(elm)
        self.list_of_circuit = new_list
            
class Serial(Combination):
    def impedance(self, frequency):
        return sum([elm.impedance(frequency) for elm in self.list_of_circuit])
    
    def impedance(self, frequency):
        result = 0
        for elm in self.list_of_circuit:
            result += elm.impedance(frequency)
        return result

class Parallel(Combination):
    def impedance(self, frequency):
        return 1/sum([1/elm.impedance(frequency) for elm in self.list_of_circuit])

