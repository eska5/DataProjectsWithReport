import matplotlib.pyplot as plt
import math
import time

def create(N,a1,a2,a3,f):
	A = []
	for i in range(N):
		listOfZeros = [0]*N
		A.append(listOfZeros)

	for i in range(N):
		b.append(math.sin((i)*(f+1))) 

	for i in range(N):
		for j in range(N):
			if j == i:
				A[i][j] = a1
				if j > 0:
					A[i][j-1]=a2
				if j > 1:
					A[i][j-2]=a3
				if j < N-1:
					A[i][j+1]=a2
				if j < N-2:
					A[i][j+2]=a3
				break

	return A,b

def norm(V,N):
	sum = 0
	for i in range(N):
		sum=sum+(V[i]*V[i])
	value = math.sqrt(sum)
	return value


def resid(A,r,b,N):
	res = [0]*N
	for i in range(N):
		sum = 0
		for j in range(N):
			sum = sum + A[i][j] * r[j]
		res[i]=sum
	for i in range(N):
		res[i]=res[i]-b[i]
	return res

def jacobi(A,b,N,border):

	r=[]
	for i in range(N):
		r.append(1)
	rPrev=[]
	for i in range(N):
		rPrev.append(1)

	check = 1
	numberOfIterations=0
	timeNumbers=0
	zbieg=True

	tic=time.time()
	while check > 0:
		for i in range(N):

			withoutDiag=0
			for j in range(N):
				if j!=i:
					withoutDiag = withoutDiag + (A[i][j] * rPrev[j])
			r[i]=(b[i]-withoutDiag)/A[i][i]
		for i in range(N):
			rPrev[i]=r[i]
		numberOfIterations=numberOfIterations+1
		res = resid(A,r,b,N)
		if norm(res,N) <= border:
			toc=time.time()
			timeNumbers=toc-tic
			check = 0
		if math.isinf(norm(res,N)) == True:
			toc=time.time()
			timeNumbers=toc-tic
			zbieg=False
			check = -1
	return timeNumbers,numberOfIterations,zbieg

def GaussSeidl(A,b,N,border):

	L=[]
	U=[]
	D=[]
	for i in range(N):
		listOfZeros1 = [0]*N
		L.append(listOfZeros1)
		listOfZeros2 = [0]*N
		U.append(listOfZeros2)
		listOfZeros3 = [0]*N
		D.append(listOfZeros3)

	for i in range(N):
		for j in range(N):
			L[i][j]=0
			U[i][j]=0
			D[i][j]=0
			if i<j:
				U[i][j]=A[i][j]
			if i==j:
				D[i][j]=A[i][j]
			if i>j:
				L[i][j]=A[i][j]

	r=[]
	for i in range(N):
		r.append(1)
	rPrev=[]
	for i in range(N):
		rPrev.append(1)

	check = 1
	numberOfIterations=0
	timeNumbers=0
	zbieg=True
	tic=time.time() 
	while check > 0:
		for i in range(N):
			sum=0

			for j in range(i+1,N):
				sum = sum + (U[i][j])*rPrev[j]
			for j in range(i):
				sum = sum + (L[i][j])*r[j]
			r[i]=(b[i]-sum)/D[i][i]

		for i in range(N):
			rPrev[i]=r[i]
		numberOfIterations=numberOfIterations+1
		res = resid(A,r,b,N)
		if norm(res,N) <= border:
			toc=time.time()
			timeNumbers=toc-tic
			check = 0
		if math.isinf(norm(res,N)) == True:
			toc=time.time()
			timeNumbers=toc-tic
			zbieg=False
			check = -1
	return timeNumbers,numberOfIterations,zbieg


def faktoryzacjaLU(A,b,N):
	L=[]
	U=[]

	for i in range(N):
		listOfZeros1 = [0]*N
		L.append(listOfZeros1)
		listOfZeros2 = [0]*N
		U.append(listOfZeros2)

	tic = time.time()
	for i in range(N):
		for j in range(N):
			U[i][j]=A[i][j]
			if i==j:
				L[i][j]=1

	for i in range(N):
		print(i)
		for j in range(i+1,N):
			L[j][i]=U[j][i]/U[i][i]
			for z in range(i,N):
				U[j][z] = U[j][z] - ( L[j][i]*U[i][z] )

	y=[]
	for i in range(N):
		y.append(1)
	y[0]=b[0]/L[0][0]

	for i in range(N):
		sum=0
		for j in range(i):
			sum = sum + L[i][j]  * y[j]
		y[i] = (b[i]-sum) / L[i][i]

	x=[]
	for i in range(N):
		x.append(1)
	x[N-1] = b[N-1]/U[N-1][N-1]

	for i in range(N-1,-1,-1):
		sum = 0
		for j in range(N-1,i,-1):
			sum = sum + (U[i][j] * x[j])
		x[i]=(y[i]-sum)/U[i][i]

	res = resid(A,x,b,N)

	toc = time.time()
	timer=toc-tic
	return norm(res,N),timer


#Main 

#Zad A

index = 179976

c = 7
d = 6
e = 9
f = 9

a1 = 5 + e
a2 = -1
a3 = -1
N = 900+(10*c)+d
b = []
A = []

border = 10**(-9) 

A,b = create(N,a1,a2,a3,f)
border = 10**(-9) 
"""
print("Zad B")

czas,iter,zbieg = jacobi(A,b,N,border)
print("Czas i iteracje (Jacobi)")
if zbieg == False:
	print("nie zbiega się")
print("czas: ",czas)
print("Liczba iteracji: ",iter)
print("--------------")

czas,iter,zbieg = GaussSeidl(A,b,N,border)
print("Czas i iteracje (Gaussa-Seidla)")
if zbieg == False:
	print("nie zbiega się")
print("czas: ",czas)
print("Liczba iteracji: ",iter)
print("--------------")

print("Zad C")

A,b = create(N,3,a2,a3,f)

czas,iter,zbieg = jacobi(A,b,N,border)
print("Czas i iteracje (Jacobi)")
if zbieg == False:
	print("nie zbiega się")
print("czas: ",czas)
print("Liczba iteracji: ",iter)
print("--------------")

czas,iter,zbieg = GaussSeidl(A,b,N,border)
print("Czas i iteracje (Gaussa-Seidla)")
if zbieg == False:
	print("nie zbiega się")
print("czas: ",czas)
print("Liczba iteracji: ",iter)
print("--------------")

"""
print("Zad D")

res,czas = faktoryzacjaLU(A,b,N)
print("Norma z residuum (faktoryzacjaLU)")
print("norma z residuum wynosi: ",res)
print("--------------")
"""
print("Zad E")

Sizes = [100,500,1000,1500,2000]
timesOne = []
timesTwo = []
timesThree = []

for size in Sizes:
	print(size)
	AA,BB = create(size,a1,a2,a3,f)
	czas,iter,zbieg = jacobi(AA,BB,size,border)
	timesOne.append(czas)
	czas,iter,zbieg = GaussSeidl(AA,BB,size,border) 
	timesTwo.append(czas)
	res,czas = faktoryzacjaLU(AA,BB,size)
	timesThree.append(czas)

print(Sizes)
print(timesOne)
print(timesTwo)
print(timesThree)


SizesPlot = ["100","500","1000","1500","2000"]
fig,axs = plt.subplots(3)

axs[0].set_title("Jacobiego")
axs[0].set_ylabel("czas wykonywania [s]")
l1=axs[0].bar(SizesPlot,timesOne,color='lightcoral',edgecolor='black')

axs[1].set_title("Gaussa-Seidla")
axs[1].set_ylabel("czas wykonywania [s]")
l2=axs[1].bar(SizesPlot,timesTwo,color='springgreen',edgecolor='black')

axs[2].set_title("faktoryzacja LU")
axs[2].set_xlabel("ilość niewiadomych")
axs[2].set_ylabel("czas wykonywania [s]")
l3=axs[2].bar(SizesPlot,timesThree,color='royalblue',edgecolor='black')

fig.suptitle('Zależność czasu trwania algorytmów od liczby niewiadomych')
fig.legend((l1,l2,l3),('Jacobi','Gauss-Seidl','faktoryzacja LU'),loc='lower right')
plt.show()
"""