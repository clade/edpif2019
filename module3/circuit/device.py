from numpy import pi

from .base import BipolarCircuit


class Device(BipolarCircuit):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{self.__class__.__name__}({self.value})'.format(self=self)
        
class Resistor(Device):
    def impedance(self, frequency):
        return self.value

class Capacitor(Device):
    def impedance(self, frequency):
        omega = 2*pi*frequency
        return 1/(1J*self.value*omega)

class Inductor(Device):
    def impedance(self, frequency):
        omega = 2*pi*frequency
        return 1J*self.value*omega
