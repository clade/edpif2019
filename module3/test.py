from circuit import Resistor, Capacitor, Inductor


r = Resistor(10)
assert r.impedance(1E3)==10

c = Capacitor(5E-6)
assert c.impedance(1E3).real==0

serial = r + c
print(serial)
assert serial.__repr__()=='Serial(Resistor(10), Capacitor(5e-06))'


