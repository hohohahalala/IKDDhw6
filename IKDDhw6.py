import random
import math

class Kmeans_use_Jaccard:
	feature_set = []
	N =[]
	
	def __init__(self, N, feature_set):
		self.N = N
		self.feature_set = feature_set


	def k_means(self):
		N = self.N
		feature_set = self.feature_set
		tmpp = self.feature_set
		centroino = []

		#init random cantroino
		#random.seed()
		#random.shuffle(feature_set)
		for i in range(0, N):
			centroino.append([i, feature_set[i]])

		num = 0
		association = []
		association = self.cluster(centroino)

		while num < 100:
			centroino  = self.reassign_centroino(association)
			#print centroino
			association = self.cluster(centroino)
			num += 1

		count = 0
		# test = 0
		for itera in association:
			if itera[0] == 0:
				print feature_set[count][0]
				# test += 1
			count += 1


	def reassign_centroino(self, association):
		N = self.N
		feature_set = self.feature_set
		mean = []
		diff = []
		new_centroino = []
		for i in range(0, N):
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

		return new_centroino

	def cluster(self, centroino):
		N = self.N
		feature_set = self.feature_set
		association = []

		max = len(feature_set)
		for i in range(0, max):
			association.append([-1, -1])
			for j in range(0, N):
				result = self.jaccard(centroino[j][1], feature_set[i])
				if result > association[i][1]:
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
			jaccard_similarity = 0
		else:
			jaccard_similarity = float(child) / float(parent)
		return jaccard_similarity


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
	
	i = 0
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
	fw = open("./data.csv",'w')
	fw.write(new_content)

	#start algorithm
	kuj = Kmeans_use_Jaccard(2, feature_set)
	kuj.k_means()



if __name__ == '__main__':
	main()

