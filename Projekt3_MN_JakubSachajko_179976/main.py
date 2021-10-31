import pandas as pd
from matplotlib import pyplot as plt
import time
import numpy as np

def create(N):
	A = []
	for i in range(N):
		listOfZeros = [0]*N
		A.append(listOfZeros) 

	return A


def loadFiles(name):
	route = pd.read_csv('2018_paths/'+ name + '.csv',usecols=['Dystans (m)','Wysokość (m)'])
	data = []

	for i in range(len(route)):
		X = route['Dystans (m)'][i]
		Y = route['Wysokość (m)'][i]
		tupleTime =(X,Y)
		data.append(tupleTime)
	return data

def wykresuj(metoda,name,nodeDistance,nodeHeight,probkiDistance,probkiHeight,numerNodesow,distance,results,czas):

	if metoda == 1:
		nazwa = 'Lagrange'
	else:
		nazwa = 'Splines'

	fig = plt.figure()
	plt.title("{}, {}, {}, {}".format(nazwa, name, numerNodesow,czas))
	plt.xlabel("Dystans (m)")
	plt.ylabel("Wysokość (m)")
	plt.plot(distance, results, color='blue', label='interpolowane wartości')
	plt.plot(probkiDistance, probkiHeight, color='orange', label='rzeczywiste wartości')
	plt.plot(nodeDistance, nodeHeight, 'o', color='red')
	plt.legend(loc='lower left')
	plt.savefig("{}-{}-{}-Chart.png".format(nazwa, name, numerNodesow))
	plt.close(fig)
	return 1

def interpolacjaLagrange(distance,number,probka):

	elevation = 0
	for i in range(number):
		a = 1
		for j in range(number):
			if i!=j:
				a *= (distance - probka[j][0])/(probka[i][0] - probka[j][0])

		elevation += a * probka[i][1]

	return elevation
def pivoting(U,L,P,j,N):
	itemp = j
	for i in range(j, N):
		if abs(U[i][j]) > abs(U[itemp][j]):
			itemp = i

	for i in range(N):
		tmp = P[itemp][i]
		P[itemp][i] = P[j][i]
		P[j][i] = tmp
		if i<j:
			tmp = L[itemp][i]
			L[itemp][i] = L[j][i]
			L[j][i] = tmp
		if i>=j:
			tmp = U[itemp][i]
			U[itemp][i] = U[j][i]
			U[j][i] = tmp

	return U, L, P


def faktoryzacjaLU(A, b, x, N):
	U=[]
	L=[]
	P=[]
	for i in range(N):
		listOfZeros1 = [0]*N
		L.append(listOfZeros1)
		listOfZeros2 = [0]*N
		U.append(listOfZeros2)
		listOfZeros3 = [0]*N
		P.append(listOfZeros3)

	for i in range(N):
		for j in range(N):
			if i==j:
				P[i][j]=1
				L[i][j]=1
			U[i][j]=A[i][j]

	for i in range(N - 1):
		U,L,P = pivoting(U,L,P,i,N)

		for j in range(i+1,N):
			L[j][i]=U[j][i]/U[i][i]
			for z in range(i,N):
				U[j][z] = U[j][z] - ( L[j][i]*U[i][z] )
	b = np.matmul(P,b)
	y=[]
	for i in range(N):
		y.append(1)

	for i in range(N):
		sum=0
		for j in range(i):
			sum = sum + L[i][j]  * y[j]
		y[i] = (b[i]-sum) / L[i][i]

	for i in range(N-1,-1,-1):
		sum = 0
		for j in range(i+1,N):
			sum = sum + (U[i][j] * x[j])
		x[i]=(y[i]-sum)/U[i][i]


	return A

def splines(distance,number,probka):
	N = 4*(number-1)
	M = create(N)

	b = [0]*N
	x = [0]*N
	for i in range(N):
		b[i] = 0
		x[i] = 1  

	M[0][0] = 1
	b[0] = probka[0][1]


	h = probka[1][0] - probka[0][0]
	M[1][0]=1
	M[1][1]=h
	M[1][2]=h**2
	M[1][3]=h**3
	b[1] = probka[1][1]

	M[2][2] = 1
	b[2] = 0

	h = probka[number - 1][0] - probka[number - 2][0]
	M[3][4*(number - 2) + 2] = 2
	M[3][4*(number - 2) + 3] = 6 * h
	b[3] = 0

	for i in range(1,number-1):
		h = probka[i][0] - probka[i-1][0]

		M[4*i][4*i]=1
		b[4*i] = probka[i][1]

		M[4*i + 1][4*i] = 1
		M[4*i + 1][4*i + 1] = h
		M[4*i + 1][4*i + 2] = h ** 2 
		M[4*i + 1][4*i + 3] = h ** 3
		b[4*i + 1] = probka[i + 1][1]

		M[4*i + 2][4*(i - 1) + 1] = 1
		M[4*i + 2][4*(i - 1) + 2] = 2* h
		M[4*i + 2][4*(i - 1) + 3] = 3* h**2
		M[4*i + 2][4*i + 1] = -1
		b[4*i + 2] = 0

		M[4*i + 3][4*(i - 1) + 2] = 2
		M[4*i + 3][4*(i - 1) + 3] = 6*h
		M[4*i + 3][4*i + 2] = -2
		b[4*i + 3] = 0

	M = faktoryzacjaLU(M, b,x, N)

	elevation = 0
	for i in range(number-1):
		elevation = 0
		if distance >= probka[i][0] and distance <= probka[i+1][0]:
			for j in range(4):
				h = distance - probka[i][0]
				elevation += x[4*i + j] * h**j
			break
	return elevation


def interpolacja(probki,numerNodesow, nodes,nazwa,metoda):

	t = time.time()
	results = []
	mostLeft = nodes[0]
	mostRight = nodes[numerNodesow-1]
	for i in range(int(mostLeft[0]), int(mostRight[0]),8):
		interpoluj = True
		for j in range(numerNodesow):
			if int(nodes[j][0]) == i:
				interpoluj = False
				result = nodes[j][1]
				break
		if interpoluj == True:
			if metoda == 1:
				result = interpolacjaLagrange(i,numerNodesow,nodes)
			else:
				result = splines(i,numerNodesow,nodes)

		results.append(result)
		
	endResult = time.time()-t
	distance = np.arange(0,mostRight[0],8)

	nodeDistance = [] 
	nodeHeight = []
	for i in range(len(nodes)):
		nodeDistance.append(nodes[i][0])
		nodeHeight.append(nodes[i][1])


	probkiDistance = [] 
	probkiHeight = []
	for i in range(len(probki)):
		probkiDistance.append(probki[i][0])
		probkiHeight.append(probki[i][1])

	wykresuj(metoda,nazwa,nodeDistance,nodeHeight,probkiDistance,probkiHeight,numerNodesow,distance,results,endResult)

	return endResult

intervals = [16,24,48,80]
avgDuration = []
names = ['MountEverest','WielkiKanionKolorado','SpacerniakGdansk']

for i in range(3):
	data = loadFiles(names[i])
	for j in range(4):
		numberOfNode = int(480 / intervals[j])
		tupleNode = []
		temp = 0
		for k in range(numberOfNode):
			coordinates = data[temp]
			tupleNode.append(coordinates)
			temp += intervals[j]
		interpolacja(data,numberOfNode,tupleNode,names[i],0)