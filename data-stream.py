import random
from datetime import datetime
import math

class Edge(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return self.x == other.x and self.y == other.y
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def forms_wedge(self, other):
		return self.y == other.x or other.y == self.x

	__repr__ = __str__

class Wedge(object):
	def __init__(self, first, second):
		self.first = first
		self.second = second

	def is_closed_by(self, et):
		return self.second.y == et.x and et.y == self.first.x or self.first.x == et.x and self.second.y == et.y

	def __str__(self):
		return "[" + str(self.first) + "->" + str(self.second) + "]"

	__repr__ = __str__

class StreamReader(object):

	def __init__(self, filename, se, sw):
		random.seed(datetime.now())

		self.filename = filename
		self.se = se
		self.sw = sw
		self.t = 0

		self.edge_res = [None for x in range(self.se)]
		self.wedge_res = [None for x in range(self.sw)]

		#self.Nt = list()
		self.tot_wedges = 0
		self.is_closed = [False for x in range(self.sw)]


	def start_stream(self):
		
		with open(self.filename, 'r') as fd:
			while True:
				
				line = fd.readline()
				if line == '':
					break

				self.t = self.t + 1
				print "Processing Et = " + str(self.t)

				line = line.strip().split()
				et = Edge(int(line[0]), int(line[1]))

				self.update(et, self.t)

				p = sum(self.is_closed)
				Kt = 3 * p
				Tt = None
				if self.tot_wedges > 0:
					Tt = ((p * math.pow(self.t, 2))/float((self.se * (self.se-1)))) * self.tot_wedges
				print "Kt = " + str(Kt) + " , Tt = " + str(Tt) + " , total_wedges " + str(self.tot_wedges) 

		#print self.edge_res
		#print self.wedge_res

	def update(self, et, t):
		
		for i in range(self.sw):
			if self.wedge_res[i] is not None:
				if self.wedge_res[i].is_closed_by(et):
					self.is_closed[i] = True

		#################### reservoir edge
		change = False

		for i in range(self.se):
			x = random.uniform(0.0, 1.0)
			if x <= 1.0/t:
				self.edge_res[i] = et
				change = True
		#################### /reservoir edge

		if change:
			self.update_total_wedges()
			new_wedges, nt = self.determine_new_wedges(et)

			if new_wedges > 0: #Added by me, if not could divide by zero or enter inexistent array index
				for i in range(self.sw):
					x = random.uniform(0.0, 1.0)
					if x <= float(new_wedges) / float(self.tot_wedges):
						urand = random.randint(0, len(nt)-1)
						self.wedge_res[i] = nt[urand]
						self.is_closed[i] = False

	def update_total_wedges(self):
		tot_wedges = 0
		for i in range(self.se):
			for j in range(self.se):
				if i < j:
					if self.edge_res[i].forms_wedge(self.edge_res[j]):
						tot_wedges += 1
		self.tot_wedges = tot_wedges

	#new wedges are the ones who involve et
	def determine_new_wedges(self, et):
		nt = []
		for i in range(self.se):
			if et.y == self.edge_res[i].x:
				nt.append(Wedge(et, self.edge_res[i]))
			elif self.edge_res[i].y == et.x:
				nt.append(Wedge(self.edge_res[i], et))
		return len(nt), nt

if __name__ == '__main__':
	StreamReader("data.dat", 100, 100).start_stream()