import random
from datetime import datetime

class Edge(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	__repr__ = __str__

class Wedge(object):
	def __init__(self, first, second):
		self.first = first
		self.second = second


class StreamReader(object):

	def __init__(self, filename, se, sw):
		random.seed(datetime.now())

		self.filename = filename
		self.se = se
		self.sw = sw
		self.t = 0

		self.edge_res = [None for x in range(self.se)]
		self.wedge_res = [None for x in range(self.sw)]

		self.Nt = list()
		self.tot_wedges = 0
		self.is_closed = [False for x in range(self.sw)]


	def start_stream(self):
		
		with open(self.filename, 'r') as fd:
			while True:
				
				line = fd.readline()
				if line == '':
					break

				self.t = self.t + 1

				line = line.strip().split()
				et = Edge(int(line[0]), int(line[1]))

				self.update(et, self.t)

		print self.edge_res

	def update(self, et, t):
		
		change = False

		for i in range(self.se):
			x = random.uniform(0.0, 1.0)
			if x <= 1.0/t:
				self.edge_res[i] = et
				change = True

if __name__ == '__main__':
	StreamReader("data.dat", 50, 50).start_stream()