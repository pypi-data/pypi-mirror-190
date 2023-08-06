
class generator1():
    def get_event(self,ev):
        ev['photons'].append(self.make_photons())
#        return ev
    def make_photons(self):
        for i in range(3):
            yield i

class generator2():
    def get_event(self,ev):
        ev['photons'].append(self.make_photons())
#        return ev
    def make_photons(self):
        for i in range(3):
            yield i**2


ev = {'photons':[]}
g1 = generator1()
g1.get_event(ev)
print(ev)
g2 = generator2()
g2.get_event(ev)
print(ev)

for bunches in ev['photons']:
    for bunch in bunches:
        print(bunch)
