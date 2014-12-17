import random as rd
import math
from random import random

class Kmeans_use_Jaccard:
	feature_set = []
	N =[]
	
	def __init__(self, N, feature_set):
		self.N = N
		self.feature_set = feature_set

	#improve the method of initial center selection
	def k_meansPP(self):
		N = self.N
		feature_set = self.feature_set
		d = [0.0 for _ in xrange(len(feature_set))]

		rand = rd.sample(range(len(feature_set)), 1)
		centroino = []
		centroino.append([0, feature_set[rand[0]]])

		sum = 0
		for i in xrange(1, N):
			for j in xrange(0, len(feature_set)):
				d[j] = self.jaccard(centroino[i-1][1], feature_set[j])
				sum += d[j]

			sum *= random()

			for k, di in enumerate(d):
				sum -= di
				if sum > 0:
					continue
				centroino.append([i, feature_set[k]])
				break
		return centroino

	def k_means(self):
		#---------------------data structure---------------------#
		#  feature_set = [0] -> id
		#				 [1~16] -> feature
		#
		#  centroino = [0] -> cluster
		#			   [1] -> feature_set
		#
		#  association = [0] -> id
		#				 [1] -> jaccard similarity to centroino
		#--------------------------------------------------------#
		N = self.N
		feature_set = self.feature_set

		#---init random cantroino---#
		centroino = self.k_meansPP()

		#---init random cantroino---#
		# rd.seed()
		# rand = rd.sample(range(len(feature_set)), N)
		# num = 0
		# for index in rand:
		# 	centroino.append([num, feature_set[index]])
		# 	num += 1	

		#---start cluster---#
		num = 0
		association = []
		association = self.cluster(centroino)
		while num < 200:
			centroino  = self.reassign_centroino(association)
			# print centroino
			association = self.cluster(centroino)
			num += 1

		#---compute result---#	
		count = 0
		num = 0
		for itera in association:
			if int(itera[0]) == 0:
				print feature_set[count][0]
				num += 1
			count += 1 
		print "total = " + str(num)

	def reassign_centroino(self, association):
		N = self.N
		feature_set = self.feature_set
		mean = []
		diff = []
		new_centroino = []

		for i in xrange(0, N):
			mean.append(0)
			diff.append(10000)
			new_centroino.append([0, ""])

		for itera in association:
			mean[itera[0]] += float(itera[1])

		i = 0
		while i < len(mean):
			mean[i] = float(mean[i]) / float(len(association))
			i += 1
		count = 0

		for itera in association:
			tmp = math.fabs(itera[1] - mean[itera[0]])
			if tmp <= diff[itera[0]]:
				new_centroino[itera[0]][0] = itera[0]
				new_centroino[itera[0]][1] = feature_set[count]
				diff[itera[0]] = tmp
			count += 1
		print new_centroino
		return new_centroino

	def cluster(self, centroino):
		N = self.N
		feature_set = self.feature_set
		association = []

		max = len(feature_set)
		for i in xrange(0, max):
			association.append([1000, 1000])
			for j in xrange(0, N):
				result = self.jaccard(centroino[j][1], feature_set[i])
				if result < association[i][1]:
					association[i][0] = j
					association[i][1] = result
		return association


	def jaccard(self, A, B):
		child = 0
		parent = 0
		i = 1 
		while i < len(A): #1~16
			if cmp(A[i], "?") != 0 and cmp(B[i], "?") != 0:
	 			child += int(A[i]) & int(B[i])
				parent += int(A[i]) | int(B[i]) 
			i += 1
		if parent == 0:
			jaccard_distance = 1
		else:
			jaccard_distance = 1 - float(child) / float(parent)
		return jaccard_distance


def main():
	#read file and output .csv file
	content = ""
	try:
		path = "./house-votes-84.data"
		fr = open(path,'r')
		content = fr.read()
		fr.close()
	except:
		print "Open File Error"

	content = content.split("\n")
	content.pop()
	new_content = '"id","handicapped-infants","water-project-cost-sharing","adoption-of-the-budget-resolution","physician-fee-freeze","el-salvador-aid","religious-groups-in-schools","anti-satellite-test-ban","aid-to-nicaraguan-contras","mx-missile","immigration","synfuels-corporation-cutback","education-spending","superfund-right-to-sue","crime","duty-free-exports","export-administration-act-south-africa"\n'
	
	i = 1
	feature_set = []
	for itera in content:
		tmp = itera.split(",")
		feature_set.append(tmp)
		tmp[0] = "\"" + str(i) + "\""
		c = 0
		while c < len(tmp):
			if cmp(tmp[c], "y") == 0:
				tmp[c] = "1"
			elif cmp(tmp[c], "n") == 0:
				tmp[c] = "0"
			c += 1
		i = i + 1
		tmp = ",".join(tmp)
		new_content = new_content + tmp + "\n"
	
	# ---Write Demo CSV's File---
	# fw = open("./data.csv",'w')
	# fw.write(new_content)

	#start algorithm
	kuj = Kmeans_use_Jaccard(2, feature_set)
	kuj.k_means()



if __name__ == '__main__':
	main()

