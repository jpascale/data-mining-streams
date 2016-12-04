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
			return (self.x == other.x and self.y == other.y) #or (self.x == other.y and self.y == other.x) ## 
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def forms_wedge(self, other):
		return self.y == other.x or self.x == other.y #or self.y == other.y or self.x == other.x ##

	__repr__ = __str__

class Wedge(object):
	def __init__(self, first, second):
		self.first = first
		self.second = second

	def is_closed_by(self, et):
		return (self.second.y == et.x and et.y == self.first.x) or (self.first.x == et.x and self.second.y == et.y)

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

				change = self.update(et, self.t)

				p = float(sum(self.is_closed))/len(self.is_closed)
				Kt = 3 * p
				Tt = 0
				if self.tot_wedges > 0:
					Tt = ((p * math.pow(self.t, 2))/float((self.se * (self.se-1)))) * self.tot_wedges
				print "Kt = " + str(Kt) + " , Tt = " + str(round(float(Tt))) + " , total_wedges " + str(self.tot_wedges) + ", change " + str(change)

				if self.t % 500 == 0:
					print self.wedge_res 

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
			if x <= 1.0/float(t):
				self.edge_res[i] = et
				change = True
				#break, Esto creo que no va
		#################### /reservoir edge

		if change:
			self.update_total_wedges()
			new_wedges, nt = self.determine_new_wedges(et)

			if new_wedges > 0: #Added by me, if not could divide by zero or enter inexistent array index
				for i in range(self.sw):
					x = random.uniform(0.0, 1.0)
					if x <= (float(new_wedges) / float(self.tot_wedges)):
						urand = random.randint(0, len(nt)-1) # Pick one element of nt randomly
						self.wedge_res[i] = nt[urand]
						self.is_closed[i] = False
				return True
		else:
			return False

	def update_total_wedges(self):
		tot_wedges = 0
		for i in range(self.se):
			for j in range(self.se):
				if i < j:
					if self.edge_res[i] is not None and self.edge_res[j] is not None:
						if self.edge_res[i].forms_wedge(self.edge_res[j]):
							tot_wedges += 1
		self.tot_wedges = tot_wedges

	#new wedges are the ones who involve et
	def determine_new_wedges(self, et):
		nt = []
		for i in range(self.se):
			if self.edge_res[i] is not None:	
				if et.y == self.edge_res[i].x:
					nt.append(Wedge(et, self.edge_res[i]))
				elif self.edge_res[i].y == et.x:
					nt.append(Wedge(self.edge_res[i], et))
		return len(nt), nt

if __name__ == '__main__':
	StreamReader("data2.dat", 500, 30000).start_stream()
	#a = Edge(1,2)
	#b = Edge(2,3)
	#c = Wedge(a,b)
	#print c.is_closed_by(Edge(1,3))