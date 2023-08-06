# Decorators are a very powerful and useful tool in Python since it allows programmers to modify the behaviour of a function or class. Decorators allow us to wrap another function in order to extend the behaviour of the wrapped function, without permanently modifying it. 


import time
from random import randint
import os

def log(func):
	def print_func(*args, **kwargs):
		f = open("machine.log", 'a')
		spl = func.__name__.split('_')
		d = ""
		for w in spl:
			d += w[0].upper() + w[1:] + " "
		ts = time.time()
		val = func(*args, **kwargs)
		te = time.time()
		dif = (te - ts)
		if dif > 1:
			t = "{:.3f}s".format(dif)
		else:
			t = "{:.3f}ms".format(dif * 1000)
		f.write('(esommier)Running: ' + d.ljust(15, ' ') + ' [ exec-time = ' + t + ' ]\n')
		f.close
		return val
	return print_func

class CoffeeMachine():
	water_level = 100

	@log
	def start_machine(self):
		if self.water_level > 20:
			return True
		else:
			print("Please add water!")
			return False

	@log
	def boil_water(self):
		return "boiling..."

	@log
	def make_coffee(self):
		if self.start_machine():
			for _ in range(20):
				time.sleep(0.1)
				self.water_level -= 1
			print(self.boil_water())
			print("Coffee is ready!")

	@log
	def add_water(self, water_level):
		time.sleep(randint(1, 5))
		self.water_level += water_level
		print("Blub blub blub...")

if __name__ == "__main__":
	f = open('machine.log', 'w')
	f.close()
	machine = CoffeeMachine()
	for i in range(0, 5):
		machine.make_coffee()

	machine.make_coffee()
	machine.add_water(70)